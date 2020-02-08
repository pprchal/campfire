import unittest
from project.core.OutputFormats import OutputFormats
from project.renderers.RendererFactory import RendererFactory
from project.renderers.PdfRenderer import PdfRenderer
from project.core.Config import Config
from project.core.Style import Style

class PdfRendererTests(unittest.TestCase):
    def test_createPdfRenderer(self):
        
        pdfRenderer = RendererFactory.createRenderer(OutputFormats.PDF, Config.fromYaml(), None)
        pdfRenderer.createPdf()
        pdfRenderer.calculateStartX()



