from operator import itemgetter
import numpy
import test_case as tc
import random

maxWeight = 0 
classes = 0
weights = [] 
values = [] 
classItems=[]
bw = 5

def get_unique_list(seq):
    seen = []
    return [x for x in seq if x not in seen and not seen.append(x)]

# check if sol contains at least 1 class
def checkClass(sol, classes, n, classItems):
    classList = {0}
    for a in range(classes):
        classList.add(a + 1)
    solList = {0}
    for i in range(n):
        if sol[i] == 1:
            solList.add(classItems[i])
    return classList == solList

# function to evaluate the coresponding values and weight of a solution x
def evaluate(x, values, weights, maxWeight, n):        
    a = x[0:n]
    b = values[:]
    c = weights[:]
    
    totalvalues = numpy.dot(a,b)     # compute the values of the knapsack selection
    totalWeight = numpy.dot(a,c)    # compute the weight values of the knapsack selection
    
    if totalWeight > maxWeight:
        return [-1, -1]

    return [totalvalues, totalWeight]   # return a list of both total values and total weight
          
# return all neighbors of a given solution x
def neighborhood(x, n):     
    nbhood = []     
    for i in range(0, n):
        nbhood.append(x[:])
        if nbhood[i][i] == 1:
            nbhood[i][i] = 0
        else:
            nbhood[i][i] = 1
      
    return nbhood


def initial_solution(n, classes, classItems, weights):    
    classIndex = [None] * (classes+1)
    for i in range(1, classes+1):
        classIndex[i] = []
    for i in range(1, classes+1):
        for j in range(len(classItems)):
            if (classItems[j] == i):
                classIndex[i].append(j)
    minIndex = []
    for i in range(1, classes+1):
        temp = []
        for s in classIndex[i]:
            temp.append(weights[s])
        # find index of min in temp
        minvaluesIndex = temp.index(min(temp))
        minIndex.append(classIndex[i][minvaluesIndex])
    res = [0] * n # ???
    for i in minIndex:
        res[i] = 1
    return res
   
def local_beam_search():
    # intilialization 
    n = len(values)
    x_start = initial_solution(n, classes, classItems, weights)
    x_start.extend(evaluate(x_start, values, weights, maxWeight, n))
    expanded = [] # list of solutions waiting for being expanded to its neighborhood
    expanded.append(x_start)
    done = 0

    # local beam searching
    while done == 0:
        nbhood = [] # nbhood of all solutions in expanded list
        for s in expanded:
            nbhood += neighborhood(s[0:n], n)
        for t in nbhood:
            t.extend(evaluate(t, values, weights, maxWeight, n))
        for t in nbhood:
            if t[n + 1] > maxWeight or not checkClass(t, classes, n, classItems): # validate weight and check class
                nbhood.remove(t)
        nbhood = sorted(nbhood, key=itemgetter(n), reverse=True) # choose bw of best neighbors
        nbhood = nbhood[0:bw]
        if nbhood[0][n] <= expanded[0][n]: # stop condition
            # display  
            if len(expanded) == 0:
                return []
            return (expanded[0][-1], expanded[0][-2], expanded[0][:-2])
        else:
            expanded = nbhood[:]

if __name__=="__main__":
    for i in range(5):
        fin = 'input/INPUT_'+str(i)+'.txt'
        fout= 'output/local_beam_search/OUTPUT_'+str(i)+'.txt'

        # fin = 'large_input/INPUT_'+str(i)+'.txt'
        # fout= 'large_output/local_beam_search/OUTPUT_'+str(i)+'.txt'

        data = tc.use_testcase(fin)
        # data = tc.use_testcase('large_input/INPUT_'+str(i)+'.txt')
        maxWeight = data[0]
        classes = data[1]
        weights = data[2]
        values = data[3]
        classItems = data[4]
        tc.time_operation(local_beam_search, fin, len(weights), classes, maxWeight, fout)

    # print(local_beam_search())
