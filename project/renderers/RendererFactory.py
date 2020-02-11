from project.core.OutputFormats import OutputFormats
from project.core.Config import Config
from project.core.Parser import Parser
from project.core.Song import Song
from project.renderers.pdf.PdfRenderer import PdfRenderer
from project.renderers.txt.TxtRenderer import TxtRenderer


class RendererFactory:
    @staticmethod
    def createRenderer(outputFormat: OutputFormats, config: Config, song: Song):
        """
        renderer factory
        """
        if outputFormat == OutputFormats.PDF:
            return PdfRenderer(config, song)
        elif outputFormat == OutputFormats.TXT:
            return TxtRenderer(config, song)

        raise NotImplementedError("Unimplemented output format: " + outputFormat)


    @staticmethod
    def renderSong(outputFormat: OutputFormats, songFileName: str, outFileName: str):
        """
        render song to output html file
        """
        fin = open(songFileName, "r", encoding="UTF-8")
        fout = open(outFileName, "wb")

        config = Config.fromYaml()
        buff = RendererFactory.createRenderer(outputFormat, config, Parser(fin, config).parse()).renderSong()
        fout.write(buff)
        fout.close()
        fin.close()
