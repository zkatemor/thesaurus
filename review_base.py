import requests
import json

url = "https://market-scanner.ru/api/reviews"
key = "9d5d736adf18d96386df47deaf23fde6"
text_list = []

# метод удаления из строки HTML-тегов
def remove_html_tags(inp):
    tag = False
    quote = False
    out = ""

    for symbol in inp:
        if symbol == '<' and not quote:
            tag = True
        elif symbol == '>' and not quote:
            tag = False
        elif (symbol == '"' or symbol == "'") and tag:
            quote = not quote
        elif not tag:
            out = out + symbol

    return out.replace('&quot;', '')


# запрос сбора отзыва по id модели
def getReviewById(id):
    data = {'key': key,
            'id': id,
            'quantity': 0,
            'minrating': 1}

    response = requests.post(url=url, data=data)
    js = response.json().get('reviews')

    for text in js:
        text_list.append(remove_html_tags(str(text['pluses']) + ' ' + str(text['minuses']) + ' ' + str(text['comment'])))


# всего 7371 отзывов о различных моделях популярных мобильных телефонах
id_model = [6058600, 6229012, 6976935, 7012977, 8226067, 9323459, 10495456, 13527763, 7713568, 1632006]

for id in id_model:
    getReviewById(id)

# сохранение в json файл
with open('tools/review_db.json', 'w', encoding='utf-8') as f:
    json.dump(text_list, f, ensure_ascii=False, indent=4)
