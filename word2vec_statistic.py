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


with open('tagged_dictionary/tagged_dictionary.json', 'r', encoding='utf-8') as f:
    dictionary = json.load(f)

count_positive = 0
count_negative = 0
count_neutral = 0

positive_words = []
negative_words = []
neutral_words = []

for word in dictionary:
    if dictionary[word] == 'positive':
        count_positive += 1
        positive_words.append(word)
    elif dictionary[word] == 'neutral':
        count_neutral += 1
        neutral_words.append(word)
    else:
        count_negative += 1
        negative_words.append(word)

print("Количество положительных слов = " + str(count_positive))
print("Количество отрицательных слов = " + str(count_negative))
print("Количество нейтральных слов = " + str(count_neutral))

print("Количество положительных прилагательных = " + str((get_ADJF_count(positive_words))))
print("Количество положительных глаголов = " + str((get_VERB_count(positive_words))))
print("Количество положительных существительных = " + str((get_NOUN_count(positive_words))))
print("Количество положительных наречий = " + str((get_ADVB_count(positive_words))))

print("Количество отрицательных прилагательных = " + str((get_ADJF_count(negative_words))))
print("Количество отрицательных глаголов = " + str((get_VERB_count(negative_words))))
print("Количество отрицательных существительных = " + str((get_NOUN_count(negative_words))))
print("Количество отрицательных наречий = " + str((get_ADVB_count(negative_words))))

print("Количество нейтральных прилагательных = " + str((get_ADJF_count(neutral_words))))
print("Количество нейтральных глаголов = " + str((get_VERB_count(neutral_words))))
print("Количество нейтральных существительных = " + str((get_NOUN_count(neutral_words))))
print("Количество нейтральных наречий = " + str((get_ADVB_count(neutral_words))))