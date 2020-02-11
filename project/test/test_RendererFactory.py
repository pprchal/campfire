import unittest
from project.test.BaseTest import BaseTest
from project.core.OutputFormats import OutputFormats
from project.core.Config import Config
from project.renderers.RendererFactory import RendererFactory
from project.renderers.pdf.PdfRenderer import PdfRenderer
from project.renderers.txt.TxtRenderer import TxtRenderer

class RendererFactoryTests(BaseTest):
    def test_createPdfRenderer(self):
        pdfRenderer = RendererFactory.createRenderer(OutputFormats.PDF, Config.fromYaml(), None)
        self.assertIsNotNone(pdfRenderer)
        self.assertIsInstance(pdfRenderer, PdfRenderer) 


    def test_createTxtRenderer(self):
        txtRenderer = RendererFactory.createRenderer(OutputFormats.TXT, Config.fromYaml(), None)
        self.assertIsNotNone(txtRenderer)
        self.assertIsInstance(txtRenderer, TxtRenderer) 


