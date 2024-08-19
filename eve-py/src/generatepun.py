# -*- coding: utf-8 -*-
from gltl2gpar import get_max_prior
import subprocess as sp

'''this generates input file for PGSolver from TTPG igraph structure'''
def ttpg2gm(TTPG,pl):
    max_idt=TTPG[pl].vcount() #highest occuring identifier
    max_prior = get_max_prior(TTPG[pl])
#    print 'parity '+str(max_idt)+';'
    tofile = 'parity '+str(max_idt)+';'
    for v in TTPG[pl].vs:
#        to_file=str(v.index)+' '+
        if v['itd']==True:
            own=1
        else:
            own=0
            
#        if len(v.successors())==1:
#            suc_list = str(v.successors()[0].index)
#        else:
#            for suc in v.successors():
#                suc_list = suc_list+','+
            
        for num,suc in enumerate(v.successors()):
            if num==0:
                suc_list = str(suc.index)
            else:
                suc_list = suc_list+','+str(suc.index)
#        print str(v.index)+' '+str(v['prior'])+' '+str(own)+' '+suc_list+';'
        tofile = tofile+'\n'+str(v.index)+' '+str((2*max_prior)-v['prior'])+' '+str(own)+' '+suc_list+';'
    f = open('../temp/ttpg_'+pl,'w')
    f.write(tofile)
    f.close()
    
def compute_pun(pl_name,PUN,TTPG):
    '''From TTPG to PGSolver representation'''
    ttpg2gm(TTPG,pl_name)
    
    '''Call PGSolver subroutine to compute Pun_i'''
    lines = sp.Popen(['../pgsolver/bin/pgsolver', '-global', 'recursive', '../temp/ttpg_%s' % pl_name], stdout=sp.PIPE, stderr=sp.PIPE, encoding='utf8')
    out, err = lines.communicate()

    ttpg_results={}
    out = out.splitlines()
    for line in out:
        word = line.split(" ")
        if word[0]=="Player":
            pl = word[1]
        for c in list(word):
#            if line[0]=="Player" and line[1]=="0":
            try:
                if c[0]=="{":
                    ttpg_results[int(pl)]=line
            except IndexError:
                pass


    try:
        PUN[pl_name]=list(map(int,ttpg_results[0].strip()[1:-1].replace(' ','').split(',')))
    except ValueError:
        PUN[pl_name]=[]
    return PUN
