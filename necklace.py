##Generates all necklaces in two beads
##using the algorithm which doesn't involve prenecklaces
##and checks them for truth


import math

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

def nextCyclicOld(touch, calltypes):
    divs = divisors(len(touch))
    t = list(touch)
    while t != len(t)*[0]:
        for pos, call in enumerate(t): # for each position in the string
            if call > 0: # If this isn't the k'th character
                t[pos] = call - 1 # set t to the next character
                for i in range(0, pos): # for every position from pos to the end
                    t[pos-i-1] = t[len(touch)-i-1] # copy characters from earlier to pos
                    #Check graph at every step here
                    
                # condition for this to be a necklace
                if len(t)-pos in divs:
                    yield list(t)
                
                break

def nextCyclic(size, n):
    divs = divisors(n)
    t = [0]*n
    while t != [size]*n:
        for pos, el in reversed(tuple(enumerate(t))): # for each position in the string
            if el < size: # If this isn't the k'th character
                t[pos] = el + 1 # set t to the next character
                
                for i in range(n-pos-1): # for every position from the end to pos
                    t[pos+i+1] = t[i] # copy characters from earlier to pos
                    #Check graph at every step here
                    
                # condition for this to be a necklace
                if pos+1 in divs:
                    yield list(t)
                
                break


def main():
    k = 1
    n = 14
    callsOld = [k]*n
    counter = 1
    ac = [(0,)*n]
    for calls in nextCyclic(k,n):
        callsOld = next(nextCyclicOld(callsOld,k))
        ac.append(tuple(calls))
        counter = counter+1
        """print(calls)
        print(tuple(reversed(tuple(k-x for x in list(callsOld)))))
        print()"""
    print(counter)
if __name__ == '__main__':
    print('main')
    main()
