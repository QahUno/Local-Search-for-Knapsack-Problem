
n = 10
W = 100
m = 2
# lst1 = [79, 32, 47, 18, 26, 85, 33, 40, 45, 59]
# lst2 = [85, 26, 48, 21, 22, 95, 43, 45, 55, 52]
# c2 = [1, 1, 2, 1, 2, 1, 1, 2, 2, 2]
lst1 = [46,24,17,36,9,24,35,21,47,45]
lst2 = [93,55,41,94,52,5,87,39,78,8]
c2 = [2,2,2,2,2,1,2,2,1,1]

v=[]
w=[]
c=[]
values_per_weight = []

for i in range(len(lst1)):
    values_per_weight.append(lst1[i] / lst2[i])
keydict1 = dict(zip(lst1, values_per_weight))
keydict2 = dict(zip(lst2, values_per_weight))
keydict3 = dict(zip(c2, values_per_weight))
#lst1.sort(key=keydict1.get)
#lst2.sort(key=keydict2.get)
v = sorted(lst1,key=keydict1.get)
w = sorted(lst2,key=keydict2.get)
c = sorted(c2,key=keydict3.get)   

class Priority_Queue:
    def __init__(self):
        self.pqueue = []
        self.length = 0
    
    def insert(self, node):
        for i in self.pqueue:
            get_bound(i)
        i = 0
        while i < len(self.pqueue):
            if self.pqueue[i].bound > node.bound:
                break
            i+=1
        self.pqueue.insert(i,node)
        self.length += 1
                    
    def remove(self):
        try:
            result = self.pqueue.pop()
            self.length -= 1
        except: 
            print("Priority queue is empty, cannot pop from empty list.")
        else:
            return result
        
class Node:
    def __init__(self, level, value, weight):
        self.level = level
        self.value = value
        self.weight = weight
        self.items = []
        self.clas = []
        
            
def get_bound(node):
    if node.weight >= W:
        return 0
    else:
        result = node.value
        j = node.level + 1
        totweight = node.weight
        while j <= n-1 and totweight + w[j] <= W:
            totweight = totweight + w[j]
            result = result + v[j]
            j+=1
        k = j
        if k<=n-1:
            result = result + (W - totweight) * (v[k]/w[k])
        return result

def checkClass(node):
    lst_classes = [0 for i in range(m)]
    for i in range(len(node.items)):
        if node.items[i]:
            lst_classes[node.clas[i]-1] = 1

    for c in lst_classes:
        if c == 0:
            return False
    
    return True


def branch_and_bound():
    Totclass = 0 
    nodes_generated = 0
    pq = Priority_Queue()
    t = Node(-1, 0, 0) # t initialized to be the root with level = 0, value = $0, weight = 0
    nodes_generated+=1
    maxprofit = 0 # maxprofit initialized to $0
    
    maxweight = 0 # maxweight initialized to 0
    t.bound = get_bound(t)
    pq.insert(t)

    while pq.length != 0 :
        t = pq.remove() #remove node with best bound
        if t.bound > maxprofit: #check if node is still promising
            #set u to the child that includes the next item

            u = Node(0, 0, 0)
            nodes_generated+=1
            u.level = t.level + 1
            u.value = t.value + v[u.level]
            u.weight = t.weight + w[u.level]

            #take t's list and add u's list
            u.items = t.items.copy()
            u.clas = t.clas.copy() # count class
            for i in range(len(v)):
                if v[u.level] == lst1[i]:
                    u.items.append(i) # adds next item
                    u.clas.append(c2[i])

            if u.weight <= W and u.value > maxprofit:
                print(u.level, u.value, u.weight)
                #update maxprofit
                maxprofit = u.value
                #update maxweight
                maxweight = u.weight
 
            u.bound = get_bound(u)

            # print(u.level, maxprofit, u.bound)

            if u.bound > maxprofit:
                pq.insert(u)

            #set u to the child that does not include the next item
            u2 = Node(u.level, t.value, t.weight)
            nodes_generated+=1
            u2.bound = get_bound(u2)
            u2.items = t.items.copy()
            u2.clas = t.clas.copy() # count class
            if u2.bound > maxprofit:
                pq.insert(u2)
    print(t.level)
                
    #rank items           
    item=[]
    u.items.sort()
    for i in range(len(v)):
        item.append(0)
    for j in range(len(u.items)):
        k = u.items[j]
        item[k] = 1
        
    print("\nMaximum possible profit = ", maxprofit)
    print("\nMaximum possible weight = ", maxweight) 
    print("\nbestitems = ", item)
    print("\nclasses = ", u.clas)
branch_and_bound()