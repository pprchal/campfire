import unittest
from project.core.Parser import Parser
from project.core.Config import Config
from project.core.Song import Song
from project.renderers.BaseRenderer import BaseRenderer
from project.songbook.PdfSongBook import PdfSongBook

class test_PdfSongBook(unittest.TestCase):
    def test_renderSongBook(self):
        songMetadata = PdfSongBook().loadPdfMetadata('project/test/testFiles/Lagrima.pdf')
        print(songMetadata)
        self.assertEqual('Lágrima', songMetadata.name)
        self.assertEqual('Preludio', songMetadata.typeSong)
        self.assertEqual('Francisco Tárrega', songMetadata.author)



