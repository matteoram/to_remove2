import math
import mmh3
from bitarray import bitarray
import hashlib
import BitVector


class BloomFilter(object):
    """
	Class for Bloom filter, using murmur3 hash function
	"""

    def __init__(self, items_count, hashes):
        """
		items_count : int
			Number of items expected to be stored in Bloom filter
		hashes : int
			Number of hashes to be used when storing items in Bloom filter
		"""

        # total count of the elements inserted in the set, initialized to zero,
        # if this is incremented on add, this will be length of the filter, given elements are not removed
        self.n = 0

        self.m = items_count
        self.k = hashes

        self.bv = BitVector.BitVector(size=self.m)
        self._setAllBitsToZero()

    def _setAllBitsToZero(self):
        for i in self.bv:
            self.bv[i] = 0

    def getBitArrayIndices(self, key):
        """
		hashes the key for k defined,
		returns the positions in the bit array for this key
		returns a list of integers as the indices positions
		"""
        returnList = []
        for i in range(1, self.k + 1):
            returnList.append((hash(key) + i * mmh3.hash(key)) % self.m)
        return returnList

    def add(self, key):
        """
		Insert an element to the filter, rest is application insert
		"""
        for i in self.getBitArrayIndices(key):
            self.bv[i] = 1
        self.n += 1

    def lookup(self, key):
        """
		returns boolean whether element exists in the set or not
		"""
        for i in self.getBitArrayIndices(key):
            if self.bv[i] != 1:
                return False
        return True

    def length(self):
        """
		Returns the current size of Bloom filter
		"""
        return self.n

    def generateStats(self):
        """
		Calculates and returns the statistics of a filter
		Probability of FP, n, m, k, predicted false positive rate.
		"""
        n = float(self.n)
        m = float(self.m)
        k = float(self.k)
        p_fp = math.pow((1.0 - math.exp(-(k * n) / m)), k)
        print("Probability of false positives: ", p_fp)
        print("Predicted false positive rate: ", p_fp * 100.0)
        print("Number of elements entered in filter: ", n)
        print("Number of bits in filter: ", m)
        print("Number of hashes in filter: ", k)

    def clear(self):
        """
		Reinitializes the filter and clears old values and statistics
		"""
        self.n = 0
        self.bv = BitVector.BitVector(size=self.m)


class BloomFilter2:
    """
    Class for Bloom filter, using murmur3 hash function
    """

    def __init__(self, n, p):
        """
        n : int
            Number of items expected to be stored in Bloom filter
        p : float
            Desired false positive rate
        """
        self.n = n
        self.p = p

        self.m = math.ceil(-n * math.log(p) / (math.log(2) ** 2))
        self.k = math.ceil((self.m / n) * math.log(2))

        self.bit_array = bitarray(self.m)
        self.bit_array.setall(0)

    def _hashes(self, item):
        """
        Generates k hash values for the given item
        """
        return [mmh3.hash(item, i) % self.m for i in range(self.k)]

    def add(self, item):
        """
        Insert an element to the filter
        """
        for hash_val in self._hashes(item):
            self.bit_array[hash_val] = 1

    def check(self, item):
        """
        Returns boolean whether element exists in the set or not
        """
        return all(self.bit_array[hash_val] for hash_val in self._hashes(item))

    def length(self):
        """
        Returns the current size of Bloom filter
        """
        return self.n

    def generateStats(self):
        """
        Calculates and returns the statistics of a filter
        Probability of FP, n, m, k, predicted false positive rate.
        """
        n = float(self.n)
        m = float(self.m)
        k = float(self.k)
        p_fp = (1 - math.exp(-k * n / m)) ** k
        print("Predicted false positive rate: ", p_fp * 100.0)
        print("Number of elements entered in filter: ", n)
        print("Number of bits in filter: ", m)
        print("Number of hashes in filter: ", k)

    def clear(self):
        """
        Reinitializes the filter and clears old values and statistics
        """
        self.bit_array.setall(0)