from bloomf import BloomFilter2
from generate_random_strings import generate_random_strings
from random import seed, shuffle
from typing import List
import matplotlib.pyplot as plt

def test_performance(bloom_filter: BloomFilter2, probability: float, names_list: List[str], sim_num: int) -> float:
    """
    Evaluate the performance of a Bloom filter in maintaining a specified false positive rate.

    Parameters:
    - bloom_filter (BloomFilter2): An instance of the BloomFilter2 class to be tested.
    - probability (float): Desired false positive probability (e.g., 0.05 for 5%).
    - names_list (List[str]): List of names used to test the Bloom filter.
    - sim_num (int): Number of simulations to run for averaging results.

    Returns:
    - float: Average false positive rate observed across simulations.

    The function evaluates the Bloom filter's ability to achieve and maintain a false positive rate
    close to the specified probability. It clears the Bloom filter, inserts a subset of names_list
    items (based on the given probability), and then checks the filter's response to items not
    inserted. This process is repeated across multiple simulations to calculate an average false
    positive rate.
    """

    false_positive_rate = []

    for _ in range(sim_num):

        bloom_filter.clear()
        shuffle(names_list)
        num_names_present = int((1 - probability) * len(names_list))
        names_present = names_list[:num_names_present]
        names_absent = names_list[num_names_present:]

        for element in names_present:
            bloom_filter.add(element)

        false_positives = 0

        for name in names_absent:
            if bloom_filter.check(name):
                false_positives += 1

        false_positive_rate.append(false_positives / len(names_absent))

    false_positive_rate_average = sum(false_positive_rate)/len(false_positive_rate)
        
    return false_positive_rate_average

def generate_graph(data, name, title):
    """
    Generate a bar graph visualizing false positive rates against sample sizes.

    Parameters:
    - data (list of dicts): Data containing 'name_list_size' and 'false_positive_rate' entries.
    - name (str): File name to save the generated graph.
    - title (str): Title of the graph.

    Generates a bar graph with sample sizes on the x-axis and corresponding false positive rates
    on the y-axis. The function expects data in the format of a list of dictionaries where each
    dictionary contains 'name_list_size' (sample size) and 'false_positive_rate' (rate to be plotted)
    entries. The graph includes a horizontal dashed line at y=0.05 to indicate the target false
    positive rate of 5%. The graph is saved as a file named 'name' and displayed using matplotlib.
    """

    name_list_sizes = [entry['name_list_size'] for entry in data]
    false_positive_rates = [entry['false_positive_rate'] for entry in data]

    fig, ax = plt.subplots(figsize=(10, 6))

    bar_width = 0.2
    index = range(len(data))
    ax.bar(index, false_positive_rates, width=bar_width, label='False Positive Rate')

    ax.set_xlabel('Sample Size')
    ax.set_ylabel('False Positive Rate')
    ax.set_title(title)
    ax.axhline(y=0.05, color='r', linestyle='--', linewidth=1, label='Target 5% FPR')
    ax.legend()
    xticks = [100, 5000, 10000, 15000, 20000, 25000, 30000]
    ax.set_xticks([name_list_sizes.index(x) for x in xticks])
    ax.set_xticklabels(xticks)

    plt.tight_layout()
    plt.savefig(name)
    plt.show()

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
        false_positive_rate = test_performance(bloom_filter, p, names_list, sim_num)
        results_fixed.append({'name_list_size': i, 'false_positive_rate': false_positive_rate})

    generate_graph(results_fixed, 'chart_1_fixed_bf.png', 'Chart 1. False positive rate for fixed Bloom filter')

    # Initialize list to store results for dynamically adjusted Bloom filter
    results_dynamic = []

    # Test performance for different sizes of name lists with dynamically adjusted Bloom filter
    for i in range(name_list_min, name_list_max + name_list_min, name_list_step):

        names_list = generate_random_strings(i, name_min_char, name_max_char)
        bloom_filter = BloomFilter2(i, p)
        false_positive_rate = test_performance(bloom_filter, p, names_list, sim_num)
        results_dynamic.append({'name_list_size': i, 'false_positive_rate': false_positive_rate})

    generate_graph(results_dynamic, 'chart_2_dynamic_bf.png', 'Chart 2. False positive rate for dynamically adjusted Bloom filter')