from random import choices, randint
import string
from typing import List

def generate_random_strings(size: int, min_length: int, max_length: int) -> List[str]:
    word_list = []
    for _ in range(size):
        word = ''.join(choices(string.ascii_letters, k=randint(min_length, max_length)))
        word_list.append(word)
    return word_list