#coding=utf-8
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from multiprocessing import cpu_count

def test_sleep(n):
    s = time.time()
    time.sleep(n)
    e = time.time()
    print('start at %.3f end at %.3f, usage %.3f' %(s, e, (e-s)))
    return True

def use_map():
    tasks = [3, 5, 3, 6, 5, 2]
    workers = cpu_count()
    time.sleep(2)
    task1 = [7, 3, 4, 2, 5]
    s = time.time()
    with ProcessPoolExecutor(max_workers=workers) as executor:
        try:
            results = executor.map(test_sleep, tasks)
            for num, result in zip(tasks, results):
                c = time.time()
                print('%s result is %s. COST: %.3f' % (num, result, (c-s)))
        except Exception as e:
            print(e)
    x = time.time()
    print('Took %.3f seconds' %(x-s))


def gcd(pair):
    a,b = pair
    low = min(a,b)
    for i in range(low,0,-1):
        if a % i == 0 and b % i ==0:
            return i


numbers = [(1963309,2265973),(2030677,3814172),
        (2039045,2020802),(1551645,2229620)]
workers = cpu_count()
'''
s1 = time.time()
pool = ProcessPoolExecutor(max_workers = workers)
res1 = list(map(gcd, numbers))
c1 = time.time()
print(res1, 'Finished in %.3f seconds' %(c1-s1))
'''
s2 = time.time()
pool = ThreadPoolExecutor(max_workers = workers)
res2 = list(map(gcd, numbers))
c2 = time.time()
print(res2, 'Finished in %.3f seconds' %(c2-s2))