import json
import os
import tellurium as te

dict = json.loads(open("metadata.json").read())
set = {"placeholder"}
set2 = {"placeholder"}
for i in dict:
    set.add(i["path"].split("/")[0])



