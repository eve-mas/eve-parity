from itertools import product
import ast
from igraph import *
from subprocess import call

'''returns set of init states'''
def productInit(mdl):
    initSet=[]
    for m in mdl:
        for n in m[3]:
            initStates=[]
            for p in eval(n):
#                print p
                for q in p:
#                    print (">>"+q)
                    initStates.append(q)
            initSet.append(initStates) 
#    print ("initset: ", initSet)
    return jointEnabled(initSet)
                     
'''returns cartesian product/joint actions'''
def jointEnabled(action):
    return product(*action)

'''returns list of variables that are true'''
def getValuation(s):
    invert_dict={}
    for var in s:
        for k, v in ast.literal_eval(var).items():
            invert_dict[v] = invert_dict.get(v, [])
            invert_dict[v].append(k)
#    print (invert_dict.get(True))
    return (invert_dict.get(True))
    
'''returns guard evaluation wrt current state'''
def guardEval(s,mdl):
    enabled=[]
    for m in mdl:
#        print ('fstack',readGuard(m))
        commands=[]
        for u in m[4]:
#            print ('updates',u)
            for command in eval(u).items():
                gEvaluation = parse_rpn(s,command[1]['guard'])
#                print gEvaluation
                if gEvaluation:                
                    commands.append(command)
                    
        '''if no update command is enabled, then skip'''
        if len(commands)==0:
            enabled.append([(-1,merge_two_dicts({'guard':['true']},gSkip(s,m)))])
        else:
            enabled.append(commands)
    return enabled

def envTransition(s,env):
    enabled=[]
    commands=[]
    for u in env[4]:
#            print ('updates',u)
        for command in eval(u).items():
            gEvaluation = parse_rpn(s,command[1]['guard'])
#                print gEvaluation
            if gEvaluation:                
                commands.append(command)
                
    '''if no update command is enabled, then skip'''
    if len(commands)==0:
        enabled.append([(-1,merge_two_dicts({'guard':['true']},gSkip(s,env)))])
    else:
        enabled.append(commands)
    return enabled
    
            
'''implements gskip'''
def gSkip(s,m):
    assignSkip={}
    for var in m[2]:
        '''if var is true in s'''        
        if var in s:
            assignSkip[var]=['true']
        else:
            assignSkip[var]=['false']
    return assignSkip
   
       
'''return dictionary contents without keys'''
def without_keys(d, keys):
    return {k: v for k, v in d.items() if (k != keys)}
    
'''evaluate propositional formula (in: guard)'''
def parse_rpn(s,xprs):
    stack = []
#    print s,xprs
    for l in xprs:
#        print ('L',l)
#        print ('stack: ',stack)
        if l in ['or', 'and', '->','<->']:
            l1 = stack.pop()
            l2 = stack.pop()
            if l=='or': result = l2 or l1
            if l=='and': result = l2 and l1
            if l=='->': result = l1 or (not l2)
            if l=='<->': result = (l1 or (not l2)) and ((not l1) or l2)
            stack.append(result)
        elif l=='!':
            l1 = stack.pop()
            result = (not l1)
            stack.append(result)
        elif l=='true':
            stack.append(True)
        elif l=='false':
            stack.append(False)
        else:
            try:
                if str(l) not in s:
#                    print (l,'IS FALSE')
                    stack.append(False)
                else:
#                    print (l,'is TRUE')
                    stack.append(True)
            except TypeError:
#                print (l,'IS FALSE')
                stack.append(False)
 
    return stack.pop()

def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z
    
def drawM(M):
    layout = M.layout("kk")
#    M.es["label"] = [direction for direction in M.es["direction"]
    out = plot(M, layout=layout, bbox =(800,800), margin=40, color="white")
    # out.save('coba.png')
    # Plot.__init__(M)
    # out.save('coba.png')

def updateLabM(M):
    M.vs['label']=[('M-'+str(v.index),list(v['label'])) for v in M.vs]