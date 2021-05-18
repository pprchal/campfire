from enum import Enum

class OutputFormats(Enum):
    PDF = 1
    TXT = 2
    HTML = 3

    @classmethod
    def parse(cls, formatS: str):
        formatS = formatS.lower()
        if formatS == 'pdf':
            return OutputFormats.PDF
        elif formatS == 'txt':
            return OutputFormats.TXT
        elif formatS == 'html':
            return OutputFormats.HTML
