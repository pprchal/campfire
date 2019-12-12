from project.core.Section import Section

metadata_shortcuts = {
    't' : 'title',
    'st': 'subtitle'
}

class Song:
    def __init__(self):
        self.metadata = {}
        self.sections = list()

    
    def getMeta(self, name):
        if name in self.metadata:
            return self.metadata.get(name)
        return None

    def addMeta(self, key, value):
        if key in metadata_shortcuts:
            key = metadata_shortcuts[key]
        self.metadata[key] = value


    def openNewSection(self, name):
        if self.isOpenSection():
            previousSection = self.sections[len(self.sections) - 1]
            # fun young cannibals ;) - reuse previous section
            if len(previousSection.lines) == 0:
                previousSection.name = name
                return

        self.sections.append(Section(name))

    def addLineToCurrentSection(self, line):
        if not self.isOpenSection():
            self.openNewSection('default')

        self.sections[len(self.sections) - 1].lines.append(line)

    def isOpenSection(self):
        return len(self.sections) > 0

    def print(self):
        for x in self.metadata:
            print(x + ' => ' + str(self.metadata[x]))
