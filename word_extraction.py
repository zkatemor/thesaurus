import pymorphy2
import json
import collections

morph = pymorphy2.MorphAnalyzer()

# загружаем очищенные отзывы из json файла
with open('data_preparation/clear_db.json', 'r', encoding='utf-8') as f:
    js = json.load(f)

data = []

for text in js:
    data.append(str(text).split(' '))

# наречия
adverb = []
# прилагательные
adjective = []
# глаголы
verb = []
# существительные
noun = []

for text in data:
    for word in text:
        p = morph.parse(word)[0]
        if p.tag.POS == 'ADVB':
            adverb.append(word)
        elif p.tag.POS == 'ADJF' or p.tag.POS == 'ADJS':
            adjective.append(word)
        elif p.tag.POS == 'VERB' or p.tag.POS == 'INFN':
            verb.append(word)
        elif p.tag.POS == 'NOUN':
            noun.append(word)

# подсчёт частоты слов в коллекции и сортировка по убыванию (по частоте)
counter_adverb = collections.Counter(adverb).most_common()
counter_adjective = collections.Counter(adjective).most_common()
counter_verb = collections.Counter(verb).most_common()
counter_noun = collections.Counter(noun).most_common()

with open('unallocated_words/adverb.json', 'w', encoding='utf-8') as f:
    json.dump(counter_adverb, f, ensure_ascii=False, indent=4)

with open('unallocated_words/adjective.json', 'w', encoding='utf-8') as f:
    json.dump(counter_adjective, f, ensure_ascii=False, indent=4)

with open('unallocated_words/verb.json', 'w', encoding='utf-8') as f:
    json.dump(counter_verb, f, ensure_ascii=False, indent=4)

with open('unallocated_words/noun.json', 'w', encoding='utf-8') as f:
    json.dump(counter_noun, f, ensure_ascii=False, indent=4)