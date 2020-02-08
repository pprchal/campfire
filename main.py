from project.core.OutputFormats import OutputFormats
from project.renderers.RendererFactory import RendererFactory

RendererFactory.renderSong(OutputFormats.PDF, 'project/test/testFiles/černá kára.cho', 'kara.pdf')
#RendererFactory.renderSong(OutputFormats.PDF, 'project/test/testFiles/saro.cho', 'saro.pdf')



