from os import listdir
from os.path import isfile, join
import re

model = '''
- model: app.ResourceFile
  pk: {}
  fields:
    resource: {}
    file: "media/uploads/resource_parts/{}"
    '''


f = open("resource-parts.txt", 'w+')

mypath = '/Users/werneriaa/Documents/Tentit'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
i = 1
for file_ in onlyfiles:
    if ".DS" in file_:
        continue
    filemodel = model.format(i, i, file_)
    i = i + 1
    print(filemodel)
    f.write(filemodel)
