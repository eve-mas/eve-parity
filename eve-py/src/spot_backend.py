# -*- coding: utf-8 -*-
"""
Spot-based LTL -> deterministic min-even parity automaton (DPW) backend.

Produces igraph Graph objects with the SAME interface the old
ltl2nbw()+nbw2dpw() pipeline always produced -- vertex 0 is the initial
state, every vertex carries an int 'colour' attribute, every edge carries
a 'word' attribute (a python set, using the same all-false-word sentinel
frozenset({''}) convention as utils.alpha2wordset/evalNBWedge) -- queried
via .es.select(word=set(w)) / .es.find(_source=, word=w), exactly as
utils.graph_product() and gltl2gpar.delta_dpw()/get_colour() already do.
Neither of those consumers needs to change.

Unlike the old pipeline (which built every one of the 2**|alphabet| words
for every state via alpha2wordset), this module only ever builds
transitions for words that actually occur somewhere in the arena/product
graph the DPW will be queried against (see relevant_words()) -- Spot's own
BDD-guarded transitions are evaluated directly against each concrete
valuation instead.

Spot is the single LTL->DPW route in EVE now: main.py uses it for both
player-goal automata and the E-Nash/A-Nash property formula (the 'e'/'a'
problem letters). ltl2nbw.py/nbw2dpw.py and the ltl2ba/ external binary
have been removed from the repository -- nothing calls them any more.
"""
import buddy
import spot
from igraph import Graph


def relevant_words(alphabet, valuations):
    """alphabet: iterable of atom names for one formula. valuations:
    iterable of frozenset/set/list of atom names true at some reachable
    arena/product state (over the full environment vocabulary, not just
    this formula's alphabet -- the intersection is taken here). Returns
    the distinct words (as frozensets) actually needed, using the same
    all-false sentinel frozenset({''}) the rest of the codebase uses."""
    alphabet = set(alphabet)
    words = set()
    for val in valuations:
        if val is None:
            # convertG's (RMG) vertex 0 is a synthetic pre-init placeholder
            # with no real valuation (see checkprofile.simulate()'s
            # docstring) -- nothing to intersect, so it contributes no word.
            continue
        w = alphabet.intersection(val)
        words.add(frozenset(w) if w else frozenset(['']))
    if not words:
        words.add(frozenset(['']))
    return words


def _translate(formula, alphabet):
    """Verified against Spot 2.15.1's actual Python API (not assumed):
    'parity min even' + 'deterministic' + 'complete' gives a deterministic
    complete parity automaton; 'SBAcc' requests state-based acceptance
    (prop_state_acc() confirmed 'yes' with this option, only 'maybe'
    without it). colorize_parity_here(aut, True) then reduces the
    acceptance condition to exactly one mark per transition -- but
    verified empirically that the 'min even' string passed to translate()
    does NOT survive colorize_parity_here(): aut.acc().is_parity() comes
    back (True, max=True, odd=False) -- i.e. MAX-even, not min-even --
    after colorizing, even though it was requested as min-even. checkprofile
    .evaluate() hardcodes 'min(colours over the cycle) % 2 == 0', which is
    only correct against a genuine canonical min-even numbering (colour 0
    is the best/most-preferred, ties resolved by taking the numerically
    smallest colour that recurs infinitely often) -- so change_parity_here
    is called explicitly afterwards to force that exact convention. Without
    it, colorize_parity_here can produce a logically-equivalent but
    differently-structured acceptance formula (confirmed: 'Inf(2) |
    (Fin(1) & Inf(0))' on a 2-state GF-p automaton) where checkprofile's
    naive min-and-check-even computation gives the WRONG answer even
    though Spot's own acc.accepting() on the same automaton is correct --
    see test_spot_backend_regression.py for the confirmed failing case
    this fixes."""
    aut = spot.formula(formula).translate(
        'parity min even', 'deterministic', 'complete', 'SBAcc')
    spot.colorize_parity_here(aut, True)
    spot.change_parity_here(aut, spot.parity_kind_min, spot.parity_style_even)
    is_parity, is_max, is_odd = aut.acc().is_parity()
    if not (is_parity and not is_max and not is_odd):
        raise AssertionError(
            "formula %r: change_parity_here did not produce genuine "
            "min-even parity acceptance (is_parity=%s, max=%s, odd=%s) -- "
            "checkprofile.evaluate()'s naive min-colour-even-check would "
            "be unsound against this automaton" % (formula, is_parity, is_max, is_odd))
    return aut


