import uuid
import sys
import argparse

from bloomf import BloomFilter

#  python scalable_bloomf_test.py --opt1 100 --opt2 1
parser = argparse.ArgumentParser(description='Script to test the BloomFilter')
parser.add_argument("--opt1", type=int, default=1)
parser.add_argument("--opt2", type=int, default=1)

args = parser.parse_args()

opt1_value = args.opt1
opt2_value = args.opt2


def getRandomString():
    return str(uuid.uuid4())


def createStringTestArray(length):
    return [getRandomString() for _ in range(length)]


def addTestArrayToFilter(bloomFilter, testArray):
    for entry in testArray:
        bloomFilter.add(entry)


def getResults(bloomFilterObject, testArray):
    # Test the keys if present
    for entry in testArray:
        if bloomFilterObject.lookup(entry):
            print(f"Test: OK -- Key: '{entry}' is present")
        else:
            print(f"Test: Failed --Key: '{entry}' is present")


def testBloomFilter(count, hashes):
    """
    Command line options define a size and a number of hashes to be used
    """
    print("Testing BloomFilter implementation...")
    bf = BloomFilter(count, hashes)
    testArray = createStringTestArray(count)
    addTestArrayToFilter(bf, testArray)
    getResults(bf, testArray)
    bf.generateStats()
    bf.clear()


if __name__ == '__main__':
    if opt1_value and opt2_value:
        testBloomFilter(opt1_value, opt2_value)
