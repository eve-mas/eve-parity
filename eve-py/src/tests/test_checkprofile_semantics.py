# -*- coding: utf-8 -*-
"""Semantic test matrix for the pure-memoryless profile checker
(checkprofile.py). Complements test_checkprofile_basic.py (happy path)
and test_srml2lts_rhs.py / test_regression_examples.py / test_gpar_sizes_
stable.py (environment-RHS, Spot-equivalence, and frontier/reachability
regressions respectively)."""

import json
import os

import checkprofile as cp
from conftest import TESTS_DIR, build_game

FIXTURES = os.path.join(TESTS_DIR, "fixtures")


def _load(name):
    with open(os.path.join(FIXTURES, name)) as f:
        return json.load(f)


ALIASES = _load("aliases.json")
ACTION_ALIASES = ALIASES["actions"]
STATE_ALIASES = ALIASES["states"]


def _load_profile(name):
    """Fixture profile JSONs are written in friendly names (aliases.json);
    resolve them to the canonical {state_id: action_id} shape
    complete_profile()/check_profile_memoryless() expect, exactly as
    checkprofile.load_profile_json() does for a file already read into
    memory (main.py's own -a/-p flags go through load_profile_json()
    directly; this mirrors that resolution for in-process tests)."""
    raw = _load(name)
    resolved = {}
    for pl, actions in raw.items():
        action_table = ACTION_ALIASES.get(pl, {})
        resolved[pl] = {
            STATE_ALIASES.get(state, state): action_table.get(name_, name_)
            for state, name_ in actions.items()
        }
    return resolved


def _check(modules, environment, M, GPar, cgsFlag, raw_profile, phi=(None, None)):
    return cp.check_profile_memoryless(
        modules, environment, M, GPar, cgsFlag, phi[0], phi[1], raw_profile)


def _contract_verification_game():
    text = open(os.path.join(os.path.dirname(TESTS_DIR), "..", "examples",
                              "contract_verification")).read()
    modules, environment, M, GPar, cgsFlag = build_game(text)
    import parsrml
    phi = cp.resolve_system_property(parsrml.propFormula, parsrml.PFAlphabets)
    return modules, environment, M, GPar, cgsFlag, phi


# ---------------------------------------------------------------------------
# 1/2/4. Profile is a memoryless NE / has a single profitable deviator /
# off-path-dependent deviation (the PA vs PB decisive pair).
# ---------------------------------------------------------------------------

def test_profile_is_nash_equilibrium():
    modules, environment, M, GPar, cgsFlag, phi = _contract_verification_game()
    result = _check(modules, environment, M, GPar, cgsFlag,
                     _load_profile("A_deliver_approve_reject.json"), phi)
    assert result['is_memoryless_nash_equilibrium'] is True
    assert result['profitable_deviators'] == {}
    assert result['individual_objectives'] == {'supplier': True, 'verifier': True}
    assert result['system_property'] is True


def test_single_profitable_deviator_pa():
    modules, environment, M, GPar, cgsFlag, phi = _contract_verification_game()
    result = _check(modules, environment, M, GPar, cgsFlag,
                     _load_profile("B_PA_claim_approve_reject.json"), phi)
    assert result['is_memoryless_nash_equilibrium'] is False
    assert list(result['profitable_deviators'].keys()) == ['supplier']
    witnesses = result['profitable_deviators']['supplier']
    assert len(witnesses) == 1
    rendered = cp.render_policy(modules, M, 'supplier', witnesses[0]['witness_policy'],
                                 action_aliases=ACTION_ALIASES)
    assert rendered == {'s0': 'deliver'}


def test_off_path_action_flips_nash_verdict_pa_vs_pb():
    """PA and PB induce the IDENTICAL on-path outcome and both players'
    objective/property values, differing only in the verifier's off-path
    response at 's1' (never visited under either profile) -- yet have
    opposite Nash-equilibrium verdicts. This is only possible if
    completeness/deviation-search genuinely range over every original-game
    decision state, not just the realised path."""
    modules, environment, M, GPar, cgsFlag, phi = _contract_verification_game()
    pa = _check(modules, environment, M, GPar, cgsFlag,
                _load_profile("B_PA_claim_approve_reject.json"), phi)
    pb = _check(modules, environment, M, GPar, cgsFlag,
                _load_profile("C_PB_claim_reject_reject.json"), phi)

    assert pa['original_lasso_prefix'] == pb['original_lasso_prefix']
    assert pa['original_lasso_cycle'] == pb['original_lasso_cycle']
    assert pa['individual_objectives'] == pb['individual_objectives']
    assert pa['system_property'] == pb['system_property']

    assert pa['is_memoryless_nash_equilibrium'] is False
    assert pb['is_memoryless_nash_equilibrium'] is True


