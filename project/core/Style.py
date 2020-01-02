from project.core.Song import Song

class Style:
    def __init__(self):
        """
        defaults
        """
        self.columns = 1
        self.columnWidth = '100px'
        self.renderMetadataKeys = ('time', 'tempo', 'capo')
        self.pageWidth = 285


    def updateFrom(self, song : Song):
        """
        update defaults from parsed song
        """
        columns = song.getMeta('columns')
        if not columns == None:
            self.columns = int(columns)

        rows = song.getMeta('rows')
        if not rows == None:
            self.rows = int(rows)

        columnWidth = song.getMeta('columnWidth')
        if not columnWidth == None:
            self.columnWidth = columnWidth

        render_metadata_keys = song.getMeta('render_metadata_keys')
        if not rows == None:
            self.renderMetadataKeys = render_metadata_keys.split(',')


    @classmethod
    def fromSong(cls, song : Song):
        """
        static constructor
        """
        style = Style()
        style.updateFrom(song)
        return style


