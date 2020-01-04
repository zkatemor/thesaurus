import json

with open('chi_square_dicts/chi_dict_minus.json', 'r', encoding='utf-8') as f:
    chi_dict_minus = json.load(f)

with open('chi_square_dicts/chi_dict_plus.json', 'r', encoding='utf-8') as f:
    chi_dict_plus = json.load(f)

print("Количество положительных слов = " + str(len(chi_dict_plus)))
print("Количество отрицательных слов = " + str(len(chi_dict_minus)))

print("Первые 10 положительно окрашенных слов:")
for i in range(0, 10):
    print(chi_dict_plus[i][0])

print("Первые 10 отрицательно окрашенных слов:")
for i in range(0, 10):
    print(chi_dict_minus[i][0])