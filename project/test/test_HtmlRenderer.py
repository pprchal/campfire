print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))

import unittest
from project.core.HtmlRenderer import HtmlRenderer
from project.core.Measure import Measure
from project.core.SectionLine import SectionLine

class HtmlRendererTests(unittest.TestCase):
    def test_simple(self):
        self.assertEqual('C', HtmlRenderer(None, None).renderChord('C'))
        self.assertEqual('Dm', HtmlRenderer(None, None).renderChord('Dm'))

    def test_flat(self):
        self.assertEqual('D&#9837;', HtmlRenderer(None, None).renderChord('Db'))
        self.assertEqual('Fm7&#9839;', HtmlRenderer(None, None).renderChord('Fm7#'))

if __name__ == '__main__':
    unittest.main()