'''
import sys
import random
import numpy
from random import sample
from math import sin, asin, cos, radians, fabs, sqrt  
import math 
import itertools
'''
import random

def readfile(filename):

	dataReadIn = []

	with open (filename, 'r') as f :
		for line in f :
			dataReadIn.append ([row for row in line.strip().split(' ')])
	f.close ()
	return dataReadIn
	
def writefile(list_input,filename2):
	fw = open (filename2, 'w') 
	for cnt1 in range( len(list_input) ) :  
		fw.write("%s\n" % list_input[cnt1])
	
if __name__ == '__main__':

	node_list = []
	for cnt in range(15233):
		node_list.append(str(cnt))
	ans = random.sample(node_list , 30)
	writefile(ans,'random_v1.txt')