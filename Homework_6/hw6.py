# Homework 6
# Filename: hw6.py
# Author: Marshall Briggs

import sympy as sp
import re
import math
from sympy.logic.inference import satisfiable
from sympy.parsing.sympy_parser import parse_expr

class Stoich_Operand:
    def __init__(self, operand, contents, start):
        self.operand = operand
        self.operand_contents = contents
        self.operand_index = start

def all_satisfiable(s):
    """
    Function: all_satisfiable(s)
    INPUT: A string, representing an equation with n variables
    OUTPUT: False, if not satisfiable. A dictionary containing all satisfying
            assignments, if satisfiable.
    Definition: A function that works like sympy's satisfiable, but returns all 
                possible satisfying assignments.
    """
    num_vars = 0
    assignments = []
    values = dict()
    str_expr = sp.sympify(s)
    variables = re.findall(r"[a-zA-Z]", s)
    for i in variables:
        try:
            bl = values[i]
        except KeyError:
            values[i] = False
            num_vars += 1

    for i in range(2**num_vars):
        bi = "{0:b}".format(i).zfill(num_vars)
        for j in range(len(bi)):
            if bi[j] == '0':
                values[variables[j]] = False
            else:
                values[variables[j]] = True
        if str_expr.subs(values):
            assignments.append(values.copy())
    
    if len(assignments) == 0:
        return False
    else:
        return assignments

def normalcurve(a,b):
    """
    Function: normalcurve(a,b)
    INPUT: Two numbers, representing boundaries under a normal curve
    OUTPUT: Probability that a standard normal variable falls between the two   
            boundaries.
    Definition: A function that takes as input two boundaries a,b, and returns the
                probability that the a standard normal random variable falls in the 
                interval between a and b.
    """
    # mu = 0, var = 1
    x = sp.symbols('x')
    std_norm = (1/(math.sqrt(2*sp.pi)))*(sp.exp(-(x**2)/2))
    return sp.integrate(std_norm, (x, a, b)).evalf()

def ball(v0):
    """
    Function: ball([v0[x], v0[y]])
    INPUT: A list, representing the horizontal and vertical components of the starting
           velocity of a ball
    OUTPUT: A number, the point on the x-axis the ball lands on
    Definition: A ball is thrown with a starting velocity [v0[x],v0[y]], with a vertical 
                and horizontal component in a 2D space. The only force acting on it is 
                the force of gravity. A function that takes as input the starting velocity,
                and outputs the point on the x-axis that the ball lands on, after it is 
                thrown from the origin.
    """
    t = sp.symbols('t')
    yt = (0 + v0[1]*t - (1.0/2.0)*9.80665*t**2)
    fstimes = sp.solveset(sp.Eq(yt, 0), t)
    ltimes = list(fstimes)
    lindex = len(ltimes)
    xt = v0[0]*ltimes[lindex-1]
    return xt

