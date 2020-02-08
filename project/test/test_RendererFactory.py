import unittest
from project.test.BaseTest import BaseTest
from project.core.OutputFormats import OutputFormats
from project.core.Config import Config
from project.renderers.RendererFactory import RendererFactory
from project.renderers.PdfRenderer import PdfRenderer

class RendererFactoryTests(BaseTest):
    def test_createPdfRenderer(self):
        pdfRenderer = RendererFactory.createRenderer(OutputFormats.PDF, Config.fromYaml(), None)
        self.assertIsNotNone(pdfRenderer)
        self.assertIsInstance(pdfRenderer, PdfRenderer) 



