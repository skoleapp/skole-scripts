import os
import re
from pathlib import Path

import requests
from requests.exceptions import RequestException

filepath = f"{Path.home()}/Downloads/resources"
os.mkdir(filepath)


for i in range(1,2000):
    url = f"https://old.digit.fi/viewexam.php?id={i}&download=1"

    try:
        with requests.get(url) as r:

            fname = ""
            if "Content-Disposition" in r.headers.keys():
                fname = re.findall("filename=(.+)", r.headers["Content-Disposition"])[0]
            else:
                fname = url.split("/")[-1]
            fname = fname[1 : -1]
            myfile = requests.get(url)
            fname = fname.replace("/", "-")
            fname = fname.replace("Ã¤", "a")
            fname = fname.replace("Ã¶", "o")
            fname = fname.replace("__", "_")
            if "iewexam" not in fname:
                print(i, fname)
                with open(f"{filepath}/{fname}", "xb") as f:
                    f.write(myfile.content)

    except (FileExistsError, RequestException) as e:
        print(str(e))
