
def caesar(key, n):
    word_ = [0] * n # Initializing an array with n cells

    i = 0
    while i < n:
        data = int(input())
        word_[i] = data + key
        i = i + 1

    i = 0
    while i < n:
        print(word_[i])
        i = i + 1

key = int(input())
n = int(input())
caesar(key, n)
