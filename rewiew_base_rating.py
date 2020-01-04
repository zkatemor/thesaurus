import requests
from pandas import DataFrame
import json

url = "https://market-scanner.ru/api/reviews"
key = "9d5d736adf18d96386df47deaf23fde6"
text_list_plus = []
text_list_minus = []


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


def getReviewById(id):
    data = {'key': key,
            'id': id,
            'quantity': 0,
            'minrating': 1}

    response = requests.post(url=url, data=data)
   # print(response.text)

    js = response.json().get('reviews')

    for text in js:
        text_list_plus.append(remove_html_tags(str(text['pluses'])))
        text_list_minus.append(remove_html_tags(str(text['minuses'])))


# 439, 689, 955, 804, 930, 529, 555, 661, 476, 1333 = 7371
id_model = [6058600, 6229012, 6976935, 7012977, 8226067, 9323459, 10495456, 13527763, 7713568, 1632006]

for id in id_model:
    getReviewById(id)

with open('chi_square_dict/corpus_minus.json', 'w', encoding='utf-8') as f:
    json.dump(text_list_minus, f, ensure_ascii=False, indent=4)

with open('chi_square_dict/corpus_plus.json', 'w', encoding='utf-8') as f:
    json.dump(text_list_plus, f, ensure_ascii=False, indent=4)