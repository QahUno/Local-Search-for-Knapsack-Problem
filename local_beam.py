from operator import itemgetter
import numpy
import test_case as tc
import random

MAX_STEPS = 500
BW = 5

maxWeight = 0 
classes = 0
weights = []
values = []
classItems=[]
n = 0

def generateRamdomState():
    while True:
        state = random.choices([0,1], weights = [10,1],  k=n)
        evaluation = evaluate(state)
        if evaluation[0] != -1 and checkClass(state):
            state.extend(evaluation)
            return state
    
    
# check if sol contains at least 1 class
def checkClass(sol):
    classList = {0}
    for a in range(classes):
        classList.add(a + 1)
    solList = {0}
    for i in range(n):
        if sol[i] == 1:
            solList.add(classItems[i])
    return classList == solList

# function to evaluate the coresponding values and weight of a solution x

def evaluate(x):
    a = x[0:n]
    b = values[:]
    c = weights[:]
    
    totalvalues = numpy.dot(a,b)     # compute the values of the knapsack selection
    totalWeight = numpy.dot(a,c)    # compute the weight values of the knapsack selection
    
    if totalWeight > maxWeight:
        return [-1, -1]

    return [totalvalues, totalWeight]   # returns a list of both total values and total weight
          
# returns all neighbors of a given solution x
def generateNbhoods(x):     
    nbhoods = []
    for i in range(0, n):
        nbhood = x[0:n]
        nbhood[i] ^= 1

        evaluation = evaluate(nbhood)
        if evaluation[0] != -1 and evaluation[0] > x[n] and checkClass(nbhood):
            nbhood.extend(evaluation)
            nbhoods.append(nbhood)

    return nbhoods

def local_beam_search():
    # intilialization 
    expanded = [generateRamdomState() for i in range(BW)]

    # local beam searching
    for i in range(MAX_STEPS):
        allNbhoods = [] # nbhood of all solutions in expanded list
        for state in expanded:
            nbhoods = generateNbhoods(state)
            allNbhoods.extend(nbhoods)

        allNbhoods = sorted(allNbhoods, key=itemgetter(n), reverse=True) # choose best BW neighbors
        best_states = allNbhoods[0:BW]
        
        if len(best_states) == 0:
            return (expanded[0][-1], expanded[0][-2], expanded[0][0:n])
        
        expanded = best_states.copy()

    return (expanded[0][-1], expanded[0][-2], expanded[0][0:n])

if __name__=="__main__":
    for i in range(5):
        fin = 'input/INPUT_'+str(i)+'.txt'
        fout= 'output/local_beam_search/OUTPUT_'+str(i)+'.txt'

        # fin = 'large_input/INPUT_'+str(i)+'.txt'
        # fout= 'large_output/local_beam_search/OUTPUT_'+str(i)+'.txt'

        data = tc.use_testcase(fin)
        maxWeight = data[0]
        classes = data[1]
        weights = data[2]
        values = data[3]
        classItems = data[4]
        n = len(values)
        tc.time_operation(local_beam_search, fin, n, classes, maxWeight, fout)