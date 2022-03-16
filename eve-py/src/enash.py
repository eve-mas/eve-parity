# -*- coding: utf-8 -*-
from utils import *
from gltl2gpar import drawGPar,sequencer_rmg_single,sequencer_cgs_single
from generatepun import compute_pun
import time

def enash(modules,GPar,draw_flag,cgsFlag,pf,DPW_prop,alphabets):
    TTPG_vmax=0 #count the max number of vertices in TTPG/GPar sequentialisation
    TTPG_emax=0 #count the max number of edges in TTPG/GPar sequentialisation
    TTPG = Graph(directed=True) #init GPar sequentialisation
    perfPGSolver = 0.0

    '''
    generate W (winning coalitions)
    reverse the list to generate from big to small
    hence always gets pareto optimal if NE exists    
    '''
    W = list(reversed(generate_set_W(modules)))

    '''Compute G^{-L}_{PAR}'''
    GPar_L = Graph(directed=True)
    NE_flag=False
    PUN = {}
    for w in W:

        if len(w)==len(modules):
            '''trivial cases all win/lose'''
            s_Alpha = build_streett_prod(GPar,w,modules)
            L,L_sigma = Streett_emptyness(GPar,s_Alpha,modules)

            '''if not empty'''
            if L.vcount()!= 0:
                DPW_product = graph_product(GPar, DPW_prop, alphabets,cgsFlag)
                e_Alpha = build_streett_prod(DPW_product, w+(len(modules),), modules+[{1:set(['environment'])}])
                E, E_sigma = Streett_emptyness(DPW_product, e_Alpha, modules+[{1:set(['environment'])}])

                if E.vcount() != 0:
                    print('>>> YES, the property '+ replace_symbols(pf) +' is satisfied in some NE <<<')
                    print('Winning Coalition',(num2name(w,modules)))
                    NE_flag=True
                    if draw_flag:
                        '''draw & printout strategy progile \vec{sigma}'''
                        drawGPar(E_sigma)
                        printSynthSigmaDetails(E_sigma)
                    break
        else:
            l = get_l(list(w),modules)
            PUN_L = set([v.index for v in GPar.vs])
            for pl in l:
                pl_name = list(modules[pl][1])[0]
                try:
                    if TTPG[pl_name]:
                        pass
                except KeyError:
                    if check_verbose_flag():
                        print("\n Sequentialising GPar for punishing <"+pl_name+">")
                    if not cgsFlag:
                        startPGSolver = time.time()*1000
                        sequencer_rmg_single(pl,GPar,TTPG,modules)
                        perfPGSolver = perfPGSolver + time.time()*1000 - startPGSolver
                        if TTPG_vmax<TTPG[pl_name].vcount():
                            TTPG_vmax=TTPG[pl_name].vcount()
                        if TTPG_emax<TTPG[pl_name].ecount():
                            TTPG_emax=TTPG[pl_name].ecount()
                    else:
                        startPGSolver = time.time()*1000
                        sequencer_cgs_single(pl,GPar,TTPG,modules)
                        perfPGSolver = perfPGSolver + time.time()*1000 - startPGSolver
                        if TTPG_vmax<TTPG[pl_name].vcount():
                            TTPG_vmax=TTPG[pl_name].vcount()
                        if TTPG_emax<TTPG[pl_name].ecount():
                            TTPG_emax=TTPG[pl_name].ecount()
                            
                '''compute pl_name pun region'''
#                print pl_name,PUN
                if pl_name not in PUN:
                    if check_verbose_flag():
                        print("\n Computing punishing region for <"+pl_name+">")
                    PUN=compute_pun(pl_name,PUN,TTPG)
#                print 'pl_name',pl_name
                PUN_L = PUN_L.intersection(set(PUN[pl_name]))
#                print '>>>>', PUN_L
                '''init state s0 not included in PUN_L'''
                if 0 in PUN_L:        
                    GPar_L[frozenset(l)]=build_GPar_L(GPar,w,l,PUN_L)
                else:
                    GPar_L[frozenset(l)]=Graph(directed=True)

            if GPar_L[frozenset(l)].vcount()!=0:
                '''build the product of streett automata'''
                s_Alpha = build_streett_prod(GPar_L[frozenset(l)],w,modules)

                '''check street automaton emptiness'''
                L,L_sigma = Streett_emptyness(GPar_L[frozenset(l)],s_Alpha,modules)

                '''if not empty'''
                if L.vcount() != 0:
                    DPW_product = graph_product(L_sigma, DPW_prop, alphabets, cgsFlag)
                    e_Alpha = build_streett_prod(DPW_product, w + (len(modules),), modules + [{1: set(['environment'])}])
                    E, E_sigma = Streett_emptyness(DPW_product, e_Alpha, modules + [{1: set(['environment'])}])

                    if E.vcount() != 0:
                        print('>>> YES, the property ' + replace_symbols(pf) + ' is satisfied in some NE <<<')
                        print('Winning Coalition', (num2name(w, modules)))
                        NE_flag = True
                        if draw_flag:
                            '''draw & printout strategy progile \vec{sigma}'''
                            drawGPar(E_sigma)
                            printSynthSigmaDetails(E_sigma)
                        break

    if not NE_flag:
        print('>>> NO, the property '+ replace_symbols(pf) +' is not satisfied in any NE <<<')
    return perfPGSolver,TTPG_vmax,TTPG_emax

