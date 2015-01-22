__author__ = 'fabienngo'

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