from enum import Enum

class OutputFormats(Enum):
    PDF = 1
    HTML = 2

    @classmethod
    def parse(cls, formatS: str):
        formatS = formatS.lower()
        if formatS == 'pdf':
            return OutputFormats.PDF
        elif formatS == 'html':
            return OutputFormats.HTML
