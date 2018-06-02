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
import operator


def readfile(filename):

	dataReadIn = []

	with open (filename, 'r') as f :
		for line in f :
			dataReadIn.append ([row for row in line.strip().split(' ')])
	f.close ()
	return dataReadIn

def writefile(data,filename):
	fw = open(filename, 'w')
	for cnt in range(len(data)):
		fw.write(data[cnt])
		fw.write('\n')
	fw.close()

if __name__ == '__main__':

	raw_data = readfile('networkdata.txt')
	node_list = (set([item for sublist in raw_data for item in sublist]))
	ans_list = []
	#avg_path_list = []
	G = nx.Graph()
	G.add_nodes_from(node_list)
	for edges_num in range(len(raw_data)):
		G.add_edge(raw_data[edges_num][0] , raw_data[edges_num][1])

	# print(len(node_list))
	node_degree = G.degree(node_list)
	#for g in nx.connected_component_subgraphs(G):
		#print(nx.average_shortest_path_length(g))
		#avg_path_list.append(nx.average_shortest_path_length(g))
	#avg_path = max(avg_path_list)

	sorted_x = sorted(node_degree.items(), key=operator.itemgetter(1) , reverse = True)
	ans_list.append(sorted_x[0][0])
	for num in range(len(node_list)):
		
		try:
			s=nx.shortest_path_length(G, source=sorted_x[num][0], target=sorted_x[num+1][0])
			print(sorted_x[num][0],sorted_x[num+1][0],s,G.degree(sorted_x[num][0]))
		except nx.NetworkXNoPath:
			s = -1
			print(sorted_x[num][0],sorted_x[num+1][0],'No path')
		
		if( s > 5 ):
			ans_list.append(sorted_x[num+1][0])
		if(len(ans_list)==30):
			break
	#print((ans_list))
	writefile(ans_list,'ans_v7.txt')