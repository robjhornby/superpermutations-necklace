## Generates all necklaces iteratively

import math
import random

class necklace:
    def __init__(self,k,n):
        pass
    
def divisors(n):
    div = set()
    for i in range(1, (int)(n/2+1)):
        if n % i == 0:
            div.add(i)

    div.add(n)
    return div

def prune(path,pos):
    if random.uniform(0,1)<0.1:
        print('last pruned')
        return True
    return False

def necklaceSearch(dictSize, nLength):
    divs = divisors(nLength)
    path = [0]*nLength
    while path != [dictSize]*nLength:
        for pos, el in reversed(tuple(enumerate(path))):
            if el < dictSize:
                path[pos] = el + 1
                #show(path,pos)
                if prune(path,pos):
                    continue
                
                for i in range(nLength-pos-1): 
                    path[pos+i+1] = path[i] # repeat the prenecklace to the end
                    
                    if prune(path,pos+i+1):
                        return
                    
                # condition for this to be a necklace
                if pos+1 in divs:
                    show(path,pos)
                    return list(path)
                
                break

def show(path,pos):
    print(''.join([str(x) for x in path]))
    print(' '*(pos)+'|')
    input()

def main():
    k = 1
    n = 18
    callsOld = [k]*n
    counter = 1
    ac = [(0,)*n]
    for calls in necklaceSearch(k,n):
        ac.append(tuple(calls))
        counter = counter+1
        """print(calls)
        print(tuple(reversed(tuple(k-x for x in list(callsOld)))))
        print()"""
    print(counter)

    
if __name__ == '__main__':
    print('main')
    main()
