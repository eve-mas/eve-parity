# -*- coding: utf-8 -*-

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

    '''d_-i'''
    for idx,m in enumerate(modules):
        pl_name=list(m[1])[0]
        TTPG[pl_name] = copy.copy(GPar)

        '''delete all edges'''
        TTPG[pl_name].delete_edges(TTPG.es)
        modules_exi = copy.copy(modules)
        
        '''delete punished player'''
        del modules_exi[idx]

        oriv_count = TTPG[pl_name].vcount()
        for v in TTPG[pl_name].vs:
            v['prior']=v['colour'][pl_name]+1
            v['itd']=False

        '''check possible d_exi'''
        for i in xrange(oriv_count):
            for d in generate_coal_dir(TTPG[pl_name].vs[i]['val'],modules_exi):
                '''add intermediate states to TTPG'''
                TTPG[pl_name].add_vertex(label=set([i,d]),prior=(TTPG[pl_name].vs[i]['colour'][pl_name]+1),itd=True)
                intermed_state = TTPG[pl_name].vs.find(label=set([i,d]))
                
                '''add edge from prev state to intermediate state'''
                TTPG[pl_name].add_edge(TTPG[pl_name].vs[i],intermed_state)
                for d_i in generate_coal_dir(TTPG[pl_name].vs[i]['val'],[m]):
                    d_a_i = list(d)+list(d_i)
                    for e in GPar.es.select(word=set(d_a_i)):
                            if e.source==i:
                                ''''add edge from intermediate state to next state'''
                                TTPG[pl_name].add_edge(intermed_state,TTPG[pl_name].vs[e.target])

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

    '''d_-i'''
    for idx,m in enumerate(modules):
        pl_name=list(m[1])[0]
        TTPG[pl_name] = copy.copy(GPar)
        '''delete all edges'''
        TTPG[pl_name].delete_edges(TTPG.es)
        modules_exi = copy.copy(modules)

        '''delete punished player'''
        del modules_exi[idx]

        oriv_count = TTPG[pl_name].vcount()
        for v in TTPG[pl_name].vs:
            v['prior']=v['colour'][pl_name]+1
            v['itd']=False

        '''check possible d_exi'''
        for i in xrange(oriv_count):
            """(pre)init state"""
            if i==0:
                for state in productInit(modules_exi):
                    stateLabel = getValuation(state)
                    if stateLabel==None:
                        stateLabel=frozenset()
                    else:
                        stateLabel=frozenset(stateLabel)
                    d = tuple(stateLabel)

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
                                    ''''add edge from intermediate state to next state'''
                                    TTPG[pl_name].add_edge(intermed_state,TTPG[pl_name].vs[e.target])
            else:
                for d in generate_coal_dir(TTPG[pl_name].vs[i]['val'],modules_exi):
                    '''add intermediate states to TTPG'''
                    TTPG[pl_name].add_vertex(label=set([i,d]),prior=(TTPG[pl_name].vs[i]['colour'][pl_name]+1),itd=True)
                    intermed_state = TTPG[pl_name].vs.find(label=set([i,d]))
                    
                    '''add edge from prev state to intermediate state'''
                    TTPG[pl_name].add_edge(TTPG[pl_name].vs[i],intermed_state)
                    for d_i in generate_coal_dir(TTPG[pl_name].vs[i]['val'],[m]):

                        d_a_i = list(d)+list(d_i)

                        for e in GPar.es.select(word=set(d_a_i)):
                                if e.source==i:

                                    ''''add edge from intermediate state to next state'''
                                    TTPG[pl_name].add_edge(intermed_state,TTPG[pl_name].vs[e.target])

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
    pl_name=list((modules[idx])[1])[0]
    TTPG[pl_name] = copy.copy(GPar)

    '''delete all edges'''
    TTPG[pl_name].delete_edges(TTPG.es)
    modules_exi = copy.copy(modules)
    
    '''delete punished player'''
    del modules_exi[idx]

    oriv_count = TTPG[pl_name].vcount()
    for v in TTPG[pl_name].vs:
        v['prior']=v['colour'][pl_name]+1
        v['itd']=False

    '''check possible d_exi'''
    for i in xrange(oriv_count):
        for d in generate_coal_dir(TTPG[pl_name].vs[i]['val'],modules_exi):

            '''add intermediate states to TTPG'''
            TTPG[pl_name].add_vertex(label=set([i,d]),prior=(TTPG[pl_name].vs[i]['colour'][pl_name]+1),itd=True)
            intermed_state = TTPG[pl_name].vs.find(label=set([i,d]))
            
            '''add edge from prev state to intermediate state'''
            TTPG[pl_name].add_edge(TTPG[pl_name].vs[i],intermed_state)
            for d_i in generate_coal_dir(TTPG[pl_name].vs[i]['val'],[m]):

                d_a_i = list(d)+list(d_i)

                for e in GPar.es.select(word=set(d_a_i)):
                        if e.source==i:

                            ''''add edge from intermediate state to next state'''
                            TTPG[pl_name].add_edge(intermed_state,TTPG[pl_name].vs[e.target])

    print summary(TTPG[pl_name])
    return True
    
