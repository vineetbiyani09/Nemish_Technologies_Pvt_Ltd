sentence = input('sentence: ')
search = input('search: ')

sentence = sentence.split()
index = None

for word in sentence :
    i = 0
    strings = []
    for j in range(1, len(word)) :
        strings.append(word[i:j])
    if any(string == search for string in strings) :
        index = sentence.index(word) + 1
        break

if index == None :
    print(-1)
else :
    print(index)
