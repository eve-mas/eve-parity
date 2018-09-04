# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 13:53:08 2017

"""

from parsrml import *
from arena2kripke import *
from srml2lts import *
import time, sys, getopt
from ltl2nbw import *
from nbw2dpw import *
from gltl2gpar import convertG,drawGPar,convertG_cgs
from utils import *
from nonemptiness import *
from enash import *
from anash import *

def print_performance(perfConstruction,perfParser,perfPGSolver,empCheck,GPar_v,GPar_e,TTPG_vmax,TTPG_emax,q_flag):
    problem=["E-Nash","A-Nash","Membership","Non-Emptiness"]
    print 'Parser Performance (milisecond)',perfParser
    print 'GPar Construction Performance (milisecond)',perfConstruction
    print 'PGSolver Performance (milisecond)',perfPGSolver
    print problem[q_flag-1]+' performance (milisecond)',empCheck
    print 'Total performance (milisecond)', perfParser+perfConstruction+perfPGSolver+empCheck
    print 'GPar states', GPar_v
    print 'GPar edges', GPar_e
    print 'Max TTPG states', TTPG_vmax
    print 'Max TTPG edges', TTPG_emax
    

def printhelp():
    print "usage: main.py [problem] [path/name of the file] [options]\n"
    print "List of problems:"
    print "a \t Solve A-Nash"
    print "e \t Solve E-Nash"
    print "n \t Solve Non-Emptiness"
    print "\nList of optional arguments:"
    print "-d \t Draw the structures"
    print "-v \t verbose mode"
    print "\n"
    sys.exit()

def main(argv):


    args_list = list(sys.argv)
    file_name = args_list[2]
    prob  = str(args_list[1])
    q_flag=0

    with open("verbose_flag","w") as f:
        f.write("0")
    verbose = False
    
    with open("draw_flag","w") as f:
        f.write("0")
    draw_flag=False
    
    try:
        opts, args = getopt.getopt(argv,"vd")
    except getopt.GetoptError:
        printhelp()
        
    for o,a in opts:
        if o == "-d":
            with open("draw_flag","w") as f:
                f.write("1")
                draw_flag=True
        elif o == "-v":
            with open("verbose_flag","w") as f:
                f.write("1")
            verbose = True
        else:
            print "ERROR: Undefined option"
            printhelp()
            
            
    '''read and parse the file'''
    perfParser = 0.0
    start = time.time()*1000
    if (yacc.parse(open(str(file_name)).read())!=False):
        perfParser = time.time()*1000 - start
    if len(environment)!=0:
        cgsFlag=True
    else:
        cgsFlag=False
    
    perfConstruction = 0.0
    start = time.time()*1000

    '''get the property formula for E/A-Nash'''
    try:
        pf = str(propFormula[0])
    except IndexError:
        pf = None
    
    if prob=="e":
        if pf==None:
            print "No property formula input..."
        else:
            print "Checking E-Nash property formula: "+pf
        '''need to add two players playing matching pennies with goal: \lnot \phi or (matching pennies goal)'''
        '''we can directly modify list modules by adding two players, can we?'''
        '''but the kripke structure will obviously change, is it a problem?'''
        q_flag=1

        '''convert \phi to NBW'''
        NBW_prop = ltl2nbw(propFormula[0],PFAlphabets[0])
        DPW_prop = nbw2dpw(NBW_prop,PFAlphabets[0])

        '''NEED TO BUILD DSW FROM DPW_prop'''
        
        '''add 2 MP players'''
    elif prob=="a":
        if pf==None:
            print "No property formula input..."
        else:
            print "Checking A-Nash property formula: "+pf

        '''convert \phi to NBW'''
        NBW_prop = ltl2nbw('!'+propFormula[0], PFAlphabets[0])
        DPW_prop = nbw2dpw(NBW_prop, PFAlphabets[0])
        q_flag=2
    elif prob=="n":
        print "Solving Non-Emptiness of "+file_name
        q_flag=4
    else:
        print "ERROR: Undefined problem"
        printhelp()

    if cgsFlag:      
        '''Concurrent Game uses LTS instead of KS'''        
        M=(Arena2LTS(modules))
    else:
        '''RMG uses Kripke structure'''
        M=(Arena2Kripke(modules))

    updateLabM(M)
    print "Kripke states", M.vcount()
    print "Kripke edges", M.ecount()
    # if draw_flag:
    #     drawM(M)
        
    '''Don't need to do LTL2DPW conversion for memoryless case'''
    if q_flag in [1,2,4]:
        NBWs = Graph(directed=True)
        DPWs = Graph(directed=True)

        '''Convert NBWs to DPWs'''
        for m in modules:
    #        states = []
            NBWs[list(m[1])[0]]=ltl2nbw(list(m[5])[0],list(m[6]))
    #           print list(m[5])[0],list(m[1])[0]
            NBWs[list(m[1])[0]]['goal']=list(m[5])[0]
            print list(m[1])[0],NBWs[list(m[1])[0]]['goal']
    #        print list(m[1])[0]
            DPWs[list(m[1])[0]] = nbw2dpw(NBWs[list(m[1])[0]],list(m[6]))
    #        for v in DPWs[list(m[1])[0]].vs:
    #            states.append(list(m[1])[0]+'-'+str(v.index))
    #        print states
    #        dpw_states[list(m[1])[0]]=states
    #    st_prod = stateprod(dpw_states,M)
        
        if not cgsFlag:
            if verbose:
                print "\n Convert G_{LTL} to G_{PAR}...\n"
            GPar = convertG(modules,DPWs,M)

        else:
            if verbose:
                print "\n Convert G_{LTL} to G_{PAR}...\n"
            GPar = convertG_cgs(modules,DPWs,M)
        GPar_v = GPar.vcount()
        GPar_e = GPar.ecount()
        perfConstruction = time.time()*1000 - start
    else:
        print "ERROR: Undefined problem"
        printhelp()
    
    

    if q_flag==1:
        '''E-Nash'''
        empCheck = 0.0
        perfPGSolver = 0.0
        TTPG_vmax=0
        TTPG_emax=0
        start = time.time()*1000
        perfPGSolver,TTPG_vmax,TTPG_emax=enash(modules,GPar,draw_flag,cgsFlag,pf,DPW_prop,PFAlphabets[0])
        empCheck = time.time()*1000 - start
    elif q_flag==2:
        '''A-Nash'''
        empCheck = 0.0
        perfPGSolver = 0.0
        TTPG_vmax=0
        TTPG_emax=0
        start = time.time()*1000
        perfPGSolver,TTPG_vmax,TTPG_emax=anash(modules,GPar,draw_flag,cgsFlag,pf,DPW_prop,PFAlphabets[0])
        empCheck = time.time()*1000 - start
    elif q_flag==4:
        '''Solving Non-Emptiness'''    
        empCheck = 0.0
        perfPGSolver = 0.0
        TTPG_vmax=0
        TTPG_emax=0
        start = time.time()*1000
        perfPGSolver,TTPG_vmax,TTPG_emax=nonemptiness(modules,GPar,draw_flag,cgsFlag)        
        empCheck = time.time()*1000 - start
    else:
        print "Undefined Problem!"
        printhelp()
        return True

    if (q_flag not in [6,7,8]) and verbose:
        print_performance(perfConstruction,perfParser,perfPGSolver,empCheck,GPar_v,GPar_e,TTPG_vmax,TTPG_emax,q_flag)
    
if __name__ == "__main__":
    main(sys.argv[3:])
    