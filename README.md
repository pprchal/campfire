# Campfire - chordpro python reloaded

Simple songbook ,,typesetting'' system

Gets `.cho` file and renders `.pdf` output.

## Recommended ussage:
1) Run `python main.py PDF mysong.cho` transforms to `mysong.pdf `
2) OPTIONAL - Grab Visual Studio code and install ChordPro extension to colorize `.cho` files


## Features:
* Real UTF8 support without any woodo-magic
* Produces nicely large printable pdfs which you can take to pub
* Keeping great support for KISS principe - just look for example `cho` file
* Multiplatform - using only python libraries without any native dependencies
* Great extensibility and modularity - write your own renderer
* PDF, HTML and TXT formats are supported
* Ligatures ;)

### Supported renderers
* PDF - Primary renderer
* TXT - Simple, but usefull in some emergency cases
* HTML - Aspiring to be primary renderer, but there is long way to go(page wrapping)


## Why another system?
* `lilypond` - perfect typesetting but doesn't work well simple songs
* `chordpro` is old and weird
* `musescore` - typesetting is perfect, MIDI support is perfect, ... use this if you want more features
* `tex - packages` - overhelming complexity for single sheet with poor UTF8 support 


## Developing & hacking
### Requirements - libs
```
python -m pip install fpdf
python -m pip install pyyaml
python -m pip install PyPDF2
```

### Planned features
* Compiled to js - enable run within browser also

```
python -m unittest discover -s tests
C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_64\python.exe" -m pip install pyaml
```

### Bugs
Not working with pdf library 
```
self.fractionSymbols = {
    '4/4': '𝄴',
    '2/4': '𝄵'
}
```

(c) Pavel Prchal, 2020