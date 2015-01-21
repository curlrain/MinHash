__author__ = 'fabienngo'

from bs4 import BeautifulSoup
import urllib3
import requests

import urllib
import re
import mmh3
import time
import cProfile
import profile
import xxhash
import timeit


maxint = (sys.maxsize-1)//2+1
type(maxint)
def compute_signature(soup, shingle_size=9):
    text = re.sub(r'\n+', ' ', soup.text)
    text = re.sub(r'\s+', '', text)
    shingles_set = {text[i:i+shingle_size] for i in range(len(text) - shingle_size+1)}
    signature_set = {str(mmh3.hash(shingle, 43)) for shingle in shingles_set}
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

url1 = "https://code.google.com/p/smhasher/"
url2a = "http://www.crutchfield.com/S-9nWHkoAgrEp/"
url2b = "http://www.crutchfield.com/S-TWcbiNReN5e/"
url3a = "http://www.apple.com/ca/"
url3b = "http://www.apple.com"
page1 = requests.get(url1)
page2a = requests.get(url2a)
page2b = requests.get(url2b)
page3a = requests.get(url3a)
page3b = requests.get(url3b)

soup1 = BeautifulSoup(page1.text)
soup2a = BeautifulSoup(page2a.text)
soup2b = BeautifulSoup(page2b.text)
soup3a = BeautifulSoup(page3a.text)
soup3b = BeautifulSoup(page3b.text)
url1_sign = compute_signature(soup1, shingle_size=9)
url2a_sign = compute_signature(soup2a, shingle_size=9)
url2b_sign = compute_signature(soup2b, shingle_size=9)
url3a_sign = compute_signature(soup3a, shingle_size=9)
url3b_sign = compute_signature(soup3b, shingle_size=9)
n = 50
minhash1 = MinHash_set(url1_sign, n)
minhash2a = MinHash_set(url2a_sign, n)
minhash2b = MinHash_set(url2b_sign, n)
minhash3a = MinHash_set(url3a_sign, n)
minhash3b = MinHash_set(url3b_sign, n)
print(jaccard_sim(minhash1, minhash2a))
print(jaccard_sim(minhash2a, minhash2b))
print(jaccard_sim(minhash3a, minhash3b))
print(jaccard_sim(minhash3a, minhash2b))
print(jaccard_sim(minhash1, minhash3b))


xxhash.xxh32("abc", 0).digest_fast32()

xxhash.xxh64("abc", 1).intdigest()


start = time.time()
minhash = MinHash(url1_sign, 50, 4)
end = time.time()
print(end-start)


cProfile.run('MinHash_set(url1_sign, 25)')
cProfile.run('compute_signature(soup1)')


