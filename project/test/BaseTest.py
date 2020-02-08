import unittest
from project.core.Config import Config
from project.core.Parser import Parser

class BaseTest(unittest.TestCase):
    def createParser(self, f):
        return Parser(f, Config.fromYaml())

    def readSong(self, songFileName:str):
        fin = open(songFileName, "r", encoding="UTF-8")
        song = self.createParser(fin).parse()
        fin.close()    
        return song