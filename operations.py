#these would happen as github actions
import json


def upload(model_type, num_species, num_reactions, location):
    try:
        with open("metadata.json", "r") as f:
            data = json.load(f)
        data.append({
            "numSpecies": num_species,
            "numReactions": num_reactions,
            "modelType": model_type,
            "path": location
        })
        with open("metadata.json", "w") as f:
            json.dump(data, f)
        with open("checksum", "w") as ch:
            ch.write(( int(ch.read())+1).__str__())
        print("added model")
        return
    except:
        print("failed to add placeholder")


def edit(filepath_to_change, replacement_ant_string, model_type, num_species, num_reactions):
    try:
        with open("metadata.json", "r") as f:
            data = json.load(f)
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


def delete(path):
    try:
        with open("metadata.json", "r") as f:
            data = json.load(f)
        for item in data:
            if item['path'] == path:
                data.remove(item)
                break
        with open("metadata.json", "w") as f:
            json.dump(data, f)
        with open("checksum", "w") as ch:
            ch.write(( int(ch.read())+1).__str__())
        print("added model")
        return
    except:
        print("failed to add placeholder")


