class Measure:
    def __init__(self, lyrics: str, chord: str):
        self.lyrics = lyrics
        self.chord = chord

    def __eq__(self, other):
        return (self.lyrics == other.lyrics) and (self.chord == other.chord)

    def createEmpty():
        return Measure('', '')
