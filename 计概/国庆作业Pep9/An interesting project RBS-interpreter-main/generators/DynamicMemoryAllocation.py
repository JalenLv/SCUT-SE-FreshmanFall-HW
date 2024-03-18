
class DynamicMemoryAllocation():

    def __init__(self, parameters, local_vars, functions):
        self.parameters = parameters
        self.local_vars = local_vars
        self.functions = functions

    # Generate local variables
    def generate(self):
        for function in self.functions:
            print(f'\n;;;; {function} function ;;;;')
            for var in sorted(self.local_vars, key = lambda x: x[2], reverse=False):
                if var[3] == function:
                    print(f'{var[0]}:\t.EQUATE {var[2]}\t;{var[1]} local variable #2d')

            for param in sorted(self.parameters, key = lambda x: x[2], reverse=False):
                if param[3] == function:
                    print(f'{param[0]}:\t.EQUATE {param[2]}\t;{param[1]} formal parameter #2d')
            