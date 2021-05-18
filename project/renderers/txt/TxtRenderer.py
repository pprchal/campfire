import os

from project.core.Config import Config
from project.core.Font import Font
from project.core.FontStyles import FontStyles
from project.core.Measure import Measure
from project.core.Section import Section
from project.core.SectionLine import SectionLine
from project.core.Song import Song
from project.core.Style import Style
from project.renderers.BaseRenderer import BaseRenderer


class TxtRenderer(BaseRenderer):
    def __init__(self, config: Config, song: Song):
        super().__init__(config, song)
        self.out = ''


    def renderMetadata(self):
        """
        render some metadata as floating line
        """
        metadataRow = self.formatMetadataRow()
        if not metadataRow == '':
            self.writeLine(metadataRow)
            self.writeLine('\n')
        

    def renderSongHeader(self):
        """
        author + song name
        """
        self.writeLine(self.song.getMeta('title'))
        self.writeLine(self.song.getMeta('artist'))
        self.renderMetadata()


    def renderSection(self, section: Section):
        """
        render single section
        """
        # ...and content
        if section.isCommandSection():
            return
            
        self.renderSectionTitle(section)
        for line in section.lines:
            self.renderSectionLine(line, section)
        self.writeLine('\n')

    
    def renderSectionTitle(self, section: Section):
        """
        render section title
        """
        self.writeLine(self.formatSectionTitle(section))
        self.writeLine('-----------------------------------------------------------------')

    
    def formatChord(self, txtChord:str):
        """
        format chord
        """
        return '[' + super().formatChord(txtChord) + ']'


    def renderSectionLine(self, sectionLine : SectionLine, section : Section):
        """
        render song line (chords + lyrics)
        """
        l1 = ''
        l2 = ''

        for i in range(0, len(sectionLine.measures)):
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

            # lyrics
            if not lyrics.strip() == '':
                l2 = l2 + lyrics


        self.writeLine(l1)
        self.writeLine(l2)
        self.writeLine('')


    def writeLine(self, text:str):
        """
        draw text
        """
        self.out = self.out + text + '\n'


    def renderSong(self):
        """
        render song in one reusable html block 
        """
        self.renderSongHeader()
        for section in self.song.sections:
            self.renderSection(section)
        return self.out.encode()
