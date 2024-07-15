#these would happen as github actions
import json
import os
import sys

import aiofiles
import tellurium as te

def process_model(file_path, filename, data):
    async with open(os.path.join(file_path, filename), "r") as file:
        model_string = file.read()
        r = te.loada(model_string)
        numSpecies = r.getNumFloatingSpecies()
        numReactions = r.getNumReactions()
        data.append({
            "numSpecies": numSpecies,
            "numReactions": numReactions,
            "path": file_path + "/" + filename
        })


def upload(location):
    try:
        with open("metadata.json", "r") as f:
            data = json.load(f)
        if(os.path.isfile(location)):
            process_model("/".join("/a/b/a.txt".split("/")[:-1]), location.split("/")[-1], data)
        else:
            for filename in os.listdir(location):
                process_model(location, filename, data)
        with open("metadata.json", "w") as f:
            json.dump(data, f)
        with open("checksum", "w") as ch:
            ch.write(( int(ch.read())+1).__str__())
        print("added model")
        return
    except:
        print("failed to add placeholder")


upload(sys.argv[1])