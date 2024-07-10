import os.path
import random

import teUtils as tu


def upload(model_type, num_species, num_reactions, location):
    try:
        data = open("metadata.json", "r").read()
        data.append({
            "numSpecies": num_species,
            "numReactions": num_reactions,
            "modelType": model_type,
            "path": location
        })
        open("metadata.json", "w").write(data)
        #edit checksum
        print("added model")
        return
    except:
        print("failed to add placeholder")


def edit(filepath_to_change, replacement_ant_string, model_type, num_species, num_reactions):
    try:
        data = open("metadata.json", "r").read()
        fp = open(filepath_to_change, "w")
        for item in data:
            if item['path'] == filepath_to_change:
                data.remove(item)
                data.append({
                    "numSpecies": num_species,
                    "numReactions": num_reactions,
                    "modelType": model_type,
                    "path": filepath_to_change
                })
                break
        open("metadata.json", "w").write(data)
        fp.write(replacement_ant_string)
        print("added model")
        # edit checksum
        return
    except:
        print("failed to add placeholder")


def delete(path):
    try:
        data = open("metadata.json", "r").read()
        for item in data:
            if item['path'] == path:
                data.remove(item)
                break
        open("metadata.json", "w").write(data)
        # edit checksum
        print("added model")
        return
    except:
        print("failed to add placeholder")


