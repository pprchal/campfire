print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))

import unittest
from project.core.Parser import Parser
from project.core.Song import Song
from project.core.Measure import Measure
from project.core.SectionLine import SectionLine

class ParserTests(unittest.TestCase):
    def test_sectionLine1(self):
        self.assertListEqual(
            [ Measure('faa ', 'F'), Measure('aaa  ', 'A'), Measure('dd d', 'D')],
            Parser('').parseSectionLine('[F]faa [A]aaa  [D]dd d').measures
        )

    def test_sectionLine2(self):
        self.assertListEqual(
            [ Measure('jedna ', ''), Measure('dvě ', 'A'), Measure('Honza jde', 'D')],
            Parser('').parseSectionLine('jedna [A]dvě [D]Honza jde').measures
        )

    def test_sectionLine3(self):
        self.assertListEqual(
            [ Measure('dvě ', 'A'), Measure('Honza jde', 'D'), Measure('', 'Hmol7')],
            Parser('').parseSectionLine('[A]dvě [D]Honza jde[Hmol7]').measures
        )

    def test_sectionLine4(self):
        self.assertListEqual(
            [ Measure('a ', 'H9+'), Measure('b ', 'Fmi7+'), Measure('', 'Hmol7/G')],
            Parser('').parseSectionLine('[H9+]a [Fmi7+]b [Hmol7/G]').measures
        )

    def test_sectionLine5(self):
        self.assertListEqual(
            [ Measure('Každej tu', 'Ab'), Measure('černou káru', 'G#'), Measure('svou', 'Db')],
            Parser('').parseSectionLine('[Ab]Každej tu[G#]černou káru[Db]svou').measures
        )      

    def test_sectionLine6(self):
        m = Parser('').parseSectionLine('[A]dvě [D]Honza jde[Hmol7]\n').measures[2]
        self.assertEqual('', m.lyrics)

    def test_sectionLine7(self):
        m = Parser('').parseSectionLine('[A]dvě [D]Honza jde\n').measures[1]
        self.assertEqual('Honza jde', m.lyrics)

    def test_sectionLine8(self):
        self.assertListEqual(
            [ Measure('a ', 'H9+'), Measure('b ', '⦁'), Measure('', 'Hmol7/G')],
            Parser('').parseSectionLine('[H9+]a []b [Hmol7/G]').measures
        )

    def test_processLine1(self):
        s = Song()
        Parser(None).processLine('{start_of_chorus: Chorus 2} {soc: Chorus 2}', s, 0)
        self.assertEqual('Chorus 2', s.sections[0].name)


    def test_processLine2(self):
        s = Song()
        Parser(None).processLine('{start_of_chorus}', s, 0)
        self.assertEqual(None, s.sections[0].name)


