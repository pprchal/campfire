class Measure:
    def __init__(self, lyrics: str, chord: str):
        self.lyrics = lyrics
        self.chord = chord
        self.repeatedChord = False

    def __eq__(self, other):
        return (self.lyrics == other.lyrics) and (self.chord == other.chord)

    @classmethod
    def createEmpty(cls):
        return Measure('', '')
