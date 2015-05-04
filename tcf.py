import sys, getopt
import networkx as nx
import numpy as np
from collections import deque

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

dummy = -1 # node title for the dummy node


def main(argv):
   inputfile = ''
   outputfile = ''
   graphfile = ''
   source = 0
   destination = 0
   budget = 0
   

   try:
      opts, args = getopt.getopt(argv,"h:i:o:s:d:b:g:",["gfile=","ifile=",\
        "ofile="])
   except getopt.GetoptError:
      print 'tcf.py -i <intermediate_output_file> -o <outputfile> -s <source>'\
         + '-d <destination> -b <budget> -g <graphfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'tcf.py -i <intermediate_output_file> -o <outputfile> -s' \
         + ' <source> -d <destination> -b <budget> -g <graphfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      elif opt in ("-s"):
         source = int(arg)
      elif opt in ("-d"):
         destination = int(arg)
      elif opt in ("-b"):
         budget = int(arg)
      elif opt in ("-g"):
         graphfile = arg

#  	Time contrained bitmap

   print graphfile
   f = open(graphfile, 'r')
   max_nodes = int(f.readline())
   f.close()
    
   graph = nx.DiGraph()
   TCGraph = nx.DiGraph()

   print "graphfile is", graphfile
   g = np.loadtxt(graphfile, dtype = int , skiprows = 1, ndmin = 2)

   # create graph from input file
   for i in range(1, max_nodes+1):
      graph.add_node(i)
      TCGraph.add_node(i)

   for i in range(0, len(g)):
      graph.add_edge(g[i][0], g[i][1], weight = g[i][2])
      graph.add_edge(g[i][1], g[i][0], weight = g[i][2])

   # Dijkstra's to find shortest distance to source and destination from
   # each node

   to_source = nx.single_source_dijkstra_path_length(graph,source)
   to_dest = nx.single_source_dijkstra_path_length(graph,destination)
   
   # For each edge, check to see if shortest path using this edge is 
   # within the time budget
   for edge in graph.edges(data = 'true'):
      if((to_source[edge[0]] + edge[2]['weight'] + to_dest[edge[1]]) <= budget):
         TCGraph.add_edge(edge[0],edge[1], weight = edge[2]['weight'])

   # print the graph
   f = open(inputfile,'w')
   f.write("Source : " + str(source) + '\n')
   f.write("Destination : " + str(destination) + '\n')
   f.write("Budget : " + str(budget) + '\n')
   f.write("Set of edges is\n")
   for e in TCGraph.edges(data = 'true'):
      f.write(str(e[0]) + ' ' + str(e[1]) + ' ' + str(e[2]['weight']) + '\n')

   f.close()

   # Loop removal using Suurballe's Algorithm
  
   print "input file", inputfile
   a = np.loadtxt(inputfile, dtype = int , delimiter = " ", skiprows = 4,\
       ndmin = 2)
   if len(a) == 0:
      f = open(outputfile,'w')
      f.write("Source : " + str(source) + '\n')
      f.write("Destination : " + str(destination) + '\n')
      f.write("Budget : " + str(budget) + '\n')
      f.write("Set of edges is\n")
      f.close()
      sys.exit(0)
  
   NG = nx.DiGraph()
    
   for i in range(0, len(a)):
      NG.add_edge(a[i][0], a[i][1], weight = a[i][2])
      NG.add_edge(a[i][1], a[i][0], weight = a[i][2])

   remaining = deque(nx.nodes(NG)) # remaining nodes to run suurballe's from
   remaining.remove(source)
   remaining.remove(destination) # these shouldn't be included

   # Split all nodes to in and out nodes connected by zero-weight edge
   working_graph = split_graph(NG)

   # add our fake node between the source and the destination with edges of 
   # latency 0
  
   working_graph.add_node(dummy)
   working_graph.add_edge(str(source) + "_out", dummy, weight = 0)
   working_graph.add_edge(str(destination) + "_out", dummy, weight = 0) 

   while len(remaining) > 0:
      # combine i in and i out
      i = remaining.popleft()
      working_graph = combine_node(working_graph, i)
      
      # step 1: run bellman ford from i to dummy, store path in a list
      # Total Latency is given by dest[dummy]
      pred, dest = nx.bellman_ford(working_graph, i, weight='weight')
      
      if(not (dummy in dest)):
          print "Error: dummy not reachable from ", i
          sys.exit(0)     
 
      # step 2: get this shortest path and invert the edges in NG
      path = []
      temp = dummy
      while(temp != i):
          path.append([pred[temp],temp])
          temp = pred[temp]
      
      for e in path:
          temp_weight = working_graph.edge[e[0]][e[1]]['weight'] 
          temp_weight*=-1
          working_graph.remove_edge(e[0],e[1])
          
          if(working_graph.has_edge(e[1],e[0])):
              temp_lat = working_graph.edge[e[1]][e[0]]['weight'] 
              working_graph.add_edge(e[1], e[0], weight = temp_weight, original\
                 = temp_lat)
          else:
              working_graph.add_edge(e[1], e[0], weight = temp_weight, original\
                = -1)
          
      
      # step 3: run bellman ford from i to dummy on new graph, store path in
      # a dictionary.  Add each latency to total latency.
      pred_inv, dest_inv = nx.bellman_ford(working_graph, i, weight='weight')

      # If bellman ford says distance to dummy is negative infinity, remove
      # node i from remaining and from NG and continue to next node in remaining
      # if total latency of both paths is higher than the budget, remove node i
      # from NG and continue to the next node in remaining
      
      if((not (dummy in dest_inv)) or ((dest[dummy] + dest_inv[dummy]) \
          > budget)):
         NG.remove_node(i)
         for e in path:
             if(working_graph.edge[e[1]][e[0]]['original'] == -1):
                  w =  working_graph.edge[e[1]][e[0]]['weight']
                  w *= -1
                  working_graph.remove_edge(e[1],e[0])
                  working_graph.add_edge(e[0],e[1], weight = w)
             else:
                  temp_lat =  working_graph.edge[e[1]][e[0]]['original']
                  w =  working_graph.edge[e[1]][e[0]]['weight']
                  w*=-1
                  working_graph.add_edge(e[1], e[0], weight = temp_lat, \
                     original = -1)
                  working_graph.add_edge(e[0],e[1], weight = w)

      else:
         path_new = {}
         temp = dummy
         while(temp != i):
             path_new[pred_inv[temp]] = temp
             temp = pred_inv[temp]

      # iterate over path 1 list -- for each item, see if its inverse exists in
      # the dictionary -- if yes remove both (makes this path edge-disjoint)  
         for e in path:
             if(e[1] in path_new):
                  if(path_new[e[1]] == e[0]):
                      path.remove(e)
                      del path_new[e[1]]
      # Else, remove path 1 node from remaining.      
             else:
                  if(remaining.count(e[0])>0):
                      remaining.remove(e[0])
                      
      # also switch inverse back on graph
             if(working_graph.edge[e[1]][e[0]]['original'] == -1):
                  w =  working_graph.edge[e[1]][e[0]]['weight']
                  w*=-1
                  working_graph.remove_edge(e[1],e[0])
                  working_graph.add_edge(e[0],e[1], weight = w) 
             else:
                  temp_lat =  working_graph.edge[e[1]][e[0]]['original']
                  w =  working_graph.edge[e[1]][e[0]]['weight']
                  w*=-1
                  working_graph.add_edge(e[1], e[0], weight = temp_lat, \
                     original = -1)
                  working_graph.add_edge(e[0],e[1], weight = w)
      
      # Create list from dictionary. Iterate over and remove each node from
      # remaining. 
          
         for n in path_new.keys():
             if(remaining.count(n)>0):
                      remaining.remove(n)

      # split i into i in and i out      
      working_graph = split_node(working_graph, i) 


   # print the graph
   f = open(outputfile,'w')
   f.write("Source : " + str(source) + '\n')
   f.write("Destination : " + str(destination) + '\n')
   f.write("Budget : " + str(budget) + '\n')
   f.write("Set of edges is\n")
   for e in NG.edges():
      f.write(str(e[0]) + '->' + str(e[1]) + '\n')

   f.close()

