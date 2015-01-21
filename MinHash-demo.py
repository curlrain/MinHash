__author__ = 'fabien'

from bs4 import BeautifulSoup
import requests
import re
import time
import cProfile
from MinHash import compute_signature, MinHash_set, jaccard_sim

from collections import defaultdict as ddict

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
    sim_list = {k:jaccard_sim(minhash_el, v) for k,v in MinHash_dict.items()}
    print(el)
    print(sim_list)
    print('\n')


def performance_test_function(html, m):
    url_sign = compute_signature(soup, shingle_size=9)
    return MinHash_set(url_sign, m)

n = 10
url_test = "https://fr-fr.facebook.com/"
soup = requests.get(url_test).text
start = time.time()
performance_test_function(soup, n)
end = time.time()
print(end-start)

cProfile.run('performance_test_function(soup, n)')