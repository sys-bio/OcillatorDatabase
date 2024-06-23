import asyncio
import json
import os.path
import time
from dataclasses import dataclass

import aiohttp
import requests


def request_metadata(checksum):
    data = requests.get(
        "https://raw.githubusercontent.com/epshteinmatthew/OscillatorDatabase/master/metadata.json").text
    open("metadata.json", "w").write(data)
    open("checksum", "w").write(checksum)
    return data


def get_metadata():
    checksum = requests.head("https://raw.githubusercontent.com/epshteinmatthew/OscillatorDatabase/master/checksum").text
    if not os.path.isfile("checksum") or not os.path.isfile("metadata.json"):
        return request_metadata(checksum)
    if checksum != open("checksum", "r").read():
        return request_metadata(checksum)
    return json.load(open("metadata.json", "r"))


async def get(url, session, resultant_dir):
    try:
        async with session.get(url=url) as response:
            resp = await response.text()
            open(resultant_dir + url.split("/")[-1], "w").write(resp)
    except Exception as e:
        print("Unable to get url {} due to {}.".format(url, e.__class__))


async def lookup(data, num_species, num_reactions, resultant_dir):
    urls = ["https://raw.githubusercontent.com/epshteinmatthew/OscillatorDatabase/master/" + item['path'] for item in
            data if
            item["numSpecies"] == num_species and item["numReactions"] == num_reactions]
    print(len(urls))
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(*(get(url, session, resultant_dir) for url in urls))


start = time.time()
#example: lookup models with 3 species and 3 reactions, and put them into the "osc123" directory
asyncio.run(lookup(get_metadata(), 2, 3, "osc123/"))
end = time.time()
print(end - start)
