import math
import mmh3
from bitarray import bitarray


class BloomFilter(object):

	"""
	Class for Bloom filter, using murmur3 hash function
	"""

	def __init__(self, items_count, fp_prob):
		"""
		items_count : int
			Number of items expected to be stored in bloomf filter
		fp_prob : float
			False Positive probability in decimal
		"""
		# False possible probability in decimal
		self.fp_prob = fp_prob

		# Size of bit array to use
		self.size = self.get_size(items_count, fp_prob)

		# Number of hash functions to use
		self.hash_count = self.get_hash_count(self.size, items_count)

		# Bit array of given size
		self.bit_array = bitarray(self.size)

		# Initialize all bits as 0
		self.bit_array.setall(0)

	def add(self, item):
		"""
		Add an item in the filter
		"""
		digests = []
		for i in range(self.hash_count):

			# Create digest for given item
			# With different seed, digest created is different
			digest = mmh3.hash(item, i) % self.size
			digests.append(digest)

			# Set the bit True in bit_array
			self.bit_array[digest] = True

	def check(self, item):
		"""
		Check for existence of an item in filter
		"""
		for i in range(self.hash_count):
			digest = mmh3.hash(item, i) % self.size
			if self.bit_array[digest] == False:

				# If any of bit is False then its not present in filter
				# else there is probability that it exist
				return False
		return True

	@classmethod
	def get_size(self, n, p):
		"""
		Return the size of bit array(m) to used using
		following formula
		m = -(n * lg(p)) / (lg(2)^2)
		n : int
			Number of items expected to be stored in filter
		p : float
			False Positive probability in decimal
		"""
		m = -(n * math.log(p))/(math.log(2)**2)
		return int(m)

	@classmethod
	def get_hash_count(self, m, n):
		"""
		Return the hash function(k) to be used using following formula
		k = (m/n) * lg(2)

		m : int
			Size of bit array
		n : int
			Number of items expected to be stored in filter
		"""
		k = (m/n) * math.log(2)
		return int(k)

class BloomFilter2:
    def __init__(self, size: int, hash_count: int):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)

    def add(self, item: str):
        for seed in range(self.hash_count):
            digest = mmh3.hash(item, seed) % self.size
            self.bit_array[digest] = 1

    def check(self, item: str) -> bool:
        for seed in range(self.hash_count):
            digest = mmh3.hash(item, seed) % self.size
            if not self.bit_array[digest]:
                return False
        return True