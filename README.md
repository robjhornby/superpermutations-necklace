# Superpermutations via necklace search
[Intro to superpermutations](https://www.youtube.com/watch?v=OZzIvl1tbPo)

This algorithm can find superpermutations of the following lengths in the following number of iterations of the algorithm:

| Number of objects | Length | Iterations | Time    |
| ----------------- | ------ | ---------- | --------|
| 3                 | 9      | 7          | <<1 s   |
| 4                 | 33     | 26         | <<1 s   |
| 5                 | 153    | 125        | <<1 s   |
| 6                 | 873    | 738        | 0.07 s  |
| 7                 | 5913   | 5122       | 2.8 s   |
| 8                 | 46233  | 40862      | 205 s   |

The number of nodes evaluated per second is increasing as the number of objects increases - need to find the source. May be to do with checking that the path doesn't visit a node twice which could be made quicker.


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

This is a [necklace](http://mathworld.wolfram.com/Necklace.html), and so I used the necklace generating algorithm described by [Cattell et al](https://www.sciencedirect.com/science/article/pii/S0196677400911088) (can be found on google) to avoid searching for every rotated repetition of the same cycle through the superpermutation graph. This algorithm generates the necklace strings in lexicographic order, meaning it tries the lowest weight edges first.

Update - after reading some more about superpermutations, it seems like they can also be flipped which makes this representation a bracelet.

## Pruning
The search can be pruned at any iteration by checking whether the current path visits any node twice. Each time the search is pruned, the string which has been pruned will never occur in any part of the future search at any position along the path thanks to the necklace generating algorithm, by construction.

The search can also be pruned by keeping track of the current minimum superpermutation length and pruning any branch which couldn't possibly find a solution with a length less than that. Currently I just calculate:

Length of current incomplete superpermutation string + the number of nodes left to visit < minimum superpermutation length

This assumes every remaining node can be visited with a weight 1 edge, which could be improved upon by using the necklace's repeating structure - the shortest possible path to complete the path must be at least as long as the path obtained by following the edges from the start of the current path again at the end of the current path and repeating them. i.e. if you are currently at this string of edges: 00001, and you need 15 edges (say), the best you can do must be worse than 000010000100001 because all paths containing 00000 have already been ruled out by this point in the search. 


## To do:
- [x] Switch to iterative algorithm to avoid recursion depth limitations
- [x] Try 7 objects
- [ ] Check new pruning method is doing what I expect
- [ ] Profile code
