import os
import yaml
from os.path import exists
from pathlib import Path

class Config:
    def __init__(self, yamlDoc):
        self.props = dict()
        self.yamlDoc = yamlDoc

    def getProperty(self, keyPath : str):
        """
        get cached property
        """
        if keyPath in self.props:
            return self.props[keyPath]

        container = self.yamlDoc
        partialKey = ''
        for partialKey in keyPath.split('.'):
            if partialKey in container:
                container = container[partialKey]
            else:
                container = None
                break

        self.props.update({keyPath: container})
        return container


    def setProperty(self, keyPath : str, value):
        """
        save property
        """
        self.props.update({keyPath: value})


    @classmethod
    def toDict(cls, inlist):
        d = dict()
        if isinstance(inlist, list):
            for li in inlist:
                d.update(li)
        return d

    @classmethod 
    def getConfigPath(cls):
        fullPath = os.path.join(Path.home(), '.campfire.yaml')
        if exists(fullPath):
            return fullPath

        return os.path.join(os.getcwd(), '.campfire.yaml')

    @classmethod
    def fromYaml(cls):
        print('loading: ' + Config.getConfigPath())
        with open(Config.getConfigPath(), encoding="utf8") as f:
            return Config(yaml.load(f, Loader=yaml.FullLoader))
