import networkx as nx
import os, pickle
from sets import Set
import itertools
import sys
from subprocess import call

def uniqify(seq):
   # Not order preserving
   set = Set(seq)
   return list(set)


notebook_mode=False;

if notebook_mode==True:
    original_graph= #name of the edgelist file
    dir= #output directory path
    dataset_tag= #name tag
    IR_weight_cutoff= #optional cutoff weight
else:
    if len(sys.argv)>=3:
        dir=str(sys.argv[1]); #insert final slash
        dataset_tag=str(sys.argv[2]); #without underlines
    else:
        print('Input is required as:\n 1) name of output directory 
        \n 2) name tag for output files');
        sys.exit();

if not os.path.exists(dir):
    os.makedirs(dir)


sys.path.append('../')
import Holes as ho

import pickle as pk
generators_dict=pk.load(open(dir+'gen/generators_'+dataset_tag+'_.pck'))


for key in generators_dict:
    if len(generators_dict[key])>0:
        print key
        ho.barcode_creator(generators_dict[key]);
        plt.show()
        ho.complete_persistence_diagram(generators_dict[key])
