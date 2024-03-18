n = int(input())                # .BLOCK 2
i = 1                           # .WORD 1
result = 1                      # .WORD 1
while i <= n:
    a = result                  # .BLOCK 2 
    b = i                       # .BLOCK 2
    mult_r = 0                  # .WORD 0
    while b > 0:
        mult_r = mult_r + a 
        b = b - 1
    result =  mult_r
    i = i + 1

print(result)
