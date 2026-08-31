# -*- coding: utf-8 -*-
"""Minimal happy-path test for the generic pure-memoryless profile checker
(checkprofile.py) and its main.py 'm' wiring. The full semantic test
matrix (multiple/off-path deviators, forced states, illegal profiles,
temporal goals, positionality-vs-memorylessness) lives in
test_checkprofile_semantics.py."""

import os

from conftest import TESTS_DIR, run_main

FIXTURES = os.path.join(TESTS_DIR, "fixtures")


def test_profile_is_memoryless_nash_equilibrium():
    result = run_main("m", "contract_verification", extra_args=(
        "-p", os.path.join(FIXTURES, "A_deliver_approve_reject.json"),
        "-a", os.path.join(FIXTURES, "aliases.json"),
    ))
    assert result["exit"] == 0, result["raw"]
    assert "is_memoryless_nash_equilibrium: True" in result["raw"], result["raw"]
    assert "s0 -> sD -> sDA^omega" in result["raw"], result["raw"]
