import os
from project.core.Config import Config
from project.core.Measure import Measure
from project.core.BaseRenderer import BaseRenderer
from project.core.Font import Font
from project.core.Style import Style
from project.core.Song import Song
from project.core.Section import Section
from project.core.FontStyles import FontStyles
from project.core.SectionLine import SectionLine
from project.renderers.pdf.PdfBox import PdfBox
from fpdf import FPDF


class PdfRenderer(BaseRenderer):
    def __init__(self, config: Config, song: Song):
        super().__init__(config, song)
        self.row = 0
        self.col = 0
        self.x = 0
        self.y = 0
        self.pdf = None
        self.xSpace = 0
        self.rowHeight = 0


    def createPdf(self):
        """
        create new PDF file
        """
        self.pdf = FPDF('L', 'mm', 'A4')

        # load fonts
        fontNames = list()
        for fontStyle in FontStyles:
            fontName = self.config.getProperty('style.' + str(fontStyle.name))[2]
            if not fontName in fontNames:
                self.loadTtfFont(fontName)
                fontNames.append(fontName)

        self.colWidth = self.pdf.w / self.style.columns
        self.pdf.set_line_width(self.style.lineWidth)
        self.xSpace = self.pdf.get_string_width('X')
        self.rowHeight = self.getFontByStyle(FontStyles.LYRICS).Height / self.pdf.k


    def loadTtfFont(self, fontName: str):
        """
        load ttf font from directory
        """
        self.pdf.add_font(fontName, '', self.getFontPath(fontName + '.ttf'), uni=True)
        self.pdf.set_font(fontName.lower(), "")        


    def getFontPath(self, font : str):
        """
        gets font from current work dir
        """
        return os.path.join(os.getcwd(), 'fonts') + os.sep + font


    def getStringWidth(self, text : str, fontStyle : FontStyles):
        """
        gets string width by font style
        """
        self.setFontStyle(fontStyle)
        return self.pdf.get_string_width(text)


    def renderMetadata(self):
        """
        render some metadata as floating line
        """
        metadataRow = self.formatMetadataRow()
        if not metadataRow == '':
            width = self.getStringWidth(metadataRow, FontStyles.METADATA)
            self.drawText(self.pdf.w - width - self.pdf.r_margin, 18, metadataRow, FontStyles.METADATA)
            self.y = self.y + self.pdf.font_size
        self.y = self.y + 2
        

    def getFontByStyle(self, fontStyle: FontStyles):
        """
        create font def by style
        """
        return Font(self.config.getProperty('style.' + str(fontStyle.name)))


    def setFontStyle(self, fontStyle: FontStyles):
        """
        font styles
        """
        font = self.getFontByStyle(fontStyle)
        self.pdf.set_font(font.Name, '', font.Height)
        if font.Color == 'red':
            self.setRedColor()
        else:
            self.setBlackColor()
        return font


    def renderSongHeader(self):
        """
        author + song name
        """
        self.y = self.pdf.t_margin
        self.y = self.y + self.drawText(self.pdf.l_margin, self.y, self.song.getMeta('title'), FontStyles.TITLE).height
        self.y = self.y + self.drawText(self.pdf.l_margin, self.y, self.song.getMeta('artist'), FontStyles.AUTHOR).height

        # line ---------------------
        yLine = 24
        self.pdf.line(self.pdf.l_margin, yLine, self.pdf.w - self.pdf.r_margin, yLine)
        # custom metadata (time: 3/4,....)
        self.renderMetadata()
        self.y = self.calculateStartY()


    def renderSection(self, section : Section):
        """
        render single section
        """
        # check size (is fit?)
        print("renderSection1({}-{}) row:{} col:{}".format(section.getSectionType(), self.formatSectionTitle(section), self.row, self.col))
        if self.isWidow(section):
            self.moveForward()
            print("renderSection2({}-{}) row:{} col:{}".format(section.getSectionType(), self.formatSectionTitle(section), self.row, self.col))

        # ...and content
        self.renderSectionTitle(section)
        for line in section.lines:
            print('Line: [{}]'.format(line.linePosition))
            self.renderSectionLine(line, section)
        print('----------------------')

    
    def renderSectionTitle(self, section: Section):
        """
        render section title
        """
        self.drawText(self.calculateStartX(), self.y, self.formatSectionTitle(section), FontStyles.CHORD)
        self.y = self.y + self.rowHeight
        self.row = self.row + 1


    def isWidow(self, section : Section):
        """
        NEED MORE WORK!!!!!!!!!
        so far, so stupid
        """
        remaining = self.style.maxRows - self.row - len(section.lines)
        return remaining < 3


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
        isLyricsRendered = 0
        isChordRendered = 0
        renderedWidth = 0

        for i in range(0, len(sectionLine.measures)):
            width = 0
            measure = sectionLine.measures[i]
            # format
            chord = self.formatChord(measure.chord)
            lyrics = self.formatLyrics(measure.lyrics)

            k = max(len(chord), len(lyrics))
            chord = chord.ljust(k)
            lyrics = lyrics.ljust(k)

            s = ''
            # chord
            if not chord.strip() == '':
                s = chord
                isChordRendered = 1
                self.drawText(self.x, self.y, chord, FontStyles.CHORD)

            # lyrics
            if not lyrics.strip() == '':
                s = lyrics
                isLyricsRendered = 1
                self.drawText(self.x, self.y + self.rowHeight, lyrics, FontStyles.LYRICS)

            # move x to next position
            width = self.pdf.get_string_width(s)
            if i < len(sectionLine.measures):
                width = width +  (self.xSpace * self.style.xSpaceFactor)
            self.x = self.x + width
            renderedWidth = renderedWidth + width

        # overflows
        if renderedWidth > self.colWidth:
            print('Line:{} [{}] is too wide! please wrap it'.format(sectionLine.linePosition, sectionLine.rawLine))

        renderedRows =  (isChordRendered + isLyricsRendered)
        self.y = self.y + self.rowHeight*renderedRows + (self.rowHeight * 0.6)
        self.row = self.row + renderedRows
        self.handlePossibleOverflow()



    def handlePossibleOverflow(self):
        """
        flow of [rows - cols - pages]
        """
        if self.row >= self.style.maxRows:
            self.row = 0
            self.y = self.calculateStartY()
            self.x = self.calculateStartX()
            self.col = self.col + 1 
            print("+COLUMN {}".format(self.col))

        if self.col >= self.style.columns:
            # owerflow column
            self.y = self.calculateStartY()
            self.addPageWithTitle()
            print("+PAGE {}".format(self.pdf.page_no()))


    def addPageWithTitle(self):
        """
        add new pdf page
        """
        self.y = self.calculateStartY()
        self.x = self.calculateStartX()
        self.col = 0
        self.pdf.add_page('L')
        self.renderSongHeader()


    def drawText(self, x: float, y: float, text:str, fontStyle:FontStyles):
        """
        draw text
        """
        print("[{} {}] x:{:.2f} y:{:.2f}    {}".format(self.row, self.col, x, y, text))
        font = self.setFontStyle(fontStyle)
        self.pdf.text(x, y, text)
        return PdfBox(self.pdf.get_string_width(text), font.Height / self.pdf.k)


    def calculateStartY(self):
        """
        calc start Y
        """
        return 34


    def calculateStartX(self):
        """
        get start x
        """
        return self.pdf.l_margin + (self.col * self.colWidth)


    def setColor(self, color):
        self.pdf.set_text_color(color[0], color[1], color[2])


    def setRedColor(self):
        self.setColor(self.style.red)


    def setBlackColor(self):
        self.setColor(self.style.black)


    def renderSong(self):
        """
        render song in one reusable html block 
        """
        self.createPdf()
        self.addPageWithTitle()

        for section in self.song.sections:
            self.renderSection(section)
        return self.pdf.output('', 'S').encode("latin1")


