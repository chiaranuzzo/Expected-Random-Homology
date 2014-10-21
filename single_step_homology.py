import networkx as nx
import os
import pickle as pk
from sets import Set
import itertools
import sys
from subprocess import call
import matplotlib.pyplot as plt


def uniqify(seq):
   # Not order preserving
   set = Set(seq)
   return list(set)


notebook_mode=False;

if notebook_mode==True:
    original_graph= #name of the edgelist file
    dir= #output directory path
    dataset_tag= #name tag
else:
    if len(sys.argv)>=4:
        original_graph=sys.argv[1]; 
        dir=sys.argv[2];
        dataset_tag = sys.argv[3];
    else:
        print('Input is required as:\n 1) full edgelist filename 
        \n 2) name of output directory 
        \n 3) name tag for output files');
        sys.exit();

if not os.path.exists(dir):
    os.makedirs(dir)


G=nx.Graph();
G=nx.read_edgelist(original_graph,delimiter=' ',nodetype=float);
cliques=nx.find_cliques_recursive(G);
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

fname=dir+dataset_tag+'_clique_filtration.pck'
filtration_file=open(fname,'w');
pk.dump(Clique_dictionary,filtration_file);
filtration_file.close();
del filtration_file;


sys.path.append('../')
import Holes as ho
import imp
imp.reload(ho);

#jython string position

max_homology_dimension=k;

try:
    ho.persistent_homology_calculation(fname,k,dataset_tag,dir)
except OSError, e:
    print "Execution failed for file:"+str(fname);


betti_num=pk.load(open(dir+'gen/betti_'+dataset_tag+'_.pck'))
print betti_num
