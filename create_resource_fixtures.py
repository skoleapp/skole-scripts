from os import listdir
from os.path import isfile, join
import re
import yaml

model = '''
- model: app.Resource
  pk: {}
  fields:
    resource_type: 1
    title: "{}"
    date: "{}"
    course: {}
    user: null
    modified: "2019-01-01 12:00:00.000000+00:00"
    created: "2019-01-01 12:00:00.000000+00:00"
'''


def create_resources(model):
    f = open("modelit.txt", 'w+')
    count = 0
    mypath = '/Users/werneriaa/Documents/Tentit'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    coursedict = create_course_dict()
    i = 1
    for file_ in onlyfiles:
        if ".DS" in file_:
            continue
        title = file_[:-15]
        title = title.replace("_", " ")
        if "Tentti" in title:
            if "Liiketoimintaosaaminen" in title:
                newtitle = title.split(" ")
            else:
                newtitle = title.split(" Tentti")
            # print(newtitle[0])
            try:
                tit = newtitle[0].replace("ä", "ä").replace("ö", "ö")
                filemodel = model.format(
                    i, title, file_[-14:-4], coursedict[tit])
                print(filemodel)
                f.write(filemodel)
                i = i + 1
            except KeyError as e:
                print(e)
                print(file_)
        elif "Välikoe" in title:
            newtitle = title.split(" Välikoe")
            try:
                tit = newtitle[0].replace("ä", "ä").replace("ö", "ö")
                filemodel = model.format(
                    i, title, file_[-14:-4], coursedict[tit])
                print(filemodel)
                f.write(filemodel)
                i = i + 1
            except KeyError as e:
                print(e)
                print(file_)


def create_exam_list():
    mypath = '/Users/werneriaa/Documents/Tentit'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    count = 0
    course_list = []
    for i, file_ in enumerate(onlyfiles, start=1):
        title = file_[:-15]
        title = title.replace("_", " ")
        if "Tentti" in title:
            x = title.split("Tentti")
            print(x[0])
            count = count + 1
        elif "Välikoe" in title:
            x = title.split("Välikoe")
            print(x[0])
            count = count + 1

    print(count)


def create_course_dict():

    with open("courses.yaml", 'r') as stream:
        x = yaml.safe_load(stream)
        coursedict = {}
        for i in x:
            try:
                coursedict.update({i['fields']['name']: i['pk']})
            except yaml.YAMLError as exc:
                print(exc)
    return coursedict


create_resources(model)