def balance(eq):
    """
    Function: balance(eq)
    INPUT: A string, representing a chemical equation
    OUTPUT: A string, representing the balanced chemical equation
    Definition: A function that balances chemical equations. So, it turns strings of the 
                form 'H2+O2=H2O' into '2H2+O2=2H2O'.
    """
    linear_system = []
    OPERANDS = []
    middle = (re.search('=', eq)).start()
    operand_indices = []
    operands_in_eq = re.findall("[a-zA-Z0-9]+", eq)
    for i in operands_in_eq:
        operand_indices.append(re.search(i,eq).start())
    elements_in_eq = re.findall("[A-Z][a-z]*", eq)
    elements = dict()
    for i in range(len(elements_in_eq)):
        try:
            holder = elements[elements_in_eq[i]]
        except KeyError:
            elements[elements_in_eq[i]] = 0

    for i in range(len(operands_in_eq)):
        elements_in_operand = re.findall("[A-Z][a-z]*[0-9]*", operands_in_eq[i])
        operand_contents = dict()
        for j in elements_in_operand:
            count = re.findall("[0-9]+", j)
            try:
                numhold = operand_contents[j]
                operand_contents[j] = numhold + 1
            except KeyError:
                if count == []:
                    operand_contents[j] = 1
                else:
                    operand_contents[j[0:len(j)-1]] = int(count[0])
        OPERANDS.append(Stoich_Operand(operands_in_eq[i], operand_contents, operand_indices[i]))

    for i in elements:
        linear_equation = []
        for j in OPERANDS:
            try:
                numhold = j.operand_contents[i]
                if j.operand_index > middle:
                    numhold *= -1
                linear_equation.append(numhold)
            except KeyError:
                linear_equation.append(0)
        linear_equation.append(0)

        raw_eq_solve = ""
        n = len(linear_equation)
        x=[parse_expr('x%d'%i) for i in range(n)]
        for j in range(len(linear_equation)):
            raw_eq_solve = raw_eq_solve + str(linear_equation[j]) + "*" + str(x[j]) + "+"
        parse_eq_solve = parse_expr(raw_eq_solve[0:len(raw_eq_solve)-1])
        dict_eq_solve = sp.solve(parse_eq_solve, *x)
        normalize_x = dict()

        exp_equations = []
        exp_equations_args = []

        for j in x:
            normalize_x[j] = 1
        for j in x:
            try:
                value = str(dict_eq_solve[0][j])
                equat = str(j) + " - (" + value + ")"
                exp_equat = parse_expr(equat)
                exp_equations.append(exp_equat)
                b = len(exp_equat.args)
                for n in range(b):
                    exp_equations_args.append(exp_equat.args[n].args)
            except KeyError:
                continue

        linear_equation = []
        for j in x:
            var_present = re.findall(str(j), str(exp_equations[0]))
            if var_present == []:
                linear_equation.append(0)
            else:
                var_present_args = 0
                for p in exp_equations_args:
                    try:
                        if p[len(p)-1] == j:
                            var_present_args = 1
                            linear_equation.append(p[0])
                    except IndexError:
                        continue
                if var_present_args == 0:
                    linear_equation.append(1)
        linear_system.append(linear_equation)

    
    M = sp.Matrix(linear_system)
    n = len(linear_system[0])
    x=[parse_expr('x%d'%i) for i in range(n)]
    sols = sp.solve_linear_system(M, *x)

    coefficients = dict()
    for i in x:
        coefficients[i] = 1
    for key in sols:
        try:
            coefficients[key] = (sols[key]).args[0]
        except IndexError:
            coefficients[key] = 1

    L_Denoms = []
    for i in coefficients:
        L_Denoms.append(sp.fraction(sp.Rational(coefficients[i]))[1])
    multiplier = sp.lcm(L_Denoms)

    for i in coefficients:
        coefficients[i] = coefficients[i] * multiplier
    print coefficients

    balanced_Stoich = ""
    equals_placed = 0
    for i in range(len(x)-1):
        if coefficients[x[i]] == 1:
            balanced_Stoich += str(OPERANDS[i].operand)
        else: balanced_Stoich += str(coefficients[x[i]]) + str(OPERANDS[i].operand)
        if equals_placed == 0:
            if i < len(x) - 2:
                if OPERANDS[i+1].operand_index > middle:
                    balanced_Stoich += " = "
                    equals_placed = 1
                else:
                    balanced_Stoich += " + "
            else:
                balanced_Stoich += " + "
        else:
            balanced_Stoich += " + "

    return balanced_Stoich[0:len(balanced_Stoich)-3]

def main():
    # Test Cases for Challenge 1
    # expr1 = "(x|y)&x"
    # print all_satisfiable(expr1)
    # expr2 = "(x&y)|(~x)&z"
    # print all_satisfiable(expr2)

    # Test Cases for Challenge 2
    # a,b = .3, .5
    # print normalcurve(a,b)
    # c,d = -3, 3
    # print normalcurve(c,d)

    # Test Cases for Challenge 3
    # v0 = [44, 34]
    # print ball(v0)

    # Test Cases for Challenge 4
    eq1 = "H2 + O2 = H2O"
    print balance(eq1)
    eq2 = "PhCH3 + KMnO4 + H2SO4 = PhCOOH + K2SO4 + MnSO4 + H2O"
    print balance(eq2)

if __name__ == "__main__": main()