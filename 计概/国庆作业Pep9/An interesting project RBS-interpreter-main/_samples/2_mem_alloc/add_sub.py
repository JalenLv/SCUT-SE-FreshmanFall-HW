value = int(input())        # .BLOCK 2
_UNIV = 42                  # .EQUATE 42
result = value + _UNIV
variable = 3                # .WORD 3
result = result - variable
variable = 1
result = result - variable
print(result)
