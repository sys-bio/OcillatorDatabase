import json
import time

now = time.time()
setdict = json.load(open("setmetadata.json", "r"))[0]

x = set(setdict["numSpecies"]["3"]) & set(setdict["numReactions"]["9"]) & set(setdict["modelType"]["oscillator"])
print(time.time() - now)
