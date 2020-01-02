from project.core.Measure import Measure
from project.core.BaseRenderer import BaseRenderer
from project.core.Style import Style
from project.core.Song import Song
from project.core.Section import Section
from project.core.SectionLine import SectionLine
from fpdf import FPDF


class PdfRenderer(BaseRenderer):
    def __init__(self, song: Song, style: Style):
        super().__init__(song, style)
        self.pdf = None
        self.currentY = 0
        self.chordSymbols = {
            'b': '♭',
            '#': '♯'
        }
        self.upperNumbers = {
            '0': '⁰',
            '1': '¹',
            '2': '²',
            '3': '³',
            '4': '⁴',
            '5': '⁵',
            '6': '⁶',
            '7': '⁷',
            '8': '⁸',
            '9': '⁹',
        }
        self.lowerNumbers = {
            '0': '₀',
            '1': '₁',
            '2': '₂',
            '3': '₃',
            '4': '₄',
            '5': '₅',
            '6': '₆',
            '7': '₇',
            '8': '₈',
            '9': '₉',
        }

    def openPdf(self):
        self.pdf = FPDF('L')
        self.pdf.set_line_width(0.2)
        self.pdf.add_font('FreeSerif', '', "c:\\Data\\campfire\\freefont-20120503\\FreeSerif.ttf", uni=True)
        self.pdf.add_font('FreeSerifBold', '', "c:\\Data\\campfire\\freefont-20120503\\FreeSerifBold.ttf", uni=True)


    def renderChord(self, chord : str):
        """
        render chord - with respect to music notation
        """
        if chord == '':
            return ''

        pdfChord = ''
        for c in chord:
            if c in self.chordSymbols:
                pdfChord += self.chordSymbols[c]
            else:
                pdfChord += c

        return pdfChord


    def renderFraction(self, fraction):
        """
        render time fraction (2/3)
        """
        split = fraction.split('/')
        uppers = ''
        for upper in split[0]:
            uppers += self.upperNumbers[upper]

        lowers = ''
        for lower in split[1]:
            lowers += self.lowerNumbers[lower]

        return '{}⁄{}'.format(uppers, lowers)


    def renderMetadata(self):
        """
        render some metadata as floating line
        """
        self.pdf.set_text_color(0, 0, 0)
        metadataRow = ''
        for key in self.style.renderMetadataKeys:
            value = self.song.getMeta(key)
            if not value == None:
                if key == 'time':
                    metadataRow =  metadataRow + '{}: {}  '.format(key, self.renderFraction(value))
                else:
                    metadataRow =  metadataRow + '{}: {}  '.format(key, value)

        if not metadataRow == '':
            self.pdf.set_font("freeserif", "", 8)
            self.pdf.cell(0, self.currentY, txt=metadataRow, ln=1, align="R")
            self.pdf.line(10, self.currentY, self.style.pageWidth, self.currentY)

            self.currentY = self.pdf.y
        
    
    def renderSongHeader(self):
        """
        author + song name
        """
        self.pdf.set_text_color(255, 0, 0)
        self.pdf.set_font("freeserif", "", 24)
        title = self.song.getMeta('title')
        if not title == None:
            self.pdf.cell(0, self.currentY, txt=title, ln=1, align="C")
            self.currentY = self.pdf.y

        artist = self.song.getMeta('artist')
        if not artist == None:
            self.pdf.set_font("freeserif", "", 17)
            self.pdf.cell(0, self.currentY + 2, txt=artist, ln=1, align="C")
            self.currentY = self.pdf.y

        # custom metadata (time: 3/4,....)
        self.renderMetadata()

        # self.pdf.set_draw_color(0, 0, 0)
        # self.pdf.line(10, self.currentY, self.style.pageWidth, self.currentY)


    def renderSectionTitle(self, section: Section):
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.set_font("freeserif", "", 18)
        self.pdf.cell(0, 10, txt=section.getSectionTitle(), ln=1)
        self.currentY = self.currentY + 18


    def renderSection(self, section : Section):
        """
        render single section
        """
        self.renderSectionTitle(section) # sloka 1, ref: 1
        # htmlSection += '<p class="numberBox">{}</p>'.format(section.getSectionTitle())
        nSectionLine = 0

        for line in section.lines:
            # htmlSection += '<table class="rowPair">\n'
            htmlChLine, htmlLyLine, hasChord = self.renderSectionLine(line, nSectionLine, section)
            nSectionLine = nSectionLine + 1

            # if hasChord:
            #     tmlSection += '<tr class="chordLine">{}</tr>\n'.format(htmlChLine)
            # htmlSection += '<tr>{}</tr>\n'.format(htmlLyLine)
            # htmlSection += '</table>\n'


    def renderLyrics(self, lyrics : str):
        """
        render lyrics
        """
        if lyrics == '':
            return ''
        return lyrics



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



    def renderSong(self):
        """
        render song in one reusable html block 
        """
        self.openPdf()
        self.pdf.add_page()
        self.renderSongHeader()

        for section in self.song.sections:
            self.renderSection(section)
        self.pdf.output("name.pdf")


