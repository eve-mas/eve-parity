# -*- coding: utf-8 -*-

import itertools
import copy

def jointGoal(modules):
#    jointGoal=[]
    for m in modules:
#        jointGoal = jointGoal.append(list)
        print "player "+str(m[1])+" goal is "+str(m[5])
        for l in list(m[5])[0].split(" "):
            print l

def evalNBWedge(AP,word):
    for a in AP:
        if a[0]=='~':
            if a.strip('~') in word:
                return False
        else:
            if a not in word:
                return False
    return True

'''constructs the powerset of a set of alphabets'''
def alpha2wordset(alphabets):
    wordset = set()
    for n in xrange(len(alphabets)+1):
        for subset in itertools.combinations(alphabets,n):
            wordset.add(subset)
    return wordset

'''this function adds two MP players for E/A-Nash'''
'''for CGSs'''
def addMPPlayers_cgs(file_name,pf):
    with open("../temp/add_mp","w") as f:
            f.write(" module matching_pennies_player_1 controls matching_pennies_player_1_var\n")
            f.write("   init\n   :: true ~> matching_pennies_player_1_var' := true;\n   :: true ~> matching_pennies_player_1_var' := false;\n   update\n   :: true ~> matching_pennies_player_1_var' := true;\n   :: true ~> matching_pennies_player_1_var' := false;\n   goal\n")
            f.write("   :: ("+pf+") or X (matching_pennies_player_1_var <-> matching_pennies_player_2_var);\n\n")
            
            f.write(" module matching_pennies_player_2 controls matching_pennies_player_2_var\n")
            f.write("   init\n   :: true ~> matching_pennies_player_2_var' := true;\n   :: true ~> matching_pennies_player_2_var' := false;\n   update\n   :: true ~> matching_pennies_player_2_var' := true;\n   :: true ~> matching_pennies_player_2_var' := false;\n   goal\n")
            f.write("   :: ("+pf+") or X !(matching_pennies_player_1_var <-> matching_pennies_player_2_var);\n\n")
            with open(file_name) as f_ori:
                f.write(f_ori.read())
                
                
'''for RMGs'''                
def addMPPlayers_rmg(file_name,pf):
    with open("../temp/add_mp","w") as f:
            f.write(" module matching_pennies_player_1 controls matching_pennies_player_1_var\n")
            f.write("   init\n   :: true ~> matching_pennies_player_1_var' := true;\n   :: true ~> matching_pennies_player_1_var' := false;\n   update\n   :: true ~> matching_pennies_player_1_var' := true;\n   :: true ~> matching_pennies_player_1_var' := false;\n   goal\n")
            f.write("   :: ("+pf+") or (matching_pennies_player_1_var <-> matching_pennies_player_2_var);\n\n")
            
            f.write(" module matching_pennies_player_2 controls matching_pennies_player_2_var\n")
            f.write("   init\n   :: true ~> matching_pennies_player_2_var' := true;\n   :: true ~> matching_pennies_player_2_var' := false;\n   update\n   :: true ~> matching_pennies_player_2_var' := true;\n   :: true ~> matching_pennies_player_2_var' := false;\n   goal\n")
            f.write("   :: ("+pf+") or !(matching_pennies_player_1_var <-> matching_pennies_player_2_var);\n\n")
            with open(file_name) as f_ori:
                f.write(f_ori.read())

def printGParDetails(GPar):
    for v in GPar.vs():
        print v
    print GPar.get_edgelist()
    for e in GPar.es():
        print e
    return True

def num2name(w,modules):
    coal=[]
    for i in w:
        coal.append(list((modules[i])[1])[0])
    return coal

def check_draw_flag():
    with open("draw_flag","r") as f:
        data = f.read()
        if data=="1":
            return True
        else:
            return False

def generate_set_W(modules):
    W = []
    for n in xrange(len(modules)+1):
        for subset in itertools.combinations(list(range(0,len(modules))),n):
            #W.add(subset)
            W.append(subset)
    return W
    
def generate_set_modules(modules):
    W = []
    for n in xrange(len(modules)+1):
        for subset in itertools.combinations((modules),n):
            print subset
            #W.add(subset)
            W.append(subset)
    return W
    
def get_l(w,modules):
    N = list(range(0,len(modules)))
    l = [item for item in N if item not in w]
    return l
    
def build_GPar_L(GPar,w,l,PUN_L):
    GPar_L=copy.copy(GPar)
    to_del=[]
    for v in GPar_L.vs:
            if v['name'] not in PUN_L:
                to_del.append(v.index)
#                GPar_L[frozenset(l)].delete_vertices(v.index)
    GPar_L.delete_vertices(to_del)
    return GPar_L

