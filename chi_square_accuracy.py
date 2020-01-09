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


# рассчет F-меры
def get_f1_score(precision, recall):
    return 2 * (precision * recall)/(precision + recall)

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
precision_a = T_a / K_a
precision_b = T_b / K_b
precision_c = T_c / K_c

recall_a = T_a / N
recall_b = T_b / N
recall_c = T_c / N

print("Точность с подкорпусом а = " + str(precision_a))
print("Точность с подкорпусом b = " + str(precision_b))
print("Точность с подкорпусом c = " + str(precision_c))

print("Полнота с подкорпусом а = " + str(recall_a))
print("Полнота с подкорпусом b = " + str(recall_b))
print("Полнота с подкорпусом c = " + str(recall_c))

print("F-мера с подкорпусом а = " + str(get_f1_score(precision_a, recall_a)))
print("F-мера с подкорпусом b = " + str(get_f1_score(precision_b, recall_b)))
print("F-мера с подкорпусом c = " + str(get_f1_score(precision_c, recall_c)))

# рассчет окончательной точности и полноты
precision = np.mean([precision_a, precision_b, precision_c])
recall = np.mean([recall_a, recall_b, recall_c])
f_score = get_f1_score(precision, recall)

print("Точность = " + str(precision))
print("Полнота = " + str(recall))
print("F-мера = " + str(f_score))




