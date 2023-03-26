from project.core.SectionLine import SectionLine

class Section:
    def __init__(self, sectionType: str, name: str, n: int):
        self.lines = [] 
        self.sectionType = sectionType
        self.name = name
        self.n = n

    def getSectionPosition(self):
        return self.n


    def getSectionType(self):
        return self.sectionType


    def getRenderableLinesCount(self):
        n = 0
        for sectionLine in self.lines:
            chord = 0
            lyrics = 0
            for measure in sectionLine.measures:
                if not measure.chord.strip() == '':
                    chord = 1
                if not measure.lyrics.strip() == '':
                    lyrics = 1
            n = n + chord + lyrics
        return n


    def isCommandSection(self):
        if self.sectionType == 'new_page':
            return True
        elif self.sectionType == 'column_break':
            return True
        return False
