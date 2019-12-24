import json
from collections import Counter

part_of_speech = ['NOUN', 'ADVB', 'ADJF', 'ADJS', 'VERB', 'INFN']

# загружаем неразмеченные списки слов из json файла
with open('unallocated_words/dictionary.json', 'r', encoding='utf-8') as f:
    js = json.load(f)

dictionary = []

# оставляем в словаре только глаголы, существительные, прилагательные и наречия
for list_js in js:
    for i in list_js:
        if i[-4:] in part_of_speech:
            dictionary.append(i)

# сортируем по частоте встречаемости и удаляем слова, которые повторяются меньше 5 раз
counter = Counter(dictionary)
new_counter = Counter({key: value for key, value in counter.items() if value > 5}).most_common()

# добавляем слова в json файл
with open('unallocated_words/unallocated_dictionary.json', 'w', encoding='utf-8') as f:
    json.dump(new_counter, f, ensure_ascii=False, indent=4)
