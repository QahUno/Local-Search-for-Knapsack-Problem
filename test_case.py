import random
import csv
import datetime
from timeit import default_timer as timer

def generate_testcase(number_items, capacity, number_classes, filename):

    #  5 small datasets of sizes 10-40 /40 35 30 25 20, capacity 100, 3 class
    with open(filename, 'w', newline='\n') as csvfile: 
        W = []
        W.append(capacity)
        m = []
        m.append(number_classes)
        MAX_ITEM_WEIGHT = 100
        weights  = random.choices(range(1, MAX_ITEM_WEIGHT+1), k=number_items)
        values = random.sample(range(1, capacity+1), number_items)
        classes = random.choices(range(1, number_classes+1), k=number_items)

        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(W) 
        csvwriter.writerow(m) 
        csvwriter.writerow(weights)
        csvwriter.writerow(values)
        csvwriter.writerow(classes)


def use_testcase(filename):
    W = 0
    m = 1
    wList = []
    vList = []
    cList = []
    with open(filename) as f:
        W = int(f.readline())
        m = int(f.readline())
        wList = [int(number) for number in f.readline().split(",")]
        vList = [int(number) for number in f.readline().split(",")]
        cList = [int(number) for number in f.readline().split(",")]

    return [W, m, wList, vList, cList]
 

def output_soulution(filename, total_value, solution):
    with open(filename, 'w', newline='\n') as csvfile:
        csvwriter = csv.writer(csvfile)
        lst = []
        lst.append(total_value) 
        csvwriter.writerow(lst) 
        csvwriter.writerow(solution)

def export_solution(W, solution, fout):
    with open(fout, 'w', newline='\n') as csvfile:
        csvwriter = csv.writer(csvfile)
        max_weight = []
        max_weight.append(W)
        csvwriter.writerow(max_weight)
        csvwriter.writerow(solution)

#time, total value, total weight, solution
def time_operation(func, filename, num_items, num_classes, W, path):
    print(filename, ": ", num_items, ' items, ', num_classes, ' classes, ', W, ' capacity')
    start = timer()
    res = func()
    if len(res) != 0:
        print('Total weights: ', res[0])
        print('Total values: ', res[1])
        print('Solution: ', res[2])
        export_solution(res[0], res[2], path)
        picked_item = []
        solution = res[2]
        for i in range(len(solution)):
            if solution[i]:
                picked_item.append(i)
        print('Picked items:', picked_item)
    else:
        print('No solution')
    end = timer()
    time = (end - start)
    print('Time processing: ',time)
    print('-----------------------')
    

if __name__  == '__main__':
    for i in range(5):
        generate_testcase(200+100*i, 2000+500*i, 5+i, 'large_input/INPUT_'+str(i)+'.txt')
    # output_soulution('output.txt', 50, [1,2,3,4,5])
    print('testcase run')