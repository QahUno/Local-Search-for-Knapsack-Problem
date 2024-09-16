from itertools import combinations
import test_case as tc
from datetime import datetime

W =0
m = 0
wList = []
vList = []
cList = []

def bruteForceKnapsack():
    iList = []
    for i in range(0,len(wList)):
        iList.append(i)
    for i in range(len(wList)):
        if int(wList[i])> W:
            iList.remove(i)
    

    subsets = []


    for i in range(len(iList)+1):
        subsets += [list(j) for j in combinations(iList,i)]

    legalSubset = []

    run = 0

    for subset in subsets:
        run += 1
        totalW = 0
        totalC = []
        for i in subset:
            totalW += int(wList[i])
            if (cList[i] not in totalC):
                totalC.append(cList[i])
        if totalW <= W and len(totalC) == m:
            legalSubset.append(subset)

    # print(legalSubset)
    maxVIndex = -1
    maxV = -1
    for subset in legalSubset:
        totalV = 0
        for i in subset:
            totalV += int(vList[i])
        if totalV > maxV:
            maxV = totalV
            maxVIndex = subsets.index(subset)

    result = []
    for i in range(0,len(wList)):
        result.append(0)
    for i in subsets[maxVIndex]:
        result[i]=1

    total_weight = 0
    total_value = 0
    for i in range(len(wList)):
        total_weight += result[i]*wList[i]
        total_value += result[i]*vList[i]
    
    return (total_weight, total_value, result)


if __name__=="__main__":
    for i in range(5):
        data = tc.use_testcase('input/INPUT_'+str(i)+'.txt')
        W = data[0]
        m = data[1]
        wList = data[2]
        vList = data[3]
        cList = data[4]
        tc.time_operation(bruteForceKnapsack, 'input/INPUT_'+str(i)+'.txt', 
                            len(wList), m, W, 'output/brute_force/OUTPUT_'+str(i)+'.txt')   
        