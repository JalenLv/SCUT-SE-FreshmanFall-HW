a = int(input())
b = int(input())

if a < b: # as b is the loop counter, minimizing it
    tmp = b
    b = a
    a = tmp

result = 0
while b > 0:
    result = result + a
    b = b - 1

print(result)