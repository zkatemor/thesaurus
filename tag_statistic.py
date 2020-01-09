# возвращает количество глаголов
def get_VERB_count(words):
    count = 0
    for word in words:
        if word[-4:] == 'VERB' or word[-4:] == 'INFN':
            count += 1
    return count


# возвращает количество существительных
def get_NOUN_count(words):
    count = 0
    for word in words:
        if word[-4:] == 'NOUN':
            count += 1
    return count


# возвращает количество прилагательных
def get_ADJF_count(words):
    count = 0
    for word in words:
        if word[-4:] == 'ADJF' or word[-4:] == 'ADJS':
            count += 1
    return count


# возвращает количество наречий
def get_ADVB_count(words):
    count = 0
    for word in words:
        if word[-4:] == 'ADVB':
            count += 1
    return count
