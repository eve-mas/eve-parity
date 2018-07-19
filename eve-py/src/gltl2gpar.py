# -*- coding: utf-8 -*-

#import itertools
from igraph import *
import copy
from srmlutil import *
from parsrml import *
from utils import check_draw_flag


'''sequentialisation of GPar to two-player zero-sum parity game'''
def sequencer(GPar,modules):
    TTPG = Graph(directed=True)    
    TTPG_vmax=0
    TTPG_emax=0
#    S_intermediate=set()
#    update_labs(GPar)
    
    '''d_-i'''
    for idx,m in enumerate(modules):
        pl_name=list(m[1])[0]
        TTPG[pl_name] = copy.copy(GPar)
        '''delete all edges'''
        TTPG[pl_name].delete_edges(TTPG.es)
#        print summary(TTPG[pl_name])
        modules_exi = copy.copy(modules)
#        print m
        
        '''delete punished player'''
        del modules_exi[idx]
#        for idx_exi,m_exi in enumerate(modules_exi):
#            print idx_exi,m_exi
#        d_exi = DGenerate(modules_exi) #generate d_{-i}
#        d_exi = [frozenset(d) for d in d_exi] #convert to list of sets
#        print d_exi
#        a_i = DGenerate(m)
#        print a_i
#        ctr_var = list(m[2])
#        print 'ctrctr_var',ctr_var
        oriv_count = TTPG[pl_name].vcount()
        for v in TTPG[pl_name].vs:
            v['prior']=v['colour'][pl_name]+1
            v['itd']=False

        '''check possible d_exi'''
#        for state in TTPG[pl_name].vs:
        for i in xrange(oriv_count):
#            print v['val']
#            print 'state[]',state['label']
            for d in generate_coal_dir(TTPG[pl_name].vs[i]['val'],modules_exi):
#                print d
                '''add intermediate states to TTPG'''
                TTPG[pl_name].add_vertex(label=set([i,d]),prior=(TTPG[pl_name].vs[i]['colour'][pl_name]+1),itd=True)
                intermed_state = TTPG[pl_name].vs.find(label=set([i,d]))
                
                '''add edge from prev state to intermediate state'''
                TTPG[pl_name].add_edge(TTPG[pl_name].vs[i],intermed_state)
                for d_i in generate_coal_dir(TTPG[pl_name].vs[i]['val'],[m]):
#                    print '>>>>',d_i
                    d_a_i = list(d)+list(d_i)
#                    print 'd_a_i',d_a_i
                    for e in GPar.es.select(word=set(d_a_i)):
                            if e.source==i:
#                                print TTPG[pl_name].vs[e.target]
                                ''''add edge from intermediate state to next state'''
                                TTPG[pl_name].add_edge(intermed_state,TTPG[pl_name].vs[e.target])
        
#        for d in d_exi:
##            print d
#            for i in xrange(oriv_count):
##                print TTPG[pl_name].vs[i]
##                print TTPG[pl_name].vs[i]['colour'][pl_name]
##                TTPG[pl_name].vs[i]['itd']=False
##                TTPG[pl_name].vs[i]['prior']=TTPG[pl_name].vs[i]['colour'][pl_name]+1
##                S_intermediate.add(frozenset([i,d]))
#                TTPG[pl_name].add_vertex(label=set([i,d]),prior=(TTPG[pl_name].vs[i]['colour'][pl_name]+1),itd=True)
#                intermed_state = TTPG[pl_name].vs.find(label=set([i,d]))
#                TTPG[pl_name].add_edge(TTPG[pl_name].vs[i],intermed_state)
##        print S_intermediate
#                for n in xrange(len(ctr_var)+1):
#                    for subset in itertools.combinations(ctr_var,n):
##                        print subset
#                        d_a_i = list(d)+list(subset)
#                        for e in GPar.es.select(word=set(d_a_i)):
#                            if e.source==i:
##                                print e
##                                print 'intermed_state',intermed_state
#                                TTPG[pl_name].add_edge(intermed_state,TTPG[pl_name].vs[e.target])
#                        stup_next=[]
#                        stup_next.append(get_next_mstate(cur,d_a_i,M))
#                        stup_next = get_next_qtup(cur,d,DPWs,modules,stup_next)
#                        GPar.add_edge(cur,GPar.vs.find(label=set(stup_next)),label=set(d))
                
#        for v in TTPG[pl_name].vs:
##            if v['colour']==None:
##                v['colour']=1
#            print v
        print summary(TTPG[pl_name])
        
        '''get max size of TTPG'''
        if TTPG_vmax<TTPG[pl_name].vcount():
            TTPG_vmax = TTPG[pl_name].vcount()
        if TTPG_emax<TTPG[pl_name].ecount():
            TTPG_emax = TTPG[pl_name].ecount()            
            
        if check_draw_flag():
            drawTTPG_kk(TTPG[pl_name])
    return TTPG,TTPG_vmax,TTPG_emax
    
'''sequentialisation of RMG GPar to two-player zero-sum parity game'''
def sequencer_rmg(GPar,modules):
    TTPG = Graph(directed=True)    
    TTPG_vmax=0
    TTPG_emax=0
#    S_intermediate=set()
#    update_labs(GPar)
    
    '''d_-i'''
    for idx,m in enumerate(modules):
        pl_name=list(m[1])[0]
        TTPG[pl_name] = copy.copy(GPar)
        '''delete all edges'''
        TTPG[pl_name].delete_edges(TTPG.es)
