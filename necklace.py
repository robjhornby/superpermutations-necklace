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

def prune(t,pos):
    if random.uniform(0,1)<0.1:
        print('prune')
        return True
    return False

def nextCyclic(size, n):
    divs = divisors(n)
    t = [0]*n
    while t != [size]*n:
        for pos, el in reversed(tuple(enumerate(t))):
            if el < size:
                t[pos] = el + 1
                show(t,pos)
                if prune(t,pos):
                    continue
                
                for i in range(n-pos-1): 
                    t[pos+i+1] = t[i] # repeat the prenecklace to the end
                    show(t,pos+i+1)
                    if prune(t,pos+i+1):
                        break
                    
                # condition for this to be a necklace
                if pos+1 in divs:
                    yield list(t)
                
                break
def show(t,pos):
    print(''.join([str(x) for x in t]))
    print(' '*(pos)+'|')
    input()

def main():
    k = 1
    n = 14
    callsOld = [k]*n
    counter = 1
    ac = [(0,)*n]
    for calls in nextCyclic(k,n):
        ac.append(tuple(calls))
        counter = counter+1
        """print(calls)
        print(tuple(reversed(tuple(k-x for x in list(callsOld)))))
        print()"""
    print(counter)

    
if __name__ == '__main__':
    print('main')
    main()
