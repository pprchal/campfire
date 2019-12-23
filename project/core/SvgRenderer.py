chords = {"C": "x32010", "A":"x02220", "G": "320033", "E": "022100", "D": "xx0232", "F": "x3321x", "Am": "x02210", "Dm": "xx0231", "Em": "022000"}


"""
experimental !!!!!!!!!!!!
"""

def drawCircle(x, y, radius):
    return "<circle cx=\"{0}\" cy=\"{1}\" r=\"{2}\" stroke=\"black\" stroke-width=\"4\" />\n".format(x, y, radius)


def drawLine(x1, y1, x2, y2, thick):
    return "<line x1=\"{0}\" y1=\"{1}\" x2=\"{2}\" y2=\"{3}\" style=\"stroke:rgb(0,0,0);stroke-width:{4}\" />\n".format(x1, y1, x2, y2, thick)

def drawCross(x, y, size, thick):
    a = size / 2
    return drawLine(x - a, y - a, x + a, y + a, thick) + drawLine(x - a, y + a, x + a, y - a, thick)

# render chord by name to SVG block
def renderChordSVG(chordName, width, height):
    chord = chords[chordName]
    minFret = 1
    startX = 10
    startY = 30
    lineW = 2       # line width
    dotSize = 5     # radius of dots
    crossSize = 10  # size of cross
    stringSpace = (width + startX - lineW -1) / 6
    fretSpace = (height - startY) / 4

    svg = "<svg width=\"{}\" height=\"{}\">\n".format(width, height)
    svg += "<style>.heavy { font: bold 22px sans-serif; }</style>"
    svg += "<text class=\"heavy\" x=\"5\" y=\"20\" class=\"small\">{0}</text>".format(chordName)

    # vertical (strings) 
    for stringNr in range(6):
        x = startX + (stringNr * stringSpace)
        svg += drawLine(x, startY, x, height, lineW)

    # horizontal (frets)
    for fretNr in range(6):
        y = startY + (fretNr * fretSpace)
        svg += drawLine(startX, y, width, y, lineW) 

    # dots (fingers)
    stringNr = 0
    for str in chord:
        x = startX + (stringNr * stringSpace)

        if str=="x":
            svg += drawCross(x, startY + 5, crossSize, lineW)
        elif str=="0":
            svg += drawCircle(x, startY + 5, dotSize)
        else:
            c = int(str)
            if c < minFret:
                minFret = c
            y = startY + (int(str) * fretSpace) - 0.5 * fretSpace
            svg += drawCircle(x, y, dotSize) 

        stringNr = stringNr + 1

    svg += "</svg>\n"
    return svg


def renderTestHtmlFile(htmlFileName):
    f = open(htmlFileName, "w")
    f.writelines(["<!DOCTYPE html>", "<html>", "<body>"])
    for chordName in chords:
        f.write("<div>" + renderChordSVG(chordName, 100, 200) + "</div>")
    f.writelines(["</body>", "</html>"])
    f.close()

renderTestHtmlFile('testCho.html')



