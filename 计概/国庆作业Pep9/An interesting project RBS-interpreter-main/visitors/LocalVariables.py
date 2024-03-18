import ast
from itertools import product
from string import ascii_uppercase
from symbol_table import SymbolTable

class LocalVariableExtraction(ast.NodeVisitor):
    
    def __init__(self, symboltable) -> None:
        super().__init__()
        self.parameters = set()
        self.local_variables = set()
        self.functions = set()
        self.visited = {}
        self.symbol_table = symboltable

    # Visitor only goes into function definition and parses relevant information
    def visit_FunctionDef(self, node):
        self.functions.add(node.name)
        params = len(node.args.args)
        stack_pointer = 0
        body = node.body
        # Goes through the body of the function instead of walkign through visitor to differentiate between local and glocal
        for statement in body:
            if type(statement) == ast.Assign: # Local variable spotted
                var_name = statement.targets[0].id

                # Check if variable is visited already
                if var_name not in self.visited:
                    # Get and append relevant information
                    old_name = var_name
                    self.visited[var_name] = True
                    self.symbol_table.dict[var_name] = self.symbol_table.symbol_generator.__next__()
                    self.symbol_table.dict[self.symbol_table.dict[var_name]] = self.symbol_table.dict[var_name]
                    self.local_variables.add((self.symbol_table.dict[var_name],old_name, stack_pointer, node.name))
                    stack_pointer += 2
            
            # Local variables are also hidden in If statements, need to find them too
            if type(statement) == ast.If or type(statement) == ast.While or type(statement) == ast.For or type(statement) == ast.With:
                for sub in statement.body:
                    if type(sub) == ast.Assign:
                        var_name = sub.targets[0].id
                        if var_name not in self.visited:
                            old_name = var_name
                            self.visited[var_name] = True
                            self.symbol_table.dict[var_name] = self.symbol_table.symbol_generator.__next__()
                            self.symbol_table.dict[self.symbol_table.dict[var_name]] = self.symbol_table.dict[var_name]
                            self.local_variables.add((self.symbol_table.dict[var_name],old_name, stack_pointer, node.name))
                            stack_pointer += 2
                
                
                for sub in statement.orelse:
                    if type(sub) == ast.Assign:
                        var_name = sub.targets[0].id
                        if var_name not in self.visited:
                            old_name = var_name
                            self.visited[var_name] = True
                            self.symbol_table.dict[var_name] = self.symbol_table.symbol_generator.__next__()
                            self.symbol_table.dict[self.symbol_table.dict[var_name]] = self.symbol_table.dict[var_name]
                            self.local_variables.add((self.symbol_table.dict[var_name],old_name, stack_pointer, node.name))
                            stack_pointer += 2
        
        # Get parameters and store information
        for param in range(params):
            old_name = node.args.args[param].arg
            self.symbol_table.dict[old_name] = self.symbol_table.symbol_generator.__next__()
            self.symbol_table.dict[self.symbol_table.dict[old_name]] = self.symbol_table.dict[old_name]
            self.parameters.add((self.symbol_table.dict[old_name], old_name, stack_pointer, node.name))
            stack_pointer += 2

    