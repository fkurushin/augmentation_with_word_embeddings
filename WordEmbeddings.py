import re
import gensim
import pandas as pd

from pymystem3 import Mystem
from gensim.models import KeyedVectors
import gensim.downloader as api

GOOD_TAGS = ('A', 'ADV', 'S', 'V')
GT_to_UPOS = {'A' : 'ADJ', 'ADV' : 'ADV', 'S' : 'NOUN', 'V' : 'VERB'}


russian_model = gensim.models.KeyedVectors.load_word2vec_format('/Users/magomednikolaev/Downloads/186/model.txt', binary=False)

m = Mystem()
df = pd.read_excel('/Users/magomednikolaev/Desktop/we/df.xlsx')
lemmatized_text = df.text_TOK_str[1500]
lemmatized_text = lemmatized_text.split(' ')

print("\nБыло: ", lemmatized_text)
for word in lemmatized_text:
    tag = m.analyze(word)[0]['analysis'][0]['gr'].split('=')[0].split(',')[0]


    if tag in GOOD_TAGS:

        upos_tag = GT_to_UPOS[tag]
        word_UPOS = word + '_' + upos_tag
        new_word = russian_model.most_similar(word_UPOS)[0][0].split('_')[0]
        index = lemmatized_text.index(word)
        lemmatized_text[index] = new_word

print("\nСтало:", lemmatized_text)
