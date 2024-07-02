import itertools
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
    to_union = []
    if num_species is not None:
        to_union.append(set(data['numSpecies'][num_species.__str__()]))
    if num_reactions is not None:
        to_union.append(set(data['numReactions'][num_reactions.__str__()]))
    if model_type is not None:
        to_union.append(set(data['modelType'][model_type.__str__()]))
    x = set.intersection(*to_union)
    return x

def countAll(data):
    x = set()
    for item in data['numSpecies']:
        x.update(set(data['numSpecies'][item]))
    for item in data['numReactions']:
        x.update(set(data['numReactions'][item]))
    for item in data['modelType']:
        x.update(set(data['modelType'][item]))
    return len(x)

def combinate(data):
    return itertools.product (
        [item for item in data['numSpecies']],
        [item for item in data['numReactions']],
        [item for item in data['modelType']])


def get_summary(data, asString = False):
    now = time.time()
    length = countAll(data)
    if (asString):
        summary = "Total amount of models: " + length.__str__()
    else:
        summary = {
            "total amount of models": length,
        }

    combinations = combinate(data)
    for ns, nr, mt in combinations:
        amnt = len(setGetPaths(data, ns, nr, mt))
        if (amnt != 0):
            if (asString):
                summary += f"\nAmount of {mt} models with {nr} reactions and {ns} species: " + amnt.__str__()
            else:
                summary[f"\nAmount of ${mt} models with ${nr} reactions and ${ns} species"] = amnt
    print(time.time() - now)
    return summary

#print(setGetPaths(json.load(open("setmetadata.json", "r"))[0], num_species=3, num_reactions=4))
#print(countAll(json.load(open("setmetadata.json", "r"))[0]))
print(get_summary(json.load(open("setmetadata.json", 'r'))[0], True))


