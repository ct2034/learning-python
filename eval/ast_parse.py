import ast
import random

def print_ast(node: ast.AST, indent: int = 0):
    print(" " * indent + "o"
        + f" [{type(node).__name__}]"
        + (f" ({node.id})" if "id" in dir(node) else "")
        + (f" ({node.value})" if "value" in dir(node) else "")
        + (f" ({node.op})" if "op" in dir(node) else "")
    )
    for child in ast.iter_child_nodes(node):
        print_ast(child, indent + 4)

if __name__ == '__main__':
    my_code = "x - y - 6"
    tree = ast.parse(my_code, mode='eval')
    
    print(f'{my_code=}')

    print_ast(tree)