from bloomf import BloomFilter2
from generate_random_strings import generate_random_strings
from random import seed, shuffle
from typing import List
import matplotlib.pyplot as plt

def test_performance(bloom_filter: BloomFilter2, probability: float, words_list: List[str], sim_num: int) -> float:
    '''Function to examine the performance of the bloom filter in holding a
    false positive rate of 5%. This is performed by using an inputted list of
    words and splitting it between 
    '''
    false_positive_rate = []

    for _ in range(sim_num):

        bloom_filter.clear()
        shuffle(words_list)
        num_words_present = int((1 - probability) * len(words_list))
        words_present = words_list[:num_words_present]
        words_absent = words_list[num_words_present:]

        for element in words_present:
            bloom_filter.add(element)

        false_positives = 0

        for word in words_absent:
            if bloom_filter.check(word):
                false_positives += 1

        false_positive_rate.append(false_positives / len(words_absent))

    false_positive_rate_average = sum(false_positive_rate)/len(false_positive_rate)
        
    return false_positive_rate_average

def generate_graph(data, title):

    word_list_sizes = [entry['word_list_size'] for entry in data]
    false_positive_rates = [entry['false_positive_rate'] for entry in data]

    fig, ax = plt.subplots(figsize=(10, 6))

    bar_width = 0.2
    index = range(len(data))
    ax.bar(index, false_positive_rates, width=bar_width, label='False Positive Rate')

    ax.set_xlabel('Sample Size')
    ax.set_ylabel('False Positive Rate')
    ax.set_title('False Positive Rates for Different Sample Sizes and Array Sizes')
    step = max(len(word_list_sizes) // 3, 1)
    ax.set_xticks(index[::step])
    ax.set_xticklabels(word_list_sizes[::step], rotation=45)
    ax.axhline(y=0.05, color='r', linestyle='--', linewidth=1, label='Target 5% FPR')
    ax.legend()

    plt.tight_layout()
    fig.savefig(title)
    plt.show()

if __name__ == "__main__":

    seed(1010)

    n = 30000
    p = 0.05
    
    sim_num = 100
    
    min_char = 1
    max_char = 255
    
    word_list_min = 100
    word_list_max = n
    word_list_step = 100

    results_fixed = []
    bloom_filter = BloomFilter2(n, p)

    for i in range(word_list_min, word_list_max + word_list_min, word_list_step):

        words_list = generate_random_strings(i, min_char, max_char)
        false_positive_rate = test_performance(bloom_filter, p, words_list, sim_num)
        results_fixed.append({'word_list_size': i, 'false_positive_rate': false_positive_rate})
        if i % 1000 == 0:
            print({'word_list_size': i, 'false_positive_rate': false_positive_rate})
    
    generate_graph(results_fixed, 'chart_1_fixed_bf.png')

    results_dynamic = []

    for i in range(word_list_min, word_list_max + word_list_min, word_list_step):

        words_list = generate_random_strings(i, min_char, max_char)
        bloom_filter = BloomFilter2(i, p)
        false_positive_rate = test_performance(bloom_filter, p, words_list, sim_num)
        results_dynamic.append({'word_list_size': i, 'false_positive_rate': false_positive_rate})
        if i % 1000 == 0:
            print({'word_list_size': i, 'false_positive_rate': false_positive_rate})
    
    generate_graph(results_dynamic, 'chart_1_dynamic_bf.png')