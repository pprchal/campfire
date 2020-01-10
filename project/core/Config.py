import os
import yaml

class Config:
    def __init__(self):
        self.props = dict()
        self.yamlDoc = None

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
    def fromYaml(cls):
        fullPath = os.getcwd() + os.sep + 'config.yaml'
        config = Config()
        with open(fullPath, encoding="utf8") as f:
            config.yamlDoc = yaml.load(f, Loader=yaml.FullLoader)

        return config


