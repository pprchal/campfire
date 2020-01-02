from project.core.Measure import Measure
from project.core.BaseRenderer import BaseRenderer
from project.core.Style import Style
from project.core.Song import Song
from project.core.Section import Section
from project.core.SectionLine import SectionLine

class HtmlRenderer(BaseRenderer):
    def __init__(self, song: Song, style: Style):
        super().__init__(song, style)
        self.chordSymbols = {
            'b': '&#9837;',
            '#': '&#9839;'
        }


    def renderFraction(self, fraction):
        """
        render time fraction (2/3)
        """
        split = fraction.split('/')
        return '<sup>{}</sup>&frasl;<sub>{}</sub>'.format(split[0], split[1])


    def renderMetadata(self):
        """
        render some metadata as floating line
        """
        htmlMetadata = '\t<div class="clearfix">\n'
        
        for key in self.style.renderMetadataKeys:
            value = self.song.getMeta(key)
            if not value == None:
                if key == 'time':
                    htmlMetadata += '\t\t<div class="box">{} {}</div>\n'.format('takt', self.renderFraction(value))
                else:
                    htmlMetadata += '\t\t<div class="box">{}</div>\n'.format(value)
        return htmlMetadata + '\t</div>\n\n'


    def renderSection(self, section : Section):
        """
        render single section
        """
        htmlSection = '<div>\n'
        htmlSection += '<p class="numberBox">{}</p>'.format(section.getSectionTitle())
        nSectionLine = 0

        for line in section.lines:
            htmlSection += '<table class="rowPair">\n'
            htmlChLine, htmlLyLine, hasChord = self.renderSectionLine(line, nSectionLine, section)
            nSectionLine = nSectionLine + 1

            if hasChord:
                htmlSection += '<tr class="chordLine">{}</tr>\n'.format(htmlChLine)
            htmlSection += '<tr>{}</tr>\n'.format(htmlLyLine)
            htmlSection += '</table>\n'

        return htmlSection + '</div>\n'


    def renderSectionLine(self, sectionLine : SectionLine, nSectionLine : int, section : Section):
        """
        render song line (chords + lyrics)
        """
        htmlChLine = ''
        htmlLyLine = ''
        hasChord = False
        nMeasure = 0

        for measure in sectionLine.measures:
            htmlChLine += '<td>{}</td>'.format(self.renderChord(measure.chord))
            htmlLyLine += '<td>{}</td>'.format(self.renderLyrics(measure.lyrics))

            if not measure.chord == '':
                hasChord = True
            nMeasure = nMeasure + 1

        return (htmlChLine, htmlLyLine, hasChord)


    def renderChord(self, chord : str):
        """
        render chord - with respect to music notation
        """
        if chord == '':
            return '&nbsp;'

        htmlChord = ''
        for c in chord:
            if c in self.chordSymbols:
                htmlChord += self.chordSymbols[c]
            else:
                htmlChord += c

        return htmlChord


    def renderLyrics(self, lyrics : str):
        """
        render lyrics
        """
        if lyrics == '':
            return '&nbsp;'
        return lyrics


    def renderFullHtmlHead(self):
        """ 
        links stylesheets and so...
        """
        htmlHead = '<head><meta charset=\"utf-8\" /></head>\n'
        htmlHead += '<link rel="stylesheet" href="css/custom.css" >'
        return htmlHead


    def renderSongHeader(self):
        """
        author + song name
        """
        htmlSongHeader = '<div class="songHeader">\n'
        htmlSongHeader += '<h3>{}</h3>\n'.format(self.song.getMeta('title'))
        htmlSongHeader += '<h4>{}</h4>\n'.format(self.song.getMeta('artist'))
        htmlSongHeader += self.renderMetadata()

        htmlSongHeader += '</div>\n'
        return htmlSongHeader


    def renderSongAsHtmlBlock(self):
        """
        render song in one reusable html block 
        """
        htmlSongBlock = '<div>\n'
        htmlSongBlock += self.renderSongHeader()
        htmlSongBlock += '<div style="column-count: {}; column-width: {};">'.format(self.style.columns, self.style.columnWidth)
        for section in self.song.sections:
            htmlSongBlock += self.renderSection(section)
        htmlSongBlock += '</div>'

        htmlSongBlock += '</div>\n\n'
        return htmlSongBlock


    def renderSongAsFullHtml(self):
        """
        render song as one html page
        """
        htmlSong = '<!DOCTYPE html>\n<html>\n'
        htmlSong += self.renderFullHtmlHead()
        htmlSong += '<body>\n'
        htmlSong += self.renderSongAsHtmlBlock()
        htmlSong += '</body>\n</html>'
        return htmlSong