#        print summary(TTPG[pl_name])
        modules_exi = copy.copy(modules)
#        print m
        
        '''delete punished player'''
        del modules_exi[idx]
#        for idx_exi,m_exi in enumerate(modules_exi):
#            print idx_exi,m_exi
#        d_exi = DGenerate(modules_exi) #generate d_{-i}
#        d_exi = [frozenset(d) for d in d_exi] #convert to list of sets
#        print d_exi
#        a_i = DGenerate(m)
#        print a_i
#        ctr_var = list(m[2])
#        print 'ctrctr_var',ctr_var
        oriv_count = TTPG[pl_name].vcount()
        for v in TTPG[pl_name].vs:
            v['prior']=v['colour'][pl_name]+1
            v['itd']=False

        '''check possible d_exi'''
#        for state in TTPG[pl_name].vs:
        for i in xrange(oriv_count):
#            print v['val']
#            print 'state[]',state['label']
            """(pre)init state"""
            if i==0:
                for state in productInit(modules_exi):
                    stateLabel = getValuation(state)
                    if stateLabel==None:
                        stateLabel=frozenset()
                    else:
                        stateLabel=frozenset(stateLabel)
                    d = tuple(stateLabel)
#                    print "%%%", d
                    '''add init intermed statte'''
                    TTPG[pl_name].add_vertex(label=set([i,d]),prior=(TTPG[pl_name].vs[i]['colour'][pl_name]+1),itd=True)
                    intermed_state = TTPG[pl_name].vs.find(label=set([i,d]))
                    '''add edge from prev state to intermediate state'''
                    TTPG[pl_name].add_edge(TTPG[pl_name].vs[i],intermed_state)
                    for state_i in productInit([m]):
                        stateLabel_i = getValuation(state_i)
                        if stateLabel_i==None:
                            stateLabel_i=frozenset()
                        else:
                            stateLabel_i=frozenset(stateLabel_i)
                        d_i = tuple(stateLabel_i)
                        d_a_i = list(d)+list(d_i)
                        for e in GPar.es.select(word=set(d_a_i)):
                                if e.source==i:
    #                                print TTPG[pl_name].vs[e.target]
                                    ''''add edge from intermediate state to next state'''
                                    TTPG[pl_name].add_edge(intermed_state,TTPG[pl_name].vs[e.target])
            else:
                for d in generate_coal_dir(TTPG[pl_name].vs[i]['val'],modules_exi):
#                    print d
                    '''add intermediate states to TTPG'''
                    TTPG[pl_name].add_vertex(label=set([i,d]),prior=(TTPG[pl_name].vs[i]['colour'][pl_name]+1),itd=True)
                    intermed_state = TTPG[pl_name].vs.find(label=set([i,d]))
                    
                    '''add edge from prev state to intermediate state'''
                    TTPG[pl_name].add_edge(TTPG[pl_name].vs[i],intermed_state)
                    for d_i in generate_coal_dir(TTPG[pl_name].vs[i]['val'],[m]):
    #                    print '>>>>',d_i
                        d_a_i = list(d)+list(d_i)
    #                    print 'd_a_i',d_a_i
                        for e in GPar.es.select(word=set(d_a_i)):
                                if e.source==i:
    #                                print TTPG[pl_name].vs[e.target]
                                    ''''add edge from intermediate state to next state'''
                                    TTPG[pl_name].add_edge(intermed_state,TTPG[pl_name].vs[e.target])
            
    #        for d in d_exi:
    ##            print d
    #            for i in xrange(oriv_count):
    ##                print TTPG[pl_name].vs[i]
    ##                print TTPG[pl_name].vs[i]['colour'][pl_name]
    ##                TTPG[pl_name].vs[i]['itd']=False
    ##                TTPG[pl_name].vs[i]['prior']=TTPG[pl_name].vs[i]['colour'][pl_name]+1
    ##                S_intermediate.add(frozenset([i,d]))
    #                TTPG[pl_name].add_vertex(label=set([i,d]),prior=(TTPG[pl_name].vs[i]['colour'][pl_name]+1),itd=True)
    #                intermed_state = TTPG[pl_name].vs.find(label=set([i,d]))
    #                TTPG[pl_name].add_edge(TTPG[pl_name].vs[i],intermed_state)
    ##        print S_intermediate
    #                for n in xrange(len(ctr_var)+1):
    #                    for subset in itertools.combinations(ctr_var,n):
    ##                        print subset
    #                        d_a_i = list(d)+list(subset)
    #                        for e in GPar.es.select(word=set(d_a_i)):
    #                            if e.source==i:
    ##                                print e
    ##                                print 'intermed_state',intermed_state
    #                                TTPG[pl_name].add_edge(intermed_state,TTPG[pl_name].vs[e.target])
    #                        stup_next=[]
    #                        stup_next.append(get_next_mstate(cur,d_a_i,M))
    #                        stup_next = get_next_qtup(cur,d,DPWs,modules,stup_next)
    #                        GPar.add_edge(cur,GPar.vs.find(label=set(stup_next)),label=set(d))
                
#        for v in TTPG[pl_name].vs:
##            if v['colour']==None:
##                v['colour']=1
#            print v
        print summary(TTPG[pl_name])
        
        '''get max size of TTPG'''
        if TTPG_vmax<TTPG[pl_name].vcount():
            TTPG_vmax = TTPG[pl_name].vcount()
        if TTPG_emax<TTPG[pl_name].ecount():
            TTPG_emax = TTPG[pl_name].ecount()            
            
        if check_draw_flag():
            drawTTPG_kk(TTPG[pl_name])
    return TTPG,TTPG_vmax,TTPG_emax
    
