import pymorphy2
import json
import nltk


# токинизируем текст
def text_tokenizer(text):
    # для перевода в нормальную форму
    morph = pymorphy2.MorphAnalyzer()
    # удаляем все символы, кроме кириллицы
    regex_tokenizer = nltk.tokenize.RegexpTokenizer('[а-яА-ЯЁё]+')
    # получаем слова
    words = regex_tokenizer.tokenize(text.lower())
    # получаем стоп-слова
    stop_words = set(nltk.corpus.stopwords.words("russian"))
    # приводим каждое слово в нормальную форму и удаляем стоп-слова
    without_stop_words = [(morph.parse(w)[0]).normal_form for w in words if w not in stop_words and len(w) > 1]
    # добавляем к каждому слову часть речи
    output = [add_part_of_speech(morph, word) for word in without_stop_words]
    return output


# добавление части речи к слову
def add_part_of_speech(morph, word):
    p = morph.parse(word)[0]
    word += '_' + str(p.tag.POS)
    return word


# загружаем исходные отзывы из json файла
with open('tools/review_db.json', 'r', encoding='utf-8') as f:
    js = json.load(f)

# получаем слова в нужной форме
tokens = [text_tokenizer(js[i]) for i in range(0, len(js))]
# добавляем слова в json файл
with open('unallocated_words/dictionary.json', 'w', encoding='utf-8') as f:
    json.dump(tokens, f, ensure_ascii=False, indent=4)
