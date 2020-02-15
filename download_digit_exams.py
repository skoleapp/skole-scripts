import re
import requests
from requests.exceptions import RequestException

for i in range(1450,1650):
    url = f'https://old.digit.fi/viewexam.php?id={i}&download=1'

    try:
        with requests.get(url) as r:

            fname = ''
            if "Content-Disposition" in r.headers.keys():
                fname = re.findall("filename=(.+)", r.headers["Content-Disposition"])[0]
                fname = fname[1 : -1]
                myfile = requests.get(url)
                fname = fname.replace("/", "-")
                fname = fname.replace("Ã¤", "ä")
                fname = fname.replace("Ã¶", "ö")
                if "iewexam" not in fname:
                    print(fname)
                    print(i)
                    open(f'/Users/werneriaa/Documents/Tentit/{fname}', 'wb').write(myfile.content)

            else:
                fname = url.split("/")[-1]
                fname = fname[1 : -1]
                myfile = requests.get(url)
                fname = fname.replace("/", "-")
                print(myfile)
                fname = fname.replace("Ã¤", "ä")
                fname = fname.replace("Ã¶", "ö")
                if "iewexam" not in fname:
                    open(f'/Users/werneriaa/Documents/Tentit/{fname}', 'wb').write(myfile.content)

    except RequestException as e:
        print(e)