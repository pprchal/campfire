class Section:
    def __init__(self, sectionType : str, name : str, n : int):
        self.lines = list()
        self.sectionType = sectionType
        self.name = name
        self.n = n


    def getSectionTitle(self):
        return self.sectionType + ': ' + str(self.n + 1)

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
