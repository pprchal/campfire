import unittest
from project.core.Parser import Parser
from project.core.Config import Config
from project.renderers.BaseRenderer import BaseRenderer


class RendererTests(unittest.TestCase):
    def createEmptyParser(self):
        return Parser(None, Config.fromYaml())

    def format_chord(self):
        self.assertEqual('E♭dim7', BaseRenderer(Config.fromYaml(), None).format_chord('Ebdim7'))



