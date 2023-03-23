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

    def render_metadata(self):
        """
        render some metadata as floating line
        """
        metadataRow = self.formatMetadataRow()
        if not metadataRow == '':
            self.drawElement(metadataRow, 'h3')
        

    def render_song_header(self):
        """
        author + song name
        """
        self.drawElement(self.song.getMeta('title'), 'h1')
        self.drawElement(self.song.getMeta('artist'), 'h2')
        self.renderMetadata()


    def render_section(self, section: Section):
        """
        render section
        """
        htmlSection = '<div>\n'
        htmlSection += '<h4>{}</h4>'.format(self.formatSectionTitle(section))
        nSectionLine = 0

        for line in section.lines:
            htmlSection += '<table>\n'
            htmlChLine, htmlLyLine, hasChord = self.render_section_line(line, nSectionLine, section)
            nSectionLine = nSectionLine + 1

            if hasChord:
                htmlSection += '<tr>{}</tr>\n'.format(htmlChLine)
            htmlSection += '<tr>{}</tr>\n'.format(htmlLyLine)
            htmlSection += '</table>\n'

        return htmlSection + '</div>\n'


    def render_section_line(self, sectionLine: SectionLine, nSectionLine: int, section: Section):
        """
        render song line (chords + lyrics)
        """
        htmlChLine = ''
        htmlLyLine = ''
        hasChord = False
        nMeasure = 0

        for measure in sectionLine.measures:
            htmlChLine += '<td>{}</td>'.format(self.format_chord(measure.chord))
            htmlLyLine += '<td>{}</td>'.format(self.format_lyrics(measure.lyrics))

            if not measure.chord == '':
                hasChord = True
            nMeasure = nMeasure + 1

        return (htmlChLine, htmlLyLine, hasChord)


    def render_section_title(self, section: Section):
        """
        render section title
        """
        self.drawElement(self.formatSectionTitle(section), 'h4')


    def draw_text(self, text:str):
        """
        draw text
        """
        self.out = self.out + text


    def drawElement(self, text:str, element:str):
        """
        draw text
        """
        self.out = self.out + "<{}>{}</{}>\n".format(element, text, element)

    def writeMeta(self):
        html = '<meta charset=\"utf-8\" />'
        for m in self.song.getMetaList():
            html += "<meta name='{}' content='{}' />".format(m[0], m[1])
        return html

    def render_song(self):
        """
        render song in one reusable html block 
        """
        self.draw_text('<html>')
        self.drawElement(self.writeMeta(), 'head')
        self.draw_text('<body>')
        self.render_song_header()
        for section in self.song.sections:
            self.draw_text(self.render_section(section))
        self.draw_text('</body>')
        self.draw_text('</html>')        
        return self.out.encode()


