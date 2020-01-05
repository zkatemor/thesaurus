import json
from xlwings import xrange
import numpy as np


def algorithm_evaluation(test, predict):
    # количество правильно определенных категорий в подкорпусе
    sum_correct = 0
    # количество определенных категорий в подкорпусе
    sum_exist = 0
    chi_words = [w[0] for w in predict]

    for i in range(0, len(test)):
        # если к слову удалось подобрать категорию
        if test[i][0] in chi_words:
            # увеличиваем значение определенных категорий
            sum_exist += 1

            for j in range(0, len(predict)):
                # находим то же самое слово в предсказанных данных
                if test[i][0] == predict[j][0]:
                    # проверяем полярность
                    if test[i][1] == predict[j][1]:
                        # если сходится, то увеличиваем значение
                        sum_correct += 1

    return sum_correct, sum_exist


# загружаем все кандидаты на тонально-окрашенные слова из json файла
with open('chi_square_dicts/dictionary_plus.json', 'r', encoding='utf-8') as f:
    dictionary_plus = json.load(f)

with open('chi_square_dicts/dictionary_minus.json', 'r', encoding='utf-8') as f:
    dictionary_minus = json.load(f)

# формирование общего словаря для разделения на корпусы
dictionary = []

for word in dictionary_plus:
    tmp_dict = [word[0], 'positive']
    dictionary.append(tmp_dict)

for word in dictionary_minus:
    tmp_dict = [word[0], 'negative']
    dictionary.append(tmp_dict)

# загружаем построенные словари оценочной лексики из json файла
with open('chi_square_dicts/chi_dict_plus.json', 'r', encoding='utf-8') as f:
    chi_dict_plus = json.load(f)

with open('chi_square_dicts/chi_dict_minus.json', 'r', encoding='utf-8') as f:
    chi_dict_minus = json.load(f)

# формирование общего полученного словаря
chi_dictionary = []

for word in chi_dict_minus:
    tmp_dict = [word[0], 'negative']
    chi_dictionary.append(tmp_dict)

for word in chi_dict_plus:
    tmp_dict = [word[0], 'positive']
    chi_dictionary.append(tmp_dict)

# разделение на три равные подкорпуса
corpus = [dictionary[i:i + int(len(dictionary) / 3)] for i in xrange(0, len(dictionary), int(len(dictionary) / 3))]

corpus_a = corpus[0]
corpus_b = corpus[1]
corpus_c = corpus[2]

# получаем количество слов в подкорпусе
N = len(corpus_a)
print("N = " + str(N))

# подсчитываем необходимые параметры
T_a, K_a = algorithm_evaluation(corpus_a, chi_dictionary)
print("T_a = " + str(T_a))
print("K_a = " + str(K_a))

T_b, K_b = algorithm_evaluation(corpus_b, chi_dictionary)
print("T_b = " + str(T_b))
print("K_b = " + str(K_b))

T_c, K_c = algorithm_evaluation(corpus_c, chi_dictionary)
print("T_c = " + str(T_c))
print("K_c = " + str(K_c))

# рассчет точности и полноты
Precision_A = T_a / K_a
Precision_B = T_b / K_b
Precision_C = T_c / K_c

Recall_A = T_a / N
Recall_B = T_b / N
Recall_C = T_c / N

print("Точность с подкорпусом а = " + str(Precision_A))
print("Точность с подкорпусом b = " + str(Precision_B))
print("Точность с подкорпусом c = " + str(Precision_C))

print("Полнота с подкорпусом а = " + str(Recall_A))
print("Полнота с подкорпусом b = " + str(Recall_B))
print("Полнота с подкорпусом c = " + str(Recall_C))

# рассчет окончательной точности и полноты
Precision = np.mean([Precision_A, Precision_B, Precision_C])
Recall = np.mean([Recall_A, Recall_B, Recall_C])

print("Точность = " + str(Precision))
print("Полнота = " + str(Recall))




