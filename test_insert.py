from bloomf import BloomFilter2
from generate_random_strings import generate_random_strings
from random import seed
from typing import List, Tuple
import time
import csv

def test_add_check(bloom_filter: BloomFilter2, words_list: List[str], sim_num: int) -> Tuple[float, float, float, float]:
    
    item_add_time = []
    total_add_time = []
    item_check_time = []
    total_check_time = []

    for _ in range(sim_num):

        start_add_time = time.time_ns()
        
        for item in words_list:
            start_add_time_elem = time.time_ns()
            bloom_filter.add(item)
            end_add_time_elem = time.time_ns()
            item_add_time.append(end_add_time_elem - start_add_time_elem)
        
        end_add_time = time.time_ns()
        total_add_time.append(end_add_time - start_add_time)

        start_check_time = time.time_ns()

        for item in words_list:
            start_check_time_elem = time.time_ns()
            bloom_filter.check(item)
            end_check_time_elem = time.time_ns()
            item_check_time.append(end_check_time_elem - start_check_time_elem)            
        
        end_check_time = time.time_ns()
        total_check_time.append(end_check_time - start_check_time)

    item_add_time_average = sum(item_add_time) / (sim_num * len(words_list))
    total_add_time_average = sum(total_add_time)/sim_num

    item_check_time_average = sum(item_check_time) / (sim_num * len(words_list))
    total_check_time_average = sum(total_check_time)/sim_num

    return item_add_time_average, total_add_time_average, item_check_time_average, total_check_time_average

if __name__ == "__main__":

    seed(1010)
    n = 1000
    p = 0.05
    min_char = 1
    max_char = 255
    samples = [1000, 10000]
    sim_num = 100

    bloom_filter = BloomFilter2(n, p)
    results = []

    for i in samples:

        words_list = generate_random_strings(i, min_char, max_char)
        
        item_add_time_average, total_add_time_average, item_check_time_average, total_check_time_average = test_add_check(bloom_filter, words_list, sim_num)

        results.append({'sample_size': i, 'item_add_time': item_add_time_average / 1e6, 'total_add_time': total_add_time_average / 1e6,
                        'item_check_time': item_check_time_average / 1e6, 'total_check_time': total_check_time_average / 1e6})

    for i, _ in enumerate(results):
        print(f'Times for {results[i]["sample_size"]} items | Add: {round(results[i]["total_add_time"], 6)} ms | Check: {round(results[i]["total_check_time"], 6)} ms')

    item_add_time_weighted_average_num = 0
    item_add_time_weighted_average_denom = 0
    item_check_time_weighted_average_num = 0
    item_check_time_weighted_average_denom = 0
    
    for i, _ in enumerate(results):
        item_add_time_weighted_average_num = item_add_time_weighted_average_num + results[i]["sample_size"] * results[i]["item_add_time"]
        item_add_time_weighted_average_denom = item_add_time_weighted_average_num + results[i]["sample_size"]
        item_check_time_weighted_average_num = item_check_time_weighted_average_num + results[i]["sample_size"] * results[i]["item_check_time"]
        item_check_time_weighted_average_denom = item_check_time_weighted_average_num + results[i]["sample_size"]
    
    print(f'\nAverage add time per element is {round(item_add_time_weighted_average_num / item_add_time_weighted_average_denom, 6)} ms\nAverage check time per element is {round(item_check_time_weighted_average_num / item_check_time_weighted_average_denom, 6)} ms')

if __name__ == "__main__":

    seed(1010)
    n = 1000
    p = 0.05
    min_char = 1
    max_char = 255
    samples = [1000, 10000]
    sim_num = 100

    results = []

    for i in samples:

        bloom_filter = BloomFilter2(i, p)

        words_list = generate_random_strings(i, min_char, max_char)
        
        item_add_time_average, total_add_time_average, item_check_time_average, total_check_time_average = test_add_check(bloom_filter, words_list, sim_num)

        results.append({'sample_size': i, 'item_add_time': item_add_time_average / 1e6, 'total_add_time': total_add_time_average / 1e6,
                        'item_check_time': item_check_time_average / 1e6, 'total_check_time': total_check_time_average / 1e6})

    for i, _ in enumerate(results):
        print(f'Times for {results[i]["sample_size"]} items | Add: {round(results[i]["total_add_time"], 6)} ms | Check: {round(results[i]["total_check_time"], 6)} ms')

    item_add_time_weighted_average_num = 0
    item_add_time_weighted_average_denom = 0
    item_check_time_weighted_average_num = 0
    item_check_time_weighted_average_denom = 0
    
    for i, _ in enumerate(results):
        item_add_time_weighted_average_num = item_add_time_weighted_average_num + results[i]["sample_size"] * results[i]["item_add_time"]
        item_add_time_weighted_average_denom = item_add_time_weighted_average_num + results[i]["sample_size"]
        item_check_time_weighted_average_num = item_check_time_weighted_average_num + results[i]["sample_size"] * results[i]["item_check_time"]
        item_check_time_weighted_average_denom = item_check_time_weighted_average_num + results[i]["sample_size"]
    
    print(f'\nAverage add time per element is {round(item_add_time_weighted_average_num / item_add_time_weighted_average_denom, 6)} ms\nAverage check time per element is {round(item_check_time_weighted_average_num / item_check_time_weighted_average_denom, 6)} ms')