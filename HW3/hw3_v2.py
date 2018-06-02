# -*- coding: utf-8 -*-
import sys
import numpy as np
from random import *
from math import sin, asin, cos, radians, fabs, sqrt  
import math 
import itertools
import networkx as nx
import os
import time
import queue
from queue import PriorityQueue as PQ


def readfile(filename):

	dataReadIn = []

	with open (filename, 'r') as f :
		for line in f :
			dataReadIn.append ([row for row in line.strip().split(' ')])
	f.close ()
	return dataReadIn

def degreeDiscountIC(G, k, p=.05):
	''' Finds initial set of nodes to propagate in Independent Cascade model (with priority queue)
	Input: G -- networkx graph object
	k -- number of nodes needed
	p -- propagation probability
	Output:
	S -- chosen k nodes
	'''
	S = []
	dd = PQ() # degree discount
	t = dict() # number of adjacent vertices that are in S
	d = dict() # degree of each vertex

	# initialize degree discount
	for u in G.nodes():
		d[u] = sum([G[u][v]['weight'] for v in G[u]]) # each edge adds degree 1
		# d[u] = len(G[u]) # each neighbor adds degree 1
		dd.add_task(u, -d[u]) # add degree of each node
		t[u] = 0

	# add vertices to S greedily
	for i in range(k):
		u, priority = dd.pop_item() # extract node with maximal degree discount
		S.append(u)
		for v in G[u]:
			if v not in S:
				t[v] += G[u][v]['weight']  # increase number of selected neighbors
				priority = d[v] - 2*t[v] - (d[v] - t[v])*t[v]*p # discount of degree
				dd.add_task(v, -priority)
	return S
	
def runIC (G, S, p = 0.05):
	''' Runs independent cascade model.
	Input: G -- networkx graph object
	S -- initial set of vertices
	p -- propagation probability
	Output: T -- resulted influenced set of vertices (including S)
	'''
	from copy import deepcopy
	from random import random
	T = deepcopy(S) # copy already selected nodes

	# ugly C++ version
	i = 0
	while i < len(T):
		for v in G[T[i]]: # for neighbors of a selected node
			if v not in T: # if it wasn't selected yet
				w = G[T[i]][v]['weight'] # count the number of edges between two nodes
				if random() <= 1 - (1-p)**w: # if at least one of edges propagate influence
					print (T[i], 'influences', v)
					T.append(v)
		i += 1

	# neat pythonic version
	# legitimate version with dynamically changing list: http://stackoverflow.com/a/15725492/2069858
	# for u in T: # T may increase size during iterations
	#     for v in G[u]: # check whether new node v is influenced by chosen node u
	#         w = G[u][v]['weight']
	#         if v not in T and random() < 1 - (1-p)**w:
	#             T.append(v)
	return T


if __name__ == '__main__': 

	start = time.time()

	# read in graph
	G = nx.Graph()
	raw_data = readfile('networkdata.txt')
	node_list = sorted(set([item for sublist in raw_data for item in sublist]))
	G = nx.Graph()
	G.add_nodes_from(node_list)
	for edges_num in range(len(raw_data)):
		G.add_edge(raw_data[edges_num][0] , raw_data[edges_num][1] , weight = 1)
	
	print ('Built graph G')
	print (time.time() - start)

	#calculate initial set
	seed_size = 30
	S = degreeDiscountIC(G, seed_size)
	print ('Initial set of', seed_size, 'nodes chosen')
	print (time.time() - start)

	# write results S to file
	with open('visualisation.txt', 'w') as f:
		for node in S:
			f.write(str(node) + os.linesep)

	# calculate average activated set size
	iterations = 200 # number of iterations
	avg = 0
	for i in range(iterations):
		T = runIC(G, S)
		avg += float(len(T))/iterations
		# print i, 'iteration of IC'
	print ('Avg. Targeted', int(round(avg)), 'nodes out of', len(G))
	print (time.time() - start)

	with open('IC/lemma1.txt', 'w') as f:
		f.write(str(len(S)) + os.linesep)
		for node in T:
			f.write(str(node) + os.linesep)
	#console = []