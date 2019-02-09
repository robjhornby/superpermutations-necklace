Generating superpermutations by a search of necklaces in the available edges
This assumes some things which I don't know are true:
1. Each node may not be visited twice, i.e. each permutation appears exactly once in the shortest superpermutation
2. The solution must be a hamiltonian cycle, such that we can search for just one rotation of that cycle (the canonical necklace)

Others have also looked for hamiltonian cycles rather than hamiltonian paths, so maybe there is a good reason for it.
It should be possible to modify the string generation to search every string rather than just necklaces, while still pruning a lot of options


To do:
Enumerate permutations to form a hash set for checking whether a perm has been visited yet
Calculate all possible edges for a given alphabet size (N) and rank them in terms of fewest to most additional characters needed
Adapt the existing code to check whether a permutation has been visited yet and prune the search if it has 