def sequencer_rmg_single(idx,GPar,TTPG,modules):
    m = modules[idx]
    pl_name=list((modules[idx])[1])[0]
    TTPG[pl_name] = copy.copy(GPar)

    '''delete all edges'''
    TTPG[pl_name].delete_edges(TTPG.es)

    modules_exi = copy.copy(modules)

    '''delete punished player'''
    del modules_exi[idx]

    oriv_count = TTPG[pl_name].vcount()
    for v in TTPG[pl_name].vs:
        v['prior']=v['colour'][pl_name]+1
        v['itd']=False

    '''check possible d_exi'''
    for i in xrange(oriv_count):

        """(pre)init state"""
        if i==0:
            for state in productInit(modules_exi):
                stateLabel = getValuation(state)
                if stateLabel==None:
                    stateLabel=frozenset()
                else:
                    stateLabel=frozenset(stateLabel)
                d = tuple(stateLabel)

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

                                ''''add edge from intermediate state to next state'''
                                TTPG[pl_name].add_edge(intermed_state,TTPG[pl_name].vs[e.target])
        else:
            for d in generate_coal_dir(TTPG[pl_name].vs[i]['val'],modules_exi):

                '''add intermediate states to TTPG'''
                TTPG[pl_name].add_vertex(label=set([i,d]),prior=(TTPG[pl_name].vs[i]['colour'][pl_name]+1),itd=True)
                intermed_state = TTPG[pl_name].vs.find(label=set([i,d]))
                
                '''add edge from prev state to intermediate state'''
                TTPG[pl_name].add_edge(TTPG[pl_name].vs[i],intermed_state)
                for d_i in generate_coal_dir(TTPG[pl_name].vs[i]['val'],[m]):

                    d_a_i = list(d)+list(d_i)

                    for e in GPar.es.select(word=set(d_a_i)):
                            if e.source==i:

                                ''''add edge from intermediate state to next state'''
                                TTPG[pl_name].add_edge(intermed_state,TTPG[pl_name].vs[e.target])

    print summary(TTPG[pl_name])
    return TTPG[pl_name].vcount(), TTPG[pl_name].ecount()
    
'''this function generates direction based on players/modules coalition'''
def generate_coal_dir(prev_val,coalition):
    direction=[]
    for updateCommand in jointEnabled(guardEval(set(list(prev_val)),coalition)):
            commands=[]

            for k,v in updateCommand:
                '''for each jointEnabled update command'''
                updateCommand_noguard = without_keys(v,'guard') #remove dict key 'guard'

                for k,l in updateCommand_noguard.items():
                    '''for each variable'''
                    commands.append(str({k:parse_rpn(frozenset(list(prev_val)),l)}))
            try:
                nextState = frozenset(getValuation(tuple(commands)))

            except TypeError:
                nextState = frozenset()

            direction.append(nextState)
    return direction
    
