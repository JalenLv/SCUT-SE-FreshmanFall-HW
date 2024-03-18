cache_ = [0] * 25 # arrays are postfixed by _ and initialized that way

def fib(n):
    if cache_[n] != 0:
        return cache_[n]
    elif n <= 1: 
        result = n
    else:
        pred_1 = n-1
        r_1 = fib(pred_1)
        pred_2 = n-2
        r_2 = fib(pred_2)
        result = r_1 + r_2
    cache_[n] = result
    return result

n = int(input())
value = fib(n)
print(value)