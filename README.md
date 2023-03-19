# Campfire - chordpro python

* Simple songbook ,,typesetting'' system based on format chodpro
* Gets `.cho` file and renders `.pdf` output.
* ChordPro to `PDF`, `HTML` and `TXT`

## Recommended ussage:
1) Run `python main.py mysong.cho` transforms to `mysong.pdf `
2) OPTIONAL - Grab Visual Studio code and install ChordPro extension to colorize `.cho` files

```
usage: campfire.py [-h] [--format FORMAT] [infile]

Process songbook.

positional arguments:
  infile

optional arguments:
  -h, --help       show this help message and exit
  --format FORMAT  [pdf] html txt
```

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
* `chordpro` is old and weird. Update: I'm not able to run version 6 on manjaro.
* `musescore` - typesetting is perfect, MIDI support is perfect, ... use this if you want more features
* `tex - packages` - overhelming complexity for single sheet with poor UTF8 support 

# Developing & hacking

## Requirements - libs
```
pip install -r requirements.txt
```

## Planned features
* Transition to `html` 
* Enable batch generation
* ~~Compiled to js - enable run within browser also~~

## Notes
```
python -m unittest discover -s tests
```

# Bugs
* Fonts cache is weird, delete `*.pkl` files
* Not working with pdf library 
```
self.fractionSymbols = {
    '4/4': '𝄴',
    '2/4': '𝄵'
}
```

(c) Pavel Prchal, 2020, 2021, 2023