# ---------------------------------------------------------------------------
# 3. More than one simultaneous profitable deviator.
# ---------------------------------------------------------------------------

TWO_INDEPENDENT_PLAYERS = '''
module p1 controls a1
init
:: true ~> a1':=false;
update
:: true ~> a1':=true;
:: true ~> a1':=false;
goal
:: F a1;

module p2 controls a2
init
:: true ~> a2':=false;
update
:: true ~> a2':=true;
:: true ~> a2':=false;
goal
:: F a2;
'''


def _uniform_profile(modules, M, choose_true):
    """Build a raw profile assigning, at every decision state of every
    player, the unique menu option matching choose_true[pl_name] (True/False)
    for that player's sole controlled variable."""
    choices = cp.original_choice_states(modules, M)
    profile = {}
    for m in modules:
        pl = cp.player_name(m)
        profile[pl] = {}
        want = choose_true[pl]
        for idx, menu in choices[pl].items():
            varying = cp.varying_vars(menu, m[2])
            option = next(o for o in menu if bool(set(o) & varying) == want)
            profile[pl][cp.state_id(idx)] = cp.action_id(option, varying)
    return profile


def test_multiple_simultaneous_profitable_deviators():
    modules, environment, M, GPar, cgsFlag = build_game(TWO_INDEPENDENT_PLAYERS)
    raw_profile = _uniform_profile(modules, M, {'p1': False, 'p2': False})
    result = _check(modules, environment, M, GPar, cgsFlag, raw_profile)

    assert result['individual_objectives'] == {'p1': False, 'p2': False}
    assert result['is_memoryless_nash_equilibrium'] is False
    assert set(result['profitable_deviators'].keys()) == {'p1', 'p2'}


# ---------------------------------------------------------------------------
# 5. Forced-action states require no profile entry.
# ---------------------------------------------------------------------------

def test_forced_states_completed_mechanically():
    modules, environment, M, GPar, cgsFlag, phi = _contract_verification_game()
    choices = cp.original_choice_states(modules, M)
    # supplier only has a real choice at s0; verifier only at s1/s2 --
    # s3..s6 (the terminal self-loop states) must not appear as decision
    # states for either player.
    assert set(choices['supplier']) == {0}
    assert set(choices['verifier']) == {1, 2}

    completed = cp.complete_profile(modules, M, _load_profile("A_deliver_approve_reject.json"))
    # every player has an entry for every one of M's 7 states, including
    # the forced ones, filled in mechanically by complete_profile.
    assert set(completed['supplier']) == set(range(M.vcount()))
    assert set(completed['verifier']) == set(range(M.vcount()))


# ---------------------------------------------------------------------------
# 6. Illegal / incomplete profiles are rejected.
# ---------------------------------------------------------------------------

def test_incomplete_profile_rejected():
    modules, environment, M, GPar, cgsFlag, phi = _contract_verification_game()
    incomplete = {"supplier": {"s0": "deliver"}, "verifier": {"s1": "approve"}}  # missing s2
    try:
        cp.complete_profile(modules, M, incomplete)
        assert False, "expected ProfileError for a missing decision-state entry"
    except cp.ProfileError:
        pass


def test_illegal_action_rejected():
    modules, environment, M, GPar, cgsFlag, phi = _contract_verification_game()
    illegal = {"supplier": {"s0": "not-a-real-action"}, "verifier": {"s1": "approve", "s2": "reject"}}
    try:
        cp.complete_profile(modules, M, illegal)
        assert False, "expected ProfileError for an illegal action id"
    except cp.ProfileError:
        pass


# ---------------------------------------------------------------------------
# 7. LTL goal requiring genuinely temporal reasoning (not a one-step check).
# ---------------------------------------------------------------------------

def test_temporal_goal_vacuously_satisfied_when_supplier_waits_forever():
    """verifier's goal G((deliver or claim) -> F settled) is a genuinely
    temporal (safety-of-a-liveness) condition; under the 'wait' profile the
    supplier never acts, so the antecedent never fires and the goal holds
    vacuously forever -- this must be recognised over the infinite cycle,
    not by inspecting a single step."""
    modules, environment, M, GPar, cgsFlag, phi = _contract_verification_game()
    result = _check(modules, environment, M, GPar, cgsFlag,
                     _load_profile("E_wait_reject_reject.json"), phi)
    assert result['original_lasso_cycle'] == ['s0']
    assert result['individual_objectives']['verifier'] is True
    assert result['individual_objectives']['supplier'] is False  # F approve never holds


