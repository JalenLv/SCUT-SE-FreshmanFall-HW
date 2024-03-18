from itertools import product
from string import ascii_uppercase

# Dictionary wrapper class
class SymbolTable:
    def __init__(self):
        self.dict = {}
        self.symbol_generator = ("".join(ch) for ch in product(ascii_uppercase, repeat=8)) # Generator