import streamlit as st
import streamlit.components.v1 as components
import numpy as np
from eng_to_ipa import convert
import pandas as pd
import re
import difflib


st.markdown("""
# New-ish English
A getting started kit for creating your English spin-off language.
""")
st.components.v1.html("""
<iframe src='https://gfycat.com/ifr/AlienatedSeparateHermitcrab' frameborder='0' scrolling='no' allowfullscreen width='640' height='300'></iframe><p> <a href="https://gfycat.com/alienatedseparatehermitcrab">via Gfycat</a></p>img src="https://gfycat.com/alienatedseparatehermitcrab"/>
""")

st.markdown("""
Writing a new language is fun, but challenging endeavour!
It's not the highest art-form, but it's an rewarding creative writing exercise.
This app is designed to get you started on defining phonological changes for what
English could sound like hundreds of years in the future.
""")

sample_passage = """It began with the forging of the Great Rings. Three were given to the Elves, immortal, wisest and fairest of all beings. Seven to the Dwarf-Lords, great miners and craftsmen of the mountain halls. And nine, nine rings were gifted to the race of Men, who above all else desire power. For within these rings was bound the strength and the will to govern each race. But they were all of them deceived, for another ring was made. Deep in the land of Mordor, in the Fires of Mount Doom, the Dark Lord Sauron forged a master ring, and into this ring he poured his cruelty, his malice and his will to dominate all life.
"""

col1, col2 = st.beta_columns(2)

col1.markdown("## corpus")
corpus = col1.text_area('What will we be writing in your new language!', value=sample_passage, height=200)
gen0_tokens = (''.join([x.lower() for x in corpus if x not in ',.'])).split(' ')
gen0_ipa = [convert(t) for t in gen0_tokens]
col2.markdown("## IPA")
col2.write(pd.DataFrame(zip(gen0_tokens, gen0_ipa), columns=['word', 'pronounciation']))

def glottal_stops(l):
    return [t.replace('təl', 'ʔel') for t in l]

def canadian_raising(l):
    # this is a small slice of how canadian raising works
    initial_vowel = 'aʊ'
    final_vowel = 'u'
    l = [w.replace(initial_vowel, final_vowel) for w in l]
    return l

def non_rhotic(l):
    return [w.replace('r', '') for w in l]

def final_rhotic(l):
    return [re.sub(r'ə$', 'ər:', w) for w in l]

def drop_schwas(l):
    return [re.sub(r'ə', '', w) for w in l]

def th_retroflex(l):
    return [w.replace('t', 'ɖ') for w in l]


st.markdown("""
## How will your language evolve?
Choose some traits below to add to your lanague
""")
mutations = {
    "Canadian Vowel Raising": [canadian_raising, 'https://en.wikipedia.org/wiki/Canadian_raising', "All speakers kneel at the alter of Tim Horton's and pronounce it as 'aboot'"],
    "Glottal Stops": [glottal_stops, "https://en.wikipedia.org/wiki/Glottal_stop", "Speak with your mouth *and* your throat!"],
    "Non Rhotic": [non_rhotic, "https://www.thoughtco.com/rhoticity-speech-4065992", "Boston ascends! With Irish-American accents at the center of your civilization nobody will pronounce any of their Rs"],
    "Final Rhotic": [final_rhotic, "https://www.thoughtco.com/rhoticity-speech-4065992", "The Pirates of the Carribean sequels are actually good! Their speach patterns echo through your civilization."],
    "Add Retroflex D": [th_retroflex, "https://en.wikipedia.org/wiki/Retroflex_consonant", "Join the Indian Sprachbund! Add sophistication to your consonants and watch tongues do backflips"],
    "Drop all Schwas ('uh', /ə/)": [drop_schwas, "https://en.wikipedia.org/wiki/Schwa", "Go nuclear and eliminate an entire sound from the language"]
}

choices = {}
for m in mutations:
    choices[m] = st.checkbox(m, help=mutations[m][1])
    st.write(mutations[m][-1])

generations = [gen0_tokens, gen0_ipa]
for c,ok in choices.items():
    if not ok: continue
    tf = mutations[c][0]
    generations.append(tf(generations[-1]))
st.markdown("""
## How will it sound?
In the table below you can see how each generation of these changes affects a generation of words.
""")
generation_columns = ["0th Gen Text"]
generation_columns.extend([str(x) + "th Gen IPA" for x in range(0, len(generations)-1)])

table = pd.DataFrame(pd.DataFrame( generations)).transpose()
table.columns = generation_columns
st.write(table.transpose())

st.markdown("## Behold!")

st.write(' '.join(generations[-1]))

text = ' '.join(generations[-1][0:20])
components.iframe("http://ipa-reader.xyz/?text=" + text, height=400)

# TODO
passage_len = len(gen0_ipa)
genDistFromPrev = [0]

for i in range(2, len(generations)):
    distances = [ difflib.SequenceMatcher(None, generations[i - 1][wi], generations[i][wi]).ratio() for wi in range(1, passage_len)]
    genDistFromPrev.append(np.mean(distances))

genDistFrom0 = [0]
for i in range(2, len(generations)):
    distances = [ difflib.SequenceMatcher(None, generations[1][wi], generations[i][wi]).ratio() for wi in range(1, passage_len)]
    genDistFrom0.append(np.mean(distances))


st.markdown("## How dissimlar is it from English? (Distance v Generation)")
st.markdown("Use the chart below to track your progress! Since we've only changed the phonology so far, the output is still probably a dialect of English, but it's cool nonetheless!")
st.line_chart(pd.DataFrame(zip(genDistFrom0[1:], genDistFromPrev[1:]), columns=["Distance From English", "Distance From Previous"]))
st.markdown("""This is just the ratio of simlarity, a smarter way to do this would be to use feature vectors and informatin gain to do a weighted analysis but that's outside scope here.

https://www.aclweb.org/anthology/W97-1102.pdf""")

st.markdown("""
## What's next?
Thankfully, languages are much more than a bag of sounds!
As English ages in your theoretical world, it will experience
* Semantic changes to existing words,
* Changes to existing grammar,
* Development of net new vocabularly,
* Calques, loan words, and features from adjacent languages
* Changes to the existing writing system.

### References:
1. Core exercise borrowed from an article in the [Linguistic Society](https://www.linguisticsociety.org/sites/default/files/02e_92.3Sanders.pdf)
1. [The Conlang Construction Toolkit](https://www.zompist.com/kitlong.html)
""")
st.components.v1.html("""
<iframe src="https://giphy.com/embed/zGnnFpOB1OjMQ" width="100%" height="100%" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/lord-of-the-rings-hobbits-shire-zGnnFpOB1OjMQ">via GIPHY</a></p>
""")
