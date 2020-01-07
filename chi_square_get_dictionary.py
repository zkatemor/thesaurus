import nltk
import json
from collections import Counter
import pymorphy2

part_of_speech = ['NOUN', 'ADVB', 'ADJF', 'ADJS', 'VERB', 'INFN']


# токинизируем текст
def text_tokenizer(text):
    # для перевода в нормальную форму
    print(text)
    morph = pymorphy2.MorphAnalyzer()
    # удаляем все символы, кроме кириллицы
    regex_tokenizer = nltk.tokenize.RegexpTokenizer('[а-яА-ЯЁё]+')
    # приводим все слова к нижнему регистру
    words = regex_tokenizer.tokenize(text.lower())
    # получаем стоп-слова
    stop_words = set(nltk.corpus.stopwords.words("russian"))
    # приводим каждое слово в нормальную форму и удаляем стоп-слова
    without_stop_words = [(morph.parse(w)[0]).normal_form for w in words if w not in stop_words and len(w) > 1]
    # добавляем к каждому слову часть речи
    output = [add_part_of_speech(morph, word) for word in without_stop_words]
    return output


# добавление части речи к слову
def add_part_of_speech(morph, word):
    p = morph.parse(word)[0]
    word += '_' + str(p.tag.POS)
    return word


# заполнение списков тонально окрашенных слов (по частям речи)
def create_dictionary(corpus):
    # получаем слова в нужной форме
    tokens = [text_tokenizer(review) for review in corpus]
    dictionary = []

    # оставляем в словаре только глаголы, существительные, прилагательные и наречия
    for words in tokens:
        for word in words:
            if word[-4:] in part_of_speech:
                dictionary.append(word)

    # сортируем по частоте встречаемости и удаляем слова, которые повторяются меньше 5 раз
    counter = Counter(dictionary)
    new_counter = Counter({key: value for key, value in counter.items() if value > 5}).most_common()

    return new_counter


# проверяет корректность словосочетания по частям речи
def check_collocations(tag_first, tag_second):
    # если существительное + прилагательное
    if tag_first == 'NOUN' and (tag_second == 'ADJF' or tag_second == 'ADJS'):
        check = True
    elif tag_second == 'NOUN' and (tag_first == 'ADJF' or tag_first == 'ADJS'):
        check = True
    # если глагол + наречие
    elif tag_first == 'VERB' and tag_second == 'ADVB':
        check = True
    elif tag_second == 'VERB' and tag_first == 'ADVB':
        check = True
    # прилагательное + наречие
    elif (tag_first == 'ADJF' or tag_first == 'ADJS') and tag_second == 'ADVB':
        check = True
    elif (tag_second == 'ADJF' or tag_second == 'ADJS') and tag_first == 'ADVB':
        check = True
    else:
        check = False

    return check


# заполнение словаря тонально окрашенных словосочетаний (с частями речи)
def create_dictionary_collocations(corpus):
    # получаем слова в нужной форме
    tokens = [text_tokenizer(review) for review in corpus]
    dictionary = []
    print(tokens)

    for words in tokens:
        for w in range(0, len(words) - 1):
            if check_collocations(words[w][-4:], words[w + 1][-4:]):
                collocations = words[w] + ' ' + words[w + 1]
                print(collocations)
                dictionary.append(collocations)

    # сортируем по частоте встречаемости
    counter = Counter(dictionary).most_common()

    return counter


with open('chi_square_dicts/corpus_minus.json', 'r', encoding='utf-8') as f:
    corpus_minus = json.load(f)

with open('chi_square_dicts/corpus_plus.json', 'r', encoding='utf-8') as f:
    corpus_plus = json.load(f)

'''
dictionary_plus = create_dictionary(corpus_plus)
dictionary_minus = create_dictionary(corpus_minus)

with open('chi_square_dicts/dictionary_plus.json', 'w', encoding='utf-8') as f:
    json.dump(dictionary_plus, f, ensure_ascii=False, indent=4)

with open('chi_square_dicts/dictionary_minus.json', 'w', encoding='utf-8') as f:
    json.dump(dictionary_minus, f, ensure_ascii=False, indent=4)

'''

dictionary_plus = create_dictionary_collocations(corpus_plus)
dictionary_minus = create_dictionary_collocations(corpus_minus)

with open('chi_square_dicts/dictionary_collocations_plus.json', 'w', encoding='utf-8') as f:
    json.dump(dictionary_plus, f, ensure_ascii=False, indent=4)

with open('chi_square_dicts/dictionary_collocations_minus.json', 'w', encoding='utf-8') as f:
    json.dump(dictionary_minus, f, ensure_ascii=False, indent=4)
