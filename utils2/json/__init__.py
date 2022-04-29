import json
from ._JsClass import JsHandler


def loadFile(file_path) -> dict:
    file = open(file_path, 'r+')
    JsData = json.load(file)
    file.close()
    return JsData


def dumpToFile(file, Js: dict):
    if isinstance(file, str):
        with open(file, 'w') as file:
            json.dump(Js, file, indent=4)
    else:
        file.seek(0)
        json.dump(Js, file, indent=4)


def update_file(data: dict, file_path):
    with open(file_path, 'r+') as file:
        JsF = json.load(file)
        JsF.update(data)

        file.seek(0)
        json.dump(JsF, file, indent=4)
        file.close()


def appendToList(key, file_name, list_content):
    Js = loadFile(file_name)

    Js[key].append(list_content)
    dumpToFile(file=file_name, Js=Js)


def getValue(key, file_name):
    Js = loadFile(file_name)
    return Js[key]


def setValue(key, value, file_name):
    Js = loadFile(file_name)
    Js[key] = value
    dumpToFile(file=file_name, Js=Js)