'''
This function builds product of streett automata
'''    
def build_streett_prod(GPar_L,w,modules):
    '''build streett automata from GPar_L'''
    s_Alpha=[]
    max_colour = get_max_colour(GPar_L,modules)

    for pl in w:
        Alpha=[]
        for i in xrange(max_colour):
            j=2*i
            a={}
            if i==0:
                a['C'+str(i)]=[]
            else:
                a['C'+str(i)]=copy.copy(list(Alpha[i-1]['C'+str(i-1)]))
            a['E'+str(i)]=[]
        
            pl_name = list(modules[pl][1])[0]
            for v in GPar_L.vs.select(lambda vertex: vertex['colour'][pl_name]==j):
                a['C'+str(i)].append(v['name'])
            for v in GPar_L.vs.select(lambda vertex: vertex['colour'][pl_name]==j+1):
                a['E'+str(i)].append(v['name'])
            a['C'+str(i)]=set(a['C'+str(i)])
            a['E'+str(i)]=set(a['E'+str(i)])
            Alpha.append(a)
        s_Alpha.append(Alpha)
    return s_Alpha
    
    
'''
This function check Street automaton emptiness
'''            
def Streett_emptyness(GPar_L,s_Alpha,modules):    
    S = copy.copy(GPar_L)

    max_colour = get_max_colour(GPar_L,modules)
    while True:
        '''to nontrivial SCC'''
        '''selfloop'''

        SCC=[]
        for v in S.vs():
            if v in v.successors():
                SCC.append([v['name']])

        '''clusters'''
        for c in S.components():
            if len(c)>1:
                SCC.append([S.vs[v]['name'] for v in c])

        changed=False
        for c in SCC:
            del_flag=False
#            for Alpha in s_Alpha:1
            for i in xrange(max_colour):
                e_to_del=[]
                v_to_del=[]
#                for i,a in enumerate(Alpha):
                for x,Alpha in enumerate(s_Alpha):
                    c_cap_E=Alpha[i]['E'+str(i)].intersection(set(c))
                    c_cap_C=Alpha[i]['C'+str(i)].intersection(set(c))
                    if c_cap_E and not c_cap_C:
                        
                        '''need to also check if the edge exists in DSW S'''
                        if len(c_cap_E)==1 and ((name2idx(S,list(c_cap_E)[0]),name2idx(S,list(c_cap_E)[0])) in S.get_edgelist()):
#                        if len(c_cap_E):
#                            S.delete_edges((name2idx(S,list(c_cap_E)[0]),name2idx(S,list(c_cap_E)[0])))
                            e_to_del.append((name2idx(S,list(c_cap_E)[0]),name2idx(S,list(c_cap_E)[0])))
#                            break
                        else:
#                            S.delete_vertices(namelist2idxlist(S,list(c_cap_E)))
#                            v_to_del.append(namelist2idxlist(S,list(c_cap_E))[0])
                            v_to_del = v_to_del + namelist2idxlist(S,list(c_cap_E))
                        del_flag=True
                        changed=True
#                        break
                if del_flag:
                    S.delete_edges(list(set(e_to_del)))
#                    try:
#                        S.delete_edges(list(set(e_to_del)))
#                    except ValueError:
#                        for v in S.vs():
#                            print v
                    S.delete_vertices(list(set(v_to_del)))
                    break
            if del_flag:
                break
            
            
        if not changed:
            break
        
    '''delete trivial SCC and non-SCC'''
    to_del=[]
    to_del_sigma=[]
    self_loop=[]
    '''trivial'''
    for v in S.vs:
        if len(v.successors())==0:
            to_del.append(v.index)
            to_del_sigma.append(v.index)
        else:
            '''self-loop'''
            if v in v.successors():
                self_loop.append(v.index)
            
    '''non-SCC'''
    for c in S.components():
        if len(c)==1 and c[0] not in self_loop:
            to_del.append(c[0])
            
    '''return strategy profile \vec{sigma}'''
    S_cpy = copy.copy(S)
    S_cpy.delete_vertices(to_del_sigma)
    
    '''emptiness check'''
    S.delete_vertices(to_del)
                
#    return S.simplify(multiple=True,loops=False)
    return S,S_cpy
    
def get_max_colour(GPar,modules):
    vcolour_max=0
    for v in GPar.vs:
        if max(v['colour'].values())>vcolour_max:
            vcolour_max = max(v['colour'].values())
    return vcolour_max

def idxlist2namelist(G,idxlist):
    namelist=[]
    for v in idxlist:
        namelist.append(G.vs[v]['name'])
    return namelist

def name2idx(G,name):
    for v in G.vs.select(name=name):
        return v.index
        
def namelist2idxlist(G,namelist):
    idxlist=[]
    for name in namelist:
        idxlist.append(name2idx(G,name))
    return idxlist