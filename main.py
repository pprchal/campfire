import sys
import io
import re
from project.core.Parser import Parser
from project.core.Style import Style
from project.core.HtmlRenderer import HtmlRenderer


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

# fin = io.StringIO(songContent)
# print(renderSongToHtml('[H7]Každej tu[Em/G]černou káru[C9]svou'))

print(sys.argv[0])
renderSongToHtmlFile('project/test/testFiles/černá kára.cho', 'kara.html')
renderSongToHtmlFile('project/test/testFiles/saro.cho', 'saro.html')
# renderSongToHtmlFile('project/test/testFiles/abc.cho', 'kara.html')
