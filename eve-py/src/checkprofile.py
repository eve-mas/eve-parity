# -*- coding: utf-8 -*-
"""
Exact pure-memoryless strategy-profile checker.

Given a finite game (an SRML model, already parsed into the arena M and its
GPar parity-game product) and a caller-supplied, complete profile assigning
one action to every player at every original-game decision state, this
module determines the induced outcome, each player's own objective
satisfaction, whether the profile is a Nash equilibrium against pure
*memoryless* deviations, and, for every losing player, every alternative
complete memoryless policy that would make them win.

Policies are memoryless over the ORIGINAL game arena (the vertices of M, the
Kripke/LTS structure built by Arena2Kripke/Arena2LTS) -- sigma_i : St -> Ac_i
where St ranges over M's vertices -- rather than over the GPar/DPW-product
states enash.py/anash.py/nonemptiness.py operate on. A strategy that is
positional in a parity-automaton product can still depend on automaton state
and therefore correspond to a history-dependent strategy in the original
game; this module never indexes a policy by a product-graph vertex. If
several product states project to the same original state, the profile is
required to make the same choice at all of them -- enforced structurally (a
policy has exactly one entry per original-state id), not checked after the
fact. Nothing in enash.py/anash.py/nonemptiness.py/utils.py's Streett/PUN
machinery is touched by this file, and this module reuses none of it: a
frozen profile's profitable deviations are found by exact brute-force
enumeration over the deviating player's own decision states (tractable for
hand-authored verification games; see the module-level test suite for
scale caveats), not by worst-case coalition punishment-region search, since
those are different questions.
"""

import itertools

from spot_backend import ltl2dpw
from gltl2gpar import generate_coal_dir, get_mstate
from srmlutil import envTransition
from utils import graph_product


class UnsupportedModelError(Exception):
    """Raised when the SRML model falls outside this checker's scope
    (nondeterministic environment reaction, nondeterministic initial state)."""
    pass


class ProfileError(Exception):
    """Raised when a supplied policy is incomplete or contains an illegal action."""
    pass


def resolve_system_property(propFormula, PFAlphabets):
    """Resolve the optional system-property formula from an SRML file's
    parsed 'property' declaration(s) -- the same single-property
    convention E-Nash/A-Nash already use (propFormula[0]). Returns
    (None, None) if the file declares no property at all: unlike E-Nash/
    A-Nash (where a property is the entire point), a frozen-profile check
    can always report each player's own objective and the Nash-equilibrium
    verdict with no system property declared at all; the property check is
    simply omitted in that case.
    """
    if not propFormula:
        return None, None
    if len(propFormula) > 1:
        print("WARNING: only the first 'property' declaration is used; "
              "%d additional declaration(s) are ignored" % (len(propFormula) - 1))
    return propFormula[0], PFAlphabets[0]


# ---------------------------------------------------------------------------
# Original-state choice menus
# ---------------------------------------------------------------------------

def player_name(module):
    return list(module[1])[0]


def state_id(m_idx):
    """External, stable identifier for an original arena state, e.g. 's3'."""
    return "s%d" % m_idx


def parse_state_id(raw):
    """Inverse of state_id. Raises ProfileError on malformed input."""
    if not (isinstance(raw, str) and raw.startswith("s") and raw[1:].isdigit()):
        raise ProfileError(
            "'%s' is not a valid original-state identifier (expected 's<N>', e.g. 's0')" % raw)
    return int(raw[1:])


def module_valuation(M, m_idx):
    """The valuation (frozenset of true controlled-variable names) at
    original arena state m_idx, as labelled by srmlutil.updateLabM."""
    return frozenset(M.vs[m_idx]['label'][1])


def state_menu(M, m_idx, module):
    """All legal actions for one module at one original arena state."""
    return generate_coal_dir(module_valuation(M, m_idx), [module])


def original_choice_states(modules, M):
    """
    For every player, the subset of M's states at which that player has a
    real decision (more than one legal action), together with the menu.

    Returns {pl_name: {m_idx: [frozenset, ...]}}
    """
    choices = {}
    for m in modules:
        pl = player_name(m)
        choices[pl] = {}
        for idx in range(M.vcount()):
            menu = state_menu(M, idx, m)
            if len(menu) > 1:
                choices[pl][idx] = menu
    return choices


