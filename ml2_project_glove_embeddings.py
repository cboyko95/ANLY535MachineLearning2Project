# -*- coding: utf-8 -*-
"""ML2 Project Glove Embeddings.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12n0J992iIMwSinRJW40w2HBX3qtzmVtR
"""

from google.colab import drive
drive.mount('/content/gdrive')

from keras.models import Sequential
from keras import layers
from keras.optimizers import RMSprop
import os
import pandas as pd
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import numpy as np
from keras.models import Sequential
from keras.layers import Embedding, Flatten, Dense
import matplotlib.pyplot as plt 
from keras import models
from keras.layers import SimpleRNN
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.models import Sequential

data = pd.read_csv('/content/gdrive/MyDrive/ML2 Project/Clickbait and Nonclickbait Data.csv')
data2 = data.values

texts = data2[:, 0]
labels = data2[:, 1]
labels = labels.astype(str).astype('int32')

max_features = 10000
maxlen = 100
training_samples = 22400
testing_samples = 9600
max_words = 10000
tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)

word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))
data = pad_sequences(sequences, maxlen=maxlen)
labels = np.asarray(labels)
print('Shape of data tensor:', data.shape)
print('Shape of label tensor:', labels.shape)
indices = np.arange(data.shape[0])
np.random.shuffle(indices)
data = data[indices]
labels = labels[indices]
x_train = data[:training_samples]
y_train = labels[:training_samples]
x_test = data[training_samples: training_samples + testing_samples]
y_test = labels[training_samples: training_samples + testing_samples]

glove_dir = '/content/gdrive/MyDrive/ML2 Project'                
embeddings_index = {}
f = open(os.path.join(glove_dir, 'glove.6B.50d.txt'), encoding="utf8")
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    embeddings_index[word] = coefs
f.close()
print('Found %s word vectors.' % len(embeddings_index))

embedding_dim = 50
embedding_matrix = np.zeros((max_words, embedding_dim))
for word, i in word_index.items():
    if i < max_words:
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector

model = Sequential()
model.add(layers.Embedding(max_features, 50, input_length=maxlen))
model.add(layers.Conv1D(32, 7, activation='relu'))
model.add(layers.MaxPooling1D(5))
model.add(layers.Conv1D(32, 7, activation='relu'))
model.add(layers.GlobalMaxPooling1D())
model.add(layers.Dense(1, activation='sigmoid'))
model.summary()

model.layers[0].set_weights([embedding_matrix])
model.layers[0].trainable = False

model.compile(optimizer='adam',loss='binary_crossentropy', metrics=['acc'])
history = model.fit(x_train, y_train,epochs=10,batch_size=128,validation_split=0.2)

model2 = Sequential()
model2.add(layers.Embedding(max_features, 50, input_length=maxlen))
model2.add(layers.Conv1D(32, 25, activation='relu'))
model2.add(layers.MaxPooling1D())
model2.add(layers.Conv1D(32, 20, activation='relu'))
model2.add(layers.MaxPooling1D())
model2.add(layers.Conv1D(32, 5, activation='relu'))
model2.add(layers.GlobalMaxPooling1D())
model2.add(layers.Dense(1, activation='sigmoid'))
model2.summary()

model2.layers[0].set_weights([embedding_matrix])
model2.layers[0].trainable = False
model2.compile(optimizer='rmsprop',loss='binary_crossentropy', metrics=['acc'])
history2 = model2.fit(x_train, y_train,epochs=30,batch_size=64,validation_split=0.2)

model2.evaluate(x_val, y_val, verbose = True)

model3 = Sequential()
model3.add(Embedding(max_features, 50))
model3.add(SimpleRNN(32))
model3.add(Dense(1, activation='sigmoid'))
model3.summary()

model3.layers[0].set_weights([embedding_matrix])
model3.layers[0].trainable = False
model3.compile(optimizer='rmsprop',loss='binary_crossentropy', metrics=['acc'])
history3 = model3.fit(x_train, y_train,epochs=20,batch_size=64,validation_split=0.2)

model4 = Sequential()
model4.add(Embedding(max_features, 50))
model4.add(LSTM(32))
model4.add(Dense(1, activation='sigmoid'))
model4.summary()

model4.layers[0].set_weights([embedding_matrix])
model4.layers[0].trainable = False
model4.compile(optimizer='adam',loss='binary_crossentropy', metrics=['acc'])
history4 = model4.fit(x_train, y_train,epochs=20,batch_size=64,validation_split=0.2)

model5 = Sequential()
model5.add(Embedding(max_features, 50))
model5.add(layers.Bidirectional(layers.LSTM(25)))
model5.add(Dense(1, activation='sigmoid'))
model5.summary()

model5.layers[0].set_weights([embedding_matrix])
model5.layers[0].trainable = False
model5.compile(optimizer='adam',loss='binary_crossentropy', metrics=['acc'])
history5 = model5.fit(x_train, y_train,epochs=30,batch_size=64,validation_split=0.2)

model6 = Sequential()
model6.add(Embedding(max_features, 50))
model6.add(layers.Bidirectional(layers.LSTM(100, return_sequences = True)))
model6.add(layers.Bidirectional(layers.LSTM(100, return_sequences= True)))
model6.add(layers.Bidirectional(layers.LSTM(100)))
model6.add(Dense(1, activation='sigmoid'))
model6.summary()

