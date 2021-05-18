import unittest
from project.test.BaseTest import BaseTest
from project.core.OutputFormats import OutputFormats
from project.core.Config import Config
from project.renderers.RendererFactory import RendererFactory

class RendererFactoryTests(BaseTest):
    def test_allAvailableRendereds(self):
        for outputFormat in OutputFormats:
            renderer = RendererFactory.createRenderer(outputFormat, Config.fromYaml(), None)
            self.assertIsNotNone(renderer)

