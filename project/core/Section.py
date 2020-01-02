class Section:
    def __init__(self, sectionType : str, name : str, n : int):
        self.lines = list()
        self.sectionType = sectionType
        self.name = name
        self.n = n


    def getSectionTitle(self):
        return self.sectionType + ': ' + str(self.n + 1)