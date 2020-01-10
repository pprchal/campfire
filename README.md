# Campfire - chordpro python reloaded

Simple songbook typesetting system
Gets `.cho` file and renders `.pdf / .html` output.


Fetures:
* Real UTF8 support without any woodo-magic
* Produces nicely large printable pdfs which you can take to pub
* Keeping great support for KISS principe - just look for example `cho` file, no 2 weeks of learning
* Multiplatform - using only python libraries without any native dependencies
* Great test coverage
* Great extensibility and modularity - write your own renderer
* Ligatures ;)

## Why another system?
* `lilypond` doesn't work well with guitar only song and is too complicated - and why export to `.mid`?
* `chordpro` is old and weird
* `musescore` - typesetting is perfect, MIDI support is perfect, ... use this if you want more features
* `tex - packages` - overhelming complexity for single sheet with poor UTF8 support 


## Running
`python main.py input.cho`


## Developing & hacking
### Requirements
* `python -m pip install fpdf`
* `python -m pip install pyyaml`

### Planned features
* Guttenberg print styles integration - dropped
* SVG chord printing - preview works, but there is long journery to go

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

