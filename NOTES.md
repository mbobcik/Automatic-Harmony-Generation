# Poznámky k teoretické (i guess)

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

* pitch class profile x chromagram??

* Popsat aktivační funkce, vložit několik grafů viz https://www.vutbr.cz/www_base/zav_prace_soubor_verejne.php?file_id=180895

*  For example, to sound a note in MIDI you send a "Note On" message, and then assign that note a "velocity", which determines how loud it plays relative to other notes.
    --MIDI tutorials

* pokud je v souboru písnička v a moll, pak má klíč A a mode 6 (minor). tedy není mollové je potřeba převádět na A

* Všechny noty jsou v rozmezí od MidiNote 11 po 92 včetně. takže je vhodné ořezat pianoRoll pomocí [11:93]. Pak při dekodování zpět na midi je potřeba každou notu zvýšit o 10!

* v celé databází je několik záznamů, které mají chybné časování, nebo nemají záznam harmonie/melodie
ty jsou vyřazeny
Total saved: 12093 Total Errors: 1540

# praktická část

## popis dat

df=
```sql
    SELECT * FROM parts
```

* v df jsou atributy
    * id - id celé skladby
    * name - jméno skladby
    * songkey - tónina skladby (asi)
    * xml - noty v xml ... dále z xml extrahované
        * xml_tag - jméno kořenového uzlu v xml (většinou "super") 
        * xml_bpm - bpm skladby
        * xml_key - opět tónina 
        * xml_mode - mód skladby
    * json - ???

___________________________

df_parts = 
```sql
    SELECT p.id, 
           p.partid, 
           i.youtubeid, 
           u.url 
    from id2parts p 
    JOIN id2youtube i ON i.id=p.id 
    JOIN url2id u ON u.id=p.id
```

* v df_parts jsou atributy 
    * id - id celé skladby (FK do df)
    * partid - id části (každý song je rozdělen na části (verse, chorus, prechorus apod.))
    * youtubeid - id pro video se skladbou na youtube (https://www.youtube.com/watch?v=youtubeid)
    * url - odkaz na skladbu na hooktheory (https://www.hooktheory.com+url)

_____________________________