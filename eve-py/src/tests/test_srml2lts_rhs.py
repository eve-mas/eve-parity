# -*- coding: utf-8 -*-
"""Regression test for the environment-RHS `direction` fix in
Arena2LTS (srml2lts.py): an environment update command's right-hand
side must see the players' just-completed joint choice (`direction`),
not just the environment's own pre-round valuation.

FIXTURE (the smallest reproduction): one player module `player`
controlling a single boolean `c`, choosing between c=true and c=false
every round; one environment module controlling two booleans, `x` and
`y` -- `y` is held constant (purely to avoid an unrelated, pre-existing
Arena2LTS gap where an all-false environment label is passed to
getValuation() as None and crashes M.add_vertex()'s very first call,
nothing to do with this fix) and `x' := c`, the smallest possible RHS
formula referencing a player-controlled variable.

Before the fix, an environment RHS was evaluated only against the
environment's own label, which never contains a player-controlled
variable like `c` -- so `x' := c` always evaluated to False regardless
of what the player chose, and both of the player's choices collapsed
onto the same successor state. After the fix, the RHS sees `direction`
(the players' completed choice) merged in, so the two choices correctly
route to two distinct states."""

import parsrml
from parsrml import yacc
from srml2lts import Arena2LTS

FIXTURE = '''
module player controls c
init
:: true ~> c' := true;
:: true ~> c' := false;
update
:: true ~> c' := true;
:: true ~> c' := false;
goal
:: F c;

module environment controls x,y
init
:: true ~> x' := false, y' := true;
update
:: true ~> x' := c, y' := true;
'''


def _build_arena():
    for name in ("modules", "environment", "propFormula", "PFAlphabets"):
        getattr(parsrml, name).clear()
    yacc.parse(FIXTURE)
    return Arena2LTS(parsrml.modules)


def _find(M, label_set):
    return next((v.index for v in M.vs if frozenset(v["label"] or []) == label_set), None)


def test_env_rhs_sees_player_direction():
    M = _build_arena()

    assert M.vcount() == 2, (
        "expected 2 reachable states (x=false and x=true); the pre-fix bug "
        "collapses both player choices onto 1 state, got %d" % M.vcount())

    labels = {frozenset(v["label"] or []) for v in M.vs}
    assert frozenset(["y"]) in labels
    assert frozenset(["x", "y"]) in labels

    x_false = _find(M, frozenset(["y"]))
    x_true = _find(M, frozenset(["x", "y"]))

    assert M.ecount() == 4, "expected 4 edges (2 source states x 2 player choices)"

    for source in (x_false, x_true):
        chose_c_edges = [e for e in M.es if e.source == source and e["direction"] == ["c"]]
        chose_not_c_edges = [e for e in M.es if e.source == source and e["direction"] is None]
        assert len(chose_c_edges) == 1 and chose_c_edges[0].target == x_true, (
            "state %d: choosing c=true must land on x=true" % source)
        assert len(chose_not_c_edges) == 1 and chose_not_c_edges[0].target == x_false, (
            "state %d: choosing c=false must land on x=false" % source)
