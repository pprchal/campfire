from project.core.Song import Song
from project.core.Style import Style


class BaseRenderer:
    def __init__(self, song: Song, style: Style):
        self.song = song
        self.style = style

        