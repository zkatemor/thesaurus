import json


def get_union(dict_first, dict_second):
    union = []

    for words_first in dict_first:
        for words_second in dict_second:
            if words_first == words_second:
                if words_second not in union:
                    union.append(words_second)
                elif words_first not in union:
                    union.append(words_first)
                else:
                    break

    return union


def get_intersections(dict_first, dict_second):
    intersections = []

    for words_first in dict_first:
        for words_second in dict_second:
            if (words_first == words_second and dict_first[words_first] == dict_second[words_second]) \
                    and words_first not in intersections:
                intersections.append(words_first)

    return intersections


# загружаем построенные словари оценочной лексики из json файла
with open('chi_square_dicts/chi_dict_plus.json', 'r', encoding='utf-8') as f:
    chi_dict_plus = json.load(f)

with open('chi_square_dicts/chi_dict_minus.json', 'r', encoding='utf-8') as f:
    chi_dict_minus = json.load(f)

# формирование общего полученного словаря
chi_dictionary = {}

for word in chi_dict_minus:
    chi_dictionary[word[0]] = 'negative'

for word in chi_dict_plus:
    chi_dictionary[word[0]] = 'positive'

with open('tagged_dictionary/tagged_dictionary.json', 'r', encoding='utf-8') as f:
    cnn_dictionary = json.load(f)

a = {'a': 0, 'b': '2'}
b = {'c': 2, 'b': 1}
c = a.copy()

a.update(b)
chi = chi_dictionary.copy()
chi.update(cnn_dictionary)

print(len(get_intersections(chi_dictionary, cnn_dictionary)))
print(len(get_union(chi_dictionary, cnn_dictionary)))
