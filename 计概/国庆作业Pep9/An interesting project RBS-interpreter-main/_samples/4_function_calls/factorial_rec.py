
def mult(a, b):
    mult_r = 0
    while b > 0:
        mult_r = mult_r + a
        b = b - 1
    return mult_r

def fac(n):
    if n == 0:
        return 1
    pred = n - 1
    f_pred = fac(pred)
    result = mult(f_pred, n)
    return result

n = int(input())
value = fac(n)
print(value)