def drawTTPG_kk(TTPG):
    layout = TTPG.layout('kk')
#    mc = get_max_prior(TTPG)+1
#    r = 3*(float(TTPG.vcount())/mc)
    for v in TTPG.vs:
        v['color']=hsv_to_rgb(float(v.index)/TTPG.vcount(),1,1)
        v['size']=20
        if v['itd']:
            v['shape']='circle'
        else:
            v['shape']='square'
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

    for idx,state in enumerate(productInit(modules)):
        s0 = ['M-'+str(idx+1)]

        stateLabel = getValuation(state)
        if stateLabel==None:
            stateLabel=()
        for m in modules:
            states = []
            alphabets=set(list(m[6])) #set of symbols in DPW
            for v in DPWs[list(m[1])[0]].vs:
                states.append(list(m[1])[0]+'-'+str(v.index))

            dpw_states[list(m[1])[0]]=states

            w = set(list(set(M.vs[idx]['label'][1]).intersection(alphabets)))

            if len(w)==0:
                w = ['']
            for edge in DPWs[list(m[1])[0]].es.select(word=set(w)):

                if edge.source==0:
                    s0.append(list(m[1])[0]+'-'+str(edge.target))
                    colour_tuple[list(m[1])[0]]=DPWs[list(m[1])[0]].vs[edge.target]['colour']

        '''init state (s0) in GPar'''

        '''convert stateLabel to tuple to match val format'''
        GPar.add_vertex(label=set(s0),colour=copy.copy(colour_tuple),val=tuple(stateLabel))
        S.add(frozenset(s0))

    prevS = set()
    while prevS != S:
        prevS = copy.copy(S)
        for state in GPar.vs:

            '''direction via updatecommand (faster than brute force method)'''
            if state.index!=0:
                for d in generate_coal_dir(state['val'],modules):
                    d = tuple(d)
                    stup_next=[]
                    next_mstate = get_next_mstate(state,d,M)
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
        if cur.index==0:
            for idx,state in enumerate(productInit(modules)):
                stateLabel = getValuation(state)
                if stateLabel==None:
                    stateLabel=frozenset()
                else:
                    stateLabel=frozenset(stateLabel)
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
    if check_draw_flag():
        drawGPar(GPar)
    return GPar

    '''this function converts G_LTL to G_Par'''
def convertG_cgs(modules,DPWs,M):
    GPar = Graph(directed=True)
    dpw_states = {}
    s0 = ['M-0'] 
    colour_tuple = {}
    S = set()
    
    for m in modules:
        states = []
        alphabets=set(list(m[6])) #set of symbols in DPW
        for v in DPWs[list(m[1])[0]].vs:
            states.append(list(m[1])[0]+'-'+str(v.index))

        dpw_states[list(m[1])[0]]=states

        w = set(list(set(M.vs[0]['label'][1]).intersection(alphabets)))

        if len(w)==0:
            w = ['']
        for edge in DPWs[list(m[1])[0]].es.select(word=set(w)):

            if edge.source==0:
                s0.append(list(m[1])[0]+'-'+str(edge.target))
                colour_tuple[list(m[1])[0]]=DPWs[list(m[1])[0]].vs[edge.target]['colour']

    '''add init state (s0) in GPar'''
    GPar.add_vertex(label=set(s0),colour=copy.copy(colour_tuple),val=frozenset(M.vs[0]['label'][1]))
    S.add(frozenset(s0))
    
    '''generate GPar states'''
    prevS = set()
    while prevS != S:
        prevS = copy.copy(S)
        for state in GPar.vs:
            '''
            this generate direction based on sequence of states/run-based strategies
            ''' 
            for d in generate_coal_dir(state['val'],modules):
                d = tuple(d)

                next_mstate,nextLabel = get_next_mstate_cgs(state,d,M)
                if d!=None:
                    if 'matching_pennies_player_1_var' in d:
                        nextLabel.append('matching_pennies_player_1_var')
                    if 'matching_pennies_player_2_var' in d:
                        nextLabel.append('matching_pennies_player_2_var') 

                stup_next = []

                if next_mstate!=None:
                    stup_next.append(next_mstate)
                    stup_next = get_next_qtup(state,tuple(nextLabel),DPWs,modules,stup_next)
                    colour_tuple = get_colour(state,tuple(nextLabel),DPWs,modules,stup_next)

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
    if check_draw_flag():
        drawGPar(GPar)
    return GPar
        
