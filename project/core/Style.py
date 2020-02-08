import yaml
from project.core.Song import Song
from project.core.Config import Config


class Style:
    def __init__(self, config : Config):
        """
        defaults
        """
        self.config = config


    @property
    def lineWidth(self):
       return float(self.config.getProperty('style.lineWidth'))

    @property
    def upperNumbers(self):
        return self.config.getProperty('style.upperNumbers')

    @property
    def lowerNumbers(self):
        return self.config.getProperty('style.lowerNumbers')

    @property
    def punctions(self):
        return self.config.getProperty('style.punctions')
    
    @property
    def maxRows(self):
        return int(self.config.getProperty('style.maxRows'))

    @property
    def columns(self):
        return int(self.config.getProperty('style.columns'))

    @columns.setter
    def columns(self, value : int):
        self.config.setProperty('style.columns', value)

    @property
    def renderMetadataKeys(self):
        return self.config.getProperty('style.renderMetadataKeys')

    @property
    def xSpaceFactor(self):
        return self.config.getProperty('style.xSpaceFactor')

    def toColor(self, arr):
        return (arr[0], arr[1], arr[2])

    @property
    def red(self):
        return self.toColor(self.config.getProperty('style.red'))

    @property
    def black(self):
        return self.toColor(self.config.getProperty('style.black'))

    @property
    def fill(self):
        return self.toColor(self.config.getProperty('style.fill'))


    def updateFromSong(self, song : Song):
        """
        update defaults from parsed song
        """
        columns = song.getMeta('columns')
        if not columns == None:
            self.config.setProperty('style.columns', int(columns))

        rows = song.getMeta('rows')
        if not rows == None:
            self.config.setProperty('style.rows', int(rows))
            self.rows = int(rows)

        render_metadata_keys = song.getMeta('render_metadata_keys')
        if not render_metadata_keys == None:
            self.config.setProperty('style.renderMetadataKeys', render_metadata_keys.split(','))


    @classmethod
    def buildFrom(cls, config : Config, song : Song):
        """
        static constructor
        """
        style = Style(config)
        style.updateFromSong(song)
        return style