# ---------------------------------------------------------------------------
# 8. Positionality in the parity-product is NOT memorylessness in the
# original game.
# ---------------------------------------------------------------------------

# Player chooses `a` only once (at S0) to route through S1 (p becomes true)
# or S2 (p stays false); both routes converge on the SAME original-arena
# state (`atEnd`, valuation always {atEnd} -- p is false there again in
# both cases). The player's goal `F p` was already decided by which route
# was taken, so GPar must keep two distinct copies of the converged state
# (goal-automaton accepting vs. still-pending) even though M has exactly
# one. A profile can only supply ONE action for that state (checkprofile
# indexes by M, not by GPar), and simulate() must still resolve the right
# GPar copy from the actual history.
DIAMOND = '''
module p controls a
init
:: true ~> a':=true;
:: true ~> a':=false;
update
:: true ~> a':=true;
:: true ~> a':=false;
goal
:: F p;

module environment controls p,atS0,atS1,atS2,atEnd
init
:: true ~> p':=false, atS0':=true, atS1':=false, atS2':=false, atEnd':=false;
update
:: atS0 and a ~> p':=true, atS0':=false, atS1':=true, atS2':=false, atEnd':=false;
:: atS0 and !a ~> p':=false, atS0':=false, atS1':=false, atS2':=true, atEnd':=false;
:: atS1 ~> p':=false, atS0':=false, atS1':=false, atS2':=false, atEnd':=true;
:: atS2 ~> p':=false, atS0':=false, atS1':=false, atS2':=false, atEnd':=true;
:: atEnd ~> p':=false, atS0':=false, atS1':=false, atS2':=false, atEnd':=true;
'''


def _find_state(M, marker):
    for idx in range(M.vcount()):
        if marker in cp.module_valuation(M, idx):
            return idx
    raise AssertionError("no M state has %r in its valuation" % marker)


def test_gpar_duplicates_a_single_original_state_by_automaton_progress():
    modules, environment, M, GPar, cgsFlag = build_game(DIAMOND)

    # M itself has exactly one state per named location: the two routes
    # converge onto a single original-arena state.
    assert M.vcount() == 4
    end_idx = _find_state(M, 'atEnd')

    # GPar, in contrast, has two distinct vertices projecting down to that
    # one M state -- one for each way of having reached it -- because the
    # goal automaton for `F p` is in a different state (already accepting
    # vs. still pending) depending on whether the p-branch was taken.
    end_gpar_vertices = [v for v in GPar.vs if cp.get_mstate(v['label']) == str(end_idx)]
    assert len(end_gpar_vertices) == 2
    colours = {v['colour']['p'] for v in end_gpar_vertices}
    assert len(colours) == 2, "the two GPar copies of the same M-state must differ in automaton progress"

    # The decision surface checkprofile.py exposes is keyed by M, not by
    # GPar: the converged state appears exactly ONCE as a decision point,
    # never twice (once per automaton-progress copy).
    choices = cp.original_choice_states(modules, M)['p']
    assert list(choices.keys()).count(end_idx) == 1

    # A profile supplies exactly one action for that M-state, and the SAME
    # profile is evaluated once via each route: the outcome differs only
    # because of which GPar copy the walk actually lands on, never because
    # the (single) policy entry itself changed.
    s0 = _find_state(M, 'atS0')
    profile_via_s1 = {"p": {cp.state_id(idx): "a" for idx in range(M.vcount())}}
    profile_via_s2 = {"p": {cp.state_id(idx): ("a" if idx != s0 else "!a") for idx in range(M.vcount())}}

    via_s1 = _check(modules, environment, M, GPar, cgsFlag, profile_via_s1)
    via_s2 = _check(modules, environment, M, GPar, cgsFlag, profile_via_s2)

    completed_end_action = via_s1['completed_profile']['p'][end_idx]
    assert completed_end_action == via_s2['completed_profile']['p'][end_idx], (
        "both profiles must resolve to the identical single action at the "
        "converged state -- there is only one entry to resolve")
    assert via_s1['individual_objectives']['p'] is True   # went through S1: p was seen
    assert via_s2['individual_objectives']['p'] is False  # went through S2: p was never seen
