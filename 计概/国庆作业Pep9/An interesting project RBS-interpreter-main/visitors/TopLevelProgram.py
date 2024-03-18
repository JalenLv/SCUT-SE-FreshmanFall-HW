import ast

LabeledInstruction = tuple[str, str]

class TopLevelProgram(ast.NodeVisitor):
    """We supports assignments and input/print calls"""
    
    def __init__(self, entry_point, to_remove, symbol_table, functions_dict, visited, f_param = 0, f_local_var = 0, global_vars = set()) -> None:
        super().__init__()
        self.__instructions = list()
        self.__record_instruction('NOP1', label=entry_point)
        self.__should_save = True
        self.__current_variable = None
        self.__elem_id = 0
        self.__is_func = False
        self.visited = visited
        self.to_remove = to_remove
        self.symbol_table = symbol_table
        self.functions = functions_dict
        self.f_param = f_param
        self.f_local_var = f_local_var
        self.global_var = global_vars

    def finalize(self):
        self.__instructions.append((None, '.END'))
        return self.__instructions
    
    # Return Functions
    def ret(self):
        if self.__instructions[-1][0] != 'RET':
            self.__record_instruction('RET')
        return self.__instructions

    ####
    ## Handling Assignments (variable = ...)
    ####

    def visit_Assign(self, node):
        # remembering the name of the target
        self.__current_variable = node.targets[0].id

        if not self.__is_func:
            self.global_var.add(self.symbol_table.dict[self.__current_variable])
            self.global_var.add(self.__current_variable)

        # visiting the left part, now knowing where to store the result
        self.visit(node.value)

        if self.__should_save:
            if self.__current_variable in self.to_remove:
                self.__remove_prev()
                self.to_remove.remove(self.__current_variable)
            else:
                self.__access_memory(node.targets[0], 'STWA')
        else:
            self.__should_save = True
        self.__current_variable = None

    def visit_Constant(self, node):
        self.__record_instruction(f'LDWA {node.value},i')
    
    def visit_Name(self, node):
        self.__access_memory(node, 'LDWA')

    def visit_BinOp(self, node):
        self.__access_memory(node.left, 'LDWA')
        if isinstance(node.op, ast.Add):
            self.__access_memory(node.right, 'ADDA')
        elif isinstance(node.op, ast.Sub):
            self.__access_memory(node.right, 'SUBA')
        else:
            raise ValueError(f'Unsupported binary operator: {node.op}')

    def visit_Call(self, node):

        if node.func.id in self.functions:
            args = node.args
            if len(args) > 0 and type(args[0]) == ast.Name:
                self.__pass_parameters(args, True)
            else:
                self.__pass_parameters(args, False)
            self.__record_instruction(f'CALL {node.func.id}')

        indicator = 's' if self.__is_func else 'd'

        match node.func.id:
            case 'int': 
                # Let's visit whatever is casted into an int
                self.visit(node.args[0])
            case 'input':
                # We are only supporting integers for now
                self.__record_instruction(f'DECI {self.symbol_table.dict[self.__current_variable]},{indicator}')
                self.__should_save = False # DECI already save the value in memory
            case 'print':
                # We are only supporting integers for now
                self.__record_instruction(f'DECO {self.symbol_table.dict[node.args[0].id]},{indicator}')
            # case _:
            #     raise ValueError(f'Unsupported function call: { node.func.id}')

    ####
    ## Handling While loops (only variable OP variable)
    ####

    def visit_While(self, node):
        loop_id = self.__identify()
        inverted = {
            ast.Lt:  'BRGE', # '<'  in the code means we branch if '>=' 
            ast.LtE: 'BRGT', # '<=' in the code means we branch if '>' 
            ast.Gt:  'BRLE', # '>'  in the code means we branch if '<='
            ast.GtE: 'BRLT', # '>=' in the code means we branch if '<'
            ast.Eq : 'BRNE', # '==' in the code means we branch if '!='
            ast.NotEq: 'BREQ', # '!=' in the code means we branch if '=='
        }
        # left part can only be a variable
        self.__access_memory(node.test.left, 'LDWA', label = f'test_{loop_id}')
        # right part can only be a variable
        self.__access_memory(node.test.comparators[0], 'CPWA')
        # Branching is condition is not true (thus, inverted)
        self.__record_instruction(f'{inverted[type(node.test.ops[0])]} end_l_{loop_id}')
        # Visiting the body of the loop
        for contents in node.body:
            self.visit(contents)
        self.__record_instruction(f'BR test_{loop_id}')
        # Sentinel marker for the end of the loop
        self.__record_instruction(f'NOP1', label = f'end_l_{loop_id}')

    def visit_If(self, node):
        if_id = self.__identify()
        inverted = {
            ast.Lt:  'BRGE', # '<'  in the code means we branch if '>=' 
            ast.LtE: 'BRGT', # '<=' in the code means we branch if '>' 
            ast.Gt:  'BRLE', # '>'  in the code means we branch if '<='
            ast.GtE: 'BRLT', # '>=' in the code means we branch if '<'
            ast.Eq : 'BRNE', # '==' in the code means we branch if '!='
            ast.NotEq: 'BREQ', # '!=' in the code means we branch if '=='
        }
        # left part can only be a variable
        self.__access_memory(node.test.left, 'LDWA', label = f'test_{if_id}')
        # right part can only be a variable
        self.__access_memory(node.test.comparators[0], 'CPWA')
        # Branching is condition is not true (thus, inverted)
        self.__record_instruction(f'{inverted[type(node.test.ops[0])]} else_{if_id}')
        # Visiting the body of the loop
        for contents in node.body:
            self.visit(contents)
        self.__record_instruction(f'BR end_{if_id}')
        # Sentinel marker for the else
        self.__record_instruction(f'NOP1', label = f'else_{if_id}')
        # Visiting the body of the else
        for contents in node.orelse:
            self.visit(contents)
        # Sentinel marker for the end of the if
        self.__record_instruction(f'NOP1', label = f'end_{if_id}')

    ####
    ## Function Calls
    ####

    def visit_FunctionDef(self, node):

        # Using __is_func to know if we are in a function or not, changes the implementation of some instructions (intermediate)
        self.__is_func = True
        stack_size = self.functions[node.name]

        if node.name not in self.visited:
            self.visited.add(node.name)

            # Allocate relevant for the function
            self.__record_instruction(f'SUBSP {stack_size},i')

            for contents in node.body:
                if type(contents) != ast.Return:
                    self.visit(contents)
            
            # Deallocate relevant memory
            self.__record_instruction(f'ADDSP {stack_size},i')

        self.__is_func = False
        
    
    def visit_Return(self, node):
        # Making sure to store the return value in the accumulator (constant vs name)
        if type(node.value) == ast.Constant:
                self.__record_instruction(f'LDWA {node.value.value},s')
        else:
            self.__record_instruction(f'LDWA {self.symbol_table.dict[node.value.id]},s')
        self.__record_instruction(f'RET')

    ####
    ## Helper functions to 
    ####

    def __record_instruction(self, instruction, label = None):
        self.__instructions.append((label, instruction))

    def __access_memory(self, node, instruction, label = None):

        # Relevant memory allocation (s, d, i)
        if self.__is_func:
            if isinstance(node, ast.Constant):
                self.__record_instruction(f'{instruction} {node.value},i', label)
            else:
                if self.symbol_table.dict[node.id] in self.global_var:
                    
                    if self.__check_constant(node.id):
                        self.__record_instruction(f'{instruction} {self.symbol_table.dict[node.id]},i', label)
                    
                    else:
                        self.__record_instruction(f'{instruction} {self.symbol_table.dict[node.id]},d', label)
                
                else:
                    self.__record_instruction(f'{instruction} {self.symbol_table.dict[node.id]},s', label)
        else:
            if isinstance(node, ast.Constant):
                self.__record_instruction(f'{instruction} {node.value},i', label)
            else:
                if self.symbol_table.dict[node.id] in self.global_var:

                    if self.__check_constant(node.id):
                        self.__record_instruction(f'{instruction} {self.symbol_table.dict[node.id]},i', label)

                    else: 
                        self.__record_instruction(f'{instruction} {self.symbol_table.dict[node.id]},d', label)

    def __identify(self):
        result = self.__elem_id
        self.__elem_id = self.__elem_id + 1
        return result

    def __remove_prev(self):
        self.__instructions.pop()

    # Passing parameters to functions, depending on the type of the parameter (stack or global)
    def __pass_parameters(self, args, in_func):
        stack = -4
        for arg in args:
            indicator = 'd'
            if type(arg) == ast.Constant:
                self.__record_instruction(f'LDWA {arg.value},s')
            elif in_func:
                indicator = 'd'
                if self.__is_func:
                    if self.symbol_table.dict[arg.id] in self.global_var:
                        indicator == 'd'
                    else:
                        indicator == 's'
                self.__record_instruction(f'LDWA {self.symbol_table.dict[arg.id]},{indicator}')
            else:
                if self.symbol_table.dict[arg.id] in self.global_var:
                    indicator == 'd'
                else:
                    indicator == 's'
                self.__record_instruction(f'LDWA {self.symbol_table.dict[arg.value]},{indicator}')
            self.__record_instruction(f'STWA {stack},s')
            stack -=2

    # Check if every char in string is uppercase
    def __check_constant(self, string):
        return all(char.isupper() for char in string[1:]) and string[0] == '_'



    #     stack_size = self.functions[func_name]
    #     # print(self.f_local_var, self.f_param) 
