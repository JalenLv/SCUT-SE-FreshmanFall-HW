a = int(input())            # .BLOCK
b = int(input())            # .BLOCK
result = 0                  # .WORD 0
while b > 0:
    result = result + a
    b = b - 1

print(result)
