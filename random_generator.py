import pickle as pk
import networkx as nx
import pandas as pd
import numpy as np
import scipy.sparse as sp
from numpy import *
from numpy.random import *
import sys, os
from subprocess import call
import matplotlib.pyplot as plt
from sets import Set
import itertools

notebook_mode=False;

if notebook_mode==True:
    original_graph= #name of the edgelist file
    dir= #output directory path
    dataset_tag= #name tag
    num_iter= #number of iterations
else:
    if len(sys.argv)>=5:
        original_graph=sys.argv[1];
        dir=sys.argv[2];
        dataset_tag=sys.argv[3]
        num_iter=int(sys.argv[4]);
    else:
        print('Input is required as:\n 1) full edgelist filename 
        \n 2) name of output directory 
        \n 3) name tag for output files 
        \n 4) number of iterations');
        sys.exit();

if not os.path.exists(dir):
    os.makedirs(dir)


G=nx.read_weighted_edgelist(original_graph)

def weights(G):
    return [edge[2]['weight'] for edge in G.edges(data = True)]

m = min(weights(G))
M = max(weights(G))
def new_weights(w):
    return [(w[i]-m)/(M-m) for i in range(len(w))]
NW = new_weights(weights(G))
G_norm=nx.Graph()
G_norm.add_nodes_from(G.nodes())
G_norm.add_edges_from([(ed[0], ed[1], {'norm_weight': w}) 
for ed,w in zip(G.edges(), NW)])


def biased_random_generator(G_norm):
    newG=nx.Graph();
    newG.add_nodes_from(G_norm.nodes())
    for edge in G_norm.edges(data=True):
        r=rand();
        #print r, edge[2]['norm_weight']
        if r < edge[2]['norm_weight']:
            newG.add_edge(edge[0], edge[1])
    return newG

#n random graphs
for i in range(num_iter):
    G_rand = biased_random_generator(G_norm)
    randi = open(dir+dataset_tag+'_random%d.pck' %i,'w')
    pk.dump(G_rand,randi)
    randi.close();
    del randi;


#clique filtration and homology
sys.path.append('../')
import Holes as ho
import imp
betti_dict = {}
for i in range(num_iter):
    randi = open(dir+dataset_tag+'_random%d.pck' %i,'r')
    G_rand = pk.load(randi)
    nx.write_edgelist(G_rand, dir+dataset_tag+'_random%d.edges' %i)
    G_rand=nx.read_edgelist(dir+dataset_tag+'_random%d.edges' 
    %i,delimiter=' ',nodetype=float);
    #clique detection in partial graph
    cliques=nx.find_cliques_recursive(G_rand);
    Clique_dictionary = {}

    # adding cliques to the filtration
    for clique in cliques: #loop on new clique
        clique.sort();
        for k in range(1,len(clique)+1): #loop on clique dimension 
        # to find missed faces of simplex
            for subclique in itertools.combinations(clique,k):
                if str(list(subclique)) not in Clique_dictionary:
                    Clique_dictionary[str(list(subclique))]=[];
                    Clique_dictionary[str(list(subclique))].append(str(1));
                    Clique_dictionary[str(list(subclique))].append(str(1))

    # output of the filtration file in a hopefully matlab compliant form
    fname=dir+dataset_tag+'_random%d_clique_filtration.pck' %i
    filtration_file=open(fname,'w');
    pk.dump(Clique_dictionary,filtration_file);
    filtration_file.close();
    del filtration_file;
    imp.reload(ho);

    max_homology_dimension=k;

    try:
        ho.persistent_homology_calculation(fname,k,dataset_tag,dir)
    except OSError, e:
        print "Execution failed for file:"+str(fname);

    generators_dict=pk.load(open(dir+'gen/generators_'
    +dataset_tag+'_.pck', 'rb'))
    gname=dir+'gen/generators_'+dataset_tag+'_random%d.pck' %i
    gfile=open(gname,'w')
    pk.dump(generators_dict,gfile)
    betti_num=pk.load(open(dir+'gen/betti_'+dataset_tag+'_.pck', 'rb'))


    for j in betti_num.strip('{}').split(','):
        d = 0
        for k in j.split(':'):
            if d == 0:
                if int(k) not in betti_dict:

                    betti_dict[int(k)]=[]
                g = int(k)
                d =+ 1
            else:

                betti_dict[g].append(int(k))


    gfile.close();
    del generators_dict;
    del gfile;
    del betti_num;
    randi.close();
    del randi;
    print i

bname=dir+'gen/betti_dictionary_'+dataset_tag+'.pck'
bfile=open(bname,'w')
pk.dump(betti_dict,bfile)
print betti_dict

