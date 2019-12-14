from project.core.Song import Song
from project.core.Section import Section
from project.core.SectionLine import SectionLine
from project.core.Measure import Measure
import re

metadata_keys = {
    'title', 't',
    'subtitle', 'st'
    'artist',
    'composer',
    'lyricist',
    'copyright',
    'album',
    'year',
    'key',
    'time',
    'tempo',
    'duration',
    'capo',
    'meta',
}

ignore_keys = {
    'end_of_verse',
    'new_song', 'ns'
}

translate_keys = {
    'st': 'subtitle',
    'soc': 'start_of_chorus',
    't': 'title'
}

class Parser:
    def __init__(self, choStream):
        self.choStream = choStream
        self.sectionRE = re.compile('{([\\w\\d]+)(:\\s?[\\w\\d\\s/]+)?}', re.UNICODE)
        self.chordRE = re.compile('(\\[[A-Za-z0-9\\+\\-/\\s#]+\\])', re.UNICODE)

    def parseSectionLine(self, line: str):
        sectionLine = SectionLine()
        n = -1
        for token in self.chordRE.split(line):
            if token == '':
                continue

            if token.startswith('['):
                chord = token[1:len(token) - 1]
                sectionLine.measures.append(Measure('', chord))
                n = len(sectionLine.measures) - 1 
            else:
                if n == -1:
                    sectionLine.measures.append(Measure.createEmpty())
                    n = 0

                sectionLine.measures[n].lyrics = token

        return sectionLine


    def ignoreLine(self, line: str):
        return line.startswith("#") or line.strip() == ''


    def processLine(self, line: str, song: Song, i: int):
        """
        main tokenizer
        """
        # skip comments and empty lines
        if self.ignoreLine(line):
            return

        # handle {key: value} lines
        matches = self.sectionRE.finditer(line)
        atLeastOne = False
        for x, match in enumerate(matches, start=1):
            atLeastOne = True
            self.processMatch(match, song, i)
 
        # line within section
        if not atLeastOne:
            song.addLineToCurrentSection(self.parseSectionLine(line))


    def processMatch(self, match, song: Song, i):
        key = match.groups()[0]
        
        if key in ignore_keys:
            print('Unsupported block: {' + key + '} at line: ' + str(i))
            return

        if key in translate_keys:
            key = translate_keys[key]

        if len(match.groups()) == 2 and not match.groups()[1] == None:
            # {key:value}
            value = match.groups()[1]
            value = value[1:len(value)].lstrip()

            isStartBlock, sectionType = self.parseStartBlock(key)
            if isStartBlock:
                song.openNewSection(sectionType, value)
            else:
                song.addMeta(key, value)
        else:
            # {key}
            if not self.isEndingBlock(key):
                song.openNewSection(key, key)

    def isEndingBlock(self, strBlock : str):
        return strBlock.startswith('end_of_')

    def parseStartBlock(self, strBlock : str):
        if strBlock.startswith('start_of_'):
            return (True, strBlock[9 : len(strBlock)])
        return (False, None)


    def parse(self):
        song = Song()
        i = 1
        for line in self.choStream:
            self.processLine(line, song, i)
            i = i + 1
        return song

