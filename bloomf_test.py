from bloomf import BloomFilter2
from generate_random_strings import generate_random_strings
from random import seed
from typing import List
import matplotlib.pyplot as plt

def test_performance(bloom_filter: BloomFilter2, probability: float, words_list: List[str], sim_num: int) -> float:
    
    false_positive_rate = []

    for _ in range(sim_num):

        num_elements_to_add = int(probability * len(words_list))
        elements_to_add = words_list[:num_elements_to_add]

        for element in elements_to_add:
            bloom_filter.add(element)

        test_words = words_list

        false_positives = 0
        for word in test_words:

            if bloom_filter.check(word) and word not in elements_to_add:
                false_positives += 1

        false_positive_rate.append(false_positives / (len(test_words) - num_elements_to_add))

    false_positive_rate_average = sum(false_positive_rate)/len(false_positive_rate)
        
    return false_positive_rate_average

def generate_graph(data):

    sample_sizes = [entry['sample_size'] for entry in data]
    false_positive_rates = [entry['false_positive_rate'] for entry in data]

    fig, ax = plt.subplots(figsize=(10, 6))

    bar_width = 0.2
    index = range(len(data))
    ax.bar(index, false_positive_rates, width=bar_width, label='False Positive Rate')

    ax.set_xlabel('Sample Size')
    ax.set_ylabel('False Positive Rate')
    ax.set_title('False Positive Rates for Different Sample Sizes and Array Sizes')
    step = max(len(sample_sizes) // 4, 1)
    ax.set_xticks(index[::step])
    ax.set_xticklabels(sample_sizes[::step], rotation=45)
    ax.axhline(y=0.05, color='r', linestyle='--', linewidth=1, label='Target 5% FPR')
    ax.legend()

    plt.tight_layout()
    fig.savefig('chart_1_false_positive_rates.png')
    plt.show()

if __name__ == "__main__":

    seed(1010)
    array_size = 9585058
    hash_functions = 7
    probability = 0.05
    min_char = 1
    max_char = 255
    sample_min = 20
    sample_max = 10000
    sample_step = 20
    sim_num = 100

    bloom_filter = BloomFilter2(array_size, hash_functions)
    results = []

    for i in range(sample_min, sample_max, sample_step):

        words_list = generate_random_strings(i, min_char, max_char)
        
        false_positive_rate = test_performance(bloom_filter, probability, words_list, sim_num)

        results.append({'sample_size': i, 'false_positive_rate': false_positive_rate})
    
    generate_graph(results)