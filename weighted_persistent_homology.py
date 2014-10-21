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
    edgelist_file= #name of the edgelist file
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


# output of the filtration file in a hopefully matlab compliant form
fname=dir+dataset_tag+'_weighted_clique_filtration.pck'
f=open(fname,'r')
weighted_fil=pickle.load(f)
k=len(sorted(weighted_fil.keys(),key=len)[-1])

# The last bit of code takes the edgelist and produces 
# the filtration file saved in the code just here above.
# The following step is to perform the persistent homology calculation.
# The problem here is that due to the code being available only in jython
# we need to pass the argument to a shell script and then 
# reload the results from the output files.


sys.path.append('../')
import Holes as ho
#jython string position


max_homology_dimension=k;

try:
    ho.persistent_homology_calculation
    (fname,max_homology_dimension,dataset_tag,dir)
except OSError, e:
    print "Execution failed for file:"+str(fname);
