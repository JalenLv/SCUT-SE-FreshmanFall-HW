 
prime_ = [0] * 100

def mult(a, b):
    mult_r = 0
    while b > 0:
        mult_r = mult_r + a
        b = b - 1
    return mult_r

def eratosthenes(num):
    p = 2
    sq_p = mult(p,p)
    while sq_p <= num:
        if (prime_[p] == 0):
            i = sq_p
            while i < num:
                prime_[i] = 1
                i = i + p
        p += 1
        sq_p = mult(p,p)

def print_primes(n):
    eratosthenes(n)
    i = 2
    while i < n:
        if prime_[i] == 0:
            print(i)
        i = i + 1

max = int(input())
print_primes(max)
