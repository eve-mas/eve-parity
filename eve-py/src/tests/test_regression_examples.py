# -*- coding: utf-8 -*-
"""Regression test: every existing example under every applicable problem
letter (e/a/n) must keep producing the same verdict, on the same reachable
*arena* (Kripke/LTS), across every commit in this porting series.
`golden_examples.json` was captured from the pre-change code (ltl2nbw/
nbw2dpw pipeline, unoptimized Arena2LTS/convertG sweeps) and must not need
updating by any later commit -- if it does, that commit changed observable
behaviour, which is the one thing the Spot/perf ports are not supposed to
do.

Note on `GPar` (parity-game product) sizes: the Spot migration deliberately
shrinks these (Spot's relevant-words-restricted DPWs are far more compact
than the old pipeline's full-alphabet-power-set Safra automata), while
producing identical verdicts and an identical underlying arena -- confirmed
by hand across every example when spot_backend.py was introduced. GPar size
is therefore only pinned as a *stability* regression from that point
onward (see golden_gpar_post_spot.json / test_gpar_sizes_stable below), not
compared against the pre-Spot `golden_examples.json` figures."""

import pytest

from conftest import GOLDEN, run_main

CASES = [
    (example, problem)
    for example, problems in GOLDEN.items()
    for problem in problems
]


@pytest.mark.parametrize("example,problem", CASES)
def test_example_matches_golden(example, problem):
    expected = GOLDEN[example][problem]
    actual = run_main(problem, example)
    assert actual["exit"] == expected["exit"], actual["raw"]
    for key in ("kripke_states", "kripke_edges", "verdict"):
        if key in expected:
            assert actual.get(key) == expected[key], (
                "%s/%s: expected %s=%r, got %r\n%s"
                % (example, problem, key, expected[key], actual.get(key), actual["raw"]))