model6.layers[0].set_weights([embedding_matrix])
model6.layers[0].trainable = False
model6.compile(optimizer='adam',loss='binary_crossentropy', metrics=['acc'])
history6 = model6.fit(x_train, y_train,epochs=30,batch_size=64,validation_split=0.2)

model7 = Sequential()
model7.add(Embedding(max_features, 50))
model7.add(layers.Bidirectional(layers.LSTM(50, return_sequences = True)))
model7.add(Dense(25, activation='relu'))
model7.add(Dense(1, activation='sigmoid'))
model7.summary()

model7.layers[0].set_weights([embedding_matrix])
model7.layers[0].trainable = False
model7.compile(optimizer='adam',loss='binary_crossentropy', metrics=['acc'])
history7 = model7.fit(x_train, y_train,epochs=30,batch_size=64,validation_split=0.2)

model8 = Sequential()
model8.add(Embedding(max_features, 50))
model8.add(layers.Bidirectional(layers.SimpleRNN(32)))
model8.add(Dense(1, activation='sigmoid'))
model8.summary()

model8.layers[0].set_weights([embedding_matrix])
model8.layers[0].trainable = False
model8.compile(optimizer='adam',loss='binary_crossentropy', metrics=['acc'])
history8 = model8.fit(x_train, y_train,epochs=30,batch_size=64,validation_split=0.2)

model9 = Sequential()
model9.add(Embedding(max_features, 50))
model9.add(layers.Bidirectional(layers.SimpleRNN(20, return_sequences= True)))
model9.add(layers.Dropout(0.2))
model9.add(layers.Bidirectional(layers.SimpleRNN(20, return_sequences= True)))
model9.add(Dense(1, activation='sigmoid'))
model9.summary()

model9.layers[0].set_weights([embedding_matrix])
model9.layers[0].trainable = False
model9.compile(optimizer='adam',loss='binary_crossentropy', metrics=['acc'])
history9 = model9.fit(x_train, y_train,epochs=30,batch_size=64,validation_split=0.2)

model10 = Sequential()
model10.add(Embedding(max_features, 50))
model10.add(layers.GRU(32, dropout=0.1,recurrent_dropout=0.5,return_sequences=True,))
model10.add(layers.GRU(64, activation='relu',dropout=0.1,recurrent_dropout=0.5))
model10.add(Dense(1, activation='sigmoid'))

model10.layers[0].set_weights([embedding_matrix])
model10.layers[0].trainable = False
model10.compile(optimizer='adam',loss='binary_crossentropy', metrics=['acc'])
history10 = model10.fit(x_train, y_train,epochs=50,batch_size=1000,validation_split=0.2)

model11 = Sequential()
model11.add(Embedding(max_features, 50))
model11.add(layers.GRU(30, dropout=0.1,recurrent_dropout=0.5,return_sequences=True))
model11.add(layers.GRU(50, activation='relu',dropout=0.1,recurrent_dropout=0.5, return_sequences=True))
model11.add(layers.GRU(100, activation='relu',dropout=0.1,recurrent_dropout=0.5))
model11.add(Dense(1, activation='sigmoid'))

import keras
from keras.callbacks import ModelCheckpoint 
early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience= 10) 
callbacks_list= ModelCheckpoint('Models/Weights-{epoch:03d}--{val_loss:.5f}.hdf5', monitor='val_loss', save_best_only = True) 
callbacks = [early_stop, callbacks_list]

model11.layers[0].set_weights([embedding_matrix])
model11.layers[0].trainable = False
model11.compile(optimizer='adam',loss='binary_crossentropy', metrics=['acc'])
history11 = model11.fit(x_train, y_train,epochs=100,batch_size=1000,validation_split=0.2, callbacks = callbacks)

model11.summary()

model11.evaluate(x_test, y_test, verbose = True)

model12 = Sequential()
model12.add(Embedding(max_features, 50))
model12.add(layers.GRU(30, dropout=0.1,recurrent_dropout=0.5,return_sequences=True))
model12.add(layers.GRU(50, activation='relu',dropout=0.1,recurrent_dropout=0.5))
model12.add(Dense(1, activation='sigmoid'))

model12.layers[0].set_weights([embedding_matrix])
model12.layers[0].trainable = False
model12.compile(optimizer='adam',loss='binary_crossentropy', metrics=['acc'])
history12 = model12.fit(x_train, y_train,epochs=30,batch_size=1000,validation_split=0.2)

predictions = model11.evaluate(x_test, y_test, verbose = True)
predictions

predictions

predictions2 = model11.predict_classes(x_test)
predictions2

from sklearn.metrics import confusion_matrix
print(confusion_matrix(y_test, predictions2))

y_test.sum()

predictions = model.predict_classes(x_test)

print(confusion_matrix(y_test, predictions))

confusion_matrix(y_test, predictions)

predictions2 = np.argmax(model.predict(x_test), axis = 1)

confusion_matrix(y_test, predictions2)

print(y_test)
print(predictions)

print(confusion_matrix(y_test, predictions))

print(confusion_matrix(predictions, y_test))