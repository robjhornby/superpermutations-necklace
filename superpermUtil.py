# -*- coding: utf-8 -*-

##The check for truth doesn't work for methods where the lead end edges
##affect more than one row

from xml.dom.minidom import parse
#import urllib2
import time
import copy
from itertools import *
from math import factorial

def permLabelsGen(rowStart, rowEnd):
	return lambda row : tuple(dict(zip(rowStart, rowEnd))[el] for el in row)

def permPosGen(rowStart, rowEnd):
	perm = []
	for el in rowEnd:
		for i in range(0, len(rowStart)):
			if el == rowStart[i]:
				perm.append(i)
	return lambda row : tuple(row[i] for i in perm)

def genEdges(N):
    edges = []
    strings = []
    identity = tuple(range(N))
    maxEdgeCost = 3#N
    maxEdges = 3
    for ii in range(1,maxEdgeCost+1):
        for p in permutations(range(0,ii)):
            p = p[::-1]
            # If the start of the perm doesn't match an existing string
            if all([p[0:len(x)] != x for x in strings]):
                strings.append(p)
                edges.append(permPosGen(identity,tuple(range(ii,N))+p))
                if len(edges) == maxEdges:
                    break
        if len(edges) == maxEdges:
            break
    comb = zip(edges,strings,tuple(len(x) for x in strings))
    comb = zip(*sorted(comb, key = lambda el : (-len(el[1]),)+el[1], reverse = True ))
    return comb


def superpermChecklist(stage,candidate):
    perms = tuple(permutations(range(stage)))
    checklist = dict(zip(perms,tuple(0 for p in perms)))
    for pos in range(len(candidate)-stage+1):
        string = candidate[pos:pos+stage]
        if string in checklist.keys():
            checklist[string] += 1
    return checklist
            
def isSuperperm(stage,candidate):
    """Checks if a superperm candidate does contain all permutations at least once."""
    checklist = superpermChecklist(stage,candidate)
    return all([x >= 1 for x in checklist.values()])

def isStrictSuperperm(stage,candidate):
    """Checks if a superperm candidate does contain all permutations.
    Strict - it must contain all permutations exactly once."""
    perms = tuple(permutations(range(stage)))
    checklist = dict(zip(perms,tuple(0 for p in perms)))
    for pos in range(len(candidate)-stage+1):
        string = candidate[pos:pos+stage]
        if string in checklist.keys():
            checklist[string] += 1
    return all([x == 1 for x in checklist.values()])

def rotate(l, n):
    return l[n:] + l[:n]

class Method:
    #notation: list of strings of place notation for each row
    #lePlaceNotation: dictionary of the form {key: notation array}
    def __init__(self, stage):


        #int
        self.stage = stage
        self.identity = tuple(range(stage))
        (a,b,c) = genEdges(stage)
        self.edges = a
        self.edgeStrings = b
        self.edgecost = c
        
        self.numNodes = factorial(stage)
        
    def nextNode(self, perm, edgei):
        return self.edges[edgei](perm)

    def shortestEdge(self, p1, p2):
        l=self.stage
        for ii in range(self.stage):
            if list(p1[ii:])==list(p2[:-ii]):
                edge = permPosGen(p1,p2)
                canon = edge(self.identity)
                edgeString = list(canon[-ii:])
                edgecost = len(edgeString)
                if edgeString in self.edgeStrings:
                    edgei = self.edgeStrings.index(edgeString)
                else:
                    edgei = -1
                return (edgei,edge,edgeString,edgecost)
                
        return -1

    def parse(self, superperm):
        """superperm - tuple of self.stage distinct objects"""
        superperm = tuple(superperm)
        stage = self.stage
        
        perm = superperm[0:stage]
        edgeStrings = []
        path = []
        lasti = 0
        
        specialedge = False
        for ii in range(1,len(superperm)-stage+1):
            cand = superperm[ii:ii+stage]
            if len(set(cand)) == len(cand):
                #is a perm
                
                edgeCost = ii-lasti
                edge = permPosGen(perm,cand)
                canon = edge(self.identity)
                edgeString = canon[-edgeCost:]
                edgeStrings.append(edgeString)
                
                
                if edgeString in self.edgeStrings:
                    path.append(self.edgeStrings.index(edgeString))
                else:
                    print(perm)
                    print(cand)
                    print(canon)
                    print(edgeString)
                    print("cost {}".format(edgeCost))
                    print("Edge type not indexed")
                    input()
                    edgei = -1
                    specialedge = True
                perm = cand
                lasti = ii
                
        if not specialedge:
            return TouchStore(self,path)


class TouchStore:
    def __init__(self, method, initial):
        self.method = method
        self.path = list(initial)
        self.node = method.identity
        self.visited = [self.node]
        self.firstFalsePos = -1
        self.truth = False
        self.pathcost = [method.stage]
        self.length = len(initial)
        
        for edgei in initial:
            self.node = self.method.nextNode(self.node, edgei)
            self.visited.append(self.node)
            self.pathcost.append(self.method.edgecost[edgei])
            

    def projectedCost(self, numEdges):
        """The minimum possible cost of visiting all nodes by repeating the
        current first numEdges edges"""
        return self.pathcost[0]+sum(islice(cycle(self.pathcost[1:numEdges+1]),self.method.numNodes-1))

    def __len__(self):
        return self.length
    
    def __repr__(self):
        return ''.join([str(x) for x in self.getSuperperm()])

    def setLastEdge(self, position, edgei):
        self.length = position+1
        self.path[position] = edgei

        self.node = self.method.nextNode(self.visited[position], edgei)
        
        self.visited[position+1] = self.node
        self.pathcost[position+1] = self.method.edgecost[edgei]
        
        self.firstFalsePos = -1
        self.truth = True
        if self.length == self.method.numNodes:
            return 0
        for fs in self.visited[:position+1]:
            if fs == self.node:
                self.truth = False
                self.firstFalsePos = position
                break

    def getPerm(self):
        return tuple(self.node)
    def getIdentity(self):
        return tuple(self.method.identity)
    def getLhsTuple(self):
        return tuple(self.visited)
    def getSuperperm(self):
        out = list(self.visited[0])
        for ii in range(0,self.length):
            ind = self.method.stage-self.method.edgecost[self.path[ii]]
            out.extend(self.visited[ii+1][ind:])
        return tuple(out)
    def getCost(self):
        return sum(self.pathcost[0:self.length+1])
    def getPathcost(self):
        return tuple(self.pathcost[0:self.length+1])
    def getPath(self):
        return tuple(self.path[0:self.length])
    def isTrue(self):
        if self.firstFalsePos == -1:
            return True
        return False

