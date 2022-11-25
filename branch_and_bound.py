import test_case as tc

n = 0
W = 0
w = []
v = []

values_per_weight = []


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
            result = self.pqueue.pop()
            self.length -= 1
            return result
        
class Node:
    def __init__(self, level, value, weight):
        self.level = level
        self.value = value
        self.weight = weight
        self.items = []
        
            
def get_bound(node):
    if node.weight >= W:
        return 0
    else:
        result = node.value
        next_level = node.level + 1
        totweight = node.weight
        while next_level <= n-1 and totweight + w[next_level] <= W:
            totweight = totweight + w[next_level]
            result = result + v[next_level]
            next_level+=1
        k = next_level
        if k<=n-1:
            result = result + (W - totweight) * values_per_weight[k]
        return result

def branch_and_bound():
    pq = Priority_Queue()

    t = Node(-1, 0, 0)
    max_profit = 0
    t.bound = get_bound(t)
    max_weight = 0

    pq.insert(t)

    while pq.length != 0:
        
        t = pq.remove()

        if t.bound > max_profit:
            u = Node(0, 0, 0)
            u.level = t.level + 1
            u.value = t.value + v[u.level]
            u.weight = t.weight + w[u.level]
            u.items = t.items.copy()

            if u.weight <= W and u.value > max_profit: 
                max_profit = u.value
                max_weight = u.weight
                u.items.append(1)

            u.bound = get_bound(u)
            
            if u.bound > max_profit:
                pq.insert(u)
                u.items.append(1)
                
            with_out = Node(u.level, t.value, t.weight)
            with_out.bound = get_bound(with_out)
            with_out.items = t.items.copy()


            if with_out.bound > max_profit:
                pq.insert(with_out)
                with_out.items.append(0)

                
    return (max_weight, max_profit, u.items)

if __name__ == '__main__':
    for i in range(5):
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
            values_per_weight.append(w[j] / v[j])
        tc.time_operation(branch_and_bound, fin, n, C, W, fout)
