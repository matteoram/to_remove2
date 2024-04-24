from bloomf import BloomFilter
from random import shuffle, seed
import time

seed(1010)

n = 20  # No of items to add
p = 0.05  # False positive probability

bloomf = BloomFilter(n, p)
print("Size of bit array:{}".format(bloomf.size))
print("False positive Probability:{}".format(bloomf.fp_prob))
print("Number of hash functions:{}".format(bloomf.hash_count))

# Words to be added
word_present = ['abound', 'abounds', 'abundance', 'abundant', 'accessible',
                'bloomf', 'blossom', 'bolster', 'bonny', 'bonus', 'bonuses',
                'coherent', 'cohesive', 'colorful', 'comely', 'comfort',
                'gems', 'generosity', 'generous', 'generously', 'genial']

# Word not added
word_absent = ['bluff', 'cheater', 'hate', 'war', 'humanity',
               'racism', 'hurt', 'nuke', 'gloomy', 'facebook',
               'geeksforgeeks', 'twitter']

for item in word_present:
    bloomf.add(item)

shuffle(word_present)
shuffle(word_absent)

test_words = word_present[:10] + word_absent
shuffle(test_words)

false_positives = 0
for word in test_words:
    if bloomf.check(word):
        if word in word_absent:
            false_positives += 1
            print("'{}' is a false positive!".format(word))
        else:
            print("'{}' is probably present!".format(word))
    else:
        print("'{}' is definitely not present!".format(word))

false_positive_rate = false_positives / len(test_words)

print(f'The percent of items not in the dataset is {round(len(word_absent)/len(test_words),4)*100}%')
print(f'The false positive rate is {round(false_positive_rate,4)*100}%.')


## Time complexity

# Inserting

sim_num = 10
times_list = []
for _ in range(sim_num):
    bloomf = BloomFilter(n, p)
    start_time = time.time_ns()
    for item in word_present:
        bloomf.add(item)
    end_time = time.time_ns()
    times_list.append(end_time - start_time)
time_avg = sum(times_list)/sim_num
print(f'The average inserting time is {round(time_avg/ 1_000_000, 3)} milliseconds.')