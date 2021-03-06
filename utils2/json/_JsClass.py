import json
from os import path
from utils2.system.paths import Path


class JsHandler:
    def __init__(self, file_name):
        if isinstance(file_name, Path):
            self.file = file_name.path
        else:
            self.file = file_name

        if path.isfile(self.file):
            self.__loadFile()
        else:
            with open(self.file, 'w+') as f:
                json.dump({}, f, indent=4)

    def __loadFile(self) -> dict:
        fl = open(self.file, 'r+')
        return json.load(fl)

    def __dump(self, newDict):
        try:
            json.dumps(newDict)
        except Exception:
            raise Exception('Unable to convert dictionary into JSON data')

        with open(self.file, 'w+') as file:
            json.dump(newDict, file, indent=4)

    def __getitem__(self, item):
        internal_json_dict = self.__loadFile()
        requestItem = internal_json_dict[item]
        return requestItem

    def __setitem__(self, key, value):
        Js = self.__loadFile()
        Js[key] = value
        self.__dump(Js)

    def __delitem__(self, key):
        Js = self.__loadFile()
        Js.pop(key)
        self.__dump(Js)

    def __contains__(self, item):
        return item in self.__loadFile()

    def __iter__(self):
        return iter(self.__loadFile())


    def __enter__(self):
        return self.__loadFile()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def update(self, updatedDict):
        Js = self.__loadFile()
        Js.update(updatedDict)
        self.__dump(Js)

    def getDict(self) -> dict:
        return self.__loadFile()

    def keys(self):
        return self.__loadFile().keys()

    def pop(self, key):
        Js = self.__loadFile()
        Js.pop(key)
        self.__dump(newDict=Js)
