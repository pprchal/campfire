import os

from fpdf import FPDF

from project.core.Config import Config
from project.core.Font import Font
from project.core.FontStyles import FontStyles
from project.core.Section import Section
from project.core.SectionLine import SectionLine
from project.core.Song import Song
from project.renderers.BaseRenderer import BaseRenderer
from project.renderers.pdf.PdfBox import PdfBox
from project.core.Transpose import Transpose

class PdfRenderer(BaseRenderer):
    def __init__(self, config: Config, song: Song):
        super().__init__(config, song)
        self.row = 0
        self.col = 0
        self.x = 0
        self.y = 0
        self.pdf = None # type: FPDF
        self.xSpace = 0
        self.rowHeight = 0

    def render_song(self):
        """
        render song in one reusable html block 
        """
        self.create_pdf()
        self.add_page_with_title()
        for self.section in range(0, len(self.song.sections)):
            if self.song.sections[self.section].sectionType == "new_page":
                self.add_page_with_title()
                continue

            self.render_section(self.song.sections[self.section])
        return self.pdf.output('', 'S').encode("latin1")
    
    def create_pdf(self):
        """
        create new PDF file
        """
        self.pdf = FPDF('L', 'mm', 'A4')

        # load fonts
        fontNames = list()
        for fontStyle in FontStyles:
            fontName = self.config.getProperty('style.' + str(fontStyle.name))[2]
            if not fontName in fontNames:
                self.load_ttf_font(fontName)
                fontNames.append(fontName)

        self.colWidth = self.pdf.w / self.style.columns
        self.pdf.set_line_width(self.style.lineWidth)
        self.xSpace = self.pdf.get_string_width('X')
        self.rowHeight = self.getFontByStyle(FontStyles.LYRICS).Height / self.pdf.k

    def load_ttf_font(self, fontName: str):
        """
        load ttf font from directory
        """
        self.pdf.add_font(fontName, '', self.get_font_path(fontName + '.ttf'), uni=True)
        self.pdf.set_font(fontName.lower(), "")        


    def get_font_path(self, font : str):
        """
        gets font from current work dir
        """
        return os.path.join(os.getcwd(), 'fonts', font)


    def get_string_width(self, text : str, fontStyle : FontStyles):
        """
        gets string width by font style
        """
        self.set_font_style(fontStyle)
        return self.pdf.get_string_width(text)


    def render_metadata(self):
        """
        render some metadata as floating line
        """
        metadataRow = self.formatMetadataRow()
        if not metadataRow == '':
            width = self.get_string_width(metadataRow, FontStyles.METADATA)
            self.draw_text(self.pdf.w - width - self.pdf.r_margin, 18, metadataRow, FontStyles.METADATA)
            self.y = self.y + self.pdf.font_size
        self.y = self.y + 2
        

    def getFontByStyle(self, fontStyle: FontStyles):
        """
        create font def by style
        """
        return Font(self.config.getProperty('style.' + str(fontStyle.name)))


    def set_font_style(self, fontStyle: FontStyles):
        """
        font styles
        """
        font = self.getFontByStyle(fontStyle)
        self.pdf.set_font(font.Name, '', font.Height)
        if font.Color == 'red':
            self.setRedColor()
        elif font.Color == 'black':
            self.setBlackColor()
        else:
            self.log(f'unkonwn color {font.Color}')

        return font


    def render_song_header(self):
        """
        author + song name
        """
        self.y = self.pdf.t_margin
        self.pdf.line(self.pdf.l_margin, 5, self.pdf.w - self.pdf.r_margin, 5)
        self.y = self.y + 5
        self.y = self.y + self.draw_text(self.pdf.l_margin, self.y, self.song.getMeta('title'), FontStyles.TITLE).height
        self.y = self.y + self.draw_text(self.pdf.l_margin, self.y, self.song.getMeta('artist'), FontStyles.AUTHOR).height

        # line ---------------------
        yLine = 26
        self.pdf.line(self.pdf.l_margin, yLine, self.pdf.w - self.pdf.r_margin, yLine)
        # custom metadata (time: 3/4,....)
        self.render_metadata()
        self.y = self.calculate_start_y()

    def max_y(self):
        return 200


    def render_section(self, section: Section):
        """
        render single section
        """
        if section.getSectionType() == 'new_page':
            self.add_page_with_title()
            return
        elif section.getSectionType() == 'column_break':
            self.next_column()

        # check size (is fit?)
        self.log("render_section({}-{}) row:{} col:{}".format(section.getSectionType(), self.formatSectionTitle(section), self.row, self.col))
        if self.is_widow(section):
            self.move_forward()
            self.log("render_section({}-{}) row:{} col:{}".format(section.getSectionType(), self.formatSectionTitle(section), self.row, self.col))

        # ...and content
        self.render_section_title(section)
        for n in range(0, len(section.lines)):
            line = section.lines[n]
            self.log('Line[{}]: [{}]'.format(n, line.linePosition))
            self.render_section_line(line)

            # too many lines - wrap to next column
            if self.y > self.max_y():
                self.y = self.calculate_start_y()
                self.next_column()
                self.handle_possible_overflow()

        self.log('----------------------')

    
    def render_section_title(self, section: Section):
        """
        render section title
        """
        self.draw_text(self.calculate_start_x(), self.y, self.formatSectionTitle(section), FontStyles.CHORD)
        self.y = self.y + self.rowHeight
        self.row = self.row + 1

    def max_rows(self):
        # todo: compute by page & font
        # step 1 - refactored out from config
        return 24

    def is_widow(self, section : Section):
        """
        NEED MORE WORK!!!!!!!!!
        so far, so stupid
        """
        remaining = self.max_rows() - self.row - len(section.lines)
        return remaining < 3


    def move_forward(self):
        """
        do owerflow
        """
        self.row = self.max_rows() + 1
        self.handle_possible_overflow()


    def next_column(self):
        """
        move to next column
        """
        self.col = self.col + 1
        self.row = 0
        self.handle_possible_overflow()


    def render_section_line(self, sectionLine : SectionLine):
        """
        render song line (chords + lyrics)
        """
        self.x = self.calculate_start_x()
        isLyricsRendered = 0
        isChordRendered = 0
        renderedWidth = 0

        for i in range(0, len(sectionLine.measures)):
            width = 0
            measure = sectionLine.measures[i]
            # format
            chord = self.format_chord(measure.chord)
            lyrics = self.format_lyrics(measure.lyrics)

            k = max(len(chord), len(lyrics))
            chord = chord.ljust(k)
            lyrics = lyrics.ljust(k)

            s = ''
            # chord
            if not chord.strip() == '':
                s = Transpose.transponse_chord(self.config, chord)
                isChordRendered = 1
                self.draw_text(self.x, self.y, chord, FontStyles.CHORD)

            # lyrics
            if not lyrics.strip() == '':
                s = lyrics
                isLyricsRendered = 1
                self.draw_text(self.x, self.y + self.rowHeight, lyrics, FontStyles.LYRICS)

            # move x to next position
            width = self.pdf.get_string_width(s)
            if i < len(sectionLine.measures):
                width = width +  (self.xSpace * self.style.xSpaceFactor)
            self.x = self.x + width
            renderedWidth = renderedWidth + width

        # overflows
        if renderedWidth > self.colWidth:
            self.warn('Line:{} [{}] is too wide! please wrap it'.format(sectionLine.linePosition, sectionLine.rawLine))

        renderedRows = (isChordRendered + isLyricsRendered)
        self.y = self.y + self.rowHeight*renderedRows + (self.rowHeight * 0.6)
        self.row = self.row + renderedRows
        self.handle_possible_overflow()



    def handle_possible_overflow(self):
        """
        flow of [rows - cols - pages]
        """
        if self.row >= self.max_rows():
            self.row = 0
            self.y = self.calculate_start_y()
            self.x = self.calculate_start_x()
            self.col = self.col + 1 
            self.log("+COLUMN {}".format(self.col))

        if self.col >= self.style.columns:
            # owerflow column
            self.y = self.calculate_start_y()

            if self.section + 1 == len(self.song.sections):
                return

            self.add_page_with_title()
            self.log("+PAGE {}".format(self.pdf.page_no()))
            # if self.section < len(self.song.sections):
            # else:
            #     self.warn("OKOKOKOK????")


    def add_page_with_title(self):
        """
        add new pdf page
        """
        self.y = self.calculate_start_y()
        self.x = self.calculate_start_x()
        self.col = 0
        self.row = 0
        self.pdf.add_page('L')
        self.render_song_header()


    def draw_text(self, x: float, y: float, text:str, fontStyle:FontStyles):
        """
        draw text
        """
        self.log("[{} {}] x:{:.2f} y:{:.2f}    {}".format(self.row, self.col, x, y, text))
        font = self.set_font_style(fontStyle)
        self.pdf.text(x, y, text)
        return PdfBox(self.pdf.get_string_width(text), font.Height / self.pdf.k)


    def calculate_start_y(self):
        """
        calc start Y
        """
        return 34


    def calculate_start_x(self):
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



