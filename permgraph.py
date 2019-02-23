#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 13:41:30 2019

@author: rob
"""
import time
import copy
from itertools import *
from math import factorial
import numpy as np
from superpermUtil import *

permGraph = dict()

# permGraph
# 1234 -> 2341 3412 etc.
# weights
# 1 2 etc same index as permGraph?



class Edge:
    # Fixed number of edges will apply to every vertex
    def __init__(self, canonNode, perm, weight):
        self.id = canonNode
        self.perm = perm
        self.weight = weight
        
    def get_perm(self):
        return self.perm
    def get_weight(self):
        return self.weight
    def get_id(self):
        return self.id
    def __str__(self):
        return str(self.id)
    def __repr__(self):
        return repr(self.id)

class Vertex:
    def __init__(self, node, edges):
        self.id = node
        self.adjacent = {}
        for edge in edges:
            self.adjacent[edge.id] = edge.perm(self.id)

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x for x in self.adjacent])

    def get_connections(self):
        return self.adjacent.values()

    def get_id(self):
        return self.id

class PermGraph:
    def __init__(self, N):
        self.identity = tuple(range(0,N))
        self.vertices = {}
        self.num_vertices = 0
        
        self.edges = self.genEdges(N, 3) # list of Edge objects
        self.num_edges = len(self.edges)
        
        for p in permutations(range(0,N)):
            self.add_vertex(p)

    def __iter__(self):
        return iter(self.vertices.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node,self.edges)
        self.vertices[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vertices:
            return self.vertices[n]
        else:
            return None

    def get_vertices(self):
        return self.vertices.keys()
    
    def get_edges(self):
        return self.edges
    
    def genEdges(self, N, maxEdgeWeight):
        strings = []
        edges = []
        
        for ii in range(1,maxEdgeWeight+1):
            for p in permutations(range(0,ii)):
                p = p[::-1]
                # If the start of the perm doesn't match an existing string
                if all([p[0:len(x)] != x for x in strings]):
                    strings.append(p)
                    edgeperm = permPosGen(self.identity,tuple(range(ii,N))+p)
                    canonNode = edgeperm(self.identity)
                    edges.append(Edge(canonNode,edgeperm,len(p)))
        
        #edges = sorted(edges, key = lambda el : el[1], reverse = True )
        return edges

class Path:
    def __init__(self, graph, pathLen):
        self.visited = set()
        self.visitList = []
        
        self.edgeList = []
        self.edgeTrial = [] # contains the last failed edge if there is one
        
        self.graph = graph
        self.startNode = graph.identity
        self.node = graph.identity
        
        self.isHamiltonian = False
        
        for ii in range(graph.num_edges):
            if not self.setLast(ii,0):
                break
        
    def pruneCondition(self):
        pass
    
    def setLast(self, ind, edgeI):
        curInd = len(self)-1
        if len(self)<len(self.edgeTrial):
            self.edgeTrial.pop()
        
        #Traverse path back to ind, removing edges
        for ii in range(curInd, ind-1,-1):
            self.visited.remove(self.visitList.pop())
            self.edgeList.pop()
            self.edgeTrial.pop()
        
        self.update_node()
        nextNode = self.get_edge(edgeI).perm(self.node)
        self.edgeTrial.append(edgeI)
        
        self.isHamiltonian = False
        if nextNode == self.startNode:
            if len(self) == self.graph.num_vertices-1:
                self.isHamiltonian = True
                self.visited.add(nextNode)
                self.visitList.append(nextNode)
                
                self.edgeList.append(edgeI)
                self.update_node()
            else:
                return False
        
        
        if nextNode not in self.visited and nextNode != self.startNode:
            self.visited.add(nextNode)
            self.visitList.append(nextNode)
            
            self.edgeList.append(edgeI)
            self.update_node()
            return True
        
        return False
    def get_edge(self,ii):
        return self.graph.edges[ii]
    
    def __len__(self):
        return len(self.edgeList)
    
    def __repr__(self):
        return str(self.edgeList)
    
    def update_node(self):
        if len(self) == 0:
            self.node = self.startNode
        else:
            self.node = self.visitList[-1]
            
        return self.node
    
    def is_hamilton(self):
        return self.isHamiltonian
    
    def get_superperm(self):
        out = list(self.startNode)
        for ii in range(0,len(self)):
            edge = self.get_edge(ii)
            ind = edge.get_weight()
            out.extend(self.visitList[ii][ind:])
        return tuple(out)
    
        
def necklaceSearch(graph):
    dictSize = graph.num_edges
    nLength = graph.num_vertices # = N!
    divs = divisors(nLength)
    path = Path(graph,nLength)
    
    while path.edgeList[0] != dictSize-1:
        #Begin from the end of the current path
#        print('While')
#        print(path)
#        print(path.edgeTrial)
#        print([x for x in reversed(tuple(enumerate(path.edgeTrial)))])
#        input()
        for pos, el in reversed(tuple(enumerate(path.edgeTrial))):
#            print('For pos el')
#            print(path)
##            print(path.edgeTrial)
##            print(pos,el,len(path))
#            input()
            if el < dictSize-1:
                
                if not path.setLast(pos, el+1):
                    if pos+1 in divs and path.is_hamilton():
                        yield path
                    break
                
                for i in range(nLength-1 - pos): 
                    # repeat the prenecklace to the end
#                    print('Repeat to end')
#                    print(path)
#                    print(path.edgeTrial)
#                    print(pos,el,len(path))
#                    input()
                    if not path.setLast(pos+1 +i, path.edgeList[i]):
                        if pos+1 in divs and path.is_hamilton():
                            yield path
                        break
                    
                # condition for this to be a necklace
#                if pos+1 in divs and path.isHamiltonian:
#                    print(path)
#                    yield path
                
                break
            
            

if __name__ == '__main__':

    g = PermGraph(4)    
    
    for v in g:
        for e in g.get_edges():
            vid = v.get_id()
            eid = e.get_id()
            neighbour = v.adjacent[e.id]
            weight = e.get_weight()
            #print('( %s , %s, %s, %d)'  % ( repr(vid), repr(eid), repr(neighbour),weight))
    successes = []
    for neck in necklaceSearch(g):
        print(neck)
        print(len(neck))
        successes.append(neck)
        print(len(successes))