def enumerate_all_complete_profiles(modules, M):
    """
    Yield every complete pure-memoryless profile over the ORIGINAL arena:
    the full cartesian product of every player's own decision-state menus
    (forced states are filled identically in every yielded profile, since
    they have only one legal action).

    Each yielded profile has the same shape as complete_profile()'s return
    value: {pl_name: {m_idx (int): frozenset(literal names)}}.
    """
    choices = original_choice_states(modules, M)
    axes = []
    for pl in choices:
        for s in sorted(choices[pl]):
            axes.append((pl, s, choices[pl][s]))

    base = {}
    for m in modules:
        pl = player_name(m)
        base[pl] = {}
        for idx in range(M.vcount()):
            menu = state_menu(M, idx, m)
            if len(menu) == 1:
                base[pl][idx] = menu[0]

    for combo in itertools.product(*(a[2] for a in axes)) if axes else [()]:
        profile = {pl: dict(actions) for pl, actions in base.items()}
        for (pl, s, _), option in zip(axes, combo):
            profile[pl][s] = option
        yield profile


def varying_vars(menu, controlled_vars):
    """Controlled variables whose truth value is not constant across menu."""
    varying = set()
    for v in controlled_vars:
        vals = {v in option for option in menu}
        if len(vals) > 1:
            varying.add(v)
    return varying


# ---------------------------------------------------------------------------
# Stable action-id <-> literal-assignment mapping (no set/frozenset reprs
# ever cross the external JSON boundary)
# ---------------------------------------------------------------------------

def action_id(option, varying):
    """Canonical, deterministic string id for one menu option, e.g. 'claim,!deliver'."""
    return ",".join(sorted(v if v in option else "!" + v for v in varying))


def action_id_to_option(action_str, menu, varying):
    """Inverse of action_id: resolve a supplied action id back to the unique
    matching menu option. Raises ProfileError if it doesn't match any option."""
    wanted = set()
    tokens = [t for t in action_str.split(",") if t != ""]
    seen_vars = set()
    for tok in tokens:
        if tok.startswith("!"):
            var = tok[1:]
            truth = False
        else:
            var = tok
            truth = True
        if var not in varying:
            raise ProfileError(
                "action id '%s' references '%s', which is not a decision "
                "variable at this state (expected one of %s)"
                % (action_str, var, sorted(varying)))
        seen_vars.add(var)
        if truth:
            wanted.add(var)
    if seen_vars != set(varying):
        raise ProfileError(
            "action id '%s' does not specify all decision variables %s"
            % (action_str, sorted(varying)))
    for option in menu:
        if set(option) & varying == wanted:
            return option
    raise ProfileError("action id '%s' does not match any legal action" % action_str)


def dump_menu(modules, M):
    """Human-readable listing of every decision state, its valuation and the
    legal action ids, for hand-authoring policy JSON files."""
    lines = []
    choices = original_choice_states(modules, M)
    for m in modules:
        pl = player_name(m)
        lines.append("player %s:" % pl)
        for idx in sorted(choices[pl]):
            menu = choices[pl][idx]
            varying = varying_vars(menu, m[2])
            ids = sorted(action_id(o, varying) for o in menu)
            lines.append("  state %s  valuation=%s  actions=%s"
                          % (state_id(idx), sorted(module_valuation(M, idx)), ids))
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Deterministic-environment validation
# ---------------------------------------------------------------------------

def validate_deterministic_environment(modules, environment, M):
    """
    Verify that, for every reachable original state and every legal joint
    player-action profile, the environment reacts with exactly one successor
    original state. The environment is not a strategic player in this
    checker; if its own SRML update section is genuinely nondeterministic
    (more than one simultaneously-enabled guarded command) this raises
    UnsupportedModelError rather than silently picking one (which is what
    Arena2LTS's own `t[0][0]` shortcut does).

    Non-CGS games (no `environment` block) are deterministic by construction
    (the joint direction of `modules` alone fixes the next Kripke state), so
    this is a no-op for them.
    """
    if not environment:
        return
    env = environment[0]
    for idx in range(M.vcount()):
        val = module_valuation(M, idx)
        menus = [state_menu(M, idx, m) for m in modules]
        for combo in itertools.product(*menus) if menus else [()]:
            direction = list(frozenset().union(*combo)) if combo else []
            t = envTransition(direction + list(val), env)
            enabled = t[0]
            if len(enabled) > 1:
                raise UnsupportedModelError(
                    "environment reaction is nondeterministic at original "
                    "state %d under joint action %s: %d guarded commands "
                    "are simultaneously enabled" % (idx, direction, len(enabled)))


