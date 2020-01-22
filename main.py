import sys
import io
import os
import re
from project.core.Parser import Parser
from project.core.Style import Style
from project.core.HtmlRenderer import HtmlRenderer
from project.core.PdfRenderer import PdfRenderer
from project.core.Config import Config

def renderSongToHtmlFile(songFileName, htmlFileName):
    """
    render song to output html file
    """
    fin = open(songFileName, "r", encoding="UTF-8")
    fout = open(htmlFileName, "w", encoding="UTF-8")

    config = Config.fromYaml()
    song = Parser(fin, config).parse()
    style = Style.buildFrom(config, song)

    fout.write(HtmlRenderer(config, song, style).renderSongAsFullHtml())
    fout.close()
    fin.close()



def renderSongToPdfFile(songFileName, pdfFileName):
    """
    render song to output html file
    """
    fin = open(songFileName, "r", encoding="UTF-8")
    fout = open(pdfFileName, "wb")

    config = Config.fromYaml()
    song = Parser(fin, config).parse()
    style = Style.buildFrom(config, song)

    buff = PdfRenderer(config, song, style).renderSong().encode("latin1")
    fout.write(buff)
    fout.close()
    fin.close()

renderSongToPdfFile('project/test/testFiles/černá kára.cho', 'kara.pdf')
#renderSongToPdfFile('project/test/testFiles/saro.cho', 'saro.pdf')



