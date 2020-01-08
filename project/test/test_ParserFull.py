print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))

import unittest
from project.core.Parser import Parser
from project.core.Song import Song
from project.core.Measure import Measure
from project.core.SectionLine import SectionLine

class ParserFullTests(unittest.TestCase):
    def test_kara(self):
        fin = open('project/test/testFiles/černá kára.cho', "r", encoding="UTF-8")
        song = Parser(fin).parse()
        fin.close()
        self.assertEqual(True, self.compare_dict({
            "title" : "Černá kára",
            "artist" :"Josef Kainar",
            "time": "4/4",
            "tempo": "120"
        }, song.metadata))
        self.assertEqual(4, len(song.sections))
        self.assertEqual(20, song.sections[0].getRenderableLinesCount())

    def test_full_spec(self):
        fin = open('project/test/testFiles/full_spec.cho', "r", encoding="UTF-8")
        n = Parser(fin).parse()
        fin.close
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
        }, n.metadata))        

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
