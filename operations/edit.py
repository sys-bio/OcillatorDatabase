#these would happen as github actions
import json
import os

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


def edit(filepath_to_change, replacement_ant_string):
    try:
        with open("metadata.json", "r") as f:
            data = json.load(f)
        for item in data:
            if item['path'] == filepath_to_change:
                data.remove(item)
                r = te.loada(replacement_ant_string)
                numSpecies = r.getNumFloatingSpecies()
                numReactions = r.getNumReactions()
                data.append({
                    "numSpecies": numSpecies,
                    "numReactions": numReactions,
                    "path": filepath_to_change
                })
                break
        with open("metadata.json", "w") as f:
            json.dump(data, f)
        with open(filepath_to_change, "w") as fp:
            fp.write(replacement_ant_string)
        with open("checksum", "w") as ch:
            ch.write(( int(ch.read())+1).__str__())
        print("added model")
        return
    except:
        print("failed to add placeholder")

