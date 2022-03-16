# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 14:42:43 2017

"""

from parsrml import *
from srmlutil import *

'''translate SRML arena to Kripke structure'''
def Arena2Kripke(mdl):
    KripkeStruct = Graph(directed=True)
    S0 = set() #set of init states
    S = set() #set of states
    
    for state in productInit(mdl):
        stateLabel = getValuation(state)
        if stateLabel==None:
            stateLabel=frozenset()
        else:
            stateLabel=frozenset(stateLabel)
        KripkeStruct.add_vertex(label=stateLabel)
        '''set of init states'''
        
#        KripkeStruct.vs
        try:
            S0.add(frozenset(stateLabel))
            S.add(frozenset(stateLabel))
            
        except TypeError:
            S0.add(frozenset())
            S.add(frozenset())

    prevS = set()
    while prevS != S:
        prevS = copy.copy(S)
        for state in KripkeStruct.vs:
#            print 'state[]',state['label']
            for updateCommand in jointEnabled(guardEval(state['label'],mdl)):
                commands=[]
#                print 'updateCommand',updateCommand
                for k,v in updateCommand:
                    '''for each jointEnabled update command'''
                    updateCommand_noguard = without_keys(v,'guard') #remove dict key 'guard'
#                    print 'updateCommand_noguard',updateCommand_noguard
                    for k,l in updateCommand_noguard.items():
                        '''for each variable'''
#                        print k,l
                        if k != 0:  # exclude checking name
                            commands.append(str({k:parse_rpn(state['label'],l)}))
                try:
                    nextState = frozenset(getValuation(tuple(commands)))
#                    print '>>>',commands,nextState
                except TypeError:
                    nextState = frozenset()
                if not nextState in S:
                    S.add(nextState)
                    KripkeStruct.add_vertex(label=nextState)
                    
    '''add all edges'''
#    for currentState in KripkeStruct.vs:
#        for nextState in KripkeStruct.vs:
#            for state in jointEnabled(guardEval(list(currentState['label']),mdl)):
#                commands=[]
#                for k,v in state:
#                    '''for each jointEnabled update command'''
#                    updateCommand_noguard = without_keys(v,'guard')
#                    for k,l in updateCommand_noguard.items():
#                        commands.append(str({k:parse_rpn(currentState['label'],l)}))
##                print nextState['label'],getValuation(commands)
#                cmdval = getValuation(commands)
#                if cmdval==None:
##                    cmdval=[]
#                    cmdval=frozenset()
#                else:
#                    cmdval=frozenset(cmdval)
##                if nextState['label']==None:
##                    nextState['label']=[]
##                try:
##                    if len(nextState['label'])==0:
##                        nextState['label']=None
##                except TypeError:
##                    print '--'
#                if ((nextState['label'])==(cmdval)):
#                    KripkeStruct.add_edge(currentState.index,nextState.index)
    '''this method of adding edges seems to be faster'''
    for currentState in KripkeStruct.vs:
#        print currentState
        for state in jointEnabled(guardEval(list(currentState['label']),mdl)):
                commands=[]
                for k,v in state:
                    '''for each jointEnabled update command'''
                    updateCommand_noguard = without_keys(v,'guard')
                    for k,l in updateCommand_noguard.items():
                        if k != 0:  # exclude checking name
                            commands.append(str({k:parse_rpn(currentState['label'],l)}))
#                print nextState['label'],getValuation(commands)
                cmdval = getValuation(commands)
#                print cmdval
                if cmdval==None:
#                    cmdval=[]
                    cmdval=frozenset()
                else:
                    cmdval=frozenset(cmdval)
                KripkeStruct.add_edge(currentState,KripkeStruct.vs.find(label=cmdval))
#    print_K(KripkeStruct)
    
    return KripkeStruct
    
def print_K(KripkeStruct):
    for v in KripkeStruct.vs:
        print(v)
    for e in KripkeStruct.es:
        print(e)
