n = int(input())
result = 0

if n == 0:
    result = 1
elif n == 1:
    result = 1
else:
    i = 1
    result = 1
    while i <= n:
        a = result
        b = i
        mult_r = 0
        while b > 0:
            mult_r = mult_r + a
            b = b - 1
        result =  mult_r
        i = i + 1

print(result)