import json

with open('tagged_dictionary/tagged_dictionary.json', 'r', encoding='utf-8') as f:
    dictionary = json.load(f)

count_positive = 0
count_negative = 0
count_neutral = 0

for word in dictionary:
    if dictionary[word] == 'positive':
        count_positive += 1
    elif dictionary[word] == 'neutral':
        count_neutral += 1
    else:
        count_negative += 1

print("Количество положительных слов = " + str(count_positive))
print("Количество отрицательных слов = " + str(count_negative))
print("Количество нейтральных слов = " + str(count_neutral))