# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 13:13:30 2019

@author: rh13
"""

from array import array
from operator import mul
from functools import reduce
from itertools import permutations
from itertools import cycle

##Generates all necklaces in two beads
##by building up true prenecklaces of increasing lengths
##and checks them for truth

from superpermUtil import *
from random import *
import math
import time


solutions = []
solnIters = []
stage = 6 # Number of objects

method = Method(stage)
k = len(method.edges) # Number of edges/size of dictionary for necklace search

minlength = 1
n = factorial(stage)     #length of prenecklaces to generate

a = [0]*(n+1)  #temporary necklace array
prenecklaces = []        #final list of prenecklaces
necklaces = [] #list of necklaces
touches = [[]]*(n+1)
stop = False

it = 0
falses = 0

touch = TouchStore(method, list(a[1:]))
abort = False

minCost = 100000000000
pruned = 0

def gen(t, p):
    global it, falses, abort, minCost,pruned
    it += 1
    if(abort):
        return 0
    if(it%500000==0):
        time.sleep(0.1)
        print("Iteration {}".format(it))
        print("Number of solutions: {}".format(len(solutions)))
        print("Shortest superperm found: {}".format(minCost))
        print("Current node: " + " ".join([repr(x) for x in touch.getPath()]))
        print("Current cost: {}".format(touch.getCost()))
        print("Current projected cost: {}".format(touch.projectedCost(p)))
        print("Nodes visited: {}".format(len(touch)))
        print("Pruned: {}".format(pruned))
        print(touch.getPath())
    if(it%6000000==0):
        check = input("Continue? (Y/n): ")
        if check is "n":
            abort = True
            print("Aborting")
        else:
            print("Continuing")

    projectedCost = touch.projectedCost(p)
    if t>1:
        touch.setLastEdge(t-2, a[t-1])
        
        if  projectedCost > minCost:
            """The current path already costs more than the best superperm - prune"""
            pruned += 1
            return 0
            
        if len(touch)+1 == touch.method.numNodes and touch.isTrue():
            """All perms visited exactly once - a superperm"""
            minCost = touch.getCost()
            PrintIt(p, t-1, touch)
            return 1
        elif not touch.isTrue():
            """A perm is visited twice - prune"""
            falses += 1
            return 1
    
    a[t] = a[t-p]
    gen(t+1, p)
    for j in range(a[t-p]+1, k):
        a[t] = j
        if gen(t+1, t) == 0:
            break

def PrintIt(p, touchlen, touch):
    if len(touch)+1 == touch.method.numNodes:
        soln = TouchStore(method,list(a[1:touchlen+1]))
        print('Success - after {} iterations'.format(it))
        print(soln)
        print(a[1:touchlen+1])
        print('Superpermutation length {}'.format(touch.getCost()))
        solutions.append(soln)
        solnIters.append(it)
        if not isSuperperm(soln.method.stage,soln.getSuperperm()):
            print('Problem - not a superperm')


print('Starting')
gen(1,1)       #initial call

print("Found {} superperms in {} iterations".format(len(solutions),it))
print("Shortest superperm found: {}".format(minCost))
print("Number of nodes pruned: {}".format(pruned))
print("")
print("Final node: " + "".join([repr(x) for x in touch.getPath()]))
print(touch.getPath())