def sequencer_cgs_single(idx,GPar,TTPG,modules):
    m = modules[idx]
#    print list((modules[idx])[1])[0]
    pl_name=list((modules[idx])[1])[0]
    TTPG[pl_name] = copy.copy(GPar)
    '''delete all edges'''
    TTPG[pl_name].delete_edges(TTPG.es)
#        print summary(TTPG[pl_name])
    modules_exi = copy.copy(modules)
    
    '''delete punished player'''
    del modules_exi[idx]
#        for idx_exi,m_exi in enumerate(modules_exi):
#            print idx_exi,m_exi
#        d_exi = DGenerate(modules_exi) #generate d_{-i}
#        d_exi = [frozenset(d) for d in d_exi] #convert to list of sets
#        print d_exi
#        a_i = DGenerate(m)
#        print a_i
#        ctr_var = list(m[2])
#        print 'ctrctr_var',ctr_var
    oriv_count = TTPG[pl_name].vcount()
    for v in TTPG[pl_name].vs:
        v['prior']=v['colour'][pl_name]+1
        v['itd']=False

    '''check possible d_exi'''
#        for state in TTPG[pl_name].vs:
    for i in xrange(oriv_count):
#            print v['val']
#            print 'state[]',state['label']
        for d in generate_coal_dir(TTPG[pl_name].vs[i]['val'],modules_exi):
#                print d
            '''add intermediate states to TTPG'''
            TTPG[pl_name].add_vertex(label=set([i,d]),prior=(TTPG[pl_name].vs[i]['colour'][pl_name]+1),itd=True)
            intermed_state = TTPG[pl_name].vs.find(label=set([i,d]))
            
            '''add edge from prev state to intermediate state'''
            TTPG[pl_name].add_edge(TTPG[pl_name].vs[i],intermed_state)
            for d_i in generate_coal_dir(TTPG[pl_name].vs[i]['val'],[m]):
#                    print '>>>>',d_i
                d_a_i = list(d)+list(d_i)
#                    print 'd_a_i',d_a_i
                for e in GPar.es.select(word=set(d_a_i)):
                        if e.source==i:
#                                print TTPG[pl_name].vs[e.target]
                            ''''add edge from intermediate state to next state'''
                            TTPG[pl_name].add_edge(intermed_state,TTPG[pl_name].vs[e.target])
    
#        for d in d_exi:
##            print d
#            for i in xrange(oriv_count):
##                print TTPG[pl_name].vs[i]
##                print TTPG[pl_name].vs[i]['colour'][pl_name]
##                TTPG[pl_name].vs[i]['itd']=False
##                TTPG[pl_name].vs[i]['prior']=TTPG[pl_name].vs[i]['colour'][pl_name]+1
##                S_intermediate.add(frozenset([i,d]))
#                TTPG[pl_name].add_vertex(label=set([i,d]),prior=(TTPG[pl_name].vs[i]['colour'][pl_name]+1),itd=True)
#                intermed_state = TTPG[pl_name].vs.find(label=set([i,d]))
#                TTPG[pl_name].add_edge(TTPG[pl_name].vs[i],intermed_state)
##        print S_intermediate
#                for n in xrange(len(ctr_var)+1):
#                    for subset in itertools.combinations(ctr_var,n):
##                        print subset
#                        d_a_i = list(d)+list(subset)
#                        for e in GPar.es.select(word=set(d_a_i)):
#                            if e.source==i:
##                                print e
##                                print 'intermed_state',intermed_state
#                                TTPG[pl_name].add_edge(intermed_state,TTPG[pl_name].vs[e.target])
#                        stup_next=[]
#                        stup_next.append(get_next_mstate(cur,d_a_i,M))
#                        stup_next = get_next_qtup(cur,d,DPWs,modules,stup_next)
#                        GPar.add_edge(cur,GPar.vs.find(label=set(stup_next)),label=set(d))
            
#        for v in TTPG[pl_name].vs:
##            if v['colour']==None:
##                v['colour']=1
#            print v
    print summary(TTPG[pl_name])
    return True
    
def sequencer_rmg_single(idx,GPar,TTPG,modules):
    m = modules[idx]
#    print list((modules[idx])[1])[0]
    pl_name=list((modules[idx])[1])[0]
    TTPG[pl_name] = copy.copy(GPar)
    '''delete all edges'''
    TTPG[pl_name].delete_edges(TTPG.es)
#        print summary(TTPG[pl_name])
    modules_exi = copy.copy(modules)
#        print m
    
    '''delete punished player'''
    del modules_exi[idx]
#        for idx_exi,m_exi in enumerate(modules_exi):
#            print idx_exi,m_exi
#        d_exi = DGenerate(modules_exi) #generate d_{-i}
#        d_exi = [frozenset(d) for d in d_exi] #convert to list of sets
#        print d_exi
#        a_i = DGenerate(m)
#        print a_i
#        ctr_var = list(m[2])
#        print 'ctrctr_var',ctr_var
    oriv_count = TTPG[pl_name].vcount()
    for v in TTPG[pl_name].vs:
        v['prior']=v['colour'][pl_name]+1
        v['itd']=False

    '''check possible d_exi'''
