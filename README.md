# Superpermutations via necklace search
[Intro to superpermutations](https://www.youtube.com/watch?v=OZzIvl1tbPo)

This algorithm can find superpermutations of the following lengths in the following number of iterations of the algorithm:

| Number of objects | Length | Iterations |
| ----------------- | ------ | ---------- |
| 3                 | 9      | 7          |
| 4                 | 33     | 26         |
| 5                 | 153    | 125        |
| 6                 | 873    | 738        |

I've used a recursive algorithm which hits Python's maximum recursion depth before it can find a solution for 7 objects. The next step will be to implement this approach in an iterative algorithm.

## Approach
Treat searching for superpermutations as a graph search, as is being done by others. Every node in the graph has the same edges coming into and out of it if you treat them as transformations of the current node rather than ad-hoc links between all of the permutations. Each edge is weighted by the number of additional objects you need to add to the end of the current string to reach the target permutation. e.g. 012 -> 120 has weight 1 because a single character, '0' has been added. 012->210 has weight 2 because '10' is two characters. etc.

After generating all possible edges for a single node in the given graph (which only depends on the number of objects), order these edges from least to most weight, and assign an arbitrary order to edges which share a weight. Label these edges A, B, C, etc. so that finding a superpermutation is equivalent to finding a string consisting of A,B,C... such that the corresponding path through the graph visits every node.

Now make some assumptions which I don't know are true so that this solution can work:
1. Each node may not be visited twice, i.e. each permutation appears exactly once in the shortest superpermutation
2. The solution must be a hamiltonian cycle with a single edge removed

Given that every node is equivalent you could start the path through the graph at any node, following the same Hamiltonian cycle, and still visit every node. Or equivalently, you can take any number of edges from the start of the cycle and stick them on the end of the cycle, start that thing from the same node and still visit every node. 

This is equivalent to saying that the string of edges is cyclically invariant, i.e. the following strings are equivalent (if they correspond to a cycle in a graph):

ABACDA

BACDAA

ACDAAB

CDAABA, etc.

This is a [necklace](https://en.wikipedia.org/wiki/Necklace_(combinatorics)), and so I used the necklace generating algorithm described by [Cattell et al](https://www.sciencedirect.com/science/article/pii/S0196677400911088) (can be found on google) to avoid searching for every rotated repetition of the same cycle through the superpermutation graph. This algorithm generates the necklace strings in lexicographic order, meaning it tries the lowest weight edges first.

## Pruning
The search can be pruned at any iteration by checking whether the current path visits any node twice. Each time the search is pruned, the string which has been pruned will never occur in any part of the future search at any position along the path thanks to the necklace generating algorithm, by construction.

The search can also be pruned by keeping track of the current minimum superpermutation length and pruning any branch which couldn't possibly find a solution with a length less than that. Currently I just calculate:

Length of current incomplete superpermutation string + the number of nodes left to visit < minimum superpermutation length

This assumes every remaining node can be visited with a weight 1 edge, which could be improved upon.


## To do:
* Switch to iterative algorithm to avoid recursion depth limitations
* Improve pruning conditions to prune branches earlier
* Try 7 objects
