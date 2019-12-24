import pickle

import numpy as np
import pandas as pd
from keras.callbacks import ModelCheckpoint
from keras_preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
import collections
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, GRU
from keras.layers.embeddings import Embedding
import gensim.downloader
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import sklearn

EMBEDDING_DIM = 300
VALIDATION_SPLIT = 0.2
EPOCH_SIZE = 15
BATCH_SIZE = 164
# загрузка русскоязычной модели Word2Vec
word2vec_model = gensim.downloader.load("word2vec-ruscorpora-300")


# получение id тональностей
def get_ids(all_tones):
    result = []

    for tone in all_tones:
        result.append(all_tones.unique().tolist().index(tone))

    return result


# получение тональностей по id
def from_tone(prediction, tones):
    answers = []

    for i in range(prediction.shape[0]):
        answers.append(tones[prediction[i]])

    return answers


# загрузка и перемешивание данных
df = pd.read_csv('tools/rusentilex.csv')
total_words, labels = sklearn.utils.shuffle(df['term'], get_ids(df['tone']))
# получение списков слов
sentences = [[word] for word in total_words]
counter = collections.Counter()

# считаем максимальную длину предложений (словосочетаний), а также частоту всех словосочетаний, считанных из файла
maxlen = 0
for words in sentences:
    if len(words) > maxlen:
        maxlen = len(words)
    for word in words:
        counter[word] += 1

# кол-во различных слов в sentences
vocab_sz = len(counter) + 1

# Создание единого словаря (слово -> число) для преобразования на основе списка текстов sentences
tokenizer = Tokenizer()
tokenizer.fit_on_texts(sentences)

# заменяем слова каждого предложения на числа
X = tokenizer.texts_to_sequences(sentences)
# уравниваем все предложения до размера maxlen
X = pad_sequences(X, maxlen)

embedding_weights = np.zeros(
    # создаём матрицу размером размерность словаря*размерность вектора слова
    (len(counter) + 1, EMBEDDING_DIM))
index = 0
# сортируем слова по частоте встречаемости
sorted_counter = counter.most_common()
# для каждого слова из нашего словаря задаём вектор из word2vec_model в матрицу
for word in sorted_counter:
    try:
        embedding_weights[index, :] = word2vec_model[word[0]]
        index += 1
    except KeyError:  # если нет слова в словаре word2vec_model
        index += 1
        pass

# создаем модель
model = Sequential()
model.add(Embedding(len(counter) + 1, EMBEDDING_DIM,
                    input_length=maxlen, weights=[embedding_weights],
                    trainable=True))
model.add(GRU(units=32, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(len(df['tone'].unique().tolist()), activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

y = to_categorical(labels)

# обучение модели
history = model.fit(X, y, batch_size=BATCH_SIZE, epochs=EPOCH_SIZE,
                    callbacks=[ModelCheckpoint('models/model.h5', save_best_only=True)],
                    validation_split=VALIDATION_SPLIT, verbose=2)

# построение графика потерь
x = range(EPOCH_SIZE)
plt.figure(figsize=(10, 5))
plt.grid(True)
plt.plot(x, history.history['loss'], 'bo-', label='Train losses')
plt.plot(x, history.history['val_loss'], 'ro-', label='Validation losses')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend(loc='upper right')
plt.show()

# проверка работоспособности модели на маленьких тестовых данных
test_samples = ['ненужный', 'отвратительный', 'прикольный', 'милый', 'нежный']
test_samples = [[test] for test in test_samples]

test_samples_tokens = tokenizer.texts_to_sequences(test_samples)
test_samples_pad = pad_sequences(test_samples_tokens, maxlen=maxlen)

predict = model.predict_classes(x=test_samples_pad)
answers = from_tone(predict, df['tone'].unique().tolist())

print(answers)

# сохранение токенайзера
with open('models/tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

# сохранение maxlen
f = open('models/maxlen.bin', 'w')
f.write(str(maxlen))
f.close()
