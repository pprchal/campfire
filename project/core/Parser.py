from project.core.Config import Config
from project.core.Song import Song
from project.core.Section import Section
from project.core.SectionLine import SectionLine
from project.core.Measure import Measure
import re


class Parser:
    def __init__(self, choStream, config : Config):
        self.config = config
        self.choStream = choStream
        self.sectionRE = re.compile('{([\\w\\d]+)(:\\s?[\\w\\d\\s/%,]+)?}', re.UNICODE)
        self.chordRE = re.compile('(\\[[A-Za-z0-9\\+\\-/\\s#]*\\])', re.UNICODE)
        self.unsupported_keys = {
            'new_song', 'ns',
            'new_physical_page', 'np',
            'new_page', 'np',
            'comment',
            'comment_italic',
            'comment_box',
            'highlight',
            'image'
        }
        self.translate_keys = {
            'st': 'subtitle',
            'soc': 'start_of_chorus',
            't': 'title',

            'col': 'columns',
            'g': 'grid',
            'ng': 'no_grid',
            'cb': 'column_break'
        }


    def parseSectionLine(self, line: str):
        sectionLine = SectionLine()
        n = -1
        for token in self.chordRE.split(line):
            if token == '':
                continue

            if token.startswith('['):
                chord = token[1:len(token) - 1].strip()
                if chord == '':
                    # repeat
                    chord = '⦁'

                sectionLine.measures.append(Measure('', chord))
                n = len(sectionLine.measures) - 1 
            else:
                if n == -1:
                    sectionLine.measures.append(Measure.createEmpty())
                    n = 0

                lyrics = token
                if lyrics.endswith('\n'):
                    lyrics = lyrics[0:len(lyrics) - 1]
                sectionLine.measures[n].lyrics = self.ligatureText(lyrics)

        return sectionLine


    def isIgnoredLine(self, line: str):
        return line.startswith("#") or line.strip() == ''


    def processLine(self, line: str, song: Song, i: int):
        """
        main tokenizer
        """
        # skip comments and empty lines
        if self.isIgnoredLine(line):
            return

        # handle {key: value} lines
        x = 0
        for x, match in enumerate(self.sectionRE.finditer(line), start=1):
            self.processMatch(match, song, i)

        if x == 0: 
            # line within section
            song.addLineToCurrentSection(self.parseSectionLine(line))


    def processMatch(self, match, song: Song, i):
        key = match.groups()[0]
        
        if key in self.unsupported_keys:
            print('Unsupported directive: {' + key + '} at line: ' + str(i))
            return

        if key in self.translate_keys:
            key = self.translate_keys[key]

        value = None
        if len(match.groups()) == 2 and not match.groups()[1] == None:
            # {key:value}
            value = match.groups()[1]
            value = self.ligatureText(value[1:len(value)].lstrip())

        # value can be None
        isStartBlock, sectionType = self.parseStartBlock(key)
        if isStartBlock:
            song.openNewSection(sectionType, value)
        else:
            if self.isReuseBlock(key):
                song.reuseSection(key, value)
            else:                
                song.addMeta(key, value)


    def isReuseBlock(self, key):
        return key == 'chorus'


    def parseStartBlock(self, strBlock : str):
        if strBlock.startswith('start_of_'):
            return (True, strBlock[9 : len(strBlock)])
        return (False, None)

    @property
    def ligatures(self):
        ligatures = self.config.getProperty('parser.ligatures')
        if not isinstance(ligatures, dict):
            ligatures = Config.toDict(ligatures)
            self.config.setProperty('parser.ligatures', ligatures)

        return ligatures

    def ligatureText(self, text : str):
        x = text
        for ligatureKey in self.ligatures:
            ligatureValue = self.ligatures[ligatureKey]
            x = x.replace(ligatureKey, ligatureValue)
        return x

    def parse(self):
        song = Song()
        i = 1
        for line in self.choStream:
            self.processLine(line, song, i)
            i = i + 1
        return song


