import test_case as tc
import numpy as np
import time 

n = 0
W = 0
C = 0
w = []
v = []
c = []
save_index = []
values_per_weight = []
        
class Node:
    def __init__(self, level, value, weight):
        self.level = level
        self.value = value
        self.weight = weight
        self.items = [0 for i in range(n)]
        
            
def get_bound(node):
    if node.weight >= W:
        return 0
    else:
        result = node.value
        next_level = node.level + 1
        totweight = node.weight
        while (next_level <= n-1) and (totweight + w[next_level] <= W ):
            totweight = totweight + w[next_level]
            result = result + v[next_level]
            next_level+=1

        k = next_level
        if k<=n-1:
            result = result + (W - totweight) * (v[k] // w[k])
        return result


def checkClass(node):
    lst_classes = [0 for i in range(C)]
    for i in range(len(node.items)):
        if node.items[i]:
            lst_classes[node.clas[i]-1] = 1

    for c in lst_classes:
        if c == 0:
            return False
    
    return True

def rerange():
    global v, w, c, values_per_weight, save_index
    l = []
    for i in range(len(w)):
        l.append(v[i] / w[i])
    save_index = np.argsort(l).tolist()
    save_index.reverse()
    new_w = []
    new_v = []
    for i in save_index:
        new_w.append(w[i])
        new_v.append(v[i])
    w = new_w.copy()
    v = new_v.copy()

def branch_and_bound():
    pq = []

    t = Node(-1, 0, 0)
    max_profit = 0
    max_weight = 0
    max_items = []
    t.bound = get_bound(t)

    pq.append(t)

    while len(pq) != 0:
        t = pq.pop()
        u = Node(0, 0, 0)
        if t.level == -1:
            u.level = 0

        if t.level == n-1:
            continue

        # print(t.bound)
        # time.sleep(1)
        u.level = t.level + 1
        u.value = t.value + v[u.level]
        u.weight = t.weight + w[u.level]
        u.items = t.items.copy()
        u.items[save_index[u.level]] = 1

        if u.weight <= W and u.value > max_profit:
            max_profit = u.value
            max_weight = u.weight
            max_items = u.items.copy()

        u.bound = get_bound(u)
        
        if u.bound > max_profit:
            pq.append(u)
            
        with_out = Node(u.level, t.value, t.weight)
        with_out.bound = get_bound(with_out)
        with_out.items = t.items.copy()
        with_out.items[save_index[with_out.level]] = 0


        if with_out.bound > max_profit:
            pq.append(with_out)

                
    return (max_weight, max_profit, max_items)

if __name__ == '__main__':
    # for i in range(5):
        i = 0
        fin = 'input/INPUT_'+str(i)+'.txt'
        fout= 'output/branch_and_bound/OUTPUT_'+str(i)+'.txt'

        # fin = 'large_input/INPUT_'+str(i)+'.txt'
        # fout= 'large_output/branch_and_bound/OUTPUT_'+str(i)+'.txt'
        data = tc.use_testcase(fin)
        W = data[0]
        C = data[1]
        w = data[2]
        v = data[3]
        c = data[4]
        n = len(w)
        for j in range(n):
            values_per_weight.append(v[j] / w[j])

        rerange()

        tc.time_operation(branch_and_bound, fin, n, C, W, fout)
    
# Solution:  [0, 0, 1, 1, 1, 0, 1, 0, 0, 0]