#        for state in TTPG[pl_name].vs:
    for i in xrange(oriv_count):
#            print v['val']
#            print 'state[]',state['label']
        """(pre)init state"""
        if i==0:
            for state in productInit(modules_exi):
                stateLabel = getValuation(state)
                if stateLabel==None:
                    stateLabel=frozenset()
                else:
                    stateLabel=frozenset(stateLabel)
                d = tuple(stateLabel)
#                    print "%%%", d
                '''add init intermed statte'''
                TTPG[pl_name].add_vertex(label=set([i,d]),prior=(TTPG[pl_name].vs[i]['colour'][pl_name]+1),itd=True)
                intermed_state = TTPG[pl_name].vs.find(label=set([i,d]))
                '''add edge from prev state to intermediate state'''
                TTPG[pl_name].add_edge(TTPG[pl_name].vs[i],intermed_state)
                for state_i in productInit([m]):
                    stateLabel_i = getValuation(state_i)
                    if stateLabel_i==None:
                        stateLabel_i=frozenset()
                    else:
                        stateLabel_i=frozenset(stateLabel_i)
                    d_i = tuple(stateLabel_i)
                    d_a_i = list(d)+list(d_i)
                    for e in GPar.es.select(word=set(d_a_i)):
                            if e.source==i:
#                                print TTPG[pl_name].vs[e.target]
                                ''''add edge from intermediate state to next state'''
                                TTPG[pl_name].add_edge(intermed_state,TTPG[pl_name].vs[e.target])
        else:
            for d in generate_coal_dir(TTPG[pl_name].vs[i]['val'],modules_exi):
#                    print d
                '''add intermediate states to TTPG'''
                TTPG[pl_name].add_vertex(label=set([i,d]),prior=(TTPG[pl_name].vs[i]['colour'][pl_name]+1),itd=True)
                intermed_state = TTPG[pl_name].vs.find(label=set([i,d]))
                
                '''add edge from prev state to intermediate state'''
                TTPG[pl_name].add_edge(TTPG[pl_name].vs[i],intermed_state)
                for d_i in generate_coal_dir(TTPG[pl_name].vs[i]['val'],[m]):
#                    print '>>>>',d_i
                    d_a_i = list(d)+list(d_i)
#                    print 'd_a_i',d_a_i
                    for e in GPar.es.select(word=set(d_a_i)):
                            if e.source==i:
#                                print TTPG[pl_name].vs[e.target]
                                ''''add edge from intermediate state to next state'''
                                TTPG[pl_name].add_edge(intermed_state,TTPG[pl_name].vs[e.target])
        
#        for d in d_exi:
##            print d
#            for i in xrange(oriv_count):
##                print TTPG[pl_name].vs[i]
##                print TTPG[pl_name].vs[i]['colour'][pl_name]
##                TTPG[pl_name].vs[i]['itd']=False
##                TTPG[pl_name].vs[i]['prior']=TTPG[pl_name].vs[i]['colour'][pl_name]+1
##                S_intermediate.add(frozenset([i,d]))
#                TTPG[pl_name].add_vertex(label=set([i,d]),prior=(TTPG[pl_name].vs[i]['colour'][pl_name]+1),itd=True)
#                intermed_state = TTPG[pl_name].vs.find(label=set([i,d]))
#                TTPG[pl_name].add_edge(TTPG[pl_name].vs[i],intermed_state)
##        print S_intermediate
#                for n in xrange(len(ctr_var)+1):
#                    for subset in itertools.combinations(ctr_var,n):
##                        print subset
#                        d_a_i = list(d)+list(subset)
#                        for e in GPar.es.select(word=set(d_a_i)):
#                            if e.source==i:
##                                print e
##                                print 'intermed_state',intermed_state
#                                TTPG[pl_name].add_edge(intermed_state,TTPG[pl_name].vs[e.target])
#                        stup_next=[]
#                        stup_next.append(get_next_mstate(cur,d_a_i,M))
#                        stup_next = get_next_qtup(cur,d,DPWs,modules,stup_next)
#                        GPar.add_edge(cur,GPar.vs.find(label=set(stup_next)),label=set(d))
            
#        for v in TTPG[pl_name].vs:
##            if v['colour']==None:
##                v['colour']=1
#            print v
    print summary(TTPG[pl_name])
    return TTPG[pl_name].vcount(), TTPG[pl_name].ecount()
    
'''this function generates direction based on players/modules coalition'''
def generate_coal_dir(prev_val,coalition):
    direction=[]
    for updateCommand in jointEnabled(guardEval(set(list(prev_val)),coalition)):
            commands=[]
#                print 'updateCommand',updateCommand
            for k,v in updateCommand:
                '''for each jointEnabled update command'''
                updateCommand_noguard = without_keys(v,'guard') #remove dict key 'guard'
#                    print 'updateCommand_noguard',updateCommand_noguard
                for k,l in updateCommand_noguard.items():
                    '''for each variable'''
#                        print k,l
                    if k != 0:
                        commands.append(str({k:parse_rpn(frozenset(list(prev_val)),l)}))
            try:
                nextState = frozenset(getValuation(tuple(commands)))
#                    print '>>>',commands,nextState
            except TypeError:
                nextState = frozenset()
#            print nextState
            direction.append(nextState)
    return direction

    
def drawTTPG_rand(TTPG):
    layout = TTPG.layout('random')
