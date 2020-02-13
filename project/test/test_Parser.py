import unittest
from project.core.Parser import Parser
from project.core.Config import Config
from project.core.Song import Song
from project.core.Measure import Measure
from project.core.SectionLine import SectionLine
from project.core.OutputFormats import OutputFormats
from project.renderers.BaseRenderer import BaseRenderer

class ParserTests(unittest.TestCase):
    def createEmptyParser(self):
        return Parser(None, Config.fromYaml())

    def test_sectionLine1(self):
        self.assertListEqual(
            [ Measure('faa ', 'F'), Measure('aaa  ', 'A'), Measure('dd d', 'D')],
            self.createEmptyParser().parseSectionLine('[F]faa [A]aaa  [D]dd d', 1).measures
        )

    def test_sectionLine2(self):
        self.assertListEqual(
            [ Measure('jedna ', ''), Measure('dvě ', 'A'), Measure('Honza jde', 'D')],
            self.createEmptyParser().parseSectionLine('jedna [A]dvě [D]Honza jde', 1).measures
        )

    def test_sectionLine3(self):
        self.assertListEqual(
            [ Measure('dvě ', 'A'), Measure('Honza jde', 'D'), Measure('', 'Hmol7')],
            self.createEmptyParser().parseSectionLine('[A]dvě [D]Honza jde[Hmol7]', 1).measures
        )

    def test_sectionLine4(self):
        self.assertListEqual(
            [ Measure('a ', 'H9+'), Measure('b ', 'Fmi7+'), Measure('', 'Hmol7/G')],
            self.createEmptyParser().parseSectionLine('[H9+]a [Fmi7+]b [Hmol7/G]', 1).measures
        )

    def test_sectionLine5(self):
        self.assertListEqual(
            [ Measure('Každej tu', 'Ab'), Measure('černou káru', 'G#'), Measure('svou', 'Db')],
            self.createEmptyParser().parseSectionLine('[Ab]Každej tu[G#]černou káru[Db]svou', 1).measures
        )      

    def test_sectionLine6(self):
        m = self.createEmptyParser().parseSectionLine('[A]dvě [D]Honza jde[Hmol7]\n', 1).measures[2]
        self.assertEqual('', m.lyrics)

    def test_sectionLine7(self):
        m = self.createEmptyParser().parseSectionLine('[A]dvě [D]Honza jde\n', 1).measures[1]
        self.assertEqual('Honza jde', m.lyrics)

    def test_sectionLine8(self):
        self.assertListEqual(
            [ Measure('a ', 'H9+'), Measure('b ', '⦁'), Measure('', 'Hmol7/G')],
            self.createEmptyParser().parseSectionLine('[H9+]a []b [Hmol7/G]', 1).measures
        )


    def test_processLine1(self):
        s = Song()
        self.createEmptyParser().processLine('{start_of_chorus: Chorus 2} {soc: Chorus 2}', s, 0)
        self.assertEqual('Chorus 2', s.sections[0].name)


    def test_processLine2(self):
        s = Song()
        self.createEmptyParser().processLine('{start_of_chorus}', s, 0)
        self.assertEqual(None, s.sections[0].name)


