from project.core.Section import Section

class Song:
    def __init__(self):
        self.metadata = {}
        self.sections = list()

    
    def getMeta(self, name: str):
        if name in self.metadata:
            return self.metadata.get(name)
        return None


    def addMeta(self, key : str, value : str):
        self.metadata[key] = value


    def openNewSection(self, sectionType : str, name : str):
        if self.isOpenSection():
            previousSection = self.sections[len(self.sections) - 1]
            # fun young cannibals ;) - reuse previous section
            if len(previousSection.lines) == 0:
                previousSection.name = name
                return

        self.sections.append(Section(sectionType, name, len(self.sections)))


    def addLineToCurrentSection(self, line : str):
        if not self.isOpenSection():
            self.openNewSection('verse', '')

        self.sections[len(self.sections) - 1].lines.append(line)


    def isOpenSection(self):
        return len(self.sections) > 0


    def print(self):
        for x in self.metadata:
            print(x + ' => ' + str(self.metadata[x]))
