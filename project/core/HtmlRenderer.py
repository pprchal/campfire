from project.core.Measure import Measure

class HtmlRenderer:
    def __init__(self, song):
        self.song = song
        self.chordSymbols = {
            'b': '&#9837;',
            '#': '&#9839;'
        }
        self.renderMetadataKeys = ('time', 'tempo', 'capo')


    def renderMetadata(self):
        """
        render some metadata as floating line
        """
        htmlMetadata = '\t<div class="clearfix">\n'
        
        for key in self.renderMetadataKeys:
            value = self.song.getMeta(key)
            if not value == None:
                if key == 'time':
                    htmlMetadata += '\t\t<div class="box">{}: {}</div>\n'.format(key, value)
                else:
                    htmlMetadata += '\t\t<div class="box">{}</div>\n'.format(value)


        return htmlMetadata + '\t</div>\n\n'


    def renderSection(self, section):
        htmlSection = '<div class="section">\n'

        nSectionLine = 0
        for line in section.lines:
            htmlSection += '<table>\n'
            tupl = self.renderLine(line, nSectionLine)
            nSectionLine = nSectionLine + 1

            if tupl[2]:
                htmlSection += '<tr class="chordLine">{}</tr>\n'.format(tupl[0])
            htmlSection += '<tr>{}</tr>\n'.format(tupl[1])
            htmlSection += '</table>\n'

        return htmlSection + "</div>\n"


    def renderLine(self, line, nSectionLine):
        """
        render song line (chords + lyrics)
        """
        htmlChLine = ''
        htmlLyLine = ''
        hasChord = False
        nMeasure = 0
        for measure in line.measures:
            isFirst = nMeasure == 0 and nSectionLine == 0
            htmlChLine += '<td>{}</td>'.format(self.renderChord(measure.chord))
            htmlLyLine += '<td{}>{}</td>'.format(("", ' class="firstLetter"')[isFirst], self.renderLyrics(measure.lyrics))

            if not measure.chord == '':
                hasChord = True
            nMeasure = nMeasure + 1

        return (htmlChLine, htmlLyLine, hasChord)


    def renderChord(self, chord):
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


    def renderLyrics(self, lyrics):
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
        htmlHead += '<link rel="stylesheet" href="css/gutenberg.css" >'
        htmlHead += '<link rel="stylesheet" href="css/themes/oldstyle.css">'
        htmlHead += '<link rel="stylesheet" href="css/pacholek_custom.css" >'
        return htmlHead


    def renderSongHeader(self):
        htmlSongHeader = '<div class="songHeader">\n'
        htmlSongHeader += '<h3>{}, {}</h3>\n'.format(self.song.getMeta('title'), self.song.getMeta('artist'))
        htmlSongHeader += self.renderMetadata()

        htmlSongHeader += '</div>\n'
        return htmlSongHeader


    def renderSongAsHtmlBlock(self):
        """
        render song in one reusable html block 
        """
        htmlSongBlock = '<div>\n'
        htmlSongHeader = self.renderSongHeader()
        if not htmlSongHeader == None:
            htmlSongBlock += htmlSongHeader

        for section in self.song.sections:
            htmlSongBlock += self.renderSection(section)

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



