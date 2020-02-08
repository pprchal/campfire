import unittest
from project.core.OutputFormats import OutputFormats
from project.renderers.RendererFactory import RendererFactory
from project.renderers.PdfRenderer import PdfRenderer

class RendererFactoryTests(unittest.TestCase):
    def test_createPdfRenderer(self):
        pdfRenderer = RendererFactory.createRenderer(OutputFormats.PDF, None, None, None)
        self.assertIsNotNone(pdfRenderer)
        self.assertIsInstance(pdfRenderer, PdfRenderer) 



