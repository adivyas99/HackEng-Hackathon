## Main py!

import os
from googletrans import Translator 
import pandas as pd
import numpy as np

gtrans = Translator()
from time import sleep

corpus_name = "cornell movie-dialogs corpus/movie_lines.txt"
corpus = os.path.join("data", corpus_name)

f= open(corpus, 'r', encoding='iso-8859-1')
sen = f.readlines()
for i in range(len(sen)):
    sen[i]=sen[i].split('+++$+++')[-1].strip()

gtrans.translate('coolness is the only thing ', dest='hi', src ='en').text

data = pd.DataFrame({'english': sen, 'hindi': ['' for i in range(len(sen)) ]})

from sklearn.utils import shuffle
data = shuffle(data)
data = data.reset_index()
data = data[['hindi', 'english']]
data = data.iloc[:800,:]
sen_hindi=[]

i=0
def transhindi(x):
    sleep(0.5)
    x = str(x)
    global i
    i+=1
    print(i)
    try:
        y = gtrans.translate(x, dest='hi', src ='en').text
        return y
    except:
        pass
from gtts import gTTS 
import nltk
language = 'en'
from pygame import mixer # Load the required library
mixer.init()

data['hindi'] = data.english.map(transhindi)
np.where(pd.isnull(data))

from gensim.scripts.glove2word2vec import glove2word2vec
glove2word2vec(glove_input_file="/Users/anilvyas/Desktop/HackEng/glove/glove.6B.100d.txt", word2vec_output_file="gensim_glove_vectors.txt")

from gensim.models.keyedvectors import KeyedVectors
glove_model = KeyedVectors.load_word2vec_format("gensim_glove_vectors.txt", binary=False)
vector = glove_model['monitoring']  
glove_model.most_similar('monitoring')

import warnings
warnings.filterwarnings("ignore")

print('So I am in a prototype mode\n')
myobj = gTTS(text='So I am in a prototype mode...\n\n', lang='en', slow=False) 
myobj.save("answer.mp3") 
mixer.music.load('answer.mp3')
mixer.music.play()
os.remove("answer.mp3")


x = 'I am a superb guy'
print(gtrans.translate(x, dest='hi', src ='en').text)
s1= input('Enter the translation(Player 1)')
s2 = input('Enter the traslation (player 2)')

# 'I am a good boy'
# 'I am an excellent man'

#calculate distance between two sentences using WMD algorithm

print('\nThe similarity of player 1 ', (glove_model.wv.n_similarity(x.lower().split(), s1.lower().split()))*100,'\n')
print('\nThe similarity of player 2 ', (glove_model.wv.n_similarity(x.lower().split(), s2.lower().split()))*100,'\n')
print('Lets decide the winners!!!')

op = input('Would you like to read the sentence? \n(y/n)\n')
if op=='y':
    
    myobj = gTTS(text=x, lang='en', slow=False) 
    myobj.save("answer.mp3") 
    mixer.music.load('answer.mp3')
    mixer.music.play()
    os.remove("answer.mp3")
else:
    print('OK')









