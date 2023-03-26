class Measure:
    def __init__(self, lyrics: str, chord: str, repeated_chord):
        self.lyrics = lyrics
        self.chord = chord
        self.repeated_chord = repeated_chord

    def __eq__(self, other):
        return (self.lyrics == other.lyrics) and (self.chord == other.chord)

    @classmethod
    def create_empty(cls):
        return Measure('', '', False)
