from project.core.Config import Config
from project.core.Song import Song
from project.core.Style import Style


class BaseRenderer:
    def __init__(self, config : Config, song: Song, style: Style):
        self.config = config
        self.song = song
        self.style = style

<<<<<<< HEAD
    @property
    def chordSymbols(self):
        chordSymbols = self.config.getProperty('pdfrenderer.chordSymbols')
        if not isinstance(chordSymbols, dict):
            chordSymbols = Config.toDict(chordSymbols)
            self.config.setProperty('pdfrenderer.chordSymbols', chordSymbols)

        return chordSymbols
=======


        
>>>>>>> 9477bd4ab1195b164b32a2f7635bbf8329e2f46b
