# -*- coding: utf-8 -*-
"""Shared test helpers: run main.py as a subprocess (it relies on module-level
globals reset per run, e.g. parser tables, so in-process re-import is not
safe across multiple invocations) and parse its stdout the same way the
golden fixtures were captured."""

import json
import os
import re
import subprocess
import sys

SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAMPLES_DIR = os.path.join(os.path.dirname(SRC_DIR), "examples")
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))

# Lets tests import eve-py/src modules (parsrml, srml2lts, checkprofile, ...)
# directly and in-process, for tests that need to inspect Python objects
# rather than just main.py's stdout.
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

with open(os.path.join(TESTS_DIR, "golden_examples.json")) as f:
    GOLDEN = json.load(f)


def run_main(problem, example, extra_args=()):
    """Runs `python main.py <problem> ../examples/<example> -v [extra_args]`
    from eve-py/src, exactly as a user would from the README, and parses the
    same fields the golden fixtures record."""
    example_path = os.path.join(EXAMPLES_DIR, example)
    cmd = [sys.executable, "main.py", problem, example_path, "-v"] + list(extra_args)
    proc = subprocess.run(
        cmd, cwd=SRC_DIR, capture_output=True, text=True, timeout=120)
    return parse_output(proc.stdout, proc.returncode)


def build_game(srml_text):
    """Parse an SRML source string in-process and build the same
    (modules, environment, M, GPar, cgsFlag) main.py builds for problems
    e/a/n/m, without going through the CLI/subprocess. Lets semantic tests
    inspect M/GPar directly (e.g. to find two GPar vertices projecting to
    the same original-arena state)."""
    import parsrml
    from parsrml import yacc
    from arena2kripke import Arena2Kripke
    from srml2lts import Arena2LTS
    from srmlutil import updateLabM
    from spot_backend import ltl2dpw
    from gltl2gpar import convertG, convertG_cgs
    from igraph import Graph

    for name in ("modules", "environment", "propFormula", "PFAlphabets"):
        getattr(parsrml, name).clear()
    yacc.parse(srml_text)
    modules = parsrml.modules
    environment = parsrml.environment
    cgsFlag = len(environment) != 0

    M = Arena2LTS(modules) if cgsFlag else Arena2Kripke(modules)
    updateLabM(M)

    valuations = [frozenset(M.vs[i]['label'][1]) for i in range(M.vcount())]
    DPWs = Graph(directed=True)
    for m in modules:
        pl = list(m[1])[0]
        goal = list(m[5])[0]
        DPWs[pl] = ltl2dpw(goal, list(m[6]), valuations)

    GPar = convertG_cgs(modules, DPWs, M) if cgsFlag else convertG(modules, DPWs, M)
    return modules, environment, M, GPar, cgsFlag


def parse_output(text, exit_code):
    entry = {"exit": exit_code}
    for key, pattern in [
        ("kripke_states", r"Kripke states (\d+)"),
        ("kripke_edges", r"Kripke edges (\d+)"),
        ("gpar_states", r"GPar states (\d+)"),
        ("gpar_edges", r"GPar edges (\d+)"),
    ]:
        m = re.search(pattern, text)
        if m:
            entry[key] = int(m.group(1))
    m = re.search(r">>> (YES|NO),", text)
    if m:
        entry["verdict"] = m.group(1)
    entry["raw"] = text
    return entry
