afinn = []
f = open('other_dictionary/AFINN-111.txt')
for line in f.readlines():
    line = line.replace("\n", "")
    tmp = line.split('\t')
    afinn.append(tmp)

positive = 0
negative = 0
neutral = 0

for word in afinn:
    score = int(word[1])
    if score == 0 or score == 1 or score == -1:
        neutral += 1
    elif score > 1:
        positive += 1
    else:
        negative += 1

print(positive)
print(negative)
print(neutral)
