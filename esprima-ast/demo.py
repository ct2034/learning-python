import ast
import esprima
from pprint import pprint
import difflib

def _esprima_ast_to_python_ast(js):
    # print(">")
    # print(js)
    if js.type == "ExpressionStatement":
        return _esprima_ast_to_python_ast(js.expression)
    elif js.type == "AssignmentExpression":
        assert js.operator == "="
        return ast.Assign(
            [_esprima_ast_to_python_ast(js.left)],
            _esprima_ast_to_python_ast(js.right),
            lineno=99
        )
    elif js.type == "Identifier":
        return ast.Name(js.name, ctx=ast.Store())
    elif js.type == "Literal":
        return ast.Constant(js.value)
    else: 
        raise NotImplementedError(js.type)

def esprima_ast_to_python_ast(js):
    js_body = js.body
    body = []
    for expression in js_body:
        body.append(_esprima_ast_to_python_ast(expression))
    return ast.Module(body, type_ignores=[])

if __name__ == "__main__":
    js_expr = "a = 42"
    ast_expr = esprima.parse(js_expr)
    pprint(ast_expr)

    py_expr_goal = ast.parse(js_expr)
    py_str_goal = ast.dump(py_expr_goal, indent=2)
    print(py_str_goal)

    py_expr = esprima_ast_to_python_ast(ast_expr)
    py_str = ast.dump(py_expr, indent=2)
    print(py_str)

    result = ast.unparse(py_expr)
    pprint(result)
