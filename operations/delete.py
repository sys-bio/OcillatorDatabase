#these would happen as github actions
import json
import os

def delete(path):
    try:
        with open("metadata.json", "r") as f:
            data = json.load(f)
        if os.path.isfile(path):
            paths = [path]
        else:
            paths = [pt for pt in os.listdir(path)]
        for item in data:
            if item['path'] in paths:
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


