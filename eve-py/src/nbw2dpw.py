# -*- coding: utf-8 -*-

from igraph import *
import copy
from utils import check_draw_flag,alpha2wordset

'''
This function converts Safra(-Piterman) Tree to its (unique) key
to be added to DPW in Safra-Piterman
'''
def sTree2key(T,e,f):
    sTreekey = []
    for node in T.vs:
        sTreekey.append(node.index)
        sTreekey.append(node['label'])
    sTreekey.append((e,f))
    return str(sTreekey)
    

'''
This function implements Safra-Piterman tree construction
'''
def buildsafratree(T,word,NBW,e,f):
    sTree = T.copy()
    green_nodes = []
    removed_nodes = []
    max_n = 0

    '''(1)'''
    '''for each node replace S with \delta(S,word)'''
    for node in sTree.vs:
        nodeLab = []
        for s in node['label']:
            for edge in NBW.es.select(word=set(['True'])):
                if edge.source==s:
                    nodeLab.append(edge.target)
            for edge in NBW.es.select(word=word):
                if edge.source==s:
                    nodeLab.append(edge.target)
        node['label']=list(set(nodeLab))
        
    if sTree.vcount()+1>max_n:
        max_n = sTree.vcount()+1
                
    '''(2)'''
    fstates = set() #fstates is the set of accepting states
    for v in NBW.vs.select(accepting=True):
        fstates.add(v.index)
    sTree_temp = sTree.copy()
    for v in sTree_temp.vs:
        s_intersect_f = set(v['label']).intersection(fstates)
        if s_intersect_f:
            sTree.add_vertex(label=list(s_intersect_f))
            sTree.add_edge(v,sTree.vs[sTree.vcount()-1])
    
    if sTree.vcount()+1>max_n:
        max_n = sTree.vcount()+1
    
    '''(3)'''
    for v in sTree.vs:
        parent = sTree.predecessors(v.index)
        if parent:
            '''M(v')<M(v)'''
            for sibling in list(filter(lambda a: a!=v.index, sTree.successors(parent[0]))):
                if v.index>sibling and set(v['label']).intersection(set(sTree.vs[sibling]['label'])):
                    cur_lab = copy.copy(v['label'])
                    for x in list(set(v['label']).intersection(set(sTree.vs[sibling]['label']))):
                        cur_lab.remove(x)
                    v['label']=cur_lab
                    '''remove all descendants'''
                    v2del=[]
                    for desc in reversed(list(filter(lambda a: a!=0, sTree.bfs(v.index)[0][1:]))):
                        removed_nodes.append(desc+1)
                        v2del.append(desc)
                    '''
                    gather vertices first, then delete
                    '''
                    sTree.delete_vertices(v2del)
                    
    if sTree.vcount()+1>max_n:
        max_n = sTree.vcount()+1
    
    '''(4)'''
    for v in sTree.vs:
        suclab_union=[]
        for suc in v.successors():
            suclab_union = suclab_union + suc['label']
        if set(v['label']) == set(suclab_union):
            green_nodes.append(v.index+1)
            '''remove all descendants'''
            v2del=[]
            for desc in reversed(list(filter(lambda a: a!=0, sTree.bfs(v.index)[0][1:]))):
                removed_nodes.append(desc+1)
                v2del.append(desc) #gather vertices to be deleted first
            '''
            v2del is the list of vertices to be deleted
            since deleting a vertex will decrease all index by 1
            '''
            sTree.delete_vertices(v2del)
                
    '''(5)'''
    v2del=[]
    for v in sTree.vs:
        if len(v['label'])==0 and v.index!=0:
            removed_nodes.append(v.index+1)
            v2del.append(v)
    sTree.delete_vertices(v2del)
    
    if len(green_nodes)!=0:
        gn = min(green_nodes)
        f = min(gn,max_n)
    else:
        f = max_n
            
    if len(removed_nodes)!=0:
        rn = min(removed_nodes)
        e = min(rn,max_n)
    else:
        e = max_n
 
    '''sink state'''
    if len(sTree.vs[0]['label'])==0:
        e = 1
    
    return sTree,e,f
    
'''
Implements conversion of e,f to parity acceptance conditions
'''
def vertex2colour(e,f):
    if f==1 and e>1:
        return 0
    elif e>1 and f>=e:
        return 2*(e-2)+1
    elif f>1 and e>f:
        return 2*(f-2)+2
    else:
        return 1

'''
This function builds DPW from NBW
Implements Safra-Piterman Construction
Paper: From Nondeterministic Buchi and Streett Automata to Deterministic Parity Automata (Piterman, 2007)
Section 3.2. From NBW to DPW
'''
def nbw2dpw(NBW,alphabets):
    DPW = Graph(directed=True)

    '''the set of '''
    N = set()

    '''build set of words/powerset construction of alphabets'''
    WordSet = alpha2wordset(alphabets)
    
    safra_tree = Graph(directed=True)
    '''init root/d_0'''
    safra_tree.add_vertex(label=[NBW.vs.find(label='init').index],M=1)
#    M_set.add(1) #add name of root to the set of names
    init_e=2
    init_f=1
    N.add(sTree2key(safra_tree,e=init_e,f=init_f))
    '''add root/d_0 to DPW'''
    DPW.add_vertex(safra_tree,e=init_e,f=init_f,keycode=sTree2key(safra_tree,init_e,init_f),colour=vertex2colour(init_e,init_f))

    '''for every (compact) Safra tree'''
    for T in DPW.vs:

        '''for every word in the set of words (\sigma \in \Sigma)'''
        for w in WordSet:            
            e=T['e']
            f=T['f']
            if len(w)==0:
                w=[''] #all alphabets are false

            (sTree,e,f) = buildsafratree(T['name'],set(list(w)),NBW,e,f)
            curTreekey = sTree2key(sTree,e,f)

            if sTree.vcount()!=0:
                '''check whether the current tree is already in the DPW '''
                '''if not then add'''
                if not curTreekey in N:
                    N.add(curTreekey)
                    DPW.add_vertex(sTree,e=e,f=f,keycode=curTreekey,colour=vertex2colour(e,f))
                    DPW.add_edge(T,DPW.vs[DPW.vcount()-1],word=set(list(w)))
                    
                    '''if already in DPW, then find the tree and add edge from current tree to it'''
                else:
                    DPW.add_edge(T,DPW.vs.find(keycode=curTreekey),word=set(list(w)))

    if check_draw_flag():
        drawdpw(DPW)
    return DPW

def drawdpw(DPW):
    layout = DPW.layout('kamada_kawai')
    DPW.es['label']=[word for word in DPW.es["word"]]
    DPW.vs['label']=[('q'+str(v.index),v['colour']) for v in DPW.vs]
    visual_style = {}
    visual_style['layout']=layout
    visual_style['bbox']=(600,600)
    visual_style['margin']=80
    visual_style['vertex_label_dist']=2
    visual_style['autocurve']=True
#    colour_dict = {0:"green"}
    plot(DPW, **visual_style)