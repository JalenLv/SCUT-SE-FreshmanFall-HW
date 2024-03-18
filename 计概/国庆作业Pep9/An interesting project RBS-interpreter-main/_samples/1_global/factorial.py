n = int(input())
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
