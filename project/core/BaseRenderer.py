import abc
from project.core.Config import Config
from project.core.Song import Song
from project.core.Style import Style


class BaseRenderer:
    def __init__(self, config : Config, song: Song):
        self.config = config
        self.song = song
        self._style = None

    def renderSong(self):        
        raise NotImplementedError("renderSong is not implemented-abstract")


    @property
    def style(self):
        """
        merged style from config and song
        """
        if self._style == None:
            self._style = Style.buildFrom(self.config, self.song)
        return self._style


    @property
    def chordSymbols(self):
        chordSymbols = self.config.getProperty('style.chordSymbols')
        if not isinstance(chordSymbols, dict):
            chordSymbols = Config.toDict(chordSymbols)
            self.config.setProperty('chordSymbols', chordSymbols)

        return chordSymbols


    def formatFraction(self, fraction):
        """
        format time fraction (2/3)
        """
        split = fraction.split('/')
        uppers = ''
        for upper in split[0]:
            uppers += self.style.upperNumbers[int(upper)]

        lowers = ''
        for lower in split[1]:
            lowers += self.style.lowerNumbers[int(lower)]

        return '{}⁄{}'.format(uppers, lowers)        


    def formatMetadataRow(self):
        """
        formats metadata
        """
        values = list()

        for key in self.style.renderMetadataKeys:
            value = self.song.getMeta(key)
            if value == None:
                print('empty metadata: [{}]'.format(key))
                continue

            if key == 'time':
                values.append(self.formatFraction(value))
            else:
                values.append('{}: {}'.format(key, value))

        return '  '.join(values)


    def formatLyrics(self, lyrics : str):
        """
        render lyrics
        """
        if lyrics == '':
            return ''
        return lyrics


    def formatChord(self, txtChord : str):
        """
        render chord - with respect to music notation
        """
        if txtChord == '':
            return ''

        chord = ''
        for c in txtChord:
            if c in self.chordSymbols:
                c = self.chordSymbols[c]

            chord += c

        return chord        