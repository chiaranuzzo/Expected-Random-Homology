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

sys.path.append('../')
import Holes as ho
import imp
imp.reload(ho);
from Holes import *

notebook_mode=False;

if notebook_mode==True:
    dir= #output directory path
    dataset_tag= #name tag
    max_index = #maximum index of the filtration
else:
	if len(sys.argv)>=3:
    		dir=str(sys.argv[1]); #insert final slash
    		dataset_tag=str(sys.argv[2]); #without underlines
    		max_index = int(sys.argv[3]);
	else:
    		print('Input is required as:\n 1) name of output directory 
    		\n 2) name tag for output files 
    		\n 3) max_index for barcodes counting');
    		sys.exit();

if not os.path.exists(dir):
    os.makedirs(dir)

generators_dict=pk.load(open(dir+'gen/generators_'+dataset_tag+'_.pck'))

def barcodes_counting(gen_dict,max_index):#,dt):
        '''
        Calculates net network hollowness over a moving window
        along the filtration.
        The result is the sum of all persistence intervals over
        a given window.

        '''
        av_h=[];
        lista_indici=range(0,max_index);
        data={};
        if len(gen_dict)>0:
                N=float(len(gen_dict));
                data[lista_indici[0]]=[];
                for l,el in enumerate(lista_indici[1:]):
                        data[el]=[];
                        for cycle in gen_dict:
                                if (float(cycle.start)<=float(el)) and (float(cycle.end)>=float(lista_indici[l])):

    #we add -1 to float(cycle.start) to include the left end
    
                                        data[el].append((int(min(float(cycle.end),float(el))-max(float(cycle.start)-1,float(lista_indici[l])))));
                                        
                for i in lista_indici:
                        if data[i]:
                                av_h.append(np.sum(data[i]));
                        else:
                                av_h.append(0);

                return lista_indici, av_h;
        else:
                print 'Cycle dictionary is empty';

for key in generators_dict:
    if len(generators_dict[key])>0:
        print key
        [n, somma] = barcodes_counting(generators_dict.values()[key],
        max_index)
        print 'betti'+str(key)
        listab = []
        for i in range(max_index):
                listab.append(somma[i])
                print i, somma[i]
        lista=open(dir+dataset_tag+'_ph_betti'+str(key)+'.pck', 'w')
        pk.dump(listab,lista)
        lista.close()


