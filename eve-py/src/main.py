# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 13:53:08 2017

"""

from parsrml import *
from arena2kripke import *
from srml2lts import *
import time, sys, getopt
from spot_backend import ltl2dpw
from gltl2gpar import convertG,drawGPar,convertG_cgs
from utils import *
from nonemptiness import *
from enash import *
from anash import *
from checkprofile import (
    check_profile_memoryless, load_profile_json, load_aliases,
    print_profile_report, to_json_result, resolve_system_property,
    UnsupportedModelError, ProfileError)

def print_performance(perfConstruction,perfParser,perfPGSolver,empCheck,GPar_v,GPar_e,TTPG_vmax,TTPG_emax,q_flag):
    problem=["E-Nash","A-Nash","Membership","Non-Emptiness"]
    print('Parser Performance (milisecond)',perfParser)
    print('GPar Construction Performance (milisecond)',perfConstruction)
    print('PGSolver Performance (milisecond)',perfPGSolver)
    print(problem[q_flag-1]+' performance (milisecond)',empCheck)
    print('Total performance (milisecond)', perfParser+perfConstruction+perfPGSolver+empCheck)
    print('GPar states', GPar_v)
    print('GPar edges', GPar_e)
    print('Max TTPG states', TTPG_vmax)
    print('Max TTPG edges', TTPG_emax)
    

def printhelp():
    print("usage: main.py [problem] [path/name of the file] [options]\n")
    print("List of problems:")
    print("a \t Solve A-Nash")
    print("e \t Solve E-Nash")
    print("n \t Solve Non-Emptiness")
    print("m \t Check a pure-memoryless strategy profile (requires -p)")
    print("\nList of optional arguments:")
    print("-d \t Draw the structures")
    print("-v \t verbose mode")
    print("-p \t path to a profile JSON file (required for problem 'm')")
    print("-a \t path to an optional alias JSON file for problem 'm' "
          "({\"actions\": {...}, \"states\": {...}})")
    print("-j \t path to write a machine-readable JSON result for problem 'm'")
    print("\n")
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

    profile_file = None
    aliases_file = None
    json_out_file = None

    try:
        opts, args = getopt.getopt(argv,"vdp:a:j:")
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
        elif o == "-p":
            profile_file = a
        elif o == "-a":
            aliases_file = a
        elif o == "-j":
            json_out_file = a
        else:
            print("ERROR: Undefined option")
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

    '''get the property formula for E/A-Nash/membership-checking'''
    try:
        pf = str(propFormula[0])
    except IndexError:
        pf = None

    if prob=="e":
        if pf==None:
            print("No property formula input...")
        else:
            print("Checking E-Nash property formula: "+replace_symbols(pf))
        '''need to add two players playing matching pennies with goal: \lnot \phi or (matching pennies goal)'''
        '''we can directly modify list modules by adding two players, can we?'''
        '''but the kripke structure will obviously change, is it a problem?'''
        q_flag=1

        '''add 2 MP players'''
    elif prob=="a":
        if pf==None:
            print("No property formula input...")
        else:
            print("Checking A-Nash property formula: "+replace_symbols(pf))
        q_flag=2
    elif prob=="n":
        print("Solving Non-Emptiness of "+file_name)
        q_flag=4
    elif prob=="m":
        '''Checking a caller-supplied pure-memoryless strategy profile.'''
        if profile_file is None:
            print("ERROR: problem 'm' requires -p <profile.json>")
            printhelp()
        phi_formula, phi_alphabet = resolve_system_property(propFormula, PFAlphabets)
        if phi_formula is None:
            print("No system property declared; checking objectives/NE only.")
        else:
            print("Checking profile against system property: "+replace_symbols(phi_formula))
        q_flag=6
    else:
        print("ERROR: Undefined problem")
        printhelp()

    if cgsFlag:      
        '''Concurrent Game uses LTS instead of KS'''        
        M=(Arena2LTS(modules))
    else:
        '''RMG uses Kripke structure'''
        M=(Arena2Kripke(modules))

    updateLabM(M)
    print("Kripke states", M.vcount())
    print("Kripke edges", M.ecount())
    # if draw_flag:
    #     drawM(M)
        
    '''Every problem below needs each player's own goal converted to a DPW
    and producted into GPar; only e/a additionally need the property
    producted in main.py itself (m's own phi product happens inside
    check_profile_memoryless, against GPar directly, not here).'''
    if q_flag in [1,2,4,6]:
        DPWs = Graph(directed=True)

        '''Convert LTL goals/property directly to DPWs via Spot (spot_backend.py).
        Every valuation these DPWs could ever be queried against, while
        convertG()/convertG_cgs() walk M to build GPar, is already present on
        M's own vertices.'''
        valuations = [frozenset(M.vs[i]['label'][1]) for i in range(M.vcount())]

        if q_flag == 1:
            DPW_prop = ltl2dpw(propFormula[0], PFAlphabets[0], valuations)
        elif q_flag == 2:
            DPW_prop = ltl2dpw('!('+propFormula[0]+')', PFAlphabets[0], valuations)

        for m in modules:
            goal = list(m[5])[0]
            goal_display = replace_symbols(goal)
            print(list(m[1])[0], goal_display)
            DPWs[list(m[1])[0]] = ltl2dpw(goal, list(m[6]), valuations)

        if not cgsFlag:
            if verbose:
                print("\n Convert G_{LTL} to G_{PAR}...\n")
            GPar = convertG(modules,DPWs,M)

        else:
            if verbose:
                print("\n Convert G_{LTL} to G_{PAR}...\n")
            GPar = convertG_cgs(modules,DPWs,M)
        GPar_v = GPar.vcount()
        GPar_e = GPar.ecount()
        perfConstruction = time.time()*1000 - start
    else:
        print("ERROR: Undefined problem")
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
    elif q_flag==6:
        '''Checking a pure-memoryless strategy profile'''
        empCheck = 0.0
        start = time.time()*1000
        if aliases_file:
            action_aliases, state_aliases = load_aliases(aliases_file)
        else:
            action_aliases, state_aliases = None, None
        try:
            raw_profile = load_profile_json(profile_file, action_aliases, state_aliases)
            result = check_profile_memoryless(
                modules, environment, M, GPar, cgsFlag,
                phi_formula, phi_alphabet, raw_profile)
        except (UnsupportedModelError, ProfileError) as e:
            print("ERROR: "+str(e))
            return True
        print(print_profile_report(modules, M, result, action_aliases, state_aliases))
        if json_out_file:
            import json
            with open(json_out_file, 'w') as f:
                json.dump(to_json_result(modules, M, result, action_aliases, state_aliases), f, indent=2)
            print("Machine-readable result written to " + json_out_file)
        empCheck = time.time()*1000 - start
    else:
        print("Undefined Problem!")
        printhelp()
        return True

    if (q_flag not in [6,7,8]) and verbose:
        print_performance(perfConstruction,perfParser,perfPGSolver,empCheck,GPar_v,GPar_e,TTPG_vmax,TTPG_emax,q_flag)
    
if __name__ == "__main__":
    main(sys.argv[3:])
    
