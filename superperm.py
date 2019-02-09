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

a = [0]*(n)  #temporary necklace array
prenecklaces = []        #final list of prenecklaces
necklaces = [] #list of necklaces
touches = [[]]*(n+1)
stop = False

it = 0
falses = 0

touch = TouchStore(method, list(a[1:]))
abort = False

minCost = 872
pruned = 0

def gen(t, p):
    global it, falses, abort, minCost,pruned
    it += 1
    if(abort):
        return 0
    if(it%10000==0):
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
        print("")
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
    global minCost
    if len(touch)+1 == touch.method.numNodes:
        # Complete the cycle by finding the final edge
        print(touch.node,touch.method.identity)
        (fi,f,fString,fCost) = touch.method.shortestEdge(touch.node,touch.method.identity)

        # Delete the longest node in the cycle, leaving the shortest path
        if fi >= 0:
            # final edge is a standard edge
            costs = touch.pathcost[1:] + [fCost]
            delInd, delCost = max(tuple(enumerate(costs))[::-1], key=lambda a:a[1])
            delInd += 1
            if delInd == touch.method.numNodes-1:
                newpath = a
            else:
                newpath = list(a[:delInd])+[fi]+list(a[delInd+1:])

            soln = TouchStore(method,newpath)
            minCost = soln.getCost()
        else:
            print('Special final edge required: {}'.format(fString))
            if all(fCost >= x for x in touch.pathcost[1:]):
                print('Final edge heaviest - ignore')
            else:
                print('Final edge provides a better solution, not implemented')
            soln = TouchStore(method,list(a[1:touchlen+1]))
            delInd = -1
            delCost = fCost

        print('Success - after {} iterations'.format(it))
        print(soln)
        print("Final edge: {}, index {}".format(fString,fi))
        print("Deleted node: {}, cost {}".format(delInd,delCost))
        print(soln.getPath())
        print('Superpermutation length {}'.format(touch.getCost()))
        solutions.append(soln)
        solnIters.append(it)
        if not isSuperperm(soln.method.stage,soln.getSuperperm()):
            print('Problem - not a superperm')



ex = (int(i)-1 for i in '12345612345162345126345123645132645136245136425136452136451234651234156234152634152364152346152341652341256341253641253461253416253412653412356412354612354162354126354123654132654312645316243516243156243165243162543162453164253146253142653142563142536142531645231465231456231452631452361452316453216453126435126431526431256432156423154623154263154236154231654231564213564215362415362145362154362153462135462134562134652134625134621536421563421653421635421634521634251634215643251643256143256413256431265432165432615342613542613452613425613426513426153246513246531246351246315246312546321546325146325416325461325463124563214563241563245163245613245631246532146532416532461532641532614532615432651436251436521435621435261435216435214635214365124361524361254361245361243561243651423561423516423514623514263514236514326541362541365241356241352641352461352416352413654213654123')
exT = method.parse(ex)



print('Starting')
gen(1,1)       #initial call

print("Found {} superperms in {} iterations".format(len(solutions),it))
print("Shortest superperm found: {}".format(minCost))
print("Number of nodes pruned: {}".format(pruned))
print("")
print("Final node: " + "".join([repr(x) for x in touch.getPath()]))
print(touch.getPath())

