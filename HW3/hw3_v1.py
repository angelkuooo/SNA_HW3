# -*- coding: utf-8 -*-
import sys
import numpy as np
from random import *
from math import sin, asin, cos, radians, fabs, sqrt  
import math 
import itertools


def readfile(filename):

	dataReadIn = []

	with open (filename, 'r') as f :
		for line in f :
			dataReadIn.append ([row for row in line.strip().split(' ')])
	f.close ()
	return dataReadIn


def independent_cascade(G, seeds, steps=0):

	# make sure the seeds are in the graph
	for s in seeds:
		if s not in G.nodes():
			raise Exception("seed", s, "is not in graph")

	# change to directed graph
	if not G.is_directed():
		DG = G.to_directed()
	else:
		DG = copy.deepcopy(G)

	# init activation probabilities
	for e in DG.edges():
		if 'act_prob' not in DG[e[0]][e[1]]:
			DG[e[0]][e[1]]['act_prob'] = 0.1
		elif DG[e[0]][e[1]]['act_prob'] > 1:
			raise Exception("edge activation probability:", \
				DG[e[0]][e[1]]['act_prob'], "cannot be larger than 1")

	# perform diffusion
	A = copy.deepcopy(seeds)  # prevent side effect
	if steps <= 0:
		# perform diffusion until no more nodes can be activated
		return _diffuse_all(DG, A)
	# perform diffusion for at most "steps" rounds
	return _diffuse_k_rounds(DG, A, steps)

def _diffuse_all(G, A):
	tried_edges = set()
	layer_i_nodes = [ ]
	layer_i_nodes.append([i for i in A])  # prevent side effect
	while True:
		len_old = len(A)
		(A, activated_nodes_of_this_round, cur_tried_edges) = \
			_diffuse_one_round(G, A, tried_edges)
		layer_i_nodes.append(activated_nodes_of_this_round)
		tried_edges = tried_edges.union(cur_tried_edges)
		if len(A) == len_old:
			break
	return layer_i_nodes

def _diffuse_k_rounds(G, A, steps):
	tried_edges = set()
	layer_i_nodes = [ ]
	layer_i_nodes.append([i for i in A])
	while steps > 0 and len(A) < len(G):
		len_old = len(A)
		(A, activated_nodes_of_this_round, cur_tried_edges) = \
			_diffuse_one_round(G, A, tried_edges)
		layer_i_nodes.append(activated_nodes_of_this_round)
		tried_edges = tried_edges.union(cur_tried_edges)
		if len(A) == len_old:
			break
		steps -= 1
	return layer_i_nodes

def _diffuse_one_round(G, A, tried_edges):
	activated_nodes_of_this_round = set()
	cur_tried_edges = set()
	for s in A:
		for nb in G.successors(s):
			if (nb in A or (s, nb) in tried_edges or (s, nb) in cur_tried_edges):
				continue
		if _prop_success(G, s, nb):
			activated_nodes_of_this_round.add(nb)
		cur_tried_edges.add((s, nb))
	activated_nodes_of_this_round = list(activated_nodes_of_this_round)
	A.extend(activated_nodes_of_this_round)
	return A, activated_nodes_of_this_round, cur_tried_edges

def _prop_success(G, src, dest):
	return random.random() <= G[src][dest]['act_prob']
	
if __name__ == '__main__':
	raw_data = readfile('networkdata.txt')
	node_list = sorted(set([item for sublist in raw_data for item in sublist]))
	G = nx.Graph()
	G.add_nodes_from(node_list)
	for edges_num in range(len(raw_data)):
		G.add_edge(raw_data[edges_num][0] , raw_data[edges_num][1])
	layers = independent_cascade(G, ['0','5'] ,steps=20)
	print(layers[0])