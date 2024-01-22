'''This module is a simple calculator that performs basic arithmetic operations'''

import sys

def add(input_x, input_y):
    '''takes in two numbers and returns their sum'''
    return input_x + input_y

def subtract(input_x, input_y):
    '''takes in two numbers and returns their difference'''
    return input_x - input_y

def multiply(input_x, input_y):
    '''takes in two numbers and returns their product'''
    return input_x * input_y

def divide(input_x, input_y):
    '''takes in two numbers and returns their quotient'''
    return input_x / input_y

if __name__ == "__main__":
    #get user input
    operand_a = int(input("Enter first operand: "))
    operand_b = int(input("Enter second operand: "))
    operator = input("Enter operation: ")

    #perform operation
    if operator == "+":
        result = add(operand_a, operand_b)
    elif operator == "-":
        result = subtract(operand_a, operand_b)
    elif operator == "*":
        result = multiply(operand_a, operand_b)
    elif operator == "/":
        result = divide(operand_a, operand_b)
    else:
        print("Invalid operation")
        sys.exit()
    #print result
    print("Result: " + str(result))
