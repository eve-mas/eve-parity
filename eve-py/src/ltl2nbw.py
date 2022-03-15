# -*- coding: utf-8 -*-

import subprocess as sp
from igraph import *
from utils import alpha2wordset,evalNBWedge

def ltl2nbw(ltl_fml,alphabets):

        lines = sp.Popen(['../ltl2ba/ltl2ba', '-f', '"%s"' % ltl_fml], stdout=sp.PIPE, stderr=sp.PIPE, encoding='utf8')

        out, err = lines.communicate()
        wordset = alpha2wordset(alphabets)
        
        out = out.splitlines()
        NBW = Graph(directed=True)
        for line in out:
            line = line.split(" ")
            if line[0] =="state":
                if line[2]=="acc":
                    acc = True
                else:
                    acc = False
                try:
                    NBW.vs.find(label=line[1])
                except (KeyError,ValueError):
                    NBW.add_vertex(label=line[1],accepting=acc)
                    
        for line in out:
            line = line.split(" ")
            if line[0] =="state":
                current_state = line[1]
            if line[0]=="<tr>":
                next_state = line[3]
#                symbols = set(str(line[1]).strip('[]').split(','))
#                print 'SYM',symbols,current_state,next_state
#                print '###',str(line[1]).strip('[]').split(','),wordset
                AP = str(line[1]).strip('[]').split(',')
                '''eval for each word'''
                for w in wordset:
                    if AP[0]=="True":
                        NBW.add_edge(NBW.vs.find(label=current_state).index,NBW.vs.find(label=next_state).index,word=set(AP))
                    else:
                        if evalNBWedge(AP,w):
                            if len(w)==0:
                                w=set([''])
                            NBW.add_edge(NBW.vs.find(label=current_state).index,NBW.vs.find(label=next_state).index,word=set(w))
#                NBW.add_edge(NBW.vs.find(label=current_state).index,NBW.vs.find(label=next_state).index,word=set(AP))
        
        # print NBW.get_edgelist()
        # for v in NBW.vs():
        #     print v['accepting']
        # for e in NBW.es():
        #     print e
        # drawnbw(NBW)
        return NBW
        
def drawnbw(NBW):
    layout = NBW.layout("kamada_kawai")
    color_dict = {True:"green", False:"red"}
    # NBW.es['label'] = [word for word in NBW.es["word"]]
    for v in NBW.vs():
        v['color'] = color_dict[v['accepting']]
    for e in NBW.es():
        e['label'] = e['word']
    visual_style = {}
    visual_style['layout'] = layout
    visual_style['bbox'] = (600, 600)
    visual_style['margin'] = 80
    visual_style['vertex_label_dist'] = 2
    visual_style['autocurve'] = True
    # visual_style['vertex_label_dist']=2
    plot(NBW,**visual_style)