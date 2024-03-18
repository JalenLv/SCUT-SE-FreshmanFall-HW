
def fib(n):
    if n <= 1:
        result = n
    else:
        pred_1 = n - 1
        r_1 = fib(pred_1)
        pred_2 = n - 2
        r_2 = fib(pred_2)
        result = r_1 + r_2
    return result

value = int(input())
result = fib(value)
print(result)
