from project.core.SongBookMetadata import SongBookMetadata
import logging
import PyPDF2 

class PdfSongBook:
    def loadPdfMetadata(self, pdfPath):
        pdfFileObj = open(pdfPath, 'rb') 

        pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
        logging.debug('PDF: {} opened pages: {}'.format(pdfPath, pdfReader.numPages))

        pageObj = pdfReader.getPage(0) 
        splits = pageObj.extractText().split('\n')
        pdfFileObj.close() 

        return SongBookMetadata(splits[0], splits[2], splits[1])




        