import sys, getopt
import networkx as nx
import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main(argv):
   inputfile = ''
   outputfile = ''
   graphfile = ''
   source = 0
   destination = 0
   positionfile = ''
   noloopsfile = ''
   edge_labels = 0

   try:
      opts, args = getopt.getopt(argv,"hg:i:o:s:d:p:w:e:",["gfile=","ifile=",
         "ofile="])
   except getopt.GetoptError:
      print 'draw_graph.py -g <original_graph_file> -i '\
                + '<time_constrained_inputfile> -o <outputfile> -s <source>' \
               +'-d <destination> -p <position file> -w <without_loops_file> '\
              + '-e <edge-labels (0 or 1)>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'draw_graph.py -g <original_graph_file> -i '\
                + '<time_constrained_inputfile> -o <outputfile> -s <source> \
               -d <destination> -p <position file> -w <without_loops_file> -e' \
              + '<edge-labels (0 or 1)>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      elif opt in ("-g", "--gfile"):
         graphfile = arg
      elif opt in ("-s"):
         source = arg
      elif opt in ("-d"):
         destination = arg
      elif opt in ("-p"):
         positionfile = arg
      elif opt in ("-w"):
         noloopsfile = arg
      elif opt in ("-e"):
         edge_labels = int(arg)

   G = nx.Graph()
   NG = nx.Graph()
   finalgraph = nx.Graph()

   f = open(graphfile,'r')
   max_nodes = int(f.readline())

   f.close()
   
   pos = open(positionfile,'r')
   if(int(pos.readline())!=max_nodes):
      print 'The nuber of nodes in the position file does not match the number'\
         + ' of nodes in the graphfile'
      sys.exit(0)
   pos.close()

   full_graph = np.loadtxt(graphfile, dtype = int, skiprows = 1, usecols = \
      (0, 1, 2),  ndmin = 2)

   a = np.loadtxt(inputfile, dtype = int, delimiter = " ", skiprows = 4,\
        usecols = (0, 1), ndmin = 2)

   p = np.loadtxt(positionfile, dtype = float, delimiter = " ", skiprows = 1, \
      ndmin = 2)
   
   nl = np.loadtxt(noloopsfile, dtype = int, delimiter = '->', skiprows = 4,\
         ndmin = 2)

   pos_dict = {}
   for i in range(1, max_nodes+1):
       G.add_node(i)
       NG.add_node(i)
       finalgraph.add_node(i)
       pos_dict[i] = [p[i-1][0],p[i-1][1]]
 
   edge_dict = {}
   for i in range(0, len(full_graph)):
       G.add_edge(full_graph[i][0],full_graph[i][1])
       G.add_edge(full_graph[i][1],full_graph[i][0])
       t = (full_graph[i][0], full_graph[i][1])
       edge_dict[t] = full_graph[i][2]

   for i in range(0, len(a)):
	   NG.add_edge(a[i][0], a[i][1])
      
   for i in range(0, len(nl)):
       finalgraph.add_edge(nl[i][0], nl[i][1])

   nx.draw_networkx_nodes(G,pos = pos_dict,nodelist= nx.nodes(G), node_color =\
      'White')
   nx.draw_networkx_nodes(G,pos = pos_dict,nodelist=[int(source)] ,node_color =\
      'Green')
   nx.draw_networkx_nodes(G,pos = pos_dict,nodelist=[int(destination)], \
      node_color = 'Yellow')
   nx.draw_networkx_edges(G,pos = pos_dict, edge_labels = edge_dict, \
      edge_color='Grey')
   nx.draw_networkx_edges(NG, pos = pos_dict, edge_color = 'Red', width = 3)
   nx.draw_networkx_edges(finalgraph, pos = pos_dict, edge_color = 'Blue', \
      width = 3)

   labels={}

   for i in range(1, max_nodes+1):
        labels[i]=i

   nx.draw_networkx_labels(G,pos = pos_dict)
   if edge_labels == 1:
      edge_labels = nx.get_edge_attributes(G, 'edge_labels')
      nx.draw_networkx_edge_labels(G, pos = pos_dict, edge_labels = edge_dict,\
         label_pos = .45)


   plt.axis('off')
   plt.savefig(outputfile, bbox_inches = "tight", pad_inches = 0) # save as png

if __name__ == "__main__":
   main(sys.argv[1:])
