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
    checksum = requests.head(
        "https://raw.githubusercontent.com/epshteinmatthew/OscillatorDatabase/master/checksum").text
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


async def lookup(data, num_species, num_reactions, model_type, resultant_dir):
    paths = [item['path'] for item in
             data if
             item["numSpecies"] == num_species and item["numReactions"] == num_reactions and item[
                 "modelType"] == model_type]
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(*(
            get("https://raw.githubusercontent.com/epshteinmatthew/OscillatorDatabase/master/" + url, session,
                resultant_dir) for url in paths))


def get_number_of_models(data, num_species, num_reactions, model_type):
    return len([item['path'] for item in
                data if
                item["numSpecies"] == num_species and item["numReactions"] == num_reactions and item[
                    "modelType"] == model_type])


def get_summary(data):
    summary = {
        "total amount of models": len(data),
    }
    reaction_nums = {item['numReactions'] for item in data}
    species_nums = {item['numSpecies'] for item in data}
    model_types = {item['modelType'] for item in data}
    for type in model_types:
        for num in reaction_nums:
            for spEnum in species_nums:
                summary[type + ' with ' + num.__str__() + ' reactions and ' + spEnum.__str__() + " species"] = (
                    len([item['path'] for item in data if
                         item["numSpecies"] == num and item["numReactions"] == spEnum and item["modelType"] == type]))
    return summary

def get_total_number_of_model_types(data):
    return len({item["modelType"] for item in data})


start = time.time()
metadata = get_metadata()
print(get_total_number_of_model_types(metadata))
#example: lookup models with 3 species and 3 reactions, and put them into the "osc123" directory
asyncio.run(lookup(metadata, 3, 9, "osc123/"))
end = time.time()
print(end - start)