#    mc = max_prior(TTPG)+1
#    r = 3*(float(TTPG.vcount())/mc)
    for v in TTPG.vs:
        v['color']=hsv_to_rgb(float(v.index)/TTPG.vcount(),1,1)
#        v['size']=r/(1+v['prior'])
        if v['itd']:
            v['shape']='circle'
#            v['color']='blue'
        else:
            v['shape']='square'
#            v['color']='red'
    for e in TTPG.es:
        e['color']=TTPG.vs[e.source]['color']
    TTPG.vs['label']=[None for v in TTPG.vs]
    TTPG.vs[0]['label']='S0'
    visual_style = {}
    visual_style['layout']=layout
    visual_style['bbox']=(1000,1000)
    visual_style['margin']=40
#    visual_style['vertex_label_dist']=2
    visual_style['autocurve']=True
    visual_style['vertex_frame_width']=0
    plot(TTPG, **visual_style)
    

'''convert LTL Game to Parity Game (RMGs)'''
def convertG(modules,DPWs,M):
    GPar = Graph(directed=True)
    dpw_states = {}
#    print M.vs[0]['label'] 
    colour_tuple = {}
    S = set()
    
    '''add (pre?)init state'''
    for m in modules:
        colour_tuple[list(m[1])[0]]=0
    GPar.add_vertex(label=set(['init']),colour=copy.copy(colour_tuple))
#    for m in modules:
#        states = []
#        alphabets=set(list(m[6])) #set of symbols in DPW
#        for v in DPWs[list(m[1])[0]].vs:
#            states.append(list(m[1])[0]+'-'+str(v.index))
##        print states,m[2]
#        dpw_states[list(m[1])[0]]=states
##        print 'states',states
#        w = set(list(set(M.vs[0]['label'][1]).intersection(alphabets)))
##        print w
#        if len(w)==0:
#            w = ['']
#        for edge in DPWs[list(m[1])[0]].es.select(word=set(w)):
##            print edge
#            if edge.source==0:
##                print edge.target,DPWs[list(m[1])[0]].vs[edge.target]['colour']
#                s0.append(list(m[1])[0]+'-'+str(edge.target))
#                colour_tuple[list(m[1])[0]]=DPWs[list(m[1])[0]].vs[edge.target]['colour']
#          
#    '''get valuation in init state s0'''
#    for state in productInit(modules):
#        stateLabel = getValuation(state)
#        print 'stateLabel',stateLabel
#    print 'stateLabel', getValuation(productInit(modules))
        
    for idx,state in enumerate(productInit(modules)):
        s0 = ['M-'+str(idx+1)]
#        print s0
        stateLabel = getValuation(state)
        if stateLabel==None:
            stateLabel=()
        for m in modules:
            states = []
            alphabets=set(list(m[6])) #set of symbols in DPW
            for v in DPWs[list(m[1])[0]].vs:
                states.append(list(m[1])[0]+'-'+str(v.index))
    #        print states,m[2]
            dpw_states[list(m[1])[0]]=states
    #        print 'states',states
            w = set(list(set(M.vs[idx]['label'][1]).intersection(alphabets)))
    #        print w
            if len(w)==0:
                w = ['']
            for edge in DPWs[list(m[1])[0]].es.select(word=set(w)):
    #            print edge
                if edge.source==0:
    #                print edge.target,DPWs[list(m[1])[0]].vs[edge.target]['colour']
                    s0.append(list(m[1])[0]+'-'+str(edge.target))
                    colour_tuple[list(m[1])[0]]=DPWs[list(m[1])[0]].vs[edge.target]['colour']
#        print s0
        '''init state (s0) in GPar'''
#    print 's0',s0,colour_tuple
        '''convert stateLabel to tuple to match val format'''
        GPar.add_vertex(label=set(s0),colour=copy.copy(colour_tuple),val=tuple(stateLabel))
        S.add(frozenset(s0))
    
    
#    print stateprod(dpw_states,M)
        
    
#    Direction = DGenerate(modules)
#    '''Why not directly check update commands???'''
#    print Direction
    prevS = set()
    while prevS != S:
        prevS = copy.copy(S)
        for state in GPar.vs:
#            print "state['label']",state
            '''direction via updatecommand (faster than brute force method)'''
#            for updateCommand in jointEnabled(guardEval(state['label'],modules)):
#                commands=[]
            if state.index!=0:
                for d in generate_coal_dir(state['val'],modules):
                    d = tuple(d)
                    stup_next=[]
                    next_mstate = get_next_mstate(state,d,M)
    #                print next_mstate
    #                print 'direction', d
                    if next_mstate!=None:
                        stup_next.append(next_mstate)
                        stup_next = get_next_qtup(state,d,DPWs,modules,stup_next)
                        colour_tuple = get_colour(state,d,DPWs,modules,stup_next)
                        if not frozenset(stup_next) in S:
                            GPar.add_vertex(label=stup_next,colour=copy.copy(colour_tuple),val=d)
                            S.add(frozenset(stup_next))
            
    #            '''direction via brute force'''
    #            for d in Direction:
    ##                print d
    #                stup_next = []
    ##                print state
    #                next_mstate = get_next_mstate(state,d,M)
    ##                print next_mstate
    ##                print 'direction', d
    #                if next_mstate!=None:
    #                    stup_next.append(next_mstate)
    #                    stup_next = get_next_qtup(state,d,DPWs,modules,stup_next)
    #                    colour_tuple = get_colour(state,d,DPWs,modules,stup_next)
    #                    if not frozenset(stup_next) in S:
    #                        GPar.add_vertex(label=stup_next,colour=copy.copy(colour_tuple),val=d)
    #                        S.add(frozenset(stup_next))
                
    '''adding edges'''
    for cur in GPar.vs:
