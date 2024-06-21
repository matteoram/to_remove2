from bloomf import BloomFilter2
from generate_random_strings import generate_random_strings
from random import seed
from typing import List
import time

def test_check(bloom_filter: BloomFilter2, words_list: List[str], sim_num: int) -> float:
    
    times_list = []

    for _ in range(sim_num):
        
        for item in words_list:
            bloom_filter.add(item)
        
        start_time = time.time_ns()

        for item in words_list:
            bloom_filter.check(item)
        
        end_time = time.time_ns()

        times_list.append(end_time - start_time)

    time_avg = sum(times_list)/sim_num

    return time_avg

if __name__ == "__main__":

    seed(1010)
    array_size = 9585058
    hash_functions = 7
    probability = 0.05
    min_char = 1
    max_char = 255
    samples = [1000, 10000]
    sim_num = 100

    bloom_filter = BloomFilter2(array_size, hash_functions)
    results = []

    for i in samples:

        words_list = generate_random_strings(i, min_char, max_char)
        
        average_check_time = test_check(bloom_filter, words_list, sim_num) / 1e6

        results.append({'sample_size': i, 'average_check_time': average_check_time})

    print(results)