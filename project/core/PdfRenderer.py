from project.core.Measure import Measure
from project.core.BaseRenderer import BaseRenderer
from project.core.Style import Style
from project.core.Song import Song
from project.core.Section import Section
from project.core.FontStyles import FontStyles
from project.core.SectionLine import SectionLine
from fpdf import FPDF


class PdfRenderer(BaseRenderer):
    def __init__(self, song: Song, style: Style):
        super().__init__(song, style)
        self.row = 0
        self.col = 0
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
        self.firstPageYOffset = 0


    def createPdf(self):
        """
        create new PDF file
        """
        pdf = FPDF('L', 'mm', 'A4')
        pdf.set_line_width(0.2)
        pdf.add_font('FreeSerif', '', "n:/campfire/freefont-20120503/FreeSerif.ttf", uni=True)
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

            if value == None:
                print('empty metadata: [{}]'.format(key))
                continue

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
            self.setFontStyle(FontStyles.METADATA)
            self.pdf.cell(0, self.y - 25, txt=metadataRow, ln=2, align="R")
            self.y = self.y + self.pdf.font_size

        self.y = self.y + 2
        

    def setFontStyle(self, fontStyle : FontStyles):
        """
        font styles
        """
        if fontStyle == FontStyles.TITLE:
            self.setRedColor()
            self.pdf.set_font_size(24)
        elif fontStyle == FontStyles.AUTHOR:
            self.setRedColor()
            self.pdf.set_font_size(17)
        elif fontStyle == FontStyles.LYRICS:
            self.setBlackColor()
            self.pdf.set_font_size(16)
        elif fontStyle == FontStyles.CHORD:
            self.setRedColor()
            self.pdf.set_font_size(16)
        elif fontStyle == FontStyles.SECTION_NUMBER:
            self.setBlackColor()
            self.pdf.set_font_size(34)
        elif fontStyle == FontStyles.METADATA:
            self.setBlackColor()
            self.pdf.set_font_size(8)



    def renderSongHeader(self):
        """
        author + song name
        """
        self.drawCenteredText(self.y, self.song.getMeta('title'), FontStyles.TITLE)
        self.y = self.y + self.pdf.font_size

        self.drawCenteredText(self.y, self.song.getMeta('artist'), FontStyles.AUTHOR)
        self.y = self.y + self.pdf.font_size

        # custom metadata (time: 3/4,....)
        self.pdf.line(self.pdf.l_margin, self.y, self.pdf.w - self.pdf.r_margin, self.y)

        if self.firstPageYOffset == 0:
            self.firstPageYOffset = self.y
        self.renderMetadata()



    def renderSection(self, section : Section):
        """
        render single section
        """

        # check size (is fit?)
        print("renderSection1({}-{}) row:{} col:{}".format(section.sectionType, section.getSectionTitle(), self.row, self.col))
        if self.isWidow(section):
            self.moveForward()
            print("renderSection2({}-{}) row:{} col:{}".format(section.sectionType, section.getSectionTitle(), self.row, self.col))

        # section number
        if self.row == 0:
            self.drawText(self.calculateStartX() - 10, self.y + 5, self.punctions[section.n], FontStyles.SECTION_NUMBER) 
            self.y = self.calculateStartY()

        # ...and content
        for line in section.lines:
            self.renderSectionLine(line, section)
        print('----------------------')
        print(' ')



    def isWidow(self, section : Section):
        return False
        #remaining = self.style.maxRows - self.row
        #return remaining < self.style.widowRows


    def moveForward(self):
        """
        do owerflow
        """
        self.row = self.style.maxRows + 1
        self.handlePossibleOverflow()


    def renderSectionLine(self, sectionLine : SectionLine, section : Section):
        """
        render song line (chords + lyrics)
        """
        self.x = self.calculateStartX()
        chordDrawed = 0
        lyricsDrawed = 0

        for measure in sectionLine.measures:
            # format
            chord = self.formatChord(measure.chord)
            lyrics = self.formatLyrics(measure.lyrics)

            k = max(len(chord), len(lyrics))
            chord = chord.ljust(k)
            lyrics = lyrics.ljust(k)

            s = ''
            # draw if not empty
            if not chord.strip() == '':
                s = chord
                chordDrawed = 1
                self.drawText(self.x, self.y, chord, FontStyles.CHORD)

            if not lyrics.strip() == '':
                s = lyrics
                lyricsDrawed = 1
                self.drawText(self.x, self.y + 5, lyrics, FontStyles.LYRICS)

            # move x to next postition
            self.x = self.x + self.pdf.get_string_width(s) + self.style.xSpace

        # overflow
        self.handlePossibleOverflow()
        print('  ')

        renderedRows = chordDrawed + lyricsDrawed
        self.row = self.row + renderedRows
        self.y = self.y + (renderedRows * 8)


    def handlePossibleOverflow(self):
        """
        flow of [rows - cols - pages]
        """
        if self.row > self.style.maxRows:
            self.row = 0
            self.y = self.calculateStartY()
            self.x = self.calculateStartX()
            self.col = self.col + 1 
            print("NEW_COLUMN {}".format(self.col))

        if self.col >= self.style.columns:
            # owerflow column
            print("NEW_PAGE {}".format(self.pdf.page_no() + 1))
            self.col = 0
            self.pdf.add_page('L')
            self.renderSongHeader()


    def drawText(self, x, y, text, fontStyle : FontStyles):
        """
        draw text
        """
        print("[{} {}] x:{:.2f} y:{:.2f}    {}".format(self.row, self.col, x, y, text))
        self.setFontStyle(fontStyle)
        self.pdf.text(x, y, text)


    def drawCenteredText(self, y, text, fontStyle : FontStyles):
        """
        draw centered text
        """
        self.setFontStyle(fontStyle)
        tw = self.pdf.get_string_width(text)
        cx = (self.pdf.w / 2) - (tw / 2)
        self.drawText(cx, y, text, fontStyle)


    def calculateStartY(self):
        """
        calc start Y
        """
        # next page(s)
        if self.row > self.style.maxRows and self.col > self.style.columns:
            return self.pdf.t_margin
        # first page
        return 30


    def calculateStartX(self):
        """
        get start x
        """
        colWidth = self.pdf.w / self.style.columns
        return (self.pdf.l_margin + self.style.xSpace) + (self.col * colWidth)


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


