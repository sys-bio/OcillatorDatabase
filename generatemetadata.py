import asyncio
import json
import os
import aiofiles
import tellurium as te


async def process_model(file_path, filename, directory):
    async with aiofiles.open(os.path.join(file_path, filename), "r") as file:
        model_string = await file.read()
        r = te.loada(model_string)
        numSpecies = r.getNumFloatingSpecies()
        numReactions = r.getNumReactions()
        directory.append({
            "numSpecies": numSpecies,
            "numReactions": numReactions,
            "path": file_path + "/" + filename
        })

async def main():
    dir_path = "/home/epshtein/Documents/GitHub/OscillatorDatabase"
    directory = []
    x = 0
    for path in os.listdir(dir_path):
        file_path = os.path.join(dir_path, path)
        if os.path.isdir(file_path):
            for filename in os.listdir(file_path):
                if "bestmodel" in filename:
                    await process_model(file_path, filename, directory)
                    x+=1
                    print(x)

    with open(os.path.join(dir_path, "metadata.json"), "w") as outfile:
        json.dump(directory, outfile, indent=4)

if __name__ == "__main__":
    asyncio.run(main())
