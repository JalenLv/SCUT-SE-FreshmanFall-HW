
def mult(a,b):
    mult_r = 0
    while b > 0:
        mult_r = mult_r + a
        b = b - 1
    return mult_r

def fac(n):
    i = 1
    result = 1
    while i <= n:
        result =  mult(result, i)
        i = i + 1
    return result

n = int(input())
value = fac(n)
print(value)
