
class StaticMemoryAllocation():

    def __init__(self, global_vars: dict()) -> None:
        self.__global_vars = global_vars

    def generate(self):
        print('; Allocating Global (static) memory')
        for n in self.__global_vars:
            if len(n) > 2:
                if n[2][0] =="_" and n[2][1:].isupper():
                    print(f'{n[0]}:\t.EQUATE {n[1]} ; {n[2]} constant')
                else:
                    print(f'{n[0]}:\t.WORD {n[1]} ; {n[2]} global variable')
            else:
                print(f'{str(n[0]+":"):<9}\t.BLOCK 2\t;{n[1]} global variable') # reserving memory
