# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 23:47:52 2019

@author: tanma
"""

import pandas as pd
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import Dense, Embedding, Input
from keras.layers import GRU, Dropout, MaxPooling1D, Conv1D
from keras.models import Model
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing import text

MAX_FEATURES = 60000
MAX_TEXT_LENGTH = 1000
BATCH_SIZE = 32
EPOCHS = 10
VALIDATION_SPLIT = 0.1
CLASSES_LIST = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]

train = pd.read_csv("Toxic Dataset/train.csv")
train_raw_text = train["comment_text"].fillna("MISSINGVALUE").values
    
tokenizer = text.Tokenizer(num_words=MAX_FEATURES)

tokenizer.fit_on_texts(list(train_raw_text))
train_tokenized = tokenizer.texts_to_sequences(train_raw_text)

data = pad_sequences(train_tokenized, maxlen=MAX_TEXT_LENGTH)

targets = train[CLASSES_LIST].values

embed_size = 300
inp = Input(shape=(MAX_TEXT_LENGTH,))
model = Embedding(MAX_FEATURES, embed_size)(inp)
model = Dropout(0.2)(model)
model = Conv1D(filters=32, kernel_size=2, padding='same', activation='relu')(model)
model = MaxPooling1D(pool_size=2)(model)
model = Conv1D(filters=32, kernel_size=2, padding='same', activation='relu')(model)
model = MaxPooling1D(pool_size=2)(model)
model = GRU(128)(model)
model = Dense(64, activation="relu")(model)
model = Dense(32, activation="relu")(model)
model = Dense(16, activation="relu")(model)
model = Dense(6, activation="sigmoid")(model)
model = Model(inputs=inp, outputs=model)
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

filepath = "weight-improvement-{epoch:02d}-{loss:4f}.hd5"
checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min',
                             period=1)
early = EarlyStopping(monitor="val_loss", mode="min", patience=2)
callbacks_list = [checkpoint, early]
model.fit(data, targets,
          batch_size=BATCH_SIZE,
          epochs=EPOCHS, verbose=1,
          validation_split=VALIDATION_SPLIT,
          callbacks=callbacks_list)





