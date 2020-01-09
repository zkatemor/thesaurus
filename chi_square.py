import json

# вычисление критерия согласия Пирсона (хи-квадрат)
def get_chi_square(a, b, c, d):
    n = a + b + c + d

    numerator = n * pow(a * d - b * c, 2)
    denominator = (a + b) * (a + c) * (b + d) * (c + d)

    return numerator / denominator


# вычисление суммы частот всех слов из словаря
def get_sum(dict):
    sum = 0

    for word in dict:
        sum += word[1]

    return sum


# получаем отсортированный словарь оценочной лексики с критерием хи-квадрат
def sort_chi_dict(dict_first, dict_sec):
    sum_first = get_sum(dict_first)
    sum_second = get_sum(dict_sec)
    sort_dict = {}

    # проходим по всем словам/словосочетаниям из словаря и высчитываем a, b, c, d
    for i in range(0, len(dict_first)):
        a = dict_first[i][1]
        b = 0

        for j in range(0, len(dict_sec)):
            # если слово/словосочетание встретилось и во втором словаре тоже
            if dict_first[i][0] == dict_sec[j][0]:
                b = dict_sec[j][1]

        c = sum_first - a
        d = sum_second - b

        # если слово/словосочетание встретилось в первом словаре больше, чем во втором
        if a > b:
            # добавляем его в словарь
            sort_dict[dict_first[i][0]] = get_chi_square(a, b, c, d)

    l = lambda x: x[1]
    # сортируем полученный словарь
    sort_dict = sorted(sort_dict.items(), key=l, reverse=True)

    return sort_dict


# загружаем рассортированные слова-кандидаты
with open('chi_square_dicts/dictionary_plus.json', 'r', encoding='utf-8') as f:
    dictionary_plus = json.load(f)

with open('chi_square_dicts/dictionary_minus.json', 'r', encoding='utf-8') as f:
    dictionary_minus = json.load(f)

chi_dict_plus = sort_chi_dict(dictionary_plus, dictionary_minus)
chi_dict_minus = sort_chi_dict(dictionary_minus, dictionary_plus)

# выгружаем полученный словарь слов
with open('chi_square_dicts/chi_dict_plus.json', 'w', encoding='utf-8') as f:
    json.dump(chi_dict_plus, f, ensure_ascii=False, indent=4)

with open('chi_square_dicts/chi_dict_minus.json', 'w', encoding='utf-8') as f:
    json.dump(chi_dict_minus, f, ensure_ascii=False, indent=4)

# загружаем рассортированные словосочетания-кандидаты
with open('chi_square_dicts/dictionary_collocations_plus.json', 'r', encoding='utf-8') as f:
    dictionary_plus = json.load(f)

with open('chi_square_dicts/dictionary_collocations_minus.json', 'r', encoding='utf-8') as f:
    dictionary_minus = json.load(f)

chi_dict_plus = sort_chi_dict(dictionary_plus, dictionary_minus)
chi_dict_minus = sort_chi_dict(dictionary_minus, dictionary_plus)

# выгружаем полученный словарь словосочетаний
with open('chi_square_dicts/chi_dict_collocations_plus.json', 'w', encoding='utf-8') as f:
    json.dump(chi_dict_plus, f, ensure_ascii=False, indent=4)

with open('chi_square_dicts/chi_dict_collocations_minus.json', 'w', encoding='utf-8') as f:
    json.dump(chi_dict_minus, f, ensure_ascii=False, indent=4)