#        for nex in GPar.vs:
#            for d in Direction:
#                stup_next=[]
#                stup_next.append(get_next_mstate(cur,d,M))
#                stup_next = get_next_qtup(cur,d,DPWs,modules,stup_next)
#                print stup_next,GPar.vs.find(label=set(stup_next))
#                if set(nex['label'])==set(stup_next):
#                    GPar.add_edge(cur,nex,label=set(d))
        if cur.index==0:
            for idx,state in enumerate(productInit(modules)):
                stateLabel = getValuation(state)
                if stateLabel==None:
                    stateLabel=frozenset()
                else:
                    stateLabel=frozenset(stateLabel)
#                print '>>>',stateLabel
                d = tuple(stateLabel)
                GPar.add_edge(cur,GPar.vs[idx+1],label=set(d))
        else:
            '''this method of adding edges seems to be faster'''
            for d in generate_coal_dir(cur['val'],modules):
                d = tuple(d)
                stup_next=[]
                next_mstate = get_next_mstate(cur,d,M)
                if next_mstate!=None:
                    stup_next.append(next_mstate)
                    stup_next = get_next_qtup(cur,d,DPWs,modules,stup_next)
                    GPar.add_edge(cur,GPar.vs.find(label=set(stup_next)),label=set(d))
    #        for d in Direction:
    #            stup_next=[]
    #            next_mstate = get_next_mstate(cur,d,M)
    #            if next_mstate!=None:
    #                stup_next.append(next_mstate)
    #                stup_next = get_next_qtup(cur,d,DPWs,modules,stup_next)
    #                GPar.add_edge(cur,GPar.vs.find(label=set(stup_next)),label=set(d))
    update_labs(GPar)
    # if check_draw_flag():
    #     drawGPar(GPar)
    return GPar
    
    """this function converts G_LTL to G_Par"""
def convertG_cgs(modules,DPWs,M):
    GPar = Graph(directed=True)
    dpw_states = {}
    s0 = ['M-0'] 
    colour_tuple = {}
    S = set()
    
    for m in modules:
        states = []
        alphabets=set(list(m[6])) #set of symbols in DPW
#        print alphabets
        for v in DPWs[list(m[1])[0]].vs:
            states.append(list(m[1])[0]+'-'+str(v.index))
#        print states,m[2]
        dpw_states[list(m[1])[0]]=states
#        print 'states',states
#        print list(set(M.vs[0]['label'][1]))
        w = set(list(set(M.vs[0]['label'][1]).intersection(alphabets)))
#        print w
        if len(w)==0:
            w = ['']
        for edge in DPWs[list(m[1])[0]].es.select(word=set(w)):
#            print edge
            if edge.source==0:
#                print edge.target,DPWs[list(m[1])[0]].vs[edge.target]['colour']
                s0.append(list(m[1])[0]+'-'+str(edge.target))
                colour_tuple[list(m[1])[0]]=DPWs[list(m[1])[0]].vs[edge.target]['colour']
                
                
#    print s0
#    '''get valuation in init state s0'''
#    for state in productInit(modules):
#        stateLabel = getValuation(state)
#        print stateLabel
    
#    for e in M.es():
#        if e.target==0:
#            print e
    '''add init state (s0) in GPar'''
    GPar.add_vertex(label=set(s0),colour=copy.copy(colour_tuple),val=frozenset(M.vs[0]['label'][1]))
    S.add(frozenset(s0))
    
    '''generate GPar states'''
    prevS = set()
    while prevS != S:
        prevS = copy.copy(S)
        for state in GPar.vs:
#            print "state['label']",state['val']
            '''
            this generate direction based on sequence of states/run-based strategies
            ''' 
            for d in generate_coal_dir(state['val'],modules):
                d = tuple(d)
#                print d
                next_mstate,nextLabel = get_next_mstate_cgs(state,d,M)
                if d!=None:
                    if 'matching_pennies_player_1_var' in d:
                        nextLabel.append('matching_pennies_player_1_var')
                    if 'matching_pennies_player_2_var' in d:
                        nextLabel.append('matching_pennies_player_2_var') 
#                print 'next_mstate', next_mstate,nextLabel
#            for d in Direction:
#                print d
                stup_next = []
#                print state

#                '''d to val'''
                
#                next_mstate = get_next_mstate(state,d,M)
#                print 'next_mstate', next_mstate
#                print 'direction', d
                if next_mstate!=None:
                    stup_next.append(next_mstate)
                    stup_next = get_next_qtup(state,tuple(nextLabel),DPWs,modules,stup_next)
                    colour_tuple = get_colour(state,tuple(nextLabel),DPWs,modules,stup_next)
#                    print S
#                    print '###',stup_next, colour_tuple
                    if not frozenset(stup_next) in S:
                        GPar.add_vertex(label=stup_next,colour=copy.copy(colour_tuple),val=frozenset(nextLabel))
                        S.add(frozenset(stup_next))
                        
    '''adding edges'''
    for cur in GPar.vs:
