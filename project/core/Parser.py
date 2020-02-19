import re

from project.core.Config import Config
from project.core.Measure import Measure
from project.core.Section import Section
from project.core.SectionLine import SectionLine
from project.core.Song import Song


class Parser:
    def __init__(self, choStream, config: Config):
        self.config = config
        self.choStream = choStream
        self.sectionRE = re.compile('{([\\w\\d]+)(:\\s?[\\w\\d\\s/%,]+)?}', re.UNICODE)
        self.chordRE = re.compile('(\\[[A-Za-z0-9\\+\\-/\\s#]*\\])', re.UNICODE)
        self.unsupported_keys = {
            'new_song', 
            'ns',
            'new_physical_page',
            'comment',
            'comment_italic',
            'comment_box',
            'highlight',
            'image'
        }
        self.translate_keys = {
            'np': 'new_page',
            'st': 'subtitle',
            'soc': 'start_of_chorus',
            't': 'title',

            'col': 'columns',
            'g': 'grid',
            'ng': 'no_grid',
            'cb': 'column_break'
        }


    def parseSectionLine(self, line: str, linePosition: int):
        """
        parse cho line -- core of parser
        """
        sectionLine = SectionLine(line, linePosition)
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
        """
        recognize comments
        """
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
            song.addLineToCurrentSection(self.parseSectionLine(line, i))


    def processMatch(self, match, song: Song, i:int):
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
        isBlock, sectionType = self.parseBlock(key)
        if isBlock:
            song.openNewSection(sectionType, value)
        else:
            if self.isReuseBlock(key):
                song.reuseSection(key, value)
            else:                
                song.addMeta(key, value)


    def isReuseBlock(self, key):
        return key == 'chorus'


    def parseBlock(self, strBlock : str):
        if strBlock.startswith('start_of_'):
            return (True, strBlock[9 : len(strBlock)])
        elif strBlock == 'new_page':
            return (True, strBlock)
        elif strBlock == 'nc':
            return (True, strBlock)
        return (False, None)


    @property
    def ligatures(self):
        ligatures = self.config.getProperty('style.ligatures')
        if not isinstance(ligatures, dict):
            ligatures = Config.toDict(ligatures)
            self.config.setProperty('style.ligatures', ligatures)

        return ligatures


    def ligatureText(self, text : str):
        """
        find ligature patterns in input and replace by config
        """
        x = text
        for ligatureKey in self.ligatures:
            ligatureValue = self.ligatures[ligatureKey]
            x = x.replace(ligatureKey, ligatureValue)
        return x


    def parse(self):
        """
        read file line by line and create song structure
        """
        song = Song()
        i = 1
        for line in self.choStream:
            self.processLine(line, song, i)
            i = i + 1
        return song
