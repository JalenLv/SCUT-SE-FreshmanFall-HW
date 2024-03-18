import ast
from symbol_table import SymbolTable

class FunctionVisitor(ast.NodeVisitor):
    """ 
        We extract all the left hand side of the global (top-level) assignments
    """
    
    def __init__(self) -> None:
        super().__init__()
        self.functions = dict()

    # Overriding the default visit method to not visit local variables
    def visit_FunctionDef(self, node):
        if node.name not in self.functions:
            self.functions[node.name] = node
