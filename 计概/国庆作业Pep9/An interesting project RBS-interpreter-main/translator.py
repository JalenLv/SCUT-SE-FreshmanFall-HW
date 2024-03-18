import argparse
import ast
from visitors.GlobalVariables import GlobalVariableExtraction
from visitors.TopLevelProgram import TopLevelProgram
from generators.StaticMemoryAllocation import StaticMemoryAllocation
from generators.EntryPoint import EntryPoint
from visitors.LocalVariables import LocalVariableExtraction
from generators.DynamicMemoryAllocation import DynamicMemoryAllocation
from symbol_table import SymbolTable
from visitors.FunctionVisitor import FunctionVisitor
from helper.FunctionInfo import FunctionInfo
from collections import defaultdict

def main():
    input_file, print_ast = process_cli()
    with open(input_file) as f:
        source = f.read()
    node = ast.parse(source)
    if print_ast:
        print(ast.dump(node, indent=2))
    else:
        process(input_file, node)
    
def process_cli():
    """"Process Command Line Interface options"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='filename to compile (.py)')
    parser.add_argument('--ast-only', default=False, action='store_true')
    args = vars(parser.parse_args())
    return args['f'], args['ast_only']

def process(input_file, root_node):

    # Create symbol table
    table = SymbolTable()
    print(f'; Translating {input_file}')

    # Visit and Parse Global Variables
    extractor = GlobalVariableExtraction(table)
    extractor.visit(root_node)
    global_vars = set()
    for var in extractor.results:
        global_vars.add(var[0])
        global_vars.add(var[-1])

    # Update symbol table with global variables
    table = extractor.symbol_table

    # Generate relavant code for global variables from extractor
    memory_alloc = StaticMemoryAllocation(extractor.results)
    to_remove = set()
    for n in extractor.results:
        if len(n) > 2:
            to_remove.add(n[0])
    
    # Visit and Parse Functions
    extractor = LocalVariableExtraction(table)
    extractor.visit(root_node)

    # Update Symbol Table
    table = extractor.symbol_table

    # Generate relavant code for local variables from extractor
    dynamic_memory_alloc = DynamicMemoryAllocation(extractor.parameters, extractor.local_variables, extractor.functions)    
    functions = FunctionVisitor()
    functions.visit(root_node)

    # Generate relevant information about each function for stack pointer management
    functions_dict = defaultdict(int)
    for fname in extractor.functions:
        functions_dict[fname] = 0
    
    # Increase stack size by 2 for each local variable and parameter in function_list that matches the function name
    for functioninfo in extractor.local_variables:
        functions_dict[functioninfo[3]] += 2
    for functioninfo in extractor.parameters:
        functions_dict[functioninfo[3]] += 2
    
    print('; Branching to top level (tl) instructions')
    print('\t\tBR tl')

    # Generating memory code
    memory_alloc.generate()
    dynamic_memory_alloc.generate()
    visited = set()
   
   # Generate code for all functions
    print('\n; Function instructions')
    for f in functions.functions:
        sub_level = TopLevelProgram(f, to_remove, table, functions_dict, visited, extractor.parameters, extractor.local_variables, global_vars)
        sub_level.visit(functions.functions[f])
        EntryPoint(sub_level.ret()).generate()
    
    # Generate main level code
    top_level = TopLevelProgram('tl', to_remove, extractor.symbol_table, functions_dict, visited, global_vars)
    top_level.visit(root_node)
    print('\n; Top Level instructions')
    ep = EntryPoint(top_level.finalize())
    ep.generate() 

if __name__ == '__main__':
    main()
