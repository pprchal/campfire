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
        self.row = 0
        self.out = ''


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

        # line ---------------------
        # self.pdf.line(self.pdf.l_margin, yLine, self.pdf.w - self.pdf.r_margin, yLine)
        # custom metadata (time: 3/4,....)
        self.renderMetadata()


    def renderSection(self, section : Section):
        """
        render single section
        """
        # ...and content
        self.renderSectionTitle(section)
        for line in section.lines:
            self.renderSectionLine(line, section)

    
    def renderSectionTitle(self, section: Section):
        """
        render section title
        """
        self.drawText(self.formatSectionTitle(section), 'h4')
        self.row = self.row + 1

    
    def formatChord(self, txtChord:str):
        """
        format chord
        """
        return '[' + super().formatChord(txtChord) + ']'


    def renderSectionLine(self, sectionLine : SectionLine, section : Section):
        """
        render song line (chords + lyrics)
        """
        isLyricsRendered = 0
        isChordRendered = 0
        renderedWidth = 0

        l1 = ''
        l2 = ''

        for i in range(0, len(sectionLine.measures)):
            width = 0
            measure = sectionLine.measures[i]
            # format
            chord = self.formatChord(measure.chord)
            lyrics = self.formatLyrics(measure.lyrics)

            k = max(len(chord), len(lyrics))
            chord = chord.ljust(k)
            lyrics = lyrics.ljust(k)

            # chord
            if not chord.strip() == '':
                l1 = l1 + chord
                isChordRendered = 1

            # lyrics
            if not lyrics.strip() == '':
                l2 = l2 + lyrics
                isLyricsRendered = 1

            renderedWidth = renderedWidth + width

        self.drawText(l1, FontStyles.CHORD)
        self.drawText('\n', FontStyles.LYRICS)
        self.drawText(l2, FontStyles.LYRICS)
        self.drawText('\n', FontStyles.LYRICS)
        # overflows
        # if renderedWidth > self.colWidth:
        #     print('Line:{} [{}] is too wide! please wrap it'.format(sectionLine.linePosition, sectionLine.rawLine))

        renderedRows =  (isChordRendered + isLyricsRendered)
        self.row = self.row + renderedRows


    def drawText(self, text:str, fontStyle:FontStyles):
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
        self.out = "<html><body>"
        self.renderSongHeader()
        for section in self.song.sections:
            self.renderSection(section)
        self.out = self.out + "</body></html>"
        return self.out.encode()


