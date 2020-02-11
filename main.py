import sys
from project.core.OutputFormats import OutputFormats
from project.renderers.RendererFactory import RendererFactory


outputFormat = sys.argv[1]
if outputFormat.lower() == 'pdf':
    outputFormat = OutputFormats.PDF
elif outputFormat.lower() == 'txt':
    outputFormat = OutputFormats.TXT

inputFileName = sys.argv[2]
outputFileName = inputFileName.replace('.cho', '.' + str(outputFormat.name.lower()))
RendererFactory.renderSong(outputFormat,  inputFileName, outputFileName)




