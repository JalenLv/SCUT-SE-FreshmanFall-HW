word_ = [0] * 25 # Initializing an array with 25 cells

key = int(input())
n = int(input())

if n > 25:
    exit(-1) # Pep/9 translation: STOP

i = 0
while i < n:
    data = int(input())
    word_[i] = data + key
    i = i + 1

i = 0
while i < n:
    print(word_[i])
    i = i + 1






