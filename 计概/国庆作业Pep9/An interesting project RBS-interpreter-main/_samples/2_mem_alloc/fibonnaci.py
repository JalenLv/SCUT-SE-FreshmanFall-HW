n = int(input())        # .BLOCK 2
a = 0                   # .WORD 0
b = 1                   # .WORD 1
i = 0                   # .WORD 1
while i < n:
    tmp  = a + b        # .BLOCK 2 (optimized: .WORD 1 as we know statically a and b)
    a = b
    b = tmp
    i = i + 1

print(a)
