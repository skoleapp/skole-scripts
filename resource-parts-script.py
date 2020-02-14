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


f=open("resource-parts.txt", 'w+')

mypath ='/Users/werneriaa/Documents/Tentit' 
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for i,file_ in enumerate(onlyfiles, start = 1):
    filemodel = model.format(i,i,file_)
    print(filemodel)
    f.write(filemodel)
