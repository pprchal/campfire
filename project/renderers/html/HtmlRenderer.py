from project.core.Config import Config
from project.core.Measure import Measure
from project.core.Font import Font
from project.core.Style import Style
from project.core.Song import Song
from project.core.Section import Section
from project.core.FontStyles import FontStyles
from project.core.SectionLine import SectionLine
from project.renderers.BaseRenderer import BaseRenderer


class HtmlRenderer(BaseRenderer):
    def __init__(self, config: Config, song: Song):
        super().__init__(config, song)
        self.out = ''

    @property
    def chordSymbols(self):
        return {
            'b': '&#9837;',
            '#': '&#9839;'
        }

    def renderMetadata(self):
        """
        render some metadata as floating line
        """
        metadataRow = self.formatMetadataRow()
        if not metadataRow == '':
            self.drawElement(metadataRow, 'h3')
        

    def renderSongHeader(self):
        """
        author + song name
        """
        self.drawElement(self.song.getMeta('title'), 'h1')
        self.drawElement(self.song.getMeta('artist'), 'h2')
        self.renderMetadata()


    def renderSection(self, section: Section):
        """
        render section
        """
        htmlSection = '<div>\n'
        htmlSection += '<div>{}</div>'.format(self.formatSectionTitle(section))
        nSectionLine = 0

        for line in section.lines:
            htmlSection += '<table>\n'
            htmlChLine, htmlLyLine, hasChord = self.renderSectionLine(line, nSectionLine, section)
            nSectionLine = nSectionLine + 1

            if hasChord:
                htmlSection += '<tr>{}</tr>\n'.format(htmlChLine)
            htmlSection += '<tr>{}</tr>\n'.format(htmlLyLine)
            htmlSection += '</table>\n'

        return htmlSection + '</div>\n'


    def renderSectionLine(self, sectionLine: SectionLine, nSectionLine: int, section: Section):
        """
        render song line (chords + lyrics)
        """
        htmlChLine = ''
        htmlLyLine = ''
        hasChord = False
        nMeasure = 0

        for measure in sectionLine.measures:
            htmlChLine += '<td>{}</td>'.format(self.formatChord(measure.chord))
            htmlLyLine += '<td>{}</td>'.format(self.formatLyrics(measure.lyrics))

            if not measure.chord == '':
                hasChord = True
            nMeasure = nMeasure + 1

        return (htmlChLine, htmlLyLine, hasChord)


    def renderSectionTitle(self, section: Section):
        """
        render section title
        """
        self.drawElement(self.formatSectionTitle(section), 'h4')


    def drawText(self, text:str):
        """
        draw text
        """
        self.out = self.out + text


    def drawElement(self, text:str, element:str):
        """
        draw text
        """
        self.out = self.out + "<{}>{}</{}>\n".format(element, text, element)


    def renderSong(self):
        """
        render song in one reusable html block 
        """
        self.drawText('<head><meta charset=\"utf-8\" /></head>')
        self.renderSongHeader()
        for section in self.song.sections:
            self.drawText(self.renderSection(section))
        self.drawText('</body></html>')
        return self.out.encode()