# ---------------------------------------------------------------------------
# Profile completion: complete over ALL decision states, not just the
# realised path; forced states are mechanically completed.
# ---------------------------------------------------------------------------

def complete_profile(modules, M, raw_profile):
    """
    raw_profile: {pl_name: {state_id (str, 's<N>'): action_id (str)}} as
    loaded from the external JSON (or built in-memory by callers/tests).

    Returns {pl_name: {m_idx (int): frozenset(literal names)}}, total over
    every state in M for every player (forced states mechanically filled).
    """
    completed = {}
    for m in modules:
        pl = player_name(m)
        supplied = {parse_state_id(k): v for k, v in raw_profile.get(pl, {}).items()}
        completed[pl] = {}
        for idx in range(M.vcount()):
            menu = state_menu(M, idx, m)
            if len(menu) == 1:
                completed[pl][idx] = menu[0]
                continue
            if idx not in supplied:
                raise ProfileError(
                    "missing required action for player '%s' at original "
                    "state %s (this state has %d legal actions)"
                    % (pl, state_id(idx), len(menu)))
            varying = varying_vars(menu, m[2])
            completed[pl][idx] = action_id_to_option(supplied[idx], menu, varying)
        extra = set(supplied) - set(range(M.vcount()))
        if extra:
            raise ProfileError(
                "player '%s' has actions for unknown states %s"
                % (pl, sorted(state_id(i) for i in extra)))
    return completed


# ---------------------------------------------------------------------------
# Building the evaluation graph: GPar (original states x per-player DPWs),
# optionally producted once more against the system property's DPW.
# ---------------------------------------------------------------------------

# The colour-dict key graph_product() uses for whatever it products GPar
# against -- 'environment' is graph_product()'s own long-standing default
# (enash.py/anash.py already product GPar against the E-Nash/A-Nash property
# DPW under this exact key), reused here unchanged rather than inventing a
# second convention.
_PROPERTY_COLOUR_KEY = 'environment'


def build_evaluation_graph(GPar, phi_formula, phi_alphabet, cgsFlag):
    """Returns (final, producted): `final` is GPar itself, unmodified, when
    no system property was declared (nothing to check); otherwise it is
    GPar producted against the property's DPW, and `producted` is True (so
    build_mstate_index/evaluate know how to read `final`'s vertex labels/
    colours)."""
    if phi_formula is None:
        return GPar, False
    # Every valuation the DPW will ever be queried against, while
    # graph_product() walks GPar, is already present on GPar's own
    # vertices -- passing them through lets the backend build only the
    # transitions actually needed instead of the full 2**|alphabet|.
    valuations = [GPar.vs[i]['val'] for i in range(GPar.vcount())]
    dpw_phi = ltl2dpw(phi_formula, phi_alphabet, valuations)
    final = graph_product(GPar, dpw_phi, phi_alphabet, cgsFlag)
    return final, True


def build_mstate_index(GPar, final, producted):
    """Precompute, for every vertex of the evaluation graph, the
    original-state (M) index it projects down to (None for the synthetic
    RMG pre-init vertex)."""
    index = {}
    for v in final.vs:
        label = GPar.vs[v['label'][0]]['label'] if producted else v['label']
        m = get_mstate(label)
        index[v.index] = int(m) if m is not None else None
    return index


def to_original_lasso(mstate_index, product_vertices):
    """Project a sequence of evaluation-graph vertices down to original-state
    identifiers ('s<N>'). This is the primary, human-facing rendering of an
    induced outcome; the raw vertex sequence remains available separately
    for debugging."""
    return [state_id(mstate_index[v]) for v in product_vertices]


def _friendly_state(sid, state_aliases):
    """Reverse-lookup a canonical 's<N>' identifier back to its semantic
    alias (e.g. 's3' -> 'sDA'), if one is defined; falls back to the
    canonical id otherwise. 's<N>' identifiers remain the internal/debug
    identifiers regardless -- this is a purely cosmetic substitution."""
    if not state_aliases:
        return sid
    for name, canonical in state_aliases.items():
        if canonical == sid:
            return name
    return sid


def _minimal_period(seq):
    """The shortest repeating unit of a (finite) sequence, e.g.
    ['s3','s3'] -> ['s3'], ['sX','sY','sX','sY'] -> ['sX','sY']."""
    n = len(seq)
    for p in range(1, n + 1):
        if n % p == 0 and all(seq[i] == seq[i % p] for i in range(n)):
            return seq[:p]
    return seq


