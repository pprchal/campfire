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
        self.currentRow = 0
        self.currentCol = 0
        self.y = 10
        self.pdf = None
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
        self.punctions = '❶❷❸❹❺❻❼❽❾❿'

        # self.fractionSymbols = {
        #     '4/4': '𝄴',
        #     '2/4': '𝄵'
        # }

    def createPdf(self):
        """
        create new PDF file
        """
        pdf = FPDF('L', 'mm', 'A4')
        pdf.set_line_width(0.2)
        pdf.add_font('FreeSerif', '', "c:\\Data\\campfire\\freefont-20120503\\FreeSerif.ttf", uni=True)
        pdf.set_font("freeserif", "")        
        self.colWidth = pdf.w / self.style.columns
        return pdf



    def formatFraction(self, fraction):
        """
        format time fraction (2/3)
        """
        split = fraction.split('/')
        uppers = ''
        for upper in split[0]:
            uppers += self.upperNumbers[upper]

        lowers = ''
        for lower in split[1]:
            lowers += self.lowerNumbers[lower]

        return '{}⁄{}'.format(uppers, lowers)


    def formatMetadataRow(self):
        """
        formats metadata
        """
        metadataRow = ''
        i = 0
        for key in self.style.renderMetadataKeys:
            value = self.song.getMeta(key)
            if key == 'time':
                metadataRow += self.formatFraction(value)
            else:
                metadataRow += '{}: {}'.format(key, value)

            if i < len(self.style.renderMetadataKeys) - 1:
                metadataRow += '   '
            i = i + 1 

        return metadataRow



    def renderMetadata(self):
        """
        render some metadata as floating line
        """
        self.setBlackColor()
        metadataRow = self.formatMetadataRow()

        if not metadataRow == '':
            self.pdf.set_font_size(8)
            self.pdf.cell(0, self.y - 25, txt=metadataRow, ln=2, align="R")
            self.y = self.y + self.pdf.font_size

        self.y = self.y + 2
        
    
    def renderSongHeader(self):
        """
        author + song name
        """
        self.setRedColor()
        self.pdf.set_font_size(24)
        self.pdf.cell(0, self.y, txt=self.song.getMeta('title'), ln=1, align="C")
        self.y = self.y + self.pdf.font_size

        self.pdf.get_string_width(self.song.getMeta('title'))
        self.pdf.set_font_size(17)
        self.pdf.cell(0, 2, txt=self.song.getMeta('artist'), ln=2, align="C")
        self.y = self.y + self.pdf.font_size

        # custom metadata (time: 3/4,....)
        self.pdf.line(self.pdf.l_margin, self.y, self.pdf.w - self.pdf.r_margin, self.y)
        self.renderMetadata()



    def renderSection(self, section : Section):
        """
        render single section
        """
        ## self.renderSectionTitle(section) # sloka 1, ref: 1
        startX = self.pdf.l_margin
        x = startX

        self.pdf.set_font_size(34)
        self.pdf.text(x, self.y + 5, self.punctions[section.n])

        # Am             C  
        # Dneska už mně  ňák nejdou
        self.pdf.set_font_size(16)
        for line in section.lines:
            self.renderSectionLine(line, section)


    def renderSectionLine(self, sectionLine : SectionLine, section : Section):
        """
        render song line (chords + lyrics)
        """
        n = 0
        startX = self.pdf.l_margin + 10
        x = startX
        xSpace = 10

        self.pdf.set_font_size(16)
        for measure in sectionLine.measures:
            chord = self.formatChord(measure.chord)
            lyrics = self.formatLyrics(measure.lyrics)

            k = max(len(chord), len(lyrics))
            chord = chord.ljust(k)
            lyrics = lyrics.ljust(k)

            self.setRedColor()
            self.pdf.text(x, self.y, chord)

            self.setBlackColor()
            self.pdf.text(x, self.y + 5, lyrics)

            x = x + self.pdf.get_string_width(lyrics) + xSpace

            if self.y > 200:
                self.pdf.add_page('L')
                self.y = 10

            n = n + 1
        self.y = self.y + 16



    def formatChord(self, chord : str):
        """
        render chord - with respect to music notation
        """
        if chord == '':
            return ''

        pdfChord = ''
        for c in chord:
            if c in self.chordSymbols:
                c = self.chordSymbols[c]
            elif c in self.lowerNumbers:
                c = self.lowerNumbers[c]

            pdfChord += c

        return pdfChord


    def setColor(self, color):
        self.pdf.set_text_color(color[0], color[1], color[2])


    def setRedColor(self):
        self.setColor(self.style.red)


    def setBlackColor(self):
        self.setColor(self.style.black)


    def formatLyrics(self, lyrics : str):
        """
        render lyrics
        """
        if lyrics == '':
            return ''
        return lyrics


    def renderSong(self):
        """
        render song in one reusable html block 
        """
        self.pdf = self.createPdf()
        self.pdf.add_page()
        self.renderSongHeader()

        for section in self.song.sections:
            self.renderSection(section)
            
        return self.pdf.output('', 'S')


