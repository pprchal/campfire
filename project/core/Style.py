from project.core.Song import Song

class Style:
    def __init__(self):
        """
        defaults
        """
        self.columns = 2
        self.renderMetadataKeys = ('time', 'tempo')
        self.red = (255, 0, 0)
        self.black = (0, 0, 0)
        self.xSpace = 7
        self.maxRows = 14
        self.widowRows = 4


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
        if not render_metadata_keys == None:
            self.renderMetadataKeys = render_metadata_keys.split(',')


    @classmethod
    def fromSong(cls, song : Song):
        """
        static constructor
        """
        style = Style()
        style.updateFrom(song)
        return style


