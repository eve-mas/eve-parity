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
        print "ERROR: Init state cannot be more than 1!!!"
        sys.exit()

    for d in productInit(mdl):
        direction = getValuation(d)
        cmd=[]
        try:
            t = envTransition(direction+label,environment[0])
        except TypeError:
            t = envTransition(label,environment[0])
        if len(t)==1:
            for k,v in without_keys(dict(t[0][0][1]),'guard').items():
                if k != 0:  # exclude checking name
                    cmd.append(str({k:parse_rpn(label,v)}))
        nextLabel = getValuation(cmd)
        try:
            M.vs.find(label=nextLabel)
        except ValueError:
            M.add_vertex(label=nextLabel)
            Q0.add(frozenset(nextLabel))
            Q.add(frozenset(nextLabel))


    prevQ = set()
    while prevQ != Q:
        prevQ = copy.copy(Q)
        for state in prevQ:
#            print state
            for updateCommand in jointEnabled(guardEval(list(state),mdl)):
                commands=[]
#                print 'updateCommand', updateCommand
                for k,v in updateCommand:
                    updateCommand_noguard = without_keys(v,'guard') #remove dict key 'guard'
                    for key,l in updateCommand_noguard.items():
                        '''for each variable'''
                        if k != 0:  # exclude checking name
                            commands.append(str({key:parse_rpn((list(state)),l)}))
                direction = getValuation(commands)
                nextState=[]
                try:
                    t = envTransition(direction+list(state),environment[0])
                except TypeError:
                    t = envTransition(list(state),environment[0])
                if len(t)==1:
                    for k,v in without_keys(dict(t[0][0][1]),'guard').items():
                        if k != 0:  # exclude checking name
                            nextState.append(str({k:parse_rpn(list(state),v)}))
                nextLabel = getValuation(nextState)
#                print 'nextLabel', nextLabel
                if direction!=None:
                    if 'matching_pennies_player_1_var' in direction:
                        nextLabel.append('matching_pennies_player_1_var')
                    if 'matching_pennies_player_2_var' in direction:
                        nextLabel.append('matching_pennies_player_2_var') 
#                print 'nextLabel', nextLabel
                if frozenset(nextLabel) not in Q:
                    Q.add(frozenset(nextLabel))
                    M.add_vertex(label=nextLabel)
                    
        '''
        maybe we can use faster method of adding edges just like in arena2kripke?
        '''
    for currentState in M.vs:
        for nextState in M.vs:
#            print (currentState['label'],nextState['label'])
            for updateCommand in jointEnabled(guardEval(currentState['label'],mdl)):
#                print updateCommand
                commands=[]
                for k,v in updateCommand:
                    updateCommand_noguard = without_keys(v,'guard') #remove dict key 'guard'
                    for key,l in updateCommand_noguard.items():
                        '''for each variable'''
                        if k != 0:  # exclude checking name
                            commands.append(str({key:parse_rpn(currentState['label'],l)}))
                direction = getValuation(commands)
#                print direction
                sNext=[]
                try:
                    t = envTransition(direction+currentState['label'],environment[0])
                except TypeError:
                    t = envTransition(currentState['label'],environment[0])
#                print t
                if len(t)==1:
                    for k,v in without_keys(dict(t[0][0][1]),'guard').items():
                        if k != 0:  # exclude checking name
                            sNext.append(str({k:parse_rpn(currentState['label'],v)}))
                nextLabel = getValuation(sNext)
#                print nextLabel
                if nextLabel==None:
                    nextLabel=[]
                if nextState['label']==None:
                    nextState['label']=[]                
                
                if(set(nextState['label'])==set(nextLabel)):
#                    if direction not in valuation_table[frozenset(nextLabel)]:
#                        valuation_table[frozenset(nextLabel)].append(direction)
                    M.add_edge(currentState.index,nextState.index,direction=direction)
#    print valuation_table
                                    
    return M
