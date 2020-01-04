import sys
import io
import re
from project.core.Parser import Parser
from project.core.Style import Style
from project.core.HtmlRenderer import HtmlRenderer
from project.core.PdfRenderer import PdfRenderer


def renderSongToHtmlFile(songFileName, htmlFileName):
    """
    render song to output html file
    """
    fin = open(songFileName, "r", encoding="UTF-8")
    fout = open(htmlFileName, "w", encoding="UTF-8")

    song = Parser(fin).parse()
    fout.write(HtmlRenderer(song, Style.fromSong(song)).renderSongAsFullHtml())
    fout.close()
    fin.close()

def renderSongToPdfFile(songFileName, pdfFileName):
    """
    render song to output html file
    """
    fin = open(songFileName, "r", encoding="UTF-8")
    fout = open(pdfFileName, "wb")

    song = Parser(fin).parse()

    buff = PdfRenderer(song, Style.fromSong(song)).renderSong().encode("latin1")
    fout.write(buff)
    fout.close()
    fin.close()

# renderSongToHtmlFile('project/test/testFiles/černá kára.cho', 'kara.html')
# renderSongToHtmlFile('project/test/testFiles/saro.cho', 'saro.html')
# renderSongToHtmlFile('project/test/testFiles/abc.cho', 'kara.html')

renderSongToPdfFile('project/test/testFiles/černá kára.cho', 'ckara.pdf')
renderSongToPdfFile('project/test/testFiles/kára.cho', 'kara.pdf')
