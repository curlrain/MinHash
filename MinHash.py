__author__ = 'fabienngo'

from bs4 import BeautifulSoup
import requests
import re
import mmh3
import time
import cProfile
import xxhash
from optparse import OptionParser
from collections import defaultdict as ddict
maxint = 4611686018427387904


def compute_signature(soup, shingle_size=9):
    text = re.sub(r'\n+', ' ', BeautifulSoup(soup).get_text())
    text = re.sub(r'\s+', '', text)
    shingles_set = {text[i:i+shingle_size] for i in range(len(text) - shingle_size+1)}
    signature_set = {str(hash(shingle)) for shingle in shingles_set}
    return signature_set


def MinHash(signature, n_hash=100, ix=0):
    minhash_value = maxint
    for el in signature:
            # minhash_temp = (mmh3.hash(el, 40) + ix * hash(el)) % maxint
            # minhash_temp = (mmh3.hash(el, 40) + ix * xxhash.xxh32(el).intdigest()) % maxint
            # minhash_temp = (xxhash.xxh32(el, 1).intdigest() + ix * hash(el)) % maxint
            minhash_temp = xxhash.xxh32(el, ix).intdigest()
            if minhash_value > minhash_temp:
                minhash_value = minhash_temp
    return minhash_value


def MinHash_set(signature, n_hash=100):
    minhash_set = set()
    for i in range(n_hash):
        minhash_value = MinHash(signature, n_hash=100, ix=i)
        minhash_set.add(minhash_value)
    return minhash_set


def jaccard_sim(minhash1, minhash2):
    return len(minhash1.intersection(minhash2))*1.0/len(minhash1.union(minhash2))



#
# if __name__ == "__main__":
#     parser = OptionParser()
#     parser.add_option("-f", "--file", default="url.txt", dest="filename", help='query file')
#     parser.add_option("-d", "--document", default="http://www.microsoft.com/fr-ca/default.aspx", type="int", dest="numBatches", help='split in n batches')
#     parser.add_option("-o", "--output", default="", dest="output", help='output folder')
#     (options, args) = parser.parse_args()
#     if not options.filename:
#         parser.error("missing query file")
#     print "building queries from query file..."
#
#

# cProfile.run('MinHash_set(url1_sign, 25)')
# cProfile.run('compute_signature(soup1)')