def format_lasso(prefix, cycle, state_aliases=None):
    """
    Human-facing normalisation of an original-state lasso, e.g.:
      prefix=['s0'], cycle=['s0','s0']            -> 's0^omega'
      prefix=['s0','s1','s3'], cycle=['s3','s3']  -> 's0 -> s1 -> s3^omega'
    The evaluation-graph-level cycle can have a longer period than its
    projection onto original states (an artefact of DPW determinisation,
    not a bug); this reduces the cycle to its own minimal period first,
    then absorbs any trailing prefix entries that are already that
    constant repeated state, so a true one-state cycle renders as a bare
    'sN^omega' rather than '[] -> ([sN,sN])^w'.
    """
    prefix = [_friendly_state(s, state_aliases) for s in prefix]
    cycle = [_friendly_state(s, state_aliases) for s in cycle]
    min_cycle = _minimal_period(cycle) if cycle else []
    while len(min_cycle) == 1 and prefix and prefix[-1] == min_cycle[0]:
        prefix.pop()
    if not min_cycle:
        return " -> ".join(prefix) if prefix else "(empty)"
    cycle_repr = ("%s^omega" % min_cycle[0] if len(min_cycle) == 1
                  else "(%s)^omega" % ",".join(min_cycle))
    return "%s -> %s" % (" -> ".join(prefix), cycle_repr) if prefix else cycle_repr


# ---------------------------------------------------------------------------
# Deterministic walk (unique outcome) and evaluation
# ---------------------------------------------------------------------------

def simulate(final, mstate_index, completed_profile, modules):
    """
    Deterministic walk over the evaluation graph from the (unique) initial
    state, following `completed_profile`, until a vertex repeats.

    Returns (prefix, cycle): lists of `final` vertex indices.

    Vertex 0 of `final` means different things under convertG (RMG) vs
    convertG_cgs (CGS): convertG's vertex 0 is a synthetic pre-init
    placeholder (never a real original-arena state -- mstate_index[0] is
    None) whose only job is to route, via exactly one edge, to the real
    initial state(s) enumerated from the players' own `init` sections;
    convertG_cgs has no such placeholder layer, so its vertex 0 already IS
    the real initial arena state (mstate_index[0] is 0), complete with
    whatever real strategic choice a player may have there. Requiring
    "exactly one successor" of vertex 0 is therefore only correct for the
    RMG placeholder case; for CGS, vertex 0 must be walked like any other
    state, selecting the outgoing edge via the supplied profile's chosen
    joint action.
    """
    if mstate_index[0] is not None:
        cur = 0
    else:
        inits = final.successors(0)
        if len(inits) != 1:
            raise UnsupportedModelError(
                "nondeterministic initial state: %d joint initial valuations "
                "found; this checker assumes a single deterministic start" % len(inits))
        cur = inits[0]
    visited_order = [cur]
    visited_pos = {cur: 0}
    bound = final.vcount() + 1
    for _ in range(bound):
        m_idx = mstate_index[cur]
        d_players = set()
        for m in modules:
            pl = player_name(m)
            d_players |= set(completed_profile[pl][m_idx])
        candidates = final.es.select(_source=cur, word=d_players)
        if len(candidates) != 1:
            raise UnsupportedModelError(
                "expected exactly one successor from original state %d under "
                "joint action %s, found %d (the model may be nondeterministic "
                "in a way this checker does not support)"
                % (m_idx, sorted(d_players), len(candidates)))
        nxt = candidates[0].target
        if nxt in visited_pos:
            start = visited_pos[nxt]
            return visited_order[:start], visited_order[start:]
        visited_pos[nxt] = len(visited_order)
        visited_order.append(nxt)
        cur = nxt
    raise UnsupportedModelError("outcome did not close into a lasso within the graph size bound")


def evaluate(final, cycle, modules, producted):
    """Even/odd-minimum-colour parity evaluation over the cycle, for every
    player's own goal, plus the system property if one was declared."""
    colours = [final.vs[v]['colour'] for v in cycle]
    keys = [player_name(m) for m in modules]
    if producted:
        keys.append(_PROPERTY_COLOUR_KEY)
    result = {key: (min(c[key] for c in colours) % 2 == 0) for key in keys}
    individual_objectives = {player_name(m): result[player_name(m)] for m in modules}
    return {
        'individual_objectives': individual_objectives,
        'system_property': result.get(_PROPERTY_COLOUR_KEY),
    }


