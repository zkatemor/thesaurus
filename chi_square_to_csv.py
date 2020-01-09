import json
import csv
from itertools import zip_longest

with open('chi_square_dicts/chi_dict_plus.json', 'r', encoding='utf-8') as f:
    words_plus = json.load(f)

with open('chi_square_dicts/chi_dict_minus.json', 'r', encoding='utf-8') as f:
    words_minus = json.load(f)

with open('chi_square_dicts/chi_dict_collocations_plus.json', 'r', encoding='utf-8') as f:
    collocations_plus = json.load(f)

with open('chi_square_dicts/chi_dict_collocations_minus.json', 'r', encoding='utf-8') as f:
    collocations_minus = json.load(f)

keys = []
answers = []

for words in words_plus:
    keys.append(words[0])
    answers.append(words[1])

d = [keys, answers]
export_data = zip_longest(*d, fillvalue='')

with open('chi_square_dicts/dictionary_plus.csv', 'w', encoding='utf-8', newline='') as f:
    wr = csv.writer(f)
    wr.writerow(("term", "chi_square"))
    wr.writerows(export_data)
f.close()

keys = []
answers = []

for words in words_minus:
    keys.append(words[0])
    answers.append(words[1])

d = [keys, answers]
export_data = zip_longest(*d, fillvalue='')

with open('chi_square_dicts/dictionary_minus.csv', 'w', encoding='utf-8', newline='') as f:
    wr = csv.writer(f)
    wr.writerow(("term", "chi_square"))
    wr.writerows(export_data)
f.close()

keys = []
answers = []

for words in collocations_plus:
    keys.append(words[0])
    answers.append(words[1])

d = [keys, answers]
export_data = zip_longest(*d, fillvalue='')

with open('chi_square_dicts/collocations_plus.csv', 'w', encoding='utf-8', newline='') as f:
    wr = csv.writer(f)
    wr.writerow(("term", "chi_square"))
    wr.writerows(export_data)
f.close()


keys = []
answers = []

for words in collocations_minus:
    keys.append(words[0])
    answers.append(words[1])

d = [keys, answers]
export_data = zip_longest(*d, fillvalue='')

with open('chi_square_dicts/collocations_minus.csv', 'w', encoding='utf-8', newline='') as f:
    wr = csv.writer(f)
    wr.writerow(("term", "chi_square"))
    wr.writerows(export_data)
f.close()