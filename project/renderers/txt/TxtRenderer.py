import os

from project.core.Config import Config
from project.core.Section import Section
from project.core.SectionLine import SectionLine
from project.core.Song import Song
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


    def render_section(self, section: Section):
        """
        render single section
        """
        # ...and content
        if section.isCommandSection():
            return
            
        self.render_section_title(section)
        for line in section.lines:
            self.render_section_line(line, section)
        self.writeLine('\n')

    
    def render_section_title(self, section: Section):
        """
        render section title
        """
        self.writeLine(self.formatSectionTitle(section))
        self.writeLine('-----------------------------------------------------------------')

    
    def format_chord(self, txtChord:str):
        """
        format chord
        """
        return '[' + super().format_chord(txtChord) + ']'


    def render_section_line(self, sectionLine : SectionLine, section : Section):
        """
        render song line (chords + lyrics)
        """
        l1 = ''
        l2 = ''

        for i in range(0, len(sectionLine.measures)):
            measure = sectionLine.measures[i]
            # format
            chord = self.format_chord(measure.chord)
            lyrics = self.format_lyrics(measure.lyrics)

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


    def render_song(self):
        """
        render song in one reusable html block 
        """
        self.renderSongHeader()
        for section in self.song.sections:
            self.render_section(section)
        return self.out.encode()