#        for nex in GPar.vs:
#            for d in Direction:
#                stup_next=[]
#                stup_next.append(get_next_mstate(cur,d,M))
#                stup_next = get_next_qtup(cur,d,DPWs,modules,stup_next)
#                print stup_next,GPar.vs.find(label=set(stup_next))
#                if set(nex['label'])==set(stup_next):
#                    GPar.add_edge(cur,nex,label=set(d))
        '''this method of adding edges seems to be faster'''
        for d in generate_coal_dir(cur['val'],modules):
            d = tuple(d)
            stup_next=[]
            next_mstate,nextLabel = get_next_mstate_cgs(cur,d,M)
            if d!=None:
                if 'matching_pennies_player_1_var' in d:
                    nextLabel.append('matching_pennies_player_1_var')
                if 'matching_pennies_player_2_var' in d:
                    nextLabel.append('matching_pennies_player_2_var') 
            if next_mstate!=None:
                stup_next.append(next_mstate)
                stup_next = get_next_qtup(cur,tuple(nextLabel),DPWs,modules,stup_next)
                GPar.add_edge(cur,GPar.vs.find(label=set(stup_next)),label=set(d))
    
    update_labs(GPar)

    # if check_draw_flag():
        # drawGPar(GPar)

    return GPar

def forpraline(GPar):
    print "FOR PRALINE"


    f = open('tcgen/update','w')


    print GPar.get_edgelist()
    for e in GPar.es:
        if e.index == 0:
            f.write("if (state ==" + str(e.source) + " && ")
        else:
            f.write("else if (state =="+str(e.source)+" && ")
        if 'ca' in e['word']:
            # print 'action p1 == 1',
            f.write('action p1 == 1')
        else:
            # print 'action p1 == 0',
            f.write('action p1 == 0')

        # print " && ",
        f.write(" && ")

        if 'cb' in e['word']:
            # print 'action p2 == 1',
            f.write('action p2 == 1')
        else:
            # print 'action p2 == 0',
            f.write('action p2 == 0')

        # print " && ",
        f.write(" && ")

        if 'c0' in e['word']:
            if 'c1' in e['word']:
                # print 'action p3 == 3',
                f.write('action p3 == 3')
            else:
                # print 'action p3 == 2',
                f.write('action p3 == 2')
        elif 'c1' in e['word']:
            # print 'action p3 == 1',
            f.write('action p3 == 1')
        else:
            # print 'action p3 == 0',
            f.write('action p3 == 0')

        # print ')'
        f.write(')\n')
        # print '{'
        f.write('{\n')
        # print 'state =',e.target,';'
        f.write('state = '+str(e.target)+';\n')
        if GPar.vs[e.target]['colour']['alice']%2==0:
            # print 'pow1 = 1',';'
            f.write('pow1 = 1;\n')
        else:
            f.write('pow1 = 0;\n')
        if GPar.vs[e.target]['colour']['bob']%2==0:
            # print 'pow2 = 1',';'
            f.write('pow2 = 1;\n')
        else:
            f.write('pow2 = 0;\n')
        if GPar.vs[e.target]['colour']['charlie']%2==0:
            # print 'pow3 = 1',';'
            f.write('pow3 = 1;\n')
        else:
            f.write('pow3 = 0;\n')
        # print '}\n'
        f.write('}\n')

    for v in GPar.vs:
        print v
        # for ac in e['word']:
        #     print ac
        #     if ac=='ca':
        #         print 'action p1 == 1'
        #     if ac=='cb':
        #         print 'action p2 == 1'

    f.close()


        
def drawGPar(GPar):
    # for v in GPar.vs:
    #     print v
    layout = GPar.layout('kk')
#    GPar.es['label']=[word for word in GPar.es["word"]]
#    GPar.vs['label']=[('q'+str(v.index),v['colour']) for v in GPar.vs]
#    mc = max_colour(GPar)+1
#    r = 12*(float(GPar.vcount())/mc)
    for v in GPar.vs:
#        v['color']=(int(v.index)*r,int(v.index)*r,int(v.index)*r)
        v['color']=hsv_to_rgb(float(v.index)/GPar.vcount(),1,1)
        sigma = 0
        for key,val in v['colour'].items():
            sigma = sigma + val
#        v['size']=r/(1+sigma)
#        print sigma
#        v['vertex_frame_color']='red'
    for e in GPar.es:
#        v['color']=(int(v.index)*r,int(v.index)*r,int(v.index)*r)
        e['color']=GPar.vs[e.source]['color']
    # GPar.vs['label']=[v['name'] for v in GPar.vs]
    GPar.vs['label'] = [v.index for v in GPar.vs]
#    GPar.vs[0]['label']='S0'
    visual_style = {}
    visual_style['layout']=layout
    visual_style['bbox']=(1000,1000)
    visual_style['margin']=40
#    visual_style['vertex_label_dist']=2
    visual_style['autocurve']=True
    visual_style['vertex_frame_width']=0
    visual_style['vertex_shape']='circle'
    visual_style['vertex_size']=300/(GPar.vcount()+1)
#    visual_style['edge_width']=2
#    colour_dict = {0:"green"}
    out = plot(GPar, **visual_style)
    out.save('../../../outputs/synth_sigma.png')

def update_labs(GPar):
    GPar.es['word']=[label for label in GPar.es["label"]]
    GPar.es['label']=[None for word in GPar.es["word"]]
    # GPar.es['label'] = [e.index for e in GPar.es]
    GPar.vs['name']=[v.index for v in GPar.vs]
    
def max_colour(GPar):
    mc=0
    for v in GPar.vs:
        sigma=0
        for key,val in v['colour'].items():
            sigma = sigma + val
        if sigma>mc:
            mc=sigma
    return mc
    
