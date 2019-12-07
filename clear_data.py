from pandas import DataFrame
import pymorphy2
import json

morph = pymorphy2.MorphAnalyzer()


# очистка текста от посторонних символов
def text_cleaner(text):
    # приведем текст к нижнему регистру
    text = text.lower()

    # оставляем в предложении только русские буквы
    alph = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

    cleaned_text = ''
    for char in text:
        if (char.isalpha() and char[0] in alph) or (char == ' '):
            cleaned_text += char

    result = []
    for word in cleaned_text.split():
        # лемматизируем
        result.append(morph.parse(word)[0].normal_form)

    return ' '.join(result)


# загружаем исходные отзывы из json файла
with open('tools/review_db.json', 'r', encoding='utf-8') as f:
    js = json.load(f)

text_list = []

# очищаем от ненужных символов каждый отзыв
for text in js:
    text_list.append(text_cleaner(text))

df = DataFrame({'Очищенные отзывы: ': text_list})
df.to_excel('data_preparation/clear_db.xlsx', sheet_name='Очищенные отзывы', index=False)

with open('data_preparation/clear_db.json', 'w', encoding='utf-8') as f:
    json.dump(text_list, f, ensure_ascii=False, indent=4)
