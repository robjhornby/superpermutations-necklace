#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 00:01:50 2019

@author: rob
"""

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
from copy import deepcopy
import time

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
        self.num_objects = N
        self.identity = tuple(range(0,N))
        self.vertices = {}
        self.num_vertices = 0
        
        self.edges = self.genEdges(N, N-1) # list of Edge objects
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
        self.edgeWeights = []
        
        self.graph = graph
        self.startNode = graph.identity
        self.node = graph.identity
        
        self.isHamiltonian = False
        
        self.bestWeight = 10000000
        
        for ii in range(graph.num_edges):
            if not self.setLast(ii,0):
                break
        
    def copy_path(self):
        p = Path(self.graph,self.graph.num_vertices)
        for ii,edge in enumerate(self.edgeList):
            p.setLast(ii,edge)
        return p
    
    def pruneCondition(self):
        if self.bestWeight < self.projected_weight():
            return True
        
        return False
    
    def projected_weight(self):
        """The minimum possible cost of visiting all nodes by repeating the
        current edges"""
        if len(self) == 0:
            return self.graph.num_vertices
        
        mul = (self.graph.num_vertices-1) // len(self)
        rem = (self.graph.num_vertices-1) % len(self)
        return self.graph.num_objects + sum(self.edgeWeights)*mul + sum(self.edgeWeights[:rem])
    
    #@profile
    def setLast(self, ind, edgeI):
        #Traverse path back to ind, removing edges
        self.backtrack_to(ind)
        
        nextNode = self.get_edge(edgeI).perm(self.node)
        self.edgeTrial.append(edgeI)
        
        self.isHamiltonian = False
        if nextNode == self.startNode:
            if len(self) == self.graph.num_vertices-1:
                weight = self.get_weight()
                if self.bestWeight >= weight:
                    self.bestWeight = weight
                    self.isHamiltonian = True
                    
                    self.visited.add(nextNode)
                    self.visitList.append(nextNode)
                    
                    self.edgeList.append(edgeI)
                    self.edgeWeights.append(self.graph.edges[edgeI].weight)
                    self.update_node()
                else:
                    return False
                
            else:
                return False
        
        
        if nextNode not in self.visited and nextNode != self.startNode and not self.pruneCondition():
            self.visited.add(nextNode)
            self.visitList.append(nextNode)
            
            self.edgeList.append(edgeI)
            self.edgeWeights.append(self.graph.edges[edgeI].weight)
            self.update_node()
            return True
        
        return False
    
    def backtrack_to(self,ind):
        if len(self)<len(self.edgeTrial):
            self.edgeTrial.pop()
        for ii in range(len(self)-1, ind-1,-1):
            self.visited.remove(self.visitList.pop())
            self.edgeList.pop()
            self.edgeTrial.pop()
            self.edgeWeights.pop()
        
        self.update_node()
    
    def get_edge(self,ii):
        return self.graph.edges[ii]
    
    def get_weight(self):
        return self.graph.num_objects + sum(self.edgeWeights)
    
    def __len__(self):
        return len(self.edgeList)
    
    def __repr__(self):
        return ' '.join([str(x) for x in self.edgeList])
    
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
    

class NecklaceSearcher:
    def __init__(self, graph):
        self.graph = graph
        self.dictSize = graph.num_edges
        self.nLength = graph.num_vertices # = N!
        self.divs = divisors(self.nLength)
        self.its = 0
        self.results = []
        self.path = Path(self.graph,self.nLength)
        self.starttime = 0
        self.dorun = True
        
    #@profile
    def run(self):
        self.starttime = time.time()
        while self.path.edgeList[0] != self.dictSize-1 and self.dorun:
            for pos in range(len(self.path.edgeTrial)-1,0,-1):
                el = self.path.edgeTrial[pos]
                self.incCounter()
                if el < self.dictSize-1:
                    if not self.path.setLast(pos, el+1):
                        if pos+1 in self.divs and self.path.is_hamilton():
                            self.save_result()
                            yield self.results[-1].copy_path()
                        break
                    
                    for i in range(self.nLength-1 - pos):
                        self.incCounter()
                        if not self.path.setLast(pos+1 +i, self.path.edgeList[i]):
                            if pos+1 in self.divs and self.path.is_hamilton():
                                self.save_result()
                                yield self.results[-1].copy_path()
                            break

                    break
                
    def incCounter(self):
        self.its += 1
        if self.its % 500000 == 0:
            print(repr(self))
            if self.its>50000:
                pass
                #self.dorun = False
    def save_result(self):
        res = self.path.copy_path()
        res.backtrack_to(self.nLength-1)
        self.results.append(res)
        print("""Result found at iteration {}, weight {}:
            {}""".format(self.its,res.get_weight(),self))
    def __repr__(self):
        return """Iteration {}, solutions found {}, elapsed time {} s, rate {} kNode/s
    Current weight {}, current projected weight {}, best weight {}, 
    Current path:
    {}""".format(self.its,len(self.results),time.time()-self.starttime,(self.its/1000/(time.time()-self.starttime)),self.path.get_weight(),self.path.projected_weight(),self.path.bestWeight,self.path)

def divisors(n):
    div = set()
    for i in range(1, (int)(n/2+1)):
        if n % i == 0:
            div.add(i)

    div.add(n)
    return div


if __name__ == '__main__':

    g = PermGraph(6)
    
    for v in g:
        for e in g.get_edges():
            vid = v.get_id()
            eid = e.get_id()
            neighbour = v.adjacent[e.id]
            weight = e.get_weight()
            #print('( %s , %s, %s, %d)'  % ( repr(vid), repr(eid), repr(neighbour),weight))
    successes = []
    ns = NecklaceSearcher(g)
    for neck in ns.run():
        successes.append(neck)
