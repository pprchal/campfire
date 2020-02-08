class SectionLine:
    def __init__(self, line:str, linePosition: int):
        self.measures = list()
        self.rawLine = line
        self.linePosition = linePosition