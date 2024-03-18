import ast
from symbol_table import SymbolTable

class GlobalVariableExtraction(ast.NodeVisitor):
    """ 
        We extract all the left hand side of the global (top-level) assignments
    """
    
    def __init__(self, symbol_table) -> None:
        super().__init__()
        self.results = set()
        self.visited = {}
        self.symbol_table = symbol_table

    # Overriding the default visit method to not visit local variables
    def visit(self, node):
        if type(node) != ast.FunctionDef:
            super().visit(node)

    def visit_Assign(self, node):

        if len(node.targets) != 1:
            raise ValueError("Only unary assignments are supported")

        old_name = node.targets[0].id
        # Change each name to the symbol table equivalent
        if node.targets[0].id in self.symbol_table.dict:
            node.targets[0].id = self.symbol_table.dict[node.targets[0].id]
        else: 
            self.symbol_table.dict[node.targets[0].id] = self.symbol_table.symbol_generator.__next__()
            self.symbol_table.dict[self.symbol_table.dict[node.targets[0].id]] = self.symbol_table.dict[node.targets[0].id]
            node.targets[0].id = self.symbol_table.dict[node.targets[0].id]

        # Check if we have visited already, if we have, ignore
        if node.targets[0].id in self.visited:
            return
        else:
            # Add to result relevant information
            self.visited[node.targets[0].id] = True
            if type(node.value) == ast.Constant: 
                self.results.add((node.targets[0].id, node.value.value, old_name))
            else:
                self.results.add((node.targets[0].id, old_name))

