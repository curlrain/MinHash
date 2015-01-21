__author__ = 'fabien'

from bs4 import BeautifulSoup
import requests as r
import re
import mmh3
import cProfile
url = "http://www.microsoft.com/fr-ca/default.aspx"
from MinHash import jaccard_sim
from collections import defaultdict as ddict


def title_signature(title_text, shingle_size=2):
    text = re.sub(r'\n+', ' ', title_text)
    text = re.sub(r'\s+', '', title_text)
    shingles_set = {text[i:i+shingle_size] for i in range(len(text) - shingle_size+1)}
    signature_set = {str(mmh3.hash(shingle, 43)) for shingle in shingles_set}
    return signature_set


def jaccard_res(sign1, sign2):
    return len(sign1.intersection(sign2))*1.0/len(sign1.union(sign2))

fn = 'url.txt'
with open(fn, 'r') as file:
    url_set = {line.rstrip('\n') for line in file}


signature_dict = ddict()
n = 50
for url in url_set:
    soup = BeautifulSoup(r.get(url).text)
    title = soup.title.text
    url_sign = title_signature(title, shingle_size=3)
    signature_dict[url] = url_sign

test_set = {"http://www.microsoft.com/fr-ca/default.aspx", "http://www.apple.com/fr/",
            "https://fr-fr.facebook.com/", "http://www.crutchfield.com/S-9nWHkoAgrEp/",
            "http://stackoverflow.com/questions/12229124/stacking-numpy-arrays"}


for el in test_set:
    el_sign = signature_dict[el]
    sim_set = {k: jaccard_res(el_sign, v) for k, v in signature_dict.items()}
    print(el)
    print(sim_set)

