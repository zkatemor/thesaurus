import json


# возвращает количество глаголов
def get_VERB_count(words):
    count = 0
    for word in words:
        if word[-4:] == 'VERB' or word[-4:] == 'INFN':
            count += 1
    return count


# возвращает количество существительных
def get_NOUN_count(words):
    count = 0
    for word in words:
        if word[-4:] == 'NOUN':
            count += 1
    return count


# возвращает количество прилагательных
def get_ADJF_count(words):
    count = 0
    for word in words:
        if word[-4:] == 'ADJF' or word[-4:] == 'ADJS':
            count += 1
    return count


# возвращает количество наречий
def get_ADVB_count(words):
    count = 0
    for word in words:
        if word[-4:] == 'ADVB':
            count += 1
    return count


with open('chi_square_dicts/chi_dict_minus.json', 'r', encoding='utf-8') as f:
    chi_dict_minus = json.load(f)

with open('chi_square_dicts/chi_dict_plus.json', 'r', encoding='utf-8') as f:
    chi_dict_plus = json.load(f)

with open('chi_square_dicts/chi_dict_collocations_minus.json', 'r', encoding='utf-8') as f:
    chi_dict_collocations_minus = json.load(f)

with open('chi_square_dicts/chi_dict_collocations_plus.json', 'r', encoding='utf-8') as f:
    chi_dict_collocations_plus = json.load(f)

print("Количество положительных слов = " + str(len(chi_dict_plus)))
print("Количество отрицательных слов = " + str(len(chi_dict_minus)))
print("Количество положительных словосочетаний = " + str(len(chi_dict_collocations_plus)))
print("Количество отрицательных словосочетаний = " + str(len(chi_dict_collocations_minus)))

words_plus = []
words_minus = []

for word in chi_dict_minus:
    words_minus.append(word[0])

for word in chi_dict_plus:
    words_plus.append(word[0])

print("Количество положительных прилагательных = " + str((get_ADJF_count(words_plus))))
print("Количество положительных глаголов = " + str((get_VERB_count(words_plus))))
print("Количество положительных существительных = " + str((get_NOUN_count(words_plus))))
print("Количество положительных наречий = " + str((get_ADVB_count(words_plus))))

print("Количество отрицательных прилагательных = " + str((get_ADJF_count(words_minus))))
print("Количество отрицательных глаголов = " + str((get_VERB_count(words_minus))))
print("Количество отрицательных существительных = " + str((get_NOUN_count(words_minus))))
print("Количество отрицательных наречий = " + str((get_ADVB_count(words_minus))))

