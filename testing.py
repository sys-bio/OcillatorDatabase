import json
import os
import time
import typing

import requests

'''
now = time.time()
y = requests.get("https://raw.githubusercontent.com/epshteinmatthew/OscillatorDatabase/master/checksum").text
if y != open("checksum", "r").read():
    print("ohno")
else:
    print([item for item in json.load(open("metadata.json", "r")) if item['numSpecies'] == 3 and item['numReactions'] == 5])
print(time.time() - now)

now = time.time()
x = requests.get("https://raw.githubusercontent.com/epshteinmatthew/OscillatorDatabase/master/metadata.json")
print(time.time() - now)
'''

def setGetPaths(data, num_species=None, num_reactions=None, model_type=None):
    now = time.time()
    to_union = []
    if num_species is not None:
        to_union.append(set(data['numSpecies'][num_species.__str__()]))
    if num_reactions is not None:
        to_union.append(set(data['numReactions'][num_species.__str__()]))
    if model_type is not None:
        to_union.append(set(data['modelType'][num_species.__str__()]))
    x = set.intersection(*to_union)
    print(time.time() - now)
    return x

def countAll(data):
    now = time.time()
    x = set()
    for item in data['numSpecies']:
        x.update(set(data['numSpecies'][item]))
    for item in data['numReactions']:
        x.update(set(data['numReactions'][item]))
    for item in data['modelType']:
        x.update(set(data['modelType'][item]))
    print(now - time.time())
    return len(x)



#print(setGetPaths(json.load(open("setmetadata.json", "r"))[0], num_species=3, num_reactions=4))
print(countAll(json.load(open("setmetadata.json", "r"))[0]))


