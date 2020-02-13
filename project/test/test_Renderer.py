import unittest
from project.core.Parser import Parser
from project.core.Config import Config
from project.core.Song import Song
from project.core.Measure import Measure
from project.core.SectionLine import SectionLine
from project.core.OutputFormats import OutputFormats
from project.renderers.BaseRenderer import BaseRenderer


class RendererTests(unittest.TestCase):
    def createEmptyParser(self):
        return Parser(None, Config.fromYaml())

    def test_formatChord(self):
        self.assertEqual('E♭dim7', BaseRenderer(Config.fromYaml(), None).formatChord('Ebdim7'))



