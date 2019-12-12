from project.core.Song import Song
from project.core.Section import Section
from project.core.SectionLine import SectionLine
from project.core.Measure import Measure
import re

#https://www.chordpro.org/chordpro/ChordPro-Directives.html
# METADATA
    # title (short: t)
    # subtitle (short: st)
    # artist
    # composer
    # lyricist
    # copyright
    # album
    # year
    # key
    # time
    # tempo
    # duration
    # capo
    # meta

# Formatting directives
#     comment (short: c)
#     comment_italic (short: ci)
#     comment_box (short: cb)
#     image


# Environment directives
# Environment directives always come in pairs, one to start the environment and one to end the environment.
#     start_of_chorus (short: soc)
#     end_of_chorus (short: eoc)
#     chorus
#     start_of_verse
#     end_of_verse
#     start_of_tab (short: sot)
#     end_of_tab (short: eot)
#     start_of_grid
#     end_of_grid


# x = re.compile('(\\[([A-Za-z0-9]+)\\])')
# y = ''
# for m in x.finditer(ins):
#     chName = m.groups()[1]
#     if not chName in chds:
#         chds.add(chName)

#     s = m.start()
#     e = m.end()
#     y = ins[:e]
#     # print('String match "%s" at %d:%d' % (s1[s:e], s, e))


class Parser:
    def __init__(self, choStream):
        self.choStream = choStream
        self.metaRE = re.compile(r'\{(\w+):\s*([^\}]*)\}', re.UNICODE)
        self.sectionRE = re.compile('\{(.+)\}', re.UNICODE)
        self.chordRE = re.compile('(\\[[A-Za-z0-9\\+\\-/\s#]+\\])', re.UNICODE)
        # self.start_of_verse = False
        # self.start_of_section = False

    def parseSectionLine(self, line):
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

    def parseSectionOpening(self, line):
        if line.strip() == '':
            return ''

        res = self.sectionRE.match(line)
        if res is not None:
            return res.group(1)

        return None
        

    def processLine(self, line, song):
        # skip comments
        if line.startswith("#"):
            return

        # metadata
        match = self.metaRE.match(line)
        if match != None:
            song.addMeta(match.group(1), match.group(2))
            return

        sectionName = self.parseSectionOpening(line)
        if sectionName is not None:
            song.openNewSection(sectionName)
            return

        song.addLineToCurrentSection(self.parseSectionLine(line))

    def parse(self):
        song = Song()
        for line in self.choStream:
            self.processLine(line, song)
        return song

