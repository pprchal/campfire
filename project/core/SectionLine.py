from typing import List

from project.core.Measure import Measure


class SectionLine:
    def __init__(self, line:str, linePosition: int):
        self.measures = []  # type: List[Measure]
        self.rawLine = line
        self.linePosition = linePosition
