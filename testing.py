import json
import os
import time
import typing

import requests

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





