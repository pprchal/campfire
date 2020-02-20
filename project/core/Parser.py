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
            'image',
            'chordcolour',
            'textcolour',
            'textsize',
            'no_grid', 'ng'
            'grid', 'g',
            'image',
            'highlight',
            'comment_box', 'cb',
            'comment_italic',
            'comment'
        }
        self.translate_keys = {
            'np': 'new_page',
            'st': 'subtitle',
            'soc': 'start_of_chorus',
            't': 'title',
            'col': 'columns',
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


    def processLine(self, line: str, song: Song, n: int):
        """
        main tokenizer - parse line and add to section
        """
        # skip comments and empty lines
        if self.isIgnoredLine(line):
            return

        # handle {key: value} lines
        x = 0
        for x, match in enumerate(self.sectionRE.finditer(line), start=1):
            self.processMatch(match, song, n)

        # line within section
        if x == 0: 
            song.addLineToCurrentSection(self.parseSectionLine(line, n))


    def processMatch(self, match, song: Song, n:int):
        """
        process match within line
        """
        key = match.groups()[0]
        
        if key in self.unsupported_keys:
            print('Unsupported directive: {} at line: {}'.format(key, str(n)))
            return

        # handle shortcuts (np -> new_page)....
        if key in self.translate_keys:
            key = self.translate_keys[key]

        # {key:value}
        value = None
        if len(match.groups()) == 2 and not match.groups()[1] == None:
            value = match.groups()[1]
            value = self.ligatureText(value[1:len(value)].lstrip())

        # value can be None
        isBlock, createSection, sectionType = self.analyzeBlockAction(key)
        if isBlock:
            # analyzed as block... add or reuse
            if createSection:
                song.openNewSection(sectionType, value)
        else:
            # this is metadata
            song.addMeta(key, value)


    def analyzeBlockAction(self, block: str):
        """
        analyze block
        (isBlock, openSection, blockName)
        """
        if block.startswith('start_of_'):
            return (True, True, block[9 : len(block)])
        elif block.startswith('end_of_'):
            return (True, False, block[7 : len(block)])
        elif block == 'new_page':
            return (True, True, block)
        elif block == 'cb':
            return (True, True, block)
        return (False, False, None)


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
        n = 1
        for line in self.choStream:
            self.processLine(line, song, n)
            n = n + 1
        return song