# ---------------------------------------------------------------------------
# Pure-memoryless deviation enumeration
# ---------------------------------------------------------------------------

def enumerate_deviations(modules, M, final, mstate_index, completed_profile, pl_name, producted):
    """
    Brute-force, exact enumeration of every alternative complete pure-
    memoryless policy for pl_name (holding every other player's supplied
    policy -- including their off-path entries -- exactly fixed), returning
    those under which pl_name flips from losing to winning.

    Each returned witness is itself a COMPLETE policy for pl_name (forced
    states included).
    """
    choice_states = original_choice_states(modules, M).get(pl_name, {})
    state_ids = sorted(choice_states)
    menus = [choice_states[s] for s in state_ids]

    profitable = []
    for combo in itertools.product(*menus) if menus else [()]:
        candidate_profile = {pl: dict(actions) for pl, actions in completed_profile.items()}
        candidate_profile[pl_name] = dict(completed_profile[pl_name])
        for s, option in zip(state_ids, combo):
            candidate_profile[pl_name][s] = option
        prefix, cycle = simulate(final, mstate_index, candidate_profile, modules)
        outcome = evaluate(final, cycle, modules, producted)
        if outcome['individual_objectives'][pl_name]:
            profitable.append({
                'witness_policy': candidate_profile[pl_name],
                'original_lasso_prefix': to_original_lasso(mstate_index, prefix),
                'original_lasso_cycle': to_original_lasso(mstate_index, cycle),
                'lasso_prefix': prefix,
                'lasso_cycle': cycle,
                'outcome': outcome,
            })
    return profitable


# ---------------------------------------------------------------------------
# Top-level orchestrator
# ---------------------------------------------------------------------------

def check_profile_memoryless(modules, environment, M, GPar, cgsFlag,
                              phi_formula, phi_alphabet, raw_profile):
    """
    Check a complete, caller-supplied pure-memoryless strategy profile
    (raw_profile) against pure-memoryless unilateral deviations.

    phi_formula/phi_alphabet (typically from resolve_system_property()) may
    be (None, None) if the SRML file declares no system property; the
    returned 'system_property' is then None too, and every other field is
    unaffected.
    """
    validate_deterministic_environment(modules, environment, M)
    completed = complete_profile(modules, M, raw_profile)

    final, producted = build_evaluation_graph(GPar, phi_formula, phi_alphabet, cgsFlag)
    mstate_index = build_mstate_index(GPar, final, producted)

    prefix, cycle = simulate(final, mstate_index, completed, modules)
    outcome = evaluate(final, cycle, modules, producted)

    deviators = {}
    for m in modules:
        pl = player_name(m)
        if outcome['individual_objectives'][pl]:
            continue
        found = enumerate_deviations(modules, M, final, mstate_index, completed, pl, producted)
        if found:
            deviators[pl] = found

    return {
        'individual_objectives': outcome['individual_objectives'],
        'system_property': outcome['system_property'],
        'is_memoryless_nash_equilibrium': len(deviators) == 0,
        'profitable_deviators': deviators,
        # primary, human-facing rendering of the induced outcome
        'original_lasso_prefix': to_original_lasso(mstate_index, prefix),
        'original_lasso_cycle': to_original_lasso(mstate_index, cycle),
        # evaluation-graph vertex sequence, kept available separately for debugging
        'lasso_prefix': prefix,
        'lasso_cycle': cycle,
        'completed_profile': completed,
    }


# ---------------------------------------------------------------------------
# JSON I/O (stable external format: player -> {state_id 's<N>': action name})
#
# `action_aliases` ({pl_name: {friendly_name: raw_action_id}}) and
# `state_aliases` ({friendly_name: 's<N>'}) are both purely cosmetic layers
# on top of the canonical action_id()/state_id() schemes, so that profile
# files and reports can read "deliver"/"sD" instead of "!claim,deliver"/"s1".
# Both are entirely optional and loaded together from one JSON file via
# load_aliases(); raw ids always work too, with or without an alias table,
# and 's<N>' / raw action ids remain the internal debug identifiers that
# every rendering can fall back to.
# ---------------------------------------------------------------------------

def load_aliases(path):
    """Load {"actions": {pl: {name: raw_action_id}}, "states": {name: "s<N>"}}
    from one JSON file. Either top-level key may be omitted."""
    import json
    with open(path, 'r') as f:
        data = json.load(f)
    return data.get('actions', {}), data.get('states', {})


