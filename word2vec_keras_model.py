from nltk.corpus import stopwords
from gensim.models import Word2Vec
import pandas as pd
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv1D, GlobalMaxPooling1D, Activation
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from keras.models import load_model
from keras.callbacks import ModelCheckpoint
from nltk.tokenize import RegexpTokenizer


def tokenize(text):
    regex_tokenizer = RegexpTokenizer('[А-Яа-я]+')
    words = regex_tokenizer.tokenize(text.lower())
    stop_words = set(stopwords.words("russian"))
    without_stop_words = [w for w in words if w not in stop_words and len(w) > 1]
    return without_stop_words


# преобразование тональностей в матрицу двоичных чисел (нужно для keras)
def to_tone(tones_for_each, unique_tones, build_binary_matrix=True):
    tones_to_digit = []

    for tone in tones_for_each:
        tones_to_digit.append(unique_tones.index(tone))

    if build_binary_matrix:
        tones_to_digit = to_categorical(tones_to_digit, len(unique_tones))

    return tones_to_digit


# получение названия тональности по номеру
def from_tone(prediction, unique_tones):
    answers = []

    for i in range(prediction.shape[0]):
        answers.append(unique_tones[prediction[i]])

    return answers


# создание keras модели на основе word2vec модели
def get_model(word2vec_model, COUNT_CLASSES):
    model = Sequential()
    model.add(word2vec_model.wv.get_keras_embedding(train_embeddings=True))

    model.add(Dropout(0.2))

    model.add(Conv1D(50, 3, padding='valid', activation='relu', strides=1))
    model.add(GlobalMaxPooling1D())

    model.add(Dense(250))
    model.add(Dropout(0.2))
    model.add(Activation('relu'))

    model.add(Dense(COUNT_CLASSES, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model


# загружаем словарь RuSentiLex для обучения модели
data = pd.read_csv('tools/rusentilex.csv')
data = data.dropna()
print("Количество слов в словаре: " + str(data['term'].apply(lambda x: len(x.split(' '))).sum()))
print(data[:6])

unique_tones = data.tone.unique()
print(data.tone.value_counts())

# получаем все слова из словаря, предварительно производим обработку на всякий случай (удаляем стоп-слова...)
sentences = np.array(data.term.apply(lambda x: tokenize(x)))
# обучение модели Word2Vec
word2vec_model = Word2Vec(sentences, min_count=1)
# сохраняем word2vec модель
word2vec_model.save('models/word2vec_model')

tokenizer = Tokenizer()
tokenizer.fit_on_texts(sentences)

# преобразование всех текстов в числовые последовательности, заменяя слова на числа по словарю.
text = tokenizer.texts_to_sequences(sentences)
text = pad_sequences(text, maxlen=10)

# работа с keras
X_train, X_test, y_train, y_test = train_test_split(text, data.tone, test_size=0.2)
y_train = to_tone(y_train, unique_tones.tolist())

COUNT_CLASSES = unique_tones.shape[0]
BATCH = 32
EPOCHS_COUNT = 10

keras_model = get_model(word2vec_model, COUNT_CLASSES)
keras_model.summary()

# обучаем keras модель + сохраняем модель
keras_model.fit(X_train, y_train, batch_size=BATCH, epochs=EPOCHS_COUNT, validation_split=0.2,
             callbacks=[ModelCheckpoint('models/keras_model.h5', save_best_only=True)])

test = ['супер', 'классно', 'безупречный', 'убожество', 'убивать', 'нормально', 'ужас']

sequences_test = tokenizer.texts_to_sequences(test)
X_predict = pad_sequences(sequences_test, maxlen=X_train.shape[1])

prediction = keras_model.predict_classes(X_predict)
answers = from_tone(prediction, unique_tones.tolist())

print(answers)
