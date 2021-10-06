import re
import gensim
import pandas as pd

from pymystem3 import Mystem
import gensim.downloader as api
from gensim.models import KeyedVectors


# class WEAugmenter(object):
#     """docstring for WEAugmenter."""
#
#     def __init__(self, tags):
#         super(WEAugmenter, self).__init__()
#         self.GOOD_TAGS = tags
#

# Существительные и глаголы плохо работают, так как не все специфические сущ-ые есть в модели
# и не все глаголы
GOOD_TAGS = ('A', 'ADV')
GT_to_UPOS = {'A' : 'ADJ', 'ADV' : 'ADV', 'S' : 'NOUN', 'V' : 'VERB'}


russian_model = gensim.models.KeyedVectors.load_word2vec_format('/Users/magomednikolaev/Downloads/186/model.txt', binary=False)

m = Mystem()
df = pd.read_excel('/Users/magomednikolaev/Desktop/we/df.xlsx')

indexes = [i for i in range(1000, 3000) if i % 100 == 0]

for i in indexes:
    lemmatized_text = df.text_TOK_str[i]
    lemmatized_text = lemmatized_text.split(' ')

    print("\nБыло: ", lemmatized_text)
    for word in lemmatized_text:

        try:
            tag = m.analyze(word)[0]['analysis'][0]['gr'].split('=')[0].split(',')[0]
        except IndexError as IE:
            pass

        if tag in GOOD_TAGS:

            upos_tag = GT_to_UPOS[tag]
            word_UPOS = word + '_' + upos_tag
            try:
                new_word = russian_model.most_similar(word_UPOS)[0][0].split('_')[0]
                if re.findall('-', new_word) == ['-']:
                    new_word = re.sub('-', '', new_word)
            except KeyError as KE:
                # print(word_UPOS, KE)
                new_word = word
            finally:
                index = lemmatized_text.index(word)
                lemmatized_text[index] = new_word

    print("\nСтало:", lemmatized_text)
