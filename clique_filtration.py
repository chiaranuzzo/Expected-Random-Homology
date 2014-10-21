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
    if len(sys.argv)>=4:
        dir=str(sys.argv[2]); #insert final slash
        dataset_tag=str(sys.argv[3]); #without underlines
        edgelist_file= str(sys.argv[1]);
        if len(sys.argv)>=5:
            IR_weight_cutoff=float(sys.argv[4]);
        else:
            IR_weight_cutoff=1;
    else:
        print('Input is required as:\n 1) full edgelist filename 
        \n 2) name of output directory \n 3) name tag for output files');
        sys.exit();

if not os.path.exists(dir):
    os.makedirs(dir)

# The next step is  filtrate the graph according to the weight 
# and produce a valid filtration

print('Loading edgelist file...');
G=nx.Graph();
G=nx.read_weighted_edgelist(edgelist_file,delimiter=' ',nodetype=float);
print(' completed.');


#preliminary scan of edge weights to define filtration steps
print('Preliminary scan of edge weights to define filtration steps...');
edge_weights=[];
for n,nbrs in G.adjacency_iter():
        for nbr,eattr in nbrs.items():
                data=eattr['weight']
                if data not in edge_weights:
                        edge_weights.append(data);
edge_weights=uniqify(edge_weights);
edge_weights=sorted(edge_weights, reverse=True);

print('Preliminary scan and sorting completed.')
print('Weight cutoff is: ' +str(IR_weight_cutoff));

#Define the clique dictionary
Clique_dictionary={};
print('Constructing filtration...');
#Beginning of filtration construction
G_supplementary=nx.Graph();
max_index=0; #the max index will be used 
# for the persistent homology computation
for index,thr in enumerate(edge_weights):
        if thr>IR_weight_cutoff:
                print "Index: "+str(index)+". Threshold: "+str(thr);
                for n,nbrs in G.adjacency_iter():
                        for nbr,eattr in nbrs.items():
                                data=eattr['weight']
                                if data>=thr:
                                        edge=[n,nbr];
                                        edge.sort();
                                        G_supplementary.add_edge(edge[0],edge[1]);
                #clique detection in partial graph
                cliques=nx.find_cliques_recursive(G_supplementary);
                # adding cliques to the filtration
                for clique in cliques: 
                #loop on new clique
                        clique.sort();

                        for k in range(1,len(clique)+1):
                         #loop on clique dimension 
                         # to find missed faces of simplex
                                for subclique in itertools.combinations(clique,k):
                                        if str(list(subclique)) not in Clique_dictionary:
                                                Clique_dictionary[str(list(subclique))]=[];
                                                Clique_dictionary[str(list(subclique))].append(str(index));
                                                Clique_dictionary[str(list(subclique))].append(str(thr))
                        max_index=index;
                del cliques

del G_supplementary;

print('Max filtration value: '+str(max_index));
print('Clique dictionary created.');

# output of the filtration file in a hopefully matlab compliant form
fname=dir+dataset_tag+'_weighted_clique_filtration.pck'
filtration_file=open(fname,'w');
pickle.dump(Clique_dictionary,filtration_file);
filtration_file.close();
print('Clique dictionary pickle-dumped to '
+ dir +dataset_tag+'_weighted_clique_filtration.pck');
del Clique_dictionary
