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

if __name__ == '__main__':

	raw_data = readfile('networkdata.txt')
	node_list = (set([item for sublist in raw_data for item in sublist]))
	G = nx.Graph()
	G.add_nodes_from(node_list)
	for edges_num in range(len(raw_data)):
		G.add_edge(raw_data[edges_num][0] , raw_data[edges_num][1])

	# print(len(node_list))
	node_degree = G.degree(node_list)
	sorted_x = sorted(node_degree.items(), key=operator.itemgetter(1) , reverse = True)
	print((sorted_x[0:30]))