# author: Pavel Prchal

from typing import List
from project.core.Section import Section


class Song:
    def __init__(self):
        self.metadata = {}
        self.sections = []  # type: List[Section]
        self.sectionNumbers = dict()

    
    def getMeta(self, name: str):
        if name in self.metadata:
            return self.metadata.get(name)

        return None


    def addMeta(self, key: str, value: str):
        self.metadata[key] = value


    def findSectionByTypeAndName(self, sectionType, sectionName):
        for section in self.sections:
            a = section.sectionType == sectionType
            b = True
            if not sectionName == None:
                b = section.name == sectionName
            if a and b:
                return section

        return None


    def openNewSection(self, sectionType: str, name: str):
        """
        open new section -- more work needs to be done to achieve reusing (verse: A) {A}
        """
        self.sections.append(Section(sectionType, name, self.getNumberForSectionType(sectionType)))


    def getNumberForSectionType(self, sectionType: str):
        """
        get section number for specified type
        """
        n = -1
        if sectionType in self.sectionNumbers:
            n = self.sectionNumbers[sectionType]

        n = n + 1
        self.sectionNumbers.update({sectionType: n})
        return n


    def addLineToCurrentSection(self, line: str):
        if self.getCurrentSection() == None:
            self.openNewSection('verse', '')
        elif self.getCurrentSection().sectionType == 'new_page':
            self.openNewSection('verse', '')

        self.getCurrentSection().lines.append(line)


    def getCurrentSection(self):
        if len(self.sections) == 0:
            return None

        return self.sections[len(self.sections) - 1]


    def print(self):
        for x in self.metadata:
            print(x + ' => ' + str(self.metadata[x]))
