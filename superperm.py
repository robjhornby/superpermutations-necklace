"""
Created on Tue Feb  5 13:13:30 2019

@author: Rob Hornby robjhornby@gmail.com
"""

from array import array
from operator import mul
from functools import reduce
from itertools import permutations
from itertools import cycle


from superpermUtil import *
from random import *
import math
import time


solutions = []
solnIters = []
stage = 5 # Number of objects

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
#tmp = [0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 4, 2, 1, 2, 1, 1, 0,0 ]
#a = tmp
touch = TouchStore(method, list(a))
abort = False

minCost = 873
pruned = 0


def divisors(n):
    div = set()
    for i in range(1, (int)(n/2+1)):
        if n % i == 0:
            div.add(i)

    div.add(n)
    return div

def pruneCondition(touch, pos,minCost):
    global pruned
    if touch.projectedCost(pos) > minCost:
        pruned += 1
        return True
    if not touch.isTrue():
        pruned += 1
        return True
    return False

itstatus = 100000
def necklaceSearch(touch):
    global it, minCost, itstatus
    n = touch.method.numNodes
    k = len(touch.method.edges)-1
    print('Starting necklace search on {} objects, n={}, k={}'.format(touch.method.stage,n,k))
    
    divs = divisors(n)
    while touch.path != [k]*n:
        debprint('While --------------------')
        
        if touch.firstFalsePos < 0:
            start = n
            debprint('Going from n')
        else:
            start = touch.firstFalsePos
            debprint('Going from first false')
        debprint(touch.path)
        for pos, el in reversed(tuple(enumerate(touch.path[0:start+1]))):
            debprint('For -----------')
            if el < k:
                touch.setLastEdge(pos, el + 1)
                it += 1
                if it%itstatus == 0:
                    PrintStatus(touch,pos)
                    
                debprint(touch.getPath())
                debprint(touch)
                debprint(pos)
                debprint(minCost)
                debprint(pruneCondition(touch,pos,minCost))
                debprint(touch.isTrue())
                debprint(touch.firstFalsePos)
                debprint()
                if pruneCondition(touch,pos,minCost):
                    debprint('prune 1')
                    continue
                debprint(n-pos-1)
                debprint(n)
                debprint(pos)
                for i in range(n-pos-1): 
                    # repeat the prenecklace to the end
                    debprint('D')
                    debprint(pos+i+1)
                    
                    touch.setLastEdge(pos+i+1, touch.path[i])
                    it += 1
                    if it%itstatus == 0:
                        PrintStatus(touch,pos)
            
                    debprint(touch.getPath())
                    isNecklace = (i == n-pos-2) and (pos+1 in divs)
                    if isNecklace and touch.isHamiltonianCycle():
                        PrintIt(touch)
                    if pruneCondition(touch,pos,minCost):
                        debprint('prune 2')
                        break
                    
                    
                """
                # condition for this to be a necklace
                if pos+1 in divs:
                    yield list(t)
                """
                break




def PrintStatus(touch,pos):
    print("Iteration {}".format(it))
    print("Number of solutions: {}".format(len(solutions)))
    print("Shortest superperm found: {}".format(minCost))
    print("Current node: " + " ".join([repr(x) for x in touch.getPath()]))
    print("Current cost: {}".format(touch.getCost()))
    print("Current projected cost: {}".format(touch.projectedCost(pos)))
    print("Nodes visited: {}".format(len(touch)))
    print("Pruned: {}".format(pruned))
    print(touch.getPath())

def PrintIt(touch):
    global minCost
    if touch.isHamiltonianCycle():
        soln = touch.optimumPath()
        minCost = touch.getCost()
        print('Success - at {} iterations'.format(it))
        print('Superpermutation length {}'.format(soln.getCost()))
        print(soln)
        print(soln.getPath())
        solutions.append(soln)
        solnIters.append(it)
        if not isSuperperm(soln.method.stage,soln.getSuperperm()):
            print('Problem - not a superperm')


"""me = Method(6)
ex = (int(i)-1 for i in '12345612345162345126345123645132645136245136425136452136451234651234156234152634152364152346152341652341256341253641253461253416253412653412356412354612354162354126354123654132654312645316243516243156243165243162543162453164253146253142653142563142536142531645231465231456231452631452361452316453216453126435126431526431256432156423154623154263154236154231654231564213564215362415362145362154362153462135462134562134652134625134621536421563421653421635421634521634251634215643251643256143256413256431265432165432615342613542613452613425613426513426153246513246531246351246315246312546321546325146325416325461325463124563214563241563245163245613245631246532146532416532461532641532614532615432651436251436521435621435261435216435214635214365124361524361254361245361243561243651423561423516423514623514263514236514326541362541365241356241352641352461352416352413654213654123')
exT = me.parse(ex)
"""


print('Starting')

necklaceSearch(touch)      #initial call

print("Found {} superperms in {} iterations".format(len(solutions),it))
print("Shortest superperm found: {}".format(minCost))
print("Number of nodes pruned: {}".format(pruned))
print("")
print("Final node: " + "".join([repr(x) for x in touch.getPath()]))
print(touch.getPath())

