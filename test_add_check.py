from bloomf import BloomFilter2
from generate_random_strings import generate_random_strings
from random import seed
from typing import List, Tuple
import time
import matplotlib.pyplot as plt

def test_add_check(bloom_filter: BloomFilter2, names_list: List[str], sim_num: int) -> Tuple[float, float, float, float]:
    """
    Test the performance of a Bloom filter in adding and checking elements.
    
    Parameters:
    - bloom_filter (BloomFilter2): The Bloom filter instance to test.
    - names_list (List[str]): List of names to add and check in the Bloom filter.
    - sim_num (int): Number of simulations to perform for averaging times.
    
    Returns:
    Tuple[float, float, float, float]: A tuple containing:
    - item_add_time_average (float): Average time taken to add each item (in milliseconds).
    - total_add_time_average (float): Average total time taken to add all items (in milliseconds).
    - item_check_time_average (float): Average time taken to check each item (in milliseconds).
    - total_check_time_average (float): Average total time taken to check all items (in milliseconds).
    """

    item_add_time = []
    total_add_time = []
    item_check_time = []
    total_check_time = []

    for _ in range(sim_num):

        start_add_time = time.time_ns()
        
        for item in names_list:
            start_add_time_elem = time.time_ns()
            bloom_filter.add(item)
            end_add_time_elem = time.time_ns()
            item_add_time.append(end_add_time_elem - start_add_time_elem)
        
        end_add_time = time.time_ns()
        total_add_time.append(end_add_time - start_add_time)

        start_check_time = time.time_ns()

        for item in names_list:
            start_check_time_elem = time.time_ns()
            bloom_filter.check(item)
            end_check_time_elem = time.time_ns()
            item_check_time.append(end_check_time_elem - start_check_time_elem)            
        
        end_check_time = time.time_ns()
        total_check_time.append(end_check_time - start_check_time)

    item_add_time_average = sum(item_add_time) / (sim_num * len(names_list))
    total_add_time_average = sum(total_add_time)/sim_num

    item_check_time_average = sum(item_check_time) / (sim_num * len(names_list))
    total_check_time_average = sum(total_check_time)/sim_num

    return item_add_time_average, total_add_time_average, item_check_time_average, total_check_time_average

def get_average_item_time(times):
    """
    Calculate the weighted average time per item for adding and checking operations.

    Parameters:
    - times (List[Dict[str, float]]): List of dictionaries containing times for different sample sizes.
      Each dictionary should have keys 'sample_size', 'item_add_time', and 'item_check_time'.

    Returns:
    Tuple[float, float]: A tuple containing:
    - item_add_time_average (float): Weighted average time per item for adding (in milliseconds).
    - item_check_time_average (float): Weighted average time per item for checking (in milliseconds).
    """

    item_add_time_weighted_average_num = 0
    item_add_time_weighted_average_denom = 0
    item_check_time_weighted_average_num = 0
    item_check_time_weighted_average_denom = 0

    for i, _ in enumerate(times):
        sample_size = times[i]["sample_size"]
        item_add_time = times[i]["item_add_time"]
        item_check_time = times[i]["item_check_time"]

        item_add_time_weighted_average_num += sample_size * item_add_time
        item_add_time_weighted_average_denom += sample_size
        item_check_time_weighted_average_num += sample_size * item_check_time
        item_check_time_weighted_average_denom += sample_size

    item_add_time_average = item_add_time_weighted_average_num / item_add_time_weighted_average_denom if item_add_time_weighted_average_denom != 0 else 0
    item_check_time_average = item_check_time_weighted_average_num / item_check_time_weighted_average_denom if item_check_time_weighted_average_denom != 0 else 0

    return item_add_time_average, item_check_time_average

if __name__ == "__main__":

    seed(1010)
    sim_num = 100

    # Parameters for Bloom filter and simulation
    n = 20000
    p = 0.05
    
    # Parameters for varying name lengths and list sizes
    name_min_char = 1
    name_max_char = 255
    name_list_min = 100
    name_list_max = 30000
    name_list_step = 100

    # Initialize list to store results and Bloom filter with fixed parameters
    results_fixed = []
    bloom_filter = BloomFilter2(n, p)

    # Test performance for different sizes of name lists with fixed Bloom filter
    for i in range(name_list_min, name_list_max + name_list_min, name_list_step):

        names_list = generate_random_strings(i, name_min_char, name_max_char)
        
        item_add_time_average, total_add_time_average, item_check_time_average, total_check_time_average = test_add_check(bloom_filter, names_list, sim_num)

        results_fixed.append({'sample_size': i, 'item_add_time': item_add_time_average / 1e6, 'total_add_time': total_add_time_average / 1e6,
                        'item_check_time': item_check_time_average / 1e6, 'total_check_time': total_check_time_average / 1e6})

    item_add_time_average_fixed, item_check_time_average_fixed = get_average_item_time(results_fixed)

    # Create plot
    sample_sizes = [entry['sample_size'] for entry in results_fixed]
    total_add_times = [entry['total_add_time'] for entry in results_fixed]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(sample_sizes, total_add_times, marker='o', linestyle='-', color='b')
    ax.set_xlabel('Sample Size')
    ax.set_ylabel('Total Add Time in Milliseconds')
    ax.set_title('Chart 3. Sample Size vs Total Add Time for Fixed Bloom Filter')
    plt.tight_layout()
    plt.savefig('chart_3_fixed_add.png')
    plt.show()

    # Create plot
    sample_sizes = [entry['sample_size'] for entry in results_fixed]
    total_check_times = [entry['total_check_time'] for entry in results_fixed]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(sample_sizes, total_check_times, marker='o', linestyle='-', color='b')
    ax.set_xlabel('Sample Size')
    ax.set_ylabel('Total Check Time in Milliseconds')
    ax.set_title('Chart 4. Sample Size vs Total Check Time for Fixed Bloom Filter')
    plt.tight_layout()
    plt.savefig('chart_4_fixed_check.png')
    plt.show()

    # Initialize list to store results for dynamically adjusted Bloom filter
    results_dynamic = []

    # Test performance for different sizes of name lists with dynamically adjusted Bloom filter
    for i in range(name_list_min, name_list_max + name_list_min, name_list_step):

        bloom_filter = BloomFilter2(i, p)

        names_list = generate_random_strings(i, name_min_char, name_max_char)
        
        item_add_time_average, total_add_time_average, item_check_time_average, total_check_time_average = test_add_check(bloom_filter, names_list, sim_num)

        results_dynamic.append({'sample_size': i, 'item_add_time': item_add_time_average / 1e6, 'total_add_time': total_add_time_average / 1e6,
                        'item_check_time': item_check_time_average / 1e6, 'total_check_time': total_check_time_average / 1e6})

        if i % 1000 == 0:
            print({'sample_size': i, 'item_add_time': total_check_time_average})

    item_add_time_average_dynamic, item_check_time_average_dynamic = get_average_item_time(results_dynamic)