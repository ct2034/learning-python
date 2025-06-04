

from sympy import symbols, Eq, solve, Matrix, linsolve

vars = symbols('u u1 u2 u3 u4 u5 u6 alpha')
u, u1, u2, u3, u4, u5, u6, alpha = vars
eqs = [
    # voltage
    Eq(u1 + u2 + u5, u),
    Eq(u2 + u4, u3),
    Eq(u4 + u6, u5),
    Eq(u1 + u3 + u6, u),
    # current
    Eq(u2 + u3, u1),
    Eq(u4 + u5, u2),
    Eq((u3 + u4)/alpha, u6),
    Eq(u5 + u6 * alpha, u1),
]

sol = solve(eqs, vars)
print(sol)