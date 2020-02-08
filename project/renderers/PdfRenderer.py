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
from project.renderers.PdfBox import PdfBox
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
        self.pdf.set_font(font.Name)
        self.pdf.set_font_size(font.Height)
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
        self.pdf.line(self.pdf.l_margin, self.y, self.pdf.w - self.pdf.r_margin, self.y)
        # custom metadata (time: 3/4,....)
        self.renderMetadata()


    def renderSection(self, section : Section):
        """
        render single section
        """
        self.renderSectionTitle(section)

        # check size (is fit?)
        print("renderSection1({}-{}) row:{} col:{}".format(section.sectionType, section.getSectionTitle(), self.row, self.col))
        if self.isWidow(section):
            self.moveForward()
            print("renderSection2({}-{}) row:{} col:{}".format(section.sectionType, section.getSectionTitle(), self.row, self.col))

        # ...and content
        for line in section.lines:
            self.renderSectionLine(line, section)
        print('----------------------')

    
    def renderSectionTitle(self, section: Section):
        """
        render section title
        """
        self.drawText(self.calculateStartX(), self.y, "---" + section.getSectionTitle() + "---", FontStyles.CHORD)
        self.y = self.y + 12


    def isWidow(self, section : Section):
        """
        NEED MORE WORK!!!!!!!!!
        so far, so stupid
        """
        return False
        #remaining = self.style.maxRows - self.row


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
            self.x = self.x + self.pdf.get_string_width(s) + (self.xSpace * self.style.xSpaceFactor)

        # overflow
        self.handlePossibleOverflow()

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
            self.addPageWithTitle()
            print("NEW_PAGE {}".format(self.pdf.page_no()))


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
        return 30


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


