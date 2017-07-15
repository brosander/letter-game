Letter-Game
===========
This is a simple game written using the pygame framework that is intended to help small children learn their ABCs while familiarizing them with how a keyboard works.

The images can be customized. (My personal version is mostly family pictures for example.)

Requirements:
1. [virtualenv](http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/)
2. Internet Connection (the first time a new picture set is used)

Usage:
-----------
Simple:
```
python LetterGameMain.py
```

Advanced:
```
./LetterGame.sh [-h] [-f] [-s] [-p PICTUREDIRECTORY] [-t TTSURLPREFIX]

A simple game to help small children learn their ABCs

optional arguments:
  -h, --help            show this help message and exit
  -f, --full            Render the whole sentence when in single letter mode (no -s flag) (default: False)
  -s, --spell           Spell the word (default: False)
  -p PICTUREDIRECTORY, --pictureDirectory PICTUREDIRECTORY
                        Directory of images to use (default: /home/bryan/Github/letter-game/default)
  -t TTSURLPREFIX, --ttsUrlPrefix TTSURLPREFIX
                        Url prefix to append tts query to (default:
                        https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=En-us&q=)
```

On startup, all of the images in the specified folder are loaded (or the default one if none is specified).  When a letter is pressed, the picture corresponding to it is shown on the screen along with the letter it starts with.  Then the sentence "LETTER is for PICTURE_NAME" is read aloud.

All of the default images come from http://www.publicdomainpictures.net/

The Google Translate TTS API is used by default for the voice clips.