def drawGPar(GPar):
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
    GPar.vs['label']=[v['name'] for v in GPar.vs]
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
    plot(GPar, **visual_style)
    
def update_labs(GPar):
    GPar.es['word']=[label for label in GPar.es["label"]]
    GPar.es['label']=[None for word in GPar.es["word"]]
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
    idx_next = gltl_tau(get_mstate(cur_stup['label']),d,M)

    if idx_next==None:
        return None
    else:
        '''plus 1 to accommodate (pre)init state'''
        return 'M-'+str(idx_next+1)
        
'''get next M-state for CGS'''
def get_next_mstate_cgs(cur_stup,d,M):
    idx_next,nextLabel = gltl_tau_cgs(get_mstate(cur_stup['label']),d,M)

    if idx_next==None:
        return None
    else:
        return 'M-'+str(idx_next),nextLabel
    
def get_next_qtup(state,d,DPWs,modules,stup_next):
    for m in modules:
        w = set(d).intersection(set(list(m[6])))
        qNext = delta_dpw(DPWs[list(m[1])[0]],get_qidx(state['label'],list(m[1])[0]),w)
        stup_next.append(list(m[1])[0]+"-"+str(qNext))
    return set(stup_next)
    
def get_colour(state,d,DPWs,modules,stup_next): #returns next q states and colours
    colour_tuple={}

    for m in modules:
        w = set(d).intersection(set(list(m[6])))
        qNext = delta_dpw(DPWs[list(m[1])[0]],get_qidx(state['label'],list(m[1])[0]),w)
        colour_tuple[list(m[1])[0]]=DPWs[list(m[1])[0]].vs[qNext]['colour']

    return colour_tuple
                
def delta_dpw(dpw,qidx,d):
    if not d:
        w = ['']
    else:
        w=d
    for edge in dpw.es.select(word=set(list(w))):
        if edge.source==qidx:
            return edge.target
    
def get_qidx(stup,player_name):
    for q in stup:
        if player_name in q:
            return int(q.split('-')[1])
                
def get_mstate(stup):
    for s in stup:
        if "M-" in s:
            return s.split("-")[1] #returns index
    
def gltl_tau(sidx,d,M):
    for s in M.successors(int(sidx)-1):
        if set(M.vs[s]['label'][1])==set(d):
            return s

def gltl_tau_cgs(sidx,d,M):
    val = M.vs[int(sidx)]['label'][1]
    
    '''transition by environment'''
    nextState=[]
    try:
        t = envTransition(list(d)+list(val),environment[0])
    except TypeError:
        t = envTransition(list(val),environment[0])
    if len(t)==1:
        for k,v in without_keys(dict(t[0][0][1]),'guard').items():
            nextState.append(str({k:parse_rpn(list(val),v)}))
    nextLabel = getValuation(nextState)

    '''get vertex id for nextstate'''
    for s in M.successors(int(sidx)):
        if set(M.vs[s]['label'][1])==set(nextLabel):
            return s,nextLabel

            
def cgs_tau(sidx,d,M):
    for s in M.successors(int(sidx)):
        if set(M.vs[s]['label'][1])==set(d):
            return M.vs[s]['label'][1]

def graph2states(g):
    s = []
    for v in g.vs:
        s.append('M-'+str(v.index))
    return s