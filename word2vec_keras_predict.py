import csv
import pickle
from itertools import zip_longest
import keras
import json
import pandas as pd


# получение тональностей по id
def from_tone(prediction, tones):
    answers = []

    for i in range(prediction.shape[0]):
        answers.append(tones[prediction[i]])

    return answers


# получение раннее сохраненной модели
from keras_preprocessing.sequence import pad_sequences

model = keras.models.load_model('models/model.h5')

f = open('models/maxlen.bin', 'r')
maxlen = int(f.read())
f.close()

with open('models/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# загружаем неразмеченный словарь из json файла
with open('drive/My Drive/coursework/unallocated_dictionary.json', 'r', encoding='utf-8') as f:
    js = json.load(f)

df = pd.read_csv('tools/rusentilex.csv')

unallocated_words = [[word[0][:-5]] for word in js]
unallocated_words_tokens = tokenizer.texts_to_sequences(unallocated_words)
unallocated_words__pad = pad_sequences(unallocated_words_tokens, maxlen=maxlen)

predict = model.predict_classes(x=unallocated_words__pad)
answers = from_tone(predict, df['tone'].unique().tolist())

keys = [word[0] for word in js]
dictionary = dict(zip(keys, answers))

# сохраняем размеченный словарь в json файл
with open('tagged_dictionary/tagged_dictionary.json', 'w', encoding='utf-8') as f:
    json.dump(dictionary, f, ensure_ascii=False, indent=4)
# и в csv файл
d = [keys, answers]
export_data = zip_longest(*d, fillvalue='')
with open('tagged_dictionary/ged_dictionary.csv', 'w', encoding='utf-8', newline='') as f:
    wr = csv.writer(f)
    wr.writerow(("term", "tone"))
    wr.writerows(export_data)
f.close()
