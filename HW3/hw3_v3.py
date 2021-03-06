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
	G = nx.Graph()
	G.add_nodes_from(node_list)
	for edges_num in range(len(raw_data)):
		G.add_edge(raw_data[edges_num][0] , raw_data[edges_num][1])

	# print(len(node_list))
	node_degree = G.degree(node_list)
	sorted_x = sorted(node_degree.items(), key=operator.itemgetter(1) , reverse = True)
	print((sorted_x[0:30]))
	for i in range(30):
		ans_list.append(sorted_x[i][0])
	writefile(ans_list,'ans_v3.txt')