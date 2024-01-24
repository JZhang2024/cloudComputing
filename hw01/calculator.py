'''This module is a simple calculator that performs basic arithmetic operations'''

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

def operation(input_x, input_y, operator):
    '''takes in two numbers and an operator and returns the result of the operation'''
    if operator == "+":
        result = add(input_x, input_y)
    elif operator == "-":
        result = subtract(input_x, input_y)
    elif operator == "*":
        result = multiply(input_x, input_y)
    elif operator == "/":
        result = divide(input_x, input_y)
    else:
        raise ValueError("Invalid operator")
    return result


def main():
    '''main function that takes in user input and calls operation function'''
    #get user input
    operand_a = int(input("Enter first operand: "))
    operand_b = int(input("Enter second operand: "))
    operator = input("Enter operation: ")

    #calculate result
    result = operation(operand_a, operand_b, operator)
    print(f'Result: {result}')

if __name__ == "__main__":
    main()