def get_max_prior(TTPG):
    mp=0
    for v in TTPG.vs:
        if mp<v['prior']:
            mp=v['prior']
    return mp
        
'''get next M-state for RMGs'''
def get_next_mstate(cur_stup,d,M):
#    print 'cur_stup',cur_stup['label']
    idx_next = gltl_tau(get_mstate(cur_stup['label']),d,M)
#    print 'idx_next',idx_next
    if idx_next==None:
        return None
    else:
        '''plus 1 to accommodate (pre)init state'''
        return 'M-'+str(idx_next+1)
        
'''get next M-state for CGS'''
def get_next_mstate_cgs(cur_stup,d,M):
#    print 'cur_stup',cur_stup['val'],d
    idx_next,nextLabel = gltl_tau_cgs(get_mstate(cur_stup['label']),d,M)
#    print 'idx_next',idx_next
    if idx_next==None:
        return None
    else:
        return 'M-'+str(idx_next),nextLabel
    
def get_next_qtup(state,d,DPWs,modules,stup_next):
    for m in modules:
        w = set(d).intersection(set(list(m[6])))
        qNext = delta_dpw(DPWs[list(m[1])[0]],get_qidx(state['label'],list(m[1])[0]),w)
#        print 'qNext', qNext, get_qidx(state['label'],list(m[1])[0])
        stup_next.append(list(m[1])[0]+"-"+str(qNext))
    return set(stup_next)
    
def get_colour(state,d,DPWs,modules,stup_next): #returns next q states and colours
    colour_tuple={}
    # print '\nstate',state
    # print '\nd',d
    # print '\nstup_next',stup_next
    for m in modules:
        w = set(d).intersection(set(list(m[6])))
        # print w,list(m[1])[0]
        qNext = delta_dpw(DPWs[list(m[1])[0]],get_qidx(state['label'],list(m[1])[0]),w)
        # print qNext
        # for e in DPWs[list(m[1])[0]].es():
        #     print e
        # print DPWs[list(m[1])[0]].get_edgelist()
        colour_tuple[list(m[1])[0]]=DPWs[list(m[1])[0]].vs[qNext]['colour']
#    print colour_tuple
#    print '==========================='
#    raw_input()
    return colour_tuple
                
def delta_dpw(dpw,qidx,d):
    #d is already set
#    print 'd',d
    if not d:
        w = ['']
    else:
        w=d
    for edge in dpw.es.select(word=set(list(w))):
#            print edge
        if edge.source==qidx:
#            print dpw.vs[edge.target]
            return edge.target
    
def get_qidx(stup,player_name):
    for q in stup:
        # print 'q',q
        if player_name == q.split('-')[0]:
#            print q.split('-')[1]
            return int(q.split('-')[1])
                
def get_mstate(stup):
    for s in stup:
#        print 'get_mstate',s
        if "M-" in s:
            return s.split("-")[1] #returns index
    
def gltl_tau(sidx,d,M):
#    print 'sidx',sidx
#    if sidx==None:
#        return None
    '''minus 1 to accommodate (pre)init state'''
    for s in M.successors(int(sidx)-1):
#        print '>>>>',M.vs[s]['label']
        if set(M.vs[s]['label'][1])==set(d):
#            print M.vs[s]['label'][1]
            return s

def gltl_tau_cgs(sidx,d,M):
#    print 'YYY',sidx,M.vs[int(sidx)]['label']
    val = M.vs[int(sidx)]['label'][1]
#    print '<><>',sidx,val,d
    
    '''transition by environment'''
    nextState=[]
    try:
        t = envTransition(list(d)+list(val),environment[0])
    except TypeError:
        t = envTransition(list(val),environment[0])
#    print 'TT',t
    if len(t)==1:
        for k,v in without_keys(dict(t[0][0][1]),'guard').items():
            if k != 0:  # exclude checking name
                nextState.append(str({k:parse_rpn(list(val),v)}))
    nextLabel = getValuation(nextState)
#    print 'NNN', nextState, nextLabel
    
    '''get vertex id for nextstate'''
#    print 'SIDX', sidx
    for s in M.successors(int(sidx)):
#        print s,M.vs[s]['label'][1]
        if set(M.vs[s]['label'][1])==set(nextLabel):
#            print s
#            print 'SSS',s
            return s,nextLabel
#    return None
            
def cgs_tau(sidx,d,M):
    for s in M.successors(int(sidx)):
#        print M.vs[s]
        if set(M.vs[s]['label'][1])==set(d):
#            print M.vs[s]['label'][1]
            return M.vs[s]['label'][1]
    
    '''brute force method for generating direction -- seems to be such a waste of computational time!!'''
#def DGenerate(modules):
#    D = []
#    setD = set()
#    for m in modules:
#        D = D + list(m[2])
#        
#    for n in xrange(len(D)+1):
#        for subset in itertools.combinations(D,n):
#            setD.add(subset)
#
#    return setD

#def stateprod(dpw_states,M):
#    list_St = {}
#    list_St['M']=graph2states(M)
#    
#    for key in dpw_states:
#        list_St[key]=dpw_states[key]  
#    st_prod = []
#    for elements in itertools.product(*list_St.values()):
#         st_prod.append(elements)
#         
#    return st_prod
    
def graph2states(g):
    s = []
    for v in g.vs:
        s.append('M-'+str(v.index))
    return s
