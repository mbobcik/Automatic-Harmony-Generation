# Poznámky

## Formáty not

* ABC notation

* __MIDI files__ - http://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html
https://github.com/colxi/midi-parser-js

* __GUIDO__ - https://en.wikipedia.org/wiki/GUIDO_music_notation

* GNU LilyPond - https://en.wikipedia.org/wiki/LilyPond
    * https://pypi.org/project/python-ly/


## Machine Learning Frameworky (Python)

* TensorFlow

* Keras =  Python interface for artificial neural networks. Keras acts as an interface for the TensorFlow library.

* PyTorch - based on the Torch library
    * nn module -  for defining complex neural networks

* Caffe - merged into PyTorch ( https://en.wikipedia.org/wiki/Caffe_(software) )


https://towardsdatascience.com/pytorch-vs-tensorflow-spotting-the-difference-25c75777377b

## Nezařazené

* HMM = Hidden Markov Model

* HMM-based modely hojně využívány při generování akordů před současnou érou Deep Learningu(comparativeStudy)

* asi bude lepší nepracovat s konkrétníma akordama, ale se stupni tóniny. a teprve po vygenerování převést podle potřeby do tóniny

* zakomponovat i funkci akordů do učení (tónika, dominanta, subdominanta, ostatní) (comparativeStudy, str. 8)

* Akordy jsou také zapsané v notovém zápise

* Akordy jde hrát "vcelku", nebo rozloženě - jde to vidět v notách na basové lince

* Jak zjistit tóninu melodie? (15) není to tak jednoduché

* pitch class profile x chromagram??

* Popsat aktivační funkce, vložit několik grafů viz https://www.vutbr.cz/www_base/zav_prace_soubor_verejne.php?file_id=180895

*  For example, to sound a note in MIDI you send a "Note On" message, and then assign that note a "velocity", which determines how loud it plays relative to other notes.
    --MIDI tutorials