import asyncio
import json
import os.path
import time

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


async def lookup(data, resultant_dir, num_species=None, num_reactions=None, model_type=None, ):
    paths = []
    for item in data:
        if (num_species is None or item.get('numSpecies') == num_species) and \
                (num_reactions is None or item.get('numReactions') == num_reactions) and \
                (model_type is None or item.get('modelType') == model_type):
            paths.append(
                "https://raw.githubusercontent.com/epshteinmatthew/OscillatorDatabase/master/" + item["path"])
    if not os.path.isdir(resultant_dir):
        os.mkdir(resultant_dir)
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(*(
            get(url, session,
                resultant_dir) for url in paths))


def get_summary(data):
    summary = {
        "total amount of models": len(data),
    }
    reaction_nums = {item['numReactions'] for item in data}
    species_nums = {item['numSpecies'] for item in data}
    model_types = {item['modelType'] for item in data}
    #this is super slow and should be reworked with itertools
    for modelType in model_types:
        for num in reaction_nums:
            for spEnum in species_nums:
                summary[modelType + ' with ' + num.__str__() + ' reactions and ' + spEnum.__str__() + " species"] = (
                    len([item['path'] for item in data if
                         item["numSpecies"] == spEnum and item["numReactions"] == num and item[
                             "modelType"] == modelType]))
    return summary


def get_total_number_of_model_types(data):
    return len({item["modelType"] for item in data})


def get_number_of_models_with_attrib(data, num_species=None, num_reactions=None, model_type=None):
    count = 0

    for item in data:
        if (num_species is None or item.get('numSpecies') == num_species) and \
                (num_reactions is None or item.get('numReactions') == num_reactions) and \
                (model_type is None or item.get('modelType') == model_type):
            count += 1

    return count


start = time.time()
metadata = get_metadata()

#example: print a summary of the dataset
print(get_summary(metadata))

#example: print the amount of models with 3 species and of type oscillator
print(get_number_of_models_with_attrib(metadata, num_species=3, model_type="oscillator"))

#example: lookup models with 3 species and 3 reactions, and put them into the "osc123" directory
asyncio.run(lookup(metadata, "osc123/", 3, 4, "oscillator"))
end = time.time()
print(end - start)
