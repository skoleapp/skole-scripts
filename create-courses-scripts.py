from os import listdir
from os.path import isfile, join
import re

model = '''
- model: app.Resource
  pk: {}
  fields:
    resource_type: 1
    title: "{}"
    date: "{}"
    course: 1
    user: null
    modified: "2019-01-01 12:00:00.000000+00:00"
    created: "2019-01-01 12:00:00.000000+00:00"
'''

f=open("modelit.txt", 'w+')

mypath ='/Users/werneriaa/Documents/Tentit' 
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for i,file_ in enumerate(onlyfiles, start = 1):
    filemodel = model.format(i,file_[:-15], file_[-14:-4])
    print(filemodel)
    f.write(filemodel)


