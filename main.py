import sys

from project.core.OutputFormats import OutputFormats
from project.renderers.RendererFactory import RendererFactory

# process args
outputFormat = OutputFormats.parse(sys.argv[1])
inputFileName = sys.argv[2]
outputFileName = inputFileName.replace('.cho', '.' + str(outputFormat.name.lower()))

# render song!
RendererFactory.renderSong(outputFormat, inputFileName, outputFileName)
