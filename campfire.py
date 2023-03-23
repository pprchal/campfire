import argparse
from project.core.OutputFormats import OutputFormats
from project.renderers.RendererFactory import RendererFactory


# process args
parser = argparse.ArgumentParser(description='Process songbook.')
parser.add_argument('--format', help='[pdf] html txt', default='pdf', type=OutputFormats.parse)
parser.add_argument('infile', nargs='?')
args = parser.parse_args()

# prepare output file
inputFileName = args.infile
outputFileName = inputFileName.replace('.cho', '.' + str(args.format.name.lower()))


# render song!
RendererFactory.render_song(args.format, inputFileName, outputFileName)
print("OK: " + outputFileName)
