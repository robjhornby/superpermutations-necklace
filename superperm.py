"""
Created on Tue Feb  5 13:13:30 2019

@author: Rob Hornby robjhornby@gmail.com
"""

from array import array
from operator import mul
from functools import reduce
from itertools import permutations
from itertools import cycle
import time

from superpermUtil import *
from random import *
import math
import time
import cProfile

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
#tmp = [0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 4, 2, 1, 2, 1, 1, 0,0 ]
#a = tmp
touch = TouchStore(method, list(a))
abort = False

minCost = 872
prunedC = 0
prunedF = 0

def divisors(n):
    div = set()
    for i in range(1, (int)(n/2+1)):
        if n % i == 0:
            div.add(i)

    div.add(n)
    return div

def pruneCost(touch, pos,minCost):
    global prunedC
    projCost = touch.projectedCost()
    if projCost > minCost:
        #debprint('Prune projected cost pos: {}, projCost: {}'.format(pos,projCost))
        prunedC += 1
        return True
    if (np.array(touch.getPath()[:-1])>2).sum()>1:
        return True
    return False

def pruneTruth(touch):
    global prunedF
    if not touch.isTrue():
        #debprint('Prune truth')
        prunedF += 1
        return True
    return False
    
itstatus = 50000
def necklaceSearch(touch):
    global it, minCost, itstatus, starttime,prunedF,prunedC
    starttime = time.time()
    n = touch.method.numNodes
    k = len(touch.method.edges)-1
    lastPrunePos = touch.firstFalsePos
    print('Starting necklace search on {} objects, n={}, k={}'.format(touch.method.stage,n,k))
    
    divs = divisors(n)
    cond = True
    while cond:
        #debprint('-------------------------------------------------------------')
        #debprint('While -------------------- it {}'.format(it))
        #if it > 10000:
        #    break
        if lastPrunePos < 0:
            start = n
            #debprint('Going from end {}'.format(start))
        else:
            start = lastPrunePos
            #debprint('Going from last pruned position {}'.format(start))
        #debprint("path {}".format(touch.getPath()))
        if touch.path[0] == 1:
            break
        for pos, el in reversed(tuple(enumerate(touch.path[0:start+1]))):
            #debprint('For --------pos {}, el {} ---------------------------------'.format(pos,el))
            if el < k:
                touch.setLastEdge(pos, el + 1)
                it += 1
                if it%itstatus == 0:
                    PrintStatus(touch,pos)
                    
                #debprint("Path {}".format(touch.getPath()))
                #debprint(touch)
                #debprint("Pos {}, minCost {}, pruneCost {}, truth {}, firstFalse {}".format(
                #        pos,minCost,pruneCost(touch,pos,minCost),touch.isTrue(),touch.firstFalsePos))
    
                if pruneCost(touch,pos,minCost):
                    """All subsequent edges will also cost too much, step back"""
                    lastPrunePos = pos-1
                    #debprint('prune 1 cost')
                    break
                if pruneTruth(touch):
                    """Keep trying edges at this position"""
                    lastPrunePos = touch.firstFalsePos
                    """Unless it was the last node"""
                    if el+1 == len(touch.method.edges)-1:
                        lastPrunePos = touch.firstFalsePos - 1
                    #debprint('prune 1 truth, lastPrunePos {}'.format(lastPrunePos))
                    break
                else:
                    lastPrunePos = -1
                #debprint("n {}, n-pos-1 {}, pos {}".format(n,n-pos-1,pos))
                for i in range(n-pos-1): 
                    # repeat the prenecklace to the end
                    #debprint('Inner for loop ---------------------------')
                    
                    touch.setLastEdge(pos+i+1, touch.path[i])
                    it += 1
                    if it%itstatus == 0:
                        PrintStatus(touch,pos)
                    
            
                    #debprint("Path {}".format(touch.getPath()))
                    isNecklace = (i == n-pos-2) and (pos+1 in divs)
                    if isNecklace and touch.isHamiltonianCycle():
                        PrintIt(touch)
                        lastPrunePos = pos+i
                        continue
                    elif pruneTruth(touch):
                        lastPrunePos = pos+i+1
                        if el+1 == len(touch.method.edges):
                            lastPrunePos = pos+1
                        break
                    else:
                        lastPrunePos = -1
                    
                    
                """
                # condition for this to be a necklace
                if pos+1 in divs:
                    yield list(t)
                """
                #debprint("Breaking main for loop")
                break
    #debprint("While loop broken")
    #debprint("Path {}".format(touch.path))



def PrintStatus(touch,pos):
    global starttime
    print(" ----- Status ----------------------------------")
    if touch.method.stage < 7:
        print("Current node: " + " ".join([repr(x) for x in touch.getPath()]))
    print("Elapsed time: {}".format(time.time()-starttime))
    print("Iteration {}".format(it))
    print("Number of solutions: {}".format(len(solutions)))
    print("Shortest superperm found: {}".format(minCost))
    print("Current cost: {}".format(touch.getCost()))
    print("Current projected cost: {}".format(touch.projectedCost()))
    print("Nodes visited: {}".format(len(touch)))
    print("Pruned false: {}".format(prunedF))
    print("Pruned cost: {}".format(prunedC))

def PrintIt(touch):
    global minCost, t, starttime
    if touch.isHamiltonianCycle():
        soln = touch.optimumPath()
        cost = soln.getCost()
        if cost < minCost:
            minCost = cost
        print('Success - at {} iterations and {} s'.format(it, time.time()-starttime))
        print('Superpermutation length {}'.format(soln.getCost()))
        print(soln)
        print(soln.getPath())
        solutions.append(soln)
        solnIters.append(it)
        
        
        if not soln.isSuperperm():
            print('Problem - not a superperm')


"""me = Method(6)
ex = (int(i)-1 for i in '12345612345162345126345123645132645136245136425136452136451234651234156234152634152364152346152341652341256341253641253461253416253412653412356412354612354162354126354123654132654312645316243516243156243165243162543162453164253146253142653142563142536142531645231465231456231452631452361452316453216453126435126431526431256432156423154623154263154236154231654231564213564215362415362145362154362153462135462134562134652134625134621536421563421653421635421634521634251634215643251643256143256413256431265432165432615342613542613452613425613426513426153246513246531246351246315246312546321546325146325416325461325463124563214563241563245163245613245631246532146532416532461532641532614532615432651436251436521435621435261435216435214635214365124361524361254361245361243561243651423561423516423514623514263514236514326541362541365241356241352641352461352416352413654213654123')
exT = me.parse(ex)
"""


print('Starting')

#necklaceSearch(touch)
#cProfile.run('necklaceSearch(touch)','profile')      #initial call
print("------------------------------------------------------")
print("Found {} superperms in {} iterations".format(len(solutions),it))
print("Shortest superperm found: {}".format(minCost))    
print("Pruned false: {}".format(prunedF))
print("Pruned cost: {}".format(prunedC))
print("")
print("Final node: " + "".join([repr(x) for x in touch.getPath()]))
print(touch.getPath())

