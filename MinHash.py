__author__ = 'fabienngo'

from bs4 import BeautifulSoup
import requests
import re
import mmh3
import time
import cProfile
import profile
import xxhash
import nltk
from collections import defaultdict as ddict



maxint = (sys.maxsize-1)//2+1
type(maxint)
def compute_signature(soup, shingle_size=9):
    text = re.sub(r'\n+', ' ', BeautifulSoup(soup).get_text())
    text = re.sub(r'\s+', '', text)
    shingles_set = {text[i:i+shingle_size] for i in range(len(text) - shingle_size+1)}
    signature_set = {str(mmh3.hash(shingle, 43)) for shingle in shingles_set}
    return signature_set


def MinHash(signature, n_hash=100, ix=0):
    minhash_value = maxint
    for el in signature:
            # minhash_temp = (mmh3.hash(el, 40) + ix * hash(el)) % maxint
            # minhash_temp = (mmh3.hash(el, 40) + ix * xxhash.xxh32(el).intdigest()) % maxint
            minhash_temp = (xxhash.xxh32(el, 1).intdigest() + ix * hash(el)) % maxint
            # minhash_temp = xxhash.xxh32(el, ix).intdigest()
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


fn = 'url.txt'
with open(fn, 'r') as file:
    url_set = {line.rstrip('\n') for line in file}


MinHash_dict = ddict()
n = 50
for url in url_set:
    soup = requests.get(url).text
    url_sign = compute_signature(soup, shingle_size=9)
    MinHash_dict[url] = MinHash_set(url_sign, n)


test_set = {"http://www.microsoft.com/fr-ca/default.aspx", "http://www.apple.com", "http://www.apple.com/fr/",
            "https://fr-fr.facebook.com/", "http://www.crutchfield.com/S-9nWHkoAgrEp/"}

for el in test_set:
    minhash_el = MinHash_dict[el]
    sim_list = [jaccard_sim(minhash_el, v) for v in MinHash_dict.values() ]
    print(el)
    print(sim_list)
    print('\n')










cProfile.run('MinHash_set(url1_sign, 25)')
cProfile.run('compute_signature(soup1)')


