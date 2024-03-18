class EntryPoint():

    def __init__(self, instructions) -> None:
        self.__instructions = instructions

    def generate(self):
        for label, instr in self.__instructions:
            s = f'\t\t{instr}' if label == None else f'{str(label+":"):<9}\t{instr}'
            print(s)