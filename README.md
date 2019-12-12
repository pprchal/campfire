# Pacholek - chordpro python reloaded

Simple `.cho` typesetting system. Gets file and renders `.html` output.
This sw should be used only for simple campfire songbook.

## Why another system?
Please, use advanced software if you want to use more features.

* why not, but some coordinates:
* `lilypond` doesn't work well with guitar only song and is complicated - and why export to `.mid`?
* `chordpro` format is the most advanced tool to do this stuff
* `musescore` - typesetting is perfect, MIDI support is perfect, ... use this

## Running
### Windows


### Other platforms
`python main.py input.cho output.html`

## Planned features
* Guttenberg print styles integration - in progress
* SVG chord printing - preview works, but there is long journery to go

```
python -m unittest discover -s tests
```

## Why python ?
* Test, only test
* But - brython helps me out to run on browser
* And I'm able to create `.exe` file