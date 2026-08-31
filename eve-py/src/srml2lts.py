# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 17:12:52 2017

"""

from parsrml import *
from srmlutil import *

'''translate SRML arena to LTS for Concurrent Games'''
def Arena2LTS(mdl):
    M = Graph(directed=True)
    Q0 = set()
    Q = set()

    '''get the (macro) state labelling from module arena'''
#    stateLabel = environment[0][2]
    check_init = 0
    for s in productInit(environment):
        label = getValuation(s)
        M.add_vertex(label=label)
        '''add s0 to valuation table dict'''
        Q0.add(frozenset(label))
        Q.add(frozenset(label))
        check_init += 1
    
    '''init state can only be 1'''
    if check_init != 1:
        print("ERROR: Init state cannot be more than 1!!!")
        sys.exit()

    for d in productInit(mdl):
        direction = getValuation(d)
        cmd=[]
        # `merged` = the players' just-completed init choice (`direction`)
        # plus the environment's own current valuation (`label`) -- the same
        # view envTransition's guard match already uses two lines below, now
        # reused for evaluating the *selected* branch's RHS too (was
        # evaluated against `label` alone, silently unable to see any
        # player-controlled variable on an RHS formula). Safe: by this point
        # every player's own init choice was already computed independently
        # of `direction` (productInit(mdl) enumerates each player's own init
        # branches on its own), so merging it in here only lets the
        # *environment* observe the completed round -- it cannot leak one
        # player's choice into another player's own computation, since no
        # player-choice computation reads `merged`.
        try:
            merged = direction+label
        except TypeError:
            merged = label
        t = envTransition(merged,environment[0])
        if len(t)==1:
            for k,v in without_keys(dict(t[0][0][1]),'guard').items():
                cmd.append(str({k:parse_rpn(merged,v)}))
        nextLabel = getValuation(cmd)
        try:
            M.vs.find(label=nextLabel)
        except ValueError:
            M.add_vertex(label=nextLabel)
            Q0.add(frozenset(nextLabel))
            Q.add(frozenset(nextLabel))


    '''Reachability sweep: process each state's own successor-discovery
    EXACTLY ONCE. guardEval/envTransition's output for a given state
    depends only on that state's own valuation and the static module
    definitions (mdl) -- never on which round of the sweep we're in --
    so re-processing a state already fully expanded in an earlier round
    (the previous version's `for state in prevQ` re-scanned the WHOLE
    of Q, which only grows, every single round) recomputes the exact
    same successor set for no benefit. Tracking just the newly-
    discovered frontier each round preserves the identical final Q/
    M.vs (same states discovered, same eventual vertex set) while
    cutting the number of guardEval/envTransition calls from
    O(rounds * |Q|) to O(|Q|).
    sorted, not raw set iteration: iterating a Python set of frozensets
    orders by hash, which is randomised per-process (PYTHONHASHSEED) for
    str contents -- that made vertex-discovery order, and therefore each
    state's assigned M.vs index, differ across otherwise-identical runs.
    Arena2Kripke avoids this by iterating its own already-built vertex
    sequence; ordering deterministically here matches that (unchanged
    from the pre-frontier version -- this property is preserved, not
    introduced, by this change).'''
    frontier = set(Q)
    while frontier:
        next_frontier = set()
        for state in sorted(frontier, key=lambda fs: sorted(fs)):
#            print state
            for updateCommand in jointEnabled(guardEval(list(state),mdl)):
                commands=[]
#                print 'updateCommand', updateCommand
                for k,v in updateCommand:
                    updateCommand_noguard = without_keys(v,'guard') #remove dict key 'guard'
                    for key,l in updateCommand_noguard.items():
                        '''for each variable'''
                        commands.append(str({key:parse_rpn((list(state)),l)}))
                direction = getValuation(commands)
                nextState=[]
                # See the site-1 comment above: `direction` here is this
                # round's players' choices, each already computed above
                # (line 96) purely from `list(state)` -- simultaneity is
                # intact by construction before we ever reach this point.
                # Reusing the merged (direction + state) view for the
                # selected branch's RHS, not just its guard, is what a
                # formula like `same' := (cp <-> cq)` needs to see the
                # players' actual current-round choices.
                try:
                    merged = direction+list(state)
                except TypeError:
                    merged = list(state)
                t = envTransition(merged,environment[0])
                if len(t)==1:
                    for k,v in without_keys(dict(t[0][0][1]),'guard').items():
                        nextState.append(str({k:parse_rpn(merged,v)}))
                nextLabel = getValuation(nextState)
#                print 'nextLabel', nextLabel
                if direction!=None:
                    if 'matching_pennies_player_1_var' in direction:
                        nextLabel.append('matching_pennies_player_1_var')
                    if 'matching_pennies_player_2_var' in direction:
                        nextLabel.append('matching_pennies_player_2_var') 
#                print 'nextLabel', nextLabel
                next_key = frozenset(nextLabel)
                if next_key not in Q:
                    Q.add(next_key)
                    M.add_vertex(label=nextLabel)
                    next_frontier.add(next_key)
        frontier = next_frontier

    '''Edge-building pass: guardEval(currentState['label'], mdl) and the
    (direction, nextLabel) it produces do not depend on `nextState` at
    all, so the previous version's `for nextState in M.vs` inner loop
    recomputed the identical guardEval/envTransition/parse_rpn work
    once per candidate target vertex -- O(|S|) redundant recomputation
    per currentState, O(|S|^2) overall. Computing each currentState's
    own (direction, nextLabel) pair once and looking the matching
    target vertex up by label (vertices carry unique labels under
    frozenset equality -- the same equality the reachability sweep
    above already deduplicates on) turns this into O(|S|) total,
    producing the exact same edge set (same (source, target, direction)
    triples) as the original set(nextState['label']) == set(nextLabel)
    comparison, just without scanning every vertex to find it.'''
    label_to_index = {frozenset(v['label'] or []): v.index for v in M.vs}
    for currentState in M.vs:
        for updateCommand in jointEnabled(guardEval(currentState['label'],mdl)):
#                print updateCommand
            commands=[]
            for k,v in updateCommand:
                updateCommand_noguard = without_keys(v,'guard') #remove dict key 'guard'
                for key,l in updateCommand_noguard.items():
                    '''for each variable'''
                    commands.append(str({key:parse_rpn(currentState['label'],l)}))
            direction = getValuation(commands)
#                print direction
            sNext=[]
            # Same fix as the two sites above, applied to the edge-building
            # pass: `direction` is this transition's already-completed
            # player choice (computed at line 152 purely from
            # currentState['label']), so merging it into the RHS-evaluation
            # view here is likewise leak-free.
            try:
                merged = direction+currentState['label']
            except TypeError:
                merged = currentState['label']
            t = envTransition(merged,environment[0])
#                print t
            if len(t)==1:
                for k,v in without_keys(dict(t[0][0][1]),'guard').items():
                    sNext.append(str({k:parse_rpn(merged,v)}))
            nextLabel = getValuation(sNext)
#                print nextLabel
            if nextLabel==None:
                nextLabel=[]

            target_index = label_to_index.get(frozenset(nextLabel))
            if target_index is not None:
#                    if direction not in valuation_table[frozenset(nextLabel)]:
#                        valuation_table[frozenset(nextLabel)].append(direction)
                M.add_edge(currentState.index,target_index,direction=direction)
#    print valuation_table

    return M
