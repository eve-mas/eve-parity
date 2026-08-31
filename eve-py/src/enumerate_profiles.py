# -*- coding: utf-8 -*-
"""
Pure-memoryless equilibrium enumeration.

Brute-forces every complete pure-memoryless profile over an already-built
game (arena M + GPar) and classifies each via checkprofile's own
check_profile_memoryless(), reusing the same prepared arena/GPar across
every candidate rather than rebuilding them per profile. This is a
separate, independent enumerator over checkprofile.py's pure-memoryless
semantics -- no perfect-recall EVE engine (enash.py/anash.py/
nonemptiness.py) or its Streett/PUN machinery is touched or called.
"""

from checkprofile import (
    enumerate_all_complete_profiles, check_profile_memoryless,
    player_name, state_id, action_id, varying_vars, state_menu,
)


def _profile_to_raw(modules, M, profile):
    """Convert an {pl: {m_idx: frozenset}} profile (enumerate_all_complete_
    profiles()'s own shape) into check_profile_memoryless()'s external
    {pl: {state_id: action_id}} input shape."""
    raw = {}
    for m in modules:
        pl = player_name(m)
        raw[pl] = {}
        for idx, option in profile[pl].items():
            menu = state_menu(M, idx, m)
            varying = varying_vars(menu, m[2]) if len(menu) > 1 else set()
            raw[pl][state_id(idx)] = action_id(option, varying)
    return raw


def enumerate_memoryless_equilibria(modules, environment, M, GPar, cgsFlag,
                                     phi_formula, phi_alphabet):
    """
    Enumerate every complete pure-memoryless profile over M's decision
    states and classify each via check_profile_memoryless().

    Returns:
      total_profiles_checked   int -- size of the Cartesian product
                                actually enumerated
      nash_equilibria          [completed_profile, ...] for every profile
                                with is_memoryless_nash_equilibrium True
      safe_nash_equilibria     same, further filtered to
                                system_property True
      nash_equilibria_count / safe_nash_equilibria_count

    Ordering is deterministic: enumerate_all_complete_profiles() iterates
    players and decision states in a fixed order and every player's menu
    is generated the same way every time, so both the enumeration and the
    returned equilibrium lists are in a stable, repeatable order.
    """
    total = 0
    nash_equilibria = []
    safe_nash_equilibria = []

    for profile in enumerate_all_complete_profiles(modules, M):
        total += 1
        raw = _profile_to_raw(modules, M, profile)
        result = check_profile_memoryless(
            modules, environment, M, GPar, cgsFlag, phi_formula, phi_alphabet, raw)
        if result['is_memoryless_nash_equilibrium']:
            nash_equilibria.append(result['completed_profile'])
            if result['system_property']:
                safe_nash_equilibria.append(result['completed_profile'])

    return {
        'total_profiles_checked': total,
        'nash_equilibria': nash_equilibria,
        'safe_nash_equilibria': safe_nash_equilibria,
        'nash_equilibria_count': len(nash_equilibria),
        'safe_nash_equilibria_count': len(safe_nash_equilibria),
    }
