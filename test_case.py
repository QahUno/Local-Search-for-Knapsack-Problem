import random
import csv
import datetime
from timeit import default_timer as timer
import os
import psutil
import time


def generate_testcase(number_items, capacity, number_classes, path_in):

    #  5 small datasets of sizes 10-40 /40 35 30 25 20, capacity 100, 3 class
    with open(path_in, 'w', newline='\n') as csvfile: 
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


def use_testcase(path_in):
    W = 0
    m = 1
    wList = []
    vList = []
    cList = []
    with open(path_in) as f:
        W = int(f.readline())
        m = int(f.readline())
        wList = [int(number) for number in f.readline().split(",")]
        vList = [int(number) for number in f.readline().split(",")]
        cList = [int(number) for number in f.readline().split(",")]

    return [W, m, wList, vList, cList]
 

def output_soulution(path_in, total_value, solution):
    with open(path_in, 'w', newline='\n') as csvfile:
        csvwriter = csv.writer(csvfile)
        lst = []
        lst.append(total_value) 
        csvwriter.writerow(lst) 
        csvwriter.writerow(solution)

def export_solution(W, solution, path_out):
    with open(path_out, 'w', newline='\n') as csvfile:
        csvwriter = csv.writer(csvfile)
        max_weight = []
        max_weight.append(W)
        csvwriter.writerow(max_weight)
        csvwriter.writerow(solution)

def elapsed_since(start):
    return time.strftime("%H:%M:%S", time.gmtime(time.time() - start))
 
def get_process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss

def profile(func):
    def wrapper(*args, **kwargs):
        mem_before = get_process_memory()
        start = time.time()
        result = func(*args, **kwargs)
        elapsed_time = elapsed_since(start)
        mem_after = get_process_memory()
        # print("{}: memory before: {:,}, after: {:,}, consumed: {:,}; exec time: {}".format(
        #     func.__name__,
        #     mem_before, mem_after, mem_after - mem_before,
        #     elapsed_time))
        return (result, mem_after - mem_before)
    return wrapper

def count():
    cnt = 0
    res = []
    for i in range(1000):
        res.append(cnt)
        cnt += 1
    return res

#time, total value, total weight, solution
def time_operation(func, path_in, num_items, num_classes, W, path_out):
    print(path_in, ": ", num_items, ' items, ', num_classes, ' classes, ', W, ' capacity')
    start = timer()
    res = profile(func)()
    end = timer()
    time = (end - start)
    if len(res[0]) != 0:
        print('Total weights: ', res[0][0])
        print('Total values: ', res[0][1])
        print('Solution: ', res[0][2])
        export_solution(res[0][1], res[0][2], path_out)
        picked_item = []
        solution = res[0][2]
        for i in range(len(solution)):
            if solution[i]:
                picked_item.append(i)
        print('Picked items:', picked_item)
    else:
        print('No solution')
    print("Memory consuming: ", res[1], 'KB')
    print('Time processing: ',time, 's')
    print('-----------------------')
    

if __name__  == '__main__':
    # for i in range(5):
    #     generate_testcase(200+100*i, 2000+500*i, 5+i, 'large_input/INPUT_'+str(i)+'.txt')
    # # output_soulution('output.txt', 50, [1,2,3,4,5])
    # print('testcase run')
    profile(count)()