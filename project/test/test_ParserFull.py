import unittest

from project.core.Config import Config
from project.core.Measure import Measure
from project.core.Parser import Parser
from project.core.SectionLine import SectionLine
from project.core.Song import Song
from project.test.BaseTest import BaseTest


class ParserFullTests(BaseTest):
    def createParser(self, f):
        return Parser(f, Config.fromYaml())
        

    def test_kara(self):
        song = self.readSong('project/test/testFiles/černá kára.cho')
        self.assertEqual(True, self.compare_dict({
            "title" : "Černá kára",
            "artist" :"Josef Kainar",
            "time": "4/4",
            "tempo": "120"
        }, song.metadata))

        self.assertFalse('end_of_verse' in song.metadata.keys())
        self.assertEqual(5, len(song.sections))
        self.assertEqual(18, song.sections[0].getRenderableLinesCount())


    def test_newPageShouldBeSection(self):
        song = self.readSong('project/test/testFiles/newpage.cho')
        self.assertFalse('end_of_verse' in song.metadata.keys())
        self.assertEqual(3, len(song.sections))


    def test_full_spec(self):
        song = self.readSong('project/test/testFiles/full_spec.cho')
        self.assertEqual(True, self.compare_dict({
            "title" : "Swing Low Sweet Chariot",
            "subtitle" :"2nd Movement",
            "artist": "Leonard Cohen",
            "composer": "Leonard Cohen",
            "lyricist": "Leonard Nijgh",
            "copyright": "year owner",
            "year": "2016",
            "key": "C",
            "time": "4/4",
            "duration": "268",
            "capo": "2",
            "tempo": "120"
        }, song.metadata))        

    def compare_dict(self, dict1, dict2):
        allSame = True
        for x1 in dict1.keys():
            z = dict1.get(x1) == dict2.get(x1)
            if not z:
                allSame = False
                print('expected: key', x1)
                print('value A', dict1.get(x1), '\nvalue B', dict2.get(x1))
                print('-----\n')

        return allSame

    def compare_measures(self, m1, m2):
        self.assertEqual(m1.chord, m2.chord)
        self.assertEqual(m1.lyrics, m2.lyrics)
