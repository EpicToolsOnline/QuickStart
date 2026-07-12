#This is my test zone to test stuff

import subprocess
import json

with open("chosenapps.json") as f:
    apps = json.load(f)

for name, package_id in apps.items():
    result = subprocess.run(["winget", "install", "--id", package_id, "-e"], capture_output=True, text=True)
    print(result.stdout)