def _state_colour(aut, state):
    """EVE's checkprofile.evaluate() indexes colour by STATE
    (final.vs[v]['colour']), not by transition. Spot stores acceptance
    marks on transitions even under state-based acceptance (SBAcc) --
    confirmed empirically that colorize_parity_here + SBAcc produces
    transitions that are uniform per state across every formula shape
    tested, but this is verified here per-automaton rather than assumed:
    if some formula ever violated it, silently picking one colour would
    reintroduce exactly the class of bug this backend replaces."""
    colours = set()
    for e in aut.out(state):
        marks = list(e.acc.sets())
        if len(marks) != 1:
            raise AssertionError(
                "Spot edge from state %d has %d acceptance marks (%s), "
                "expected exactly 1 per transition after colorize_parity_here"
                % (state, len(marks), marks))
        colours.add(marks[0])
    if len(colours) != 1:
        raise AssertionError(
            "state %d has non-uniform outgoing transition colours %s -- "
            "SBAcc was expected to guarantee one colour per state for this "
            "formula and did not; refusing to silently pick one" % (state, colours))
    return colours.pop()


def ltl2dpw_spot(formula, alphabet, valuations):
    """Direct LTL -> DPW via Spot. Does not enumerate 2**|alphabet|: only
    builds transitions for the words in relevant_words(alphabet,
    valuations). Returns an igraph Graph matching the old pipeline's
    output contract (see module docstring)."""
    aut = _translate(formula, alphabet)
    words = relevant_words(alphabet, valuations)

    d = aut.get_dict()
    varnums = {str(a): d.varnum(a) for a in aut.ap()}

    def letter_bdd(true_names):
        b = buddy.bddtrue
        for a in aut.ap():
            name = str(a)
            v = varnums[name]
            lit = buddy.bdd_ithvar(v) if name in true_names else buddy.bdd_nithvar(v)
            b = buddy.bdd_and(b, lit)
        return b

    n = aut.num_states()
    init = aut.get_init_state_number()
    # Spot does not guarantee the initial state is numbered 0 (confirmed:
    # e.g. GF(p|q) inits at state 1) -- every existing consumer assumes
    # DPW vertex 0 is the start state, so remap explicitly rather than
    # relying on it coinciding by luck.
    order = [init] + [s for s in range(n) if s != init]
    spot_to_igraph = {spot_idx: ig_idx for ig_idx, spot_idx in enumerate(order)}

    DPW = Graph(directed=True)
    for spot_idx in order:
        DPW.add_vertex(colour=_state_colour(aut, spot_idx))

    for spot_src, ig_src in spot_to_igraph.items():
        for w in words:
            true_names = set(w) - {''}
            lb = letter_bdd(true_names)
            matches = [e for e in aut.out(spot_src)
                       if buddy.bdd_and(e.cond, lb) != buddy.bddfalse]
            if len(matches) != 1:
                raise AssertionError(
                    "expected exactly one Spot transition from state %d on "
                    "word %s (automaton is deterministic+complete), found %d"
                    % (spot_src, sorted(true_names), len(matches)))
            e = matches[0]
            DPW.add_edge(ig_src, spot_to_igraph[e.dst], word=set(w))
    return DPW


def ltl2dpw(formula, alphabet, valuations):
    """Single supported entry point for LTL -> DPW construction (used by
    every call site that used to do nbw2dpw(ltl2nbw(formula, alphabet),
    alphabet), including both player goals and the E-Nash/A-Nash property
    formula). Always routes through Spot; there is no runtime backend
    switch any more."""
    return ltl2dpw_spot(formula, list(alphabet), valuations)
