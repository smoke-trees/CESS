# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 22:13:38 2019

@author: tanma
"""
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from keras.models import Model
from keras.models import Sequential
from keras.layers import Dense, Embedding, Input
from keras.layers import LSTM, Bidirectional, GlobalMaxPool1D, Dropout
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.optimizers import Adam
from sklearn.metrics import roc_auc_score
from keras.models import load_model

import keras.backend as K
if len(K.tensorflow_backend._get_available_gpus()) > 0:
  from keras.layers import CuDNNLSTM as LSTM
  from keras.layers import CuDNNGRU as GRU

maxLength = 100
  
train = pd.read_csv("Toxic Dataset/train.csv")
sentences = train["comment_text"].fillna("DUMMY_VALUE").values
possible_labels = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]
targets = train[possible_labels].values

copy = sentences

max_vocab_size = 200000
input_tokenizer = Tokenizer(max_vocab_size)
input_tokenizer.fit_on_texts(sentences)
input_vocab_size = len(input_tokenizer.word_index) + 1
sentences = np.array(pad_sequences(input_tokenizer.texts_to_sequences(sentences), 
                                maxlen=maxLength))

embedding_dim = 256
model = Sequential()
model.add(Embedding(input_vocab_size, embedding_dim,input_length = maxLength))
model.add(GRU(256, return_sequences=True))
model.add(Dropout(0.9))
model.add(GRU(256))
model.add(Dropout(0.9))
model.add(Dense(len(possible_labels), activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

history = model.fit(sentences, targets, validation_split=0.1, batch_size=128, epochs=10)

model.save('model_gru.h5')

acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(acc))

plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()

plt.figure()

plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()

plt.show()

model = load_model('model_gru.h5')

def custom_input(string):
    input_seq = input_tokenizer.texts_to_sequences(string)
    input_seq = pad_sequences(input_seq, maxlen=maxLength)
    predicted = model.predict(input_seq)[0]
    return predicted

take_input = str(input())
gt = sum(custom_input(take_input))
for j in copy:
    for i, prob in enumerate(custom_input(j)):
        if prob > 0.5:
            print(possible_labels[i],j)