def load_profile_json(path, action_aliases=None, state_aliases=None):
    import json
    with open(path, 'r') as f:
        raw = json.load(f)
    if not action_aliases and not state_aliases:
        return raw
    resolved = {}
    for pl, actions in raw.items():
        action_table = (action_aliases or {}).get(pl, {})
        resolved[pl] = {
            (state_aliases or {}).get(state, state): action_table.get(name, name)
            for state, name in actions.items()
        }
    return resolved


def _friendly_action(pl, raw_action, action_aliases):
    """Reverse-lookup a raw action id back to its alias, if one is defined;
    falls back to the raw id otherwise (so nothing is ever hidden)."""
    if not action_aliases or pl not in action_aliases:
        return raw_action
    for name, raw in action_aliases[pl].items():
        if raw == raw_action:
            return name
    return raw_action


def render_policy(modules, M, pl, policy, action_aliases=None, state_aliases=None,
                   decision_states_only=True):
    """Render one player's {m_idx: frozenset} policy as {state_name: friendly
    action name}, falling back to raw 's<N>' / raw action ids wherever no
    alias is defined."""
    m = next(mod for mod in modules if player_name(mod) == pl)
    choices = original_choice_states(modules, M).get(pl, {})
    rendered = {}
    for idx, option in policy.items():
        if decision_states_only and idx not in choices:
            continue
        if idx in choices:
            varying = varying_vars(choices[idx], m[2])
        else:
            varying = m[2]
        raw = action_id(option, varying)
        rendered[_friendly_state(state_id(idx), state_aliases)] = _friendly_action(pl, raw, action_aliases)
    return rendered


def print_profile_report(modules, M, result, action_aliases=None, state_aliases=None):
    lines = []
    lines.append("individual_objectives: %s" % result['individual_objectives'])
    lines.append("system_property: %s" % result['system_property'])
    lines.append("is_memoryless_nash_equilibrium: %s" % result['is_memoryless_nash_equilibrium'])
    lines.append("induced outcome (original states): %s"
                  % format_lasso(result['original_lasso_prefix'], result['original_lasso_cycle'], state_aliases))
    lines.append("  [evaluation-graph debug: %s -> (%s)^w]"
                  % (result['lasso_prefix'], result['lasso_cycle']))
    if result['profitable_deviators']:
        lines.append("profitable deviators:")
        for pl, witnesses in result['profitable_deviators'].items():
            policy_word = "policy" if len(witnesses) == 1 else "policies"
            lines.append("  %s (%d witness %s):" % (pl, len(witnesses), policy_word))
            for w in witnesses:
                rendered = render_policy(modules, M, pl, w['witness_policy'], action_aliases, state_aliases)
                lines.append("    %s" % rendered)
                lines.append("      outcome (original states): %s"
                              % format_lasso(w['original_lasso_prefix'], w['original_lasso_cycle'], state_aliases))
                lines.append("      [evaluation-graph debug: %s -> (%s)^w]"
                              % (w['lasso_prefix'], w['lasso_cycle']))
    return "\n".join(lines)


def to_json_result(modules, M, result, action_aliases=None, state_aliases=None):
    """Machine-readable rendering of a check_profile_memoryless() result:
    individual objectives, system property, ML-NE verdict, profitable
    deviators, complete witness policies, and the original-state lasso --
    all in plain, JSON-serialisable types (no frozensets)."""

    def lasso_dict(prefix, cycle):
        return {
            'prefix': [_friendly_state(s, state_aliases) for s in prefix],
            'cycle': [_friendly_state(s, state_aliases) for s in cycle],
            'formatted': format_lasso(prefix, cycle, state_aliases),
        }

    deviators = {}
    for pl, witnesses in result['profitable_deviators'].items():
        deviators[pl] = [
            {
                'witness_policy': render_policy(
                    modules, M, pl, w['witness_policy'], action_aliases, state_aliases,
                    decision_states_only=False),
                'original_state_lasso': lasso_dict(w['original_lasso_prefix'], w['original_lasso_cycle']),
            }
            for w in witnesses
        ]

    return {
        'individual_objectives': result['individual_objectives'],
        'system_property': result['system_property'],
        'is_memoryless_nash_equilibrium': result['is_memoryless_nash_equilibrium'],
        'original_state_lasso': lasso_dict(result['original_lasso_prefix'], result['original_lasso_cycle']),
        'profitable_deviators': deviators,
    }
