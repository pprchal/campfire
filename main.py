import io
import re
from project.core.Parser import Parser
from project.core.HtmlRenderer import HtmlRenderer


def renderSongToHtmlFile(songFileName, htmlFileName):
    """
    render song to output html file
    """
    fin = open(songFileName, "r", encoding="UTF-8")
    fout = open(htmlFileName, "w", encoding="UTF-8")
    fout.write(HtmlRenderer(Parser(fin).parse()).renderSongAsFullHtml())
    fout.close()
    fin.close()


def renderSongToHtml(songContent):
    """
    render song to output html file
    """
    fin = io.StringIO(songContent)
    html = HtmlRenderer(Parser(fin).parse()).renderSongAsFullHtml()
    fin.close()
    return html

# print(renderSongToHtml('[H7]Každej tu[Em/G]černou káru[C9]svou'))
renderSongToHtmlFile('project/test/testFiles/černá kára.cho', 'kara.html')
# renderSongToHtmlFile('project/test/testFiles/abc.cho', 'kara.html')