# Split a node into its in and out nodes connected by a zero-latency
# edge
def split_node(G, n):
   nin = str(n) + "_in"
   nout = str(n) + "_out"
   outgoing = G.out_edges(nbunch=[n], data=True)
   incoming = G.in_edges(nbunch=[n], data=True)
   G.remove_node(n)
   G.add_edge(nin, nout, weight = 0)
   for edge in outgoing: # make edge from outgoing to the prev dest
      G.add_edge(nout, edge[1], weight=edge[2]['weight'])
   for edge in incoming:
      G.add_edge(edge[0], nin, weight=edge[2]['weight'])
   return G

# Combine the in and out nodes back to one
def combine_node(G, n):
   nin = str(n) + "_in"
   nout = str(n) + "_out"
   outgoing = G.out_edges(nbunch = [nout], data=True)
   incoming = G.in_edges(nbunch = [nin], data=True)
   G.remove_node(str(n) + "_in")
   G.remove_node(str(n) + "_out")
   for edge in outgoing:
      G.add_edge(n, edge[1], weight=edge[2]['weight'])
   for edge in incoming:
      G.add_edge(edge[0], n, weight=edge[2]['weight'])
   return G
    
# return a version of graph with every node split into an in and out node
# and connect with edge of 0 weight from in to out
# except for dummy node
def split_graph(graph):
    node_iter = graph.nodes_iter()
    edge_iter = graph.edges_iter(data=True)
    G = nx.DiGraph()
    while True:
        try:
            n = node_iter.next()
        except StopIteration:
            break
        nin = str(n) + "_in"
        nout = str(n) + "_out"
        G.add_edge(nin, nout, weight = 0)
    while True:
        try:
            e = edge_iter.next()
        except StopIteration:
            break
        G.add_edge(str(e[0]) + "_out", str(e[1]) + "_in", weight=e[2]['weight'])
    return G

if __name__ == "__main__":
   main(sys.argv[1:])
