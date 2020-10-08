import random
from termcolor import colored
import general_move
import general2
import areanew_proj
import mathead_code_proj
import check_close
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sqr_code_proj
from scipy import ndimage
import numpy as np
from PIL import Image

"""
                ---------------------------------------------------------------------------
                                    MATHEMATICAL RIDDLES GUI FUNCTIONS
                ---------------------------------------------------------------------------
"""

# Constant for printing the digits and operators. Each digit / operator is splitted by the 'enter' characters.
digits_dict = {'minus': '        \n' + ' __     \n' + '        ',
               'plus': '         \n' + '__|__    \n' + '  |      ',
               '=': ' __     \n' + ' __     \n' + '        ',
               0: ' __     \n' + '|  |    \n' + '|__|    ',
               1: '     \n|    \n' + '|    ',
               2: ' __     \n' + ' __|    \n' + '|__     ',
               3: ' __     \n' + ' __|    \n' + ' __|    ',
               4: '        \n' + '|__|    \n' + '   |    ',
               5: ' __     \n' + '|__     \n' + ' __|    ',
               6: ' __     \n' + '|__     \n' + '|__|    ',
               7: ' __     \n' + '   |    \n' + '   |    ',
               8: ' __     \n' + '|__|    \n' + '|__|    ',
               9: ' __     \n' + '|__|    \n' + ' __|    '}


def operand_input(num_digits, i):
    """
    This function gets the number of digits per operand - num_digits and an operand index - i (must be 1, 2 or 3).
    It receives an operand input from the user.
    It checks that the input is a natural number (including 0) and includes maximum (num_digits) digits.
    If yes - it returns the operand
    Else - it continues receiving input.
    """
    while True:
        dig1 = raw_input("""Enter number """ + str(i) + """: """)
        if dig1.isdigit():
            if 0 <= int(dig1) < 10 ** int(num_digits):
                return dig1
            else:
                print """

---Error---

You entered an invalid integer! Reminder: you entered the number of digits per operand to be: """ + str(
                    num_digits) + """
Choose a number which has """ + str(num_digits) + """ digits or less.
    """
        else:
            print """
---Error---

You entered an invalid string. Your input must be an integer!
                             """


def operator_input():
    """
    This function receives a string as an input for the riddle's operator. The operator must be 'minus' or 'plus'.
    It checks that the input string equals 'minus' or 'plus'.
    If yes - it returns the operator.
    Else - it continues receiving input.
    """
    while True:
        op = raw_input("""Enter 'plus' or 'minus': """)
        if op == 'minus' or op == 'plus':
            return op
        else:
            print """
---Error---

You entered an invalid string. Your input must be 'minus' or 'plus'!
                                         """


def equation_input(num_digits, man_rnd_con):
    """
    This function gets the number of digits per operand - num_digits.

    There are 2 options:
        Manual input - the function receives an operand input from the user.
        Random input - the function randomly chooses legal operands, according to the number of digits per operand.

    It receives a string as an input for the riddle's operator. The operator must be 'minus' or 'plus'.

    It checks that the operands are natural numbers (including 0) and each operand includes maximum (num_digits) digits.
    It checks that the operator string equals 'plus' or 'minus'.

    If the inputs are valid - it returns the equation for the riddle.
    Else - it continues receiving inputs.
    """
    dig1 = 0
    dig2 = 0
    result = 0


    if man_rnd_con == 'C':
        dig1, dig2, result = (-1, -1, -1)

    if man_rnd_con == 'M':
        # first operand input
        dig1 = operand_input(num_digits, 1)

        # second operand input
        dig2 = operand_input(num_digits, 2)

        # result input
        result = operand_input(num_digits, 3)
    elif man_rnd_con == 'R':
        dig1 = random.randint(0, 10 ** int(num_digits) - 1)
        dig2 = random.randint(0, 10 ** int(num_digits) - 1)
        result = random.randint(0, 10 ** int(num_digits) - 1)

    plus_or_minus = operator_input()

    return dig1, dig2, result, plus_or_minus


def equation_print(dig1, dig2, result, plus_or_minus, num_digits, num_allowed, operation):
    """
    This function prints a riddle's equation. (The equation may be an input or an output - solution: satisfied equation)

    Input options:
        If the riddle is a normal one (the number of matchsticks to add/remove/move is given and different than -1):
        the equation will be printed with the number of matchsticks and the operation (add/remove/move)

        If the riddle is an optimization problem (the number of matchsticks to add/remove/move equals -1):
        only the equation will be printed

    Output options:
        If the riddle is a normal one: the satisfied equation will be printed with the constant number of matchsticks
        and the operation (add/remove/move)

        If the riddle is an optimization problem: the satisfied equation will be printed with the minimal number of
        matchsticks and the operation (add/remove/move)

    """
    st11, st12, st13 = print_number(num_digits, dig1).split('\n')
    st21, st22, st23 = print_number(num_digits, dig2).split('\n')
    st31, st32, st33 = print_number(num_digits, result).split('\n')
    op1, op2, op3 = digits_dict[plus_or_minus].split('\n')
    eq1, eq2, eq3 = digits_dict['='].split('\n')
    print colored(st11 + op1 + st21 + eq1 + st31, 'yellow')
    print colored(st12 + op2 + st22 + eq2 + st32, 'yellow')
    print colored(st13 + op3 + st23 + eq3 + st33, 'yellow')
    if num_allowed != -1:  # not an input for an optimization problem
        print colored("""
                                   NUMBER OF MATCHSTICKS TO """ + operation + """: """ + str(num_allowed), 'yellow')


def print_number(num_digits, num):
    """
    This function gets num_digits - the number of digits per operand, and num - an operand.
    It creates a string for printing the operand by the 7-segment format and returns it.
    """
    st_1st_part = ''
    st_2nd_part = ''
    st_3rd_part = ''
    for i in range(int(num_digits) - 1, -1, -1):
        dig = (int(num) / (10 ** i)) % 10
        s11, s12, s13 = digits_dict[dig].split('\n')
        st_1st_part += s11
        st_2nd_part += s12
        st_3rd_part += s13
    return st_1st_part + '\n' + st_2nd_part + '\n' + st_3rd_part


def add():
    """
    Number of digits per operand - user input - 'add matchsticks' riddles (must be 1, 2 or 3)
    """
    while True:
        num_digits = raw_input("""
Now you need to choose the number of digits per operand.
It must be 1, 2 or 3.
Enter it here: """)
        if num_digits.isdigit():
            if 0 < int(num_digits) < 4:
                print 'ok'
                return num_digits
            else:
                print """

---Error---

You entered an invalid integer!
                 """
        else:
            print """
---Error---

You entered an invalid string. Your input must be an integer!
             """


def remove():
    """
    Number of digits per operand - user input - 'remove matchsticks' riddles (must be 1, 2 or 3)
    """
    while True:
        num_digits = raw_input("""
Now you need to choose the number of digits per operand.
It must be 1, 2 or 3.
Enter it here: """)
        if num_digits.isdigit():
            if 0 < int(num_digits) < 4:
                print 'ok'
                return num_digits
            else:
                print """

---Error---

You entered an invalid integer!
                     """
        else:
            print """
---Error---

You entered an invalid string. Your input must be an integer!
                 """


def move():
    """
    Number of digits per operand - user input - 'move matchsticks' riddles (must be 1, 2)
    """
    while True:
        num_digits = raw_input("""
Now you need to choose the number of digits per operand.
It must be 1 or 2.
Enter it here: """)
        if num_digits.isdigit():
            if 0 < int(num_digits) < 3:
                print 'ok'
                return num_digits
            else:
                print """

---Error---

You entered an invalid integer!
                     """
        else:
            print """
---Error---

You entered an invalid string. Your input must be an integer!
                 """


def num_allowed_input(num_digits, operation):
    """
    This function gets num_digits - the number of digits per operand, and operation - add, move or remove.
    It receives input from the user - the number of matchsticks required for solving the riddle.
    (This function is used only in the normal riddles, not in the optimization riddles)
    """
    while True:
        num_allowed = raw_input("""Now you need to enter the number of matchsticks to """ + operation + """.
It must be an integer between 0 - """ + str(15 * int(num_digits)) + """. Enter it here: """)
        if num_allowed.isdigit():
            if 0 <= int(num_allowed) <= 15 * int(num_digits):
                print 'ok'
                return num_allowed
            else:
                print """

---Error---

You entered an invalid integer!
                """
        else:
            print """
---Error---

You entered an invalid string. Your input must be an integer!
                """


def math_general_input(num_digits, operation, man_rnd_con):
    """
    This function gets num_digits - the number of digits per operand, and operation - add, move or remove.
    It receives input from the user - the riddle's equation and the number of matchsticks required for solving the riddle.
    It prints the input by 7-segment format.
    This function is used only for the normal riddles, not the optimization riddles
    """
    dig1, dig2, result, plus_or_minus = equation_input(num_digits, man_rnd_con)
    num_allowed = num_allowed_input(num_digits, operation)
    print """

    ---------------------------------------------------------------------------------------------------------
                                                 YOUR INPUT IS:
                """
    equation_print(dig1, dig2, result, plus_or_minus, num_digits, num_allowed, operation)
    print """---------------------------------------------------------------------------------------------------------"""
    return dig1, dig2, result, plus_or_minus, num_allowed


def math_optimal_input(num_digits, operation, man_rnd_con):
    """
        This function gets num_digits - the number of digits per operand, and operation - add, move or remove.
        It receives input from the user - the riddle's equation.
        It prints the input by 7-segment format.
        This function is used only for the optimization riddles, not the normal riddles
    """
    dig1, dig2, result, plus_or_minus = equation_input(num_digits, man_rnd_con)
    print """

    ---------------------------------------------------------------------------------------------------------
                                                 YOUR INPUT IS:
                """
    equation_print(dig1, dig2, result, plus_or_minus, num_digits, -1, operation)
    print """---------------------------------------------------------------------------------------------------------"""
    return dig1, dig2, result, plus_or_minus


def math_general_output(dig1, dig2, result, plus_or_minus, num_digits, num_allowed, operation):
    """
    This function gets num_digits - the number of digits per operand
                       operation - add, move or remove
                       the output equation
    It prints the output equation on the screen with the constant number of matchsticks and the operation
    (add/remove/move).
    This function is used only for the normal riddles, not the optimization riddles
    """
    print """

    ---------------------------------------------------------------------------------------------------------
                                                 YOUR OUTPUT IS:
                """
    equation_print(dig1, dig2, result, plus_or_minus, num_digits, num_allowed, operation)
    print """---------------------------------------------------------------------------------------------------------"""


def optimal_output(dig1, dig2, result, plus_or_minus, num_digits, operation, num_allowed):
    """
    This function gets num_digits - the number of digits per operand
                       operation - add, move or remove
                       the output equation
    It prints the output equation on the screen with the minimal number of matchsticks and the operation
    (add/remove/move).
    This function is used only for the optimization riddles, not the normal riddles
    """
    print """

    ---------------------------------------------------------------------------------------------------------
                                                 YOUR OUTPUT IS:
                """
    equation_print(dig1, dig2, result, plus_or_minus, num_digits, num_allowed, operation)

    print """---------------------------------------------------------------------------------------------------------"""


def math_general_in_out(j, num_digits, operation, man_rnd_con):
    """
    This function gets:
    :param j: Index of the input / output file
    :param num_digits: Number of digits per operand
    :param operation: add/remove/move matchsticks

    It receives input from the user (normal riddle):
    The operands, the operator (plus/minus), the number of matchsticks to add/remove/move

    It prints the input on the screen
    It solves the normal mathematical riddle and prints the solution

    """
    dig1, dig2, result, plus_or_minus, num_allowed = math_general_input(num_digits, operation, man_rnd_con)
    if operation == 'ADD' or operation == 'REMOVE':
        times, flag_solved, run_time = general2.solve_equation_input(j, int(dig1), int(dig2), int(result),
                                                                     plus_or_minus, int(num_allowed), operation.lower(),
                                                                     int(num_digits))
    else:
        times, flag_solved, run_time = general_move.solve_equation_input(j, int(dig1), int(dig2), int(result),
                                                                         plus_or_minus, int(num_allowed),
                                                                         int(num_digits))
    if flag_solved == 1:
        print colored("""                                NO SOLUTION                               """, 'red')

    elif flag_solved == 2:
        if operation == 'ADD' or operation == 'REMOVE':
            dig1, dig2, result = general2.find_info(j)
        else:
            dig1, dig2, result = general_move.find_info(j)
        math_general_output(dig1, dig2, result, plus_or_minus, num_digits, num_allowed, operation)
    else:
        print colored("""                                NO SOLUTION                               """, 'red')


def math_optimal_in_out(j, num_digits, operation, man_rnd_con):
    """
    This function gets:
    :param j: Index of the input / output file
    :param num_digits: Number of digits per operand
    :param operation: add/remove/move matchsticks

    It receives input from the user (optimization riddle):
    The operands and the operator (plus/minus)

    It prints the input on the screen

    It solves the mathematical optimization riddle and prints the solution with the minimal number of operations
     (add/remove/move) on the screen

    """
    dig1, dig2, result, plus_or_minus = math_optimal_input(int(num_digits), operation, man_rnd_con)
    if operation == 'ADD' or operation == 'REMOVE':
        times, flag_solved, run_time, dig1, dig2, result, num_allowed = general2.solve_equation_opt_input(j, int(dig1),
                                                                                                          int(dig2),
                                                                                                          int(result),
                                                                                                          plus_or_minus,
                                                                                                          operation.lower(),
                                                                                                          int(
                                                                                                              num_digits))
    else:
        times, flag_solved, run_time, dig1, dig2, result, num_allowed = general_move.solve_equation_opt_input(j,
                                                                                                              int(dig1),
                                                                                                              int(dig2),
                                                                                                              int(
                                                                                                                  result),
                                                                                                              plus_or_minus,
                                                                                                              int(
                                                                                                                  num_digits))
    if flag_solved == 1:
        print colored("""                                NO SOLUTION                               """, 'red')

    elif flag_solved == 0 and plus_or_minus == 'plus' and dig1 + dig2 != result:
        print colored("""                                NO SOLUTION                               """, 'red')

    elif flag_solved == 0 and plus_or_minus == 'minus' and dig1 - dig2 != result:
        print colored("""                                NO SOLUTION                               """, 'red')

    else:
        optimal_output(dig1, dig2, result, plus_or_minus, num_digits, operation, num_allowed)


def math_normal_generate_in_out(j, num_digits, operation):
    plus_or_minus = operator_input()
    times, flag_solved, run_time, dig1, dig2, result, dig1_or, dig2_or, dig3_or, num_allowed = (0, 0, 0, 0, 0, 0, 0, 0,
                                                                                                0, 0)

    if operation == 'ADD' or operation == 'REMOVE':
        times, flag_solved, run_time, dig1, dig2, result, dig1_or, dig2_or, dig3_or, num_allowed = \
            general2.solve_equation_gen(j, plus_or_minus, operation.lower(),
                                        int(num_digits))
    else:
        times, flag_solved, run_time, dig1, dig2, result, dig1_or, dig2_or, dig3_or, num_allowed = \
            general_move.solve_equation_gen(j, plus_or_minus, int(num_digits))

    if flag_solved == 1:
        print colored("""                                NO SOLUTION                               """, 'red')

    elif flag_solved == 2:
        print """

            ---------------------------------------------------------------------------------------------------------
                                                         YOUR INPUT IS:
                        """
        equation_print(dig1_or, dig2_or, dig3_or, plus_or_minus, num_digits, num_allowed, operation)
        print """---------------------------------------------------------------------------------------------------------"""

        math_general_output(dig1, dig2, result, plus_or_minus, num_digits, num_allowed, operation)
    else:
        print colored("""                                NO SOLUTION                               """, 'red')


def math_optimal_generate_in_out(j, num_digits, operation):
    plus_or_minus = operator_input()

    if operation == 'ADD' or operation == 'REMOVE':

        times, flag_solved, run_time, dig1, dig2, result, dig1_or, dig2_or, dig3_or, num_allowed = \
            general2.solve_equation_gen(j, plus_or_minus, operation.lower(),
                                        int(num_digits))
        print """

                    ---------------------------------------------------------------------------------------------------------
                                                                 YOUR INPUT IS:
                                """
        equation_print(dig1_or, dig2_or, dig3_or, plus_or_minus, num_digits, -1, operation)
        print """---------------------------------------------------------------------------------------------------------"""

        times, flag_solved, run_time, dig1, dig2, result, current_min = general2.solve_equation_opt_input(j, dig1_or, dig2_or, dig3_or, plus_or_minus, operation.lower(), int(num_digits))

    else:
        times, flag_solved, run_time, dig1, dig2, result, dig1_or, dig2_or, dig3_or, num_allowed = \
            general_move.solve_equation_gen(j, plus_or_minus, int(num_digits))
        print """

                     ---------------------------------------------------------------------------------------------------------
                                                                  YOUR INPUT IS:
                                 """
        equation_print(dig1_or, dig2_or, dig3_or, plus_or_minus, num_digits, -1, operation)
        print """---------------------------------------------------------------------------------------------------------"""

        times, flag_solved, run_time, dig1, dig2, result, current_min = general_move.solve_equation_opt_input(j, dig1_or,
                                                                                                          dig2_or,
                                                                                                          dig3_or,
                                                                                                          plus_or_minus,
                                                                                                          int(num_digits))

    if flag_solved == 1:
        print colored("""                                NO SOLUTION                               """, 'red')

    elif flag_solved == 2:

        math_general_output(dig1, dig2, result, plus_or_minus, num_digits, current_min, operation)


def math_generate_in_out(j, num_digits, operation, normal_or_optimal):
    if normal_or_optimal == 'N':
        math_normal_generate_in_out(j, num_digits, operation)
    elif normal_or_optimal == 'O':
        math_optimal_generate_in_out(j, num_digits, operation)


def math_solve(operation, j, normal_or_optimal, man_rnd_con):
    """
    This function gets:
    :param operation: add/remove/move matchsticks
    :param j: The index of the input/output files
    :param normal_or_optimal: 'O' - optimization riddle, 'N' - normal math riddle
    :param generate: True - algorithmically generate input for the riddle, False - manual / random input

    It receives user input - number of digits pe operand

    It solves the math riddle (normal / optimization), the input and output (solution) are printed on the screen
    """
    num_digits = 0

    if operation == 'ADD':
        num_digits = add()
    elif operation == 'REMOVE':
        num_digits = remove()
    elif operation == 'MOVE':
        num_digits = move()

    if man_rnd_con == 'M' or man_rnd_con == 'R':
        if normal_or_optimal == 'N':
            math_general_in_out(j, num_digits, operation, man_rnd_con)
        else:  # normal_or_optimal == 'O'
            math_optimal_in_out(j, num_digits, operation, man_rnd_con)
    else:
        math_generate_in_out(j, num_digits, operation, normal_or_optimal)


def menu_math(j):
    """
    User menu for solving mathematical equations riddles - infinite loop (until the user enters EXIT as an operation)

    It gets j - the initial input/output file's index

    It receives input from the user - the operation(add/remove/move), the riddle type (normal/optimization) and the
    riddle's parameters

    It prints the input riddle on the screen
    It solves the riddle (considering its type) and prints the solution

    It returns the last input/output file's index
    """
    print """Welcome to our matchstick riddles solver!
You can solve: mathematical equations"""
    while True:
        j += 1
        operation = raw_input("""
Now you need to choose your input.
The operations are:
Add matchsticks - enter 'ADD' 
Remove matchsticks - enter 'REMOVE'
Move matchsticks - enter 'MOVE'
Exit - enter 'EXIT' 
Enter your decision here: """)
        if operation == 'ADD' or operation == 'REMOVE' or operation == 'MOVE':
            normal_or_optimal = normal_or_optimal_input()
            man_rnd_con = man_rnd_con_input()
            math_solve(operation, j, normal_or_optimal, man_rnd_con)

        elif operation == 'EXIT':
            print 'Bye'
            return j
        else:
            print 'Error! Invalid operation.'


def normal_or_optimal_input():
    """
    This function receives input from the user:
    'O' - solving an optimization riddle
    'N' - solving a normal riddle
    It returns the user's input
    """
    while True:
        normal_or_optimal = raw_input("""ENTER 'N' IF YOU WANT TO SOLVE A NORMAL RIDDLE.
ENTER 'O' IF YOU WANT TO ENTER LESS INPUT PARAMETERS - THE SOLVER WILL RETURN AN OPTIMAL OUTPUT. """)
        if normal_or_optimal == 'N' or normal_or_optimal == 'O':
            return normal_or_optimal


"""
-----------------------------------------------------------------------------------------------------------
                            SUM OF MATCHSTICK HEADS RIDDLES GUI FUNCTIONS
-----------------------------------------------------------------------------------------------------------
"""


def print_match_cons_sum(arr_rows, arr_cols, title):
    """
    This function gets:
    :param arr_rows: an array of 24 integers, each integer represents a matchstick direction:
    1 - the matchstick points to row 1
    2 - the matchstick points to row 2,
    3 - the matchstick points to row 3,
    4 - the matchstick points to row 4

    :param arr_cols: an array of 24 integers, each integer represents a matchstick direction:
    1 - the matchstick points to col 1
    2 - the matchstick points to col 2,
    3 - the matchstick points to col 3,
    4 - the matchstick points to col 4

    :param title: the configuration's title: input / solution
    It prints the matchsticks configuration
    """
    font = {'family': 'serif',
            'color': 'darkred',
            'weight': 'bold',
            'size': 26,
            }

    rows = 4
    cols = 7
    fig = plt.figure(figsize=(6, 6))
    plt.title(title, fontdict=font)
    plt.axis('off')
    for i in range(1, rows * cols + 1):
        if i <= 21 or i == 23 or i == 25 or i == 27:
            if (i % 7) % 2 == 0 and i % 7 != 0:
                img = mpimg.imread('./match2.jpg')
            else:
                img = mpimg.imread('./match5.jpg')
        else:
            img = mpimg.imread('./white.jpg')
        fig.add_subplot(rows, cols, i)
        plt.axis('off')
        if i % 7 == 2:
            if arr_cols[i - 2] != 1:
                img = np.fliplr(img)

        elif i % 7 == 4:
            if arr_cols[i - 3] != 2:
                img = np.fliplr(img)

        elif i % 7 == 6:
            if arr_cols[i - 4] != 3:
                img = np.fliplr(img)

        elif i != 22 and i % 7 == 1:
            if arr_rows[i + 2] == i / 7 + 2:
                img = ndimage.rotate(img, 180)
        elif i != 24 and i % 7 == 3:
            if arr_rows[i + 1] == i / 7 + 2:
                img = ndimage.rotate(img, 180)
        elif i != 26 and i % 7 == 5:
            if arr_rows[i] == i / 7 + 2:
                img = ndimage.rotate(img, 180)
        elif i != 28 and i % 7 == 0:
            if arr_rows[i - 1] == i / 7 + 1:
                img = ndimage.rotate(img, 180)
        plt.imshow(img)
    plt.subplots_adjust(left=0.1,
                        bottom=0.14,
                        right=0.9,
                        top=0.79,
                        wspace=0,
                        hspace=0.05)
    plt.show()


def matchsticks_input():
    """
    This function receives input from the user - matchsticks' directions: up('U')/down('D')/left('L')/right('R')
    :return: Integer arrays, representing the row/column/diagonal that each matchstick points to.
    (Each index represents a matchstick, and each array value represents a row/column/diagonal)
    """
    arr_dir = []
    for i in range(0, 24):

        if 3 <= i <= 6 or 10 <= i <= 13 or 17 <= i <= 20:

            while True:
                direction = raw_input("INDEX " + str(i) + " - ENTER UP - 'U' OR DOWN - 'D': ")
                if direction == 'U' or direction == 'D':
                    arr_dir.append(direction)
                    break

        else:

            while True:
                direction = raw_input("INDEX " + str(i) + " - ENTER RIGHT - 'R' OR LEFT - 'L': ")
                if direction == 'R' or direction == 'L':
                    arr_dir.append(direction)
                    break

    match_rows, match_cols, match_dis = create_arrays_from_input(arr_dir)
    return match_rows, match_cols, match_dis


def create_arrays_from_input(dir_arr):
    """
    This function gets:
    :param dir_arr: an array of 24 strings: matchsticks' directions: up('U')/down('D')/left('L')/right('R')
    :return: 3 arrays of 24 integers:
    Each index represents a matchstick
    The values represent rows, columns and diagonals: matchsticks' directions:
    row - must be 1 - 4
    col - must be 1 - 4
    di - must be 1 or 2 (0 - not pointing to any diagonal)
    """
    match_rows = []
    match_cols = []
    match_dis = []
    row = 0
    col = 0
    di = 0
    for i in range(0, 24):
        if 0 <= i <= 2:
            row = 1
        if 3 <= i <= 6:
            if dir_arr[i] == 'U':
                row = 1
            elif dir_arr[i] == 'D':
                row = 2
        if 7 <= i <= 9:
            row = 2
        if 10 <= i <= 13:
            if dir_arr[i] == 'U':
                row = 2
            elif dir_arr[i] == 'D':
                row = 3
        if 14 <= i <= 16:
            row = 3
        if 17 <= i <= 20:
            if dir_arr[i] == 'U':
                row = 3
            elif dir_arr[i] == 'D':
                row = 4
        if 21 <= i <= 23:
            row = 4
        match_rows.append(row)
        if i % 7 == 3:
            col = 1
        if i % 7 == 4:
            col = 2
        if i % 7 == 5:
            col = 3
        if i % 7 == 6:
            col = 4
        if i % 7 == 0:
            if dir_arr[i] == 'L':
                col = 1
            elif dir_arr[i] == 'R':
                col = 2
        if i % 7 == 1:
            if dir_arr[i] == 'L':
                col = 2
            elif dir_arr[i] == 'R':
                col = 3
        if i % 7 == 2:
            if dir_arr[i] == 'L':
                col = 3
            elif dir_arr[i] == 'R':
                col = 4
        match_cols.append(col)
        if i == 1 or i == 10 or i == 13 or i == 22:
            di = 0

        if i == 8:
            if dir_arr[i] == 'R':
                di = 2
            if dir_arr[i] == 'L':
                di = 1

        if i == 15:
            if dir_arr[i] == 'R':
                di = 1
            if dir_arr[i] == 'L':
                di = 2

        if i == 11:
            if dir_arr[i] == 'U':
                di = 1
            if dir_arr[i] == 'D':
                di = 2

        if i == 12:
            if dir_arr[i] == 'U':
                di = 2
            if dir_arr[i] == 'D':
                di = 1

        if i in [0, 3, 4, 7, 16, 19, 20, 23]:
            if match_cols[i] == match_rows[i]:
                di = 1
            else:
                di = 0
        if i in [2, 5, 6, 9, 14, 17, 18, 21]:
            if match_cols[i] == 5 - match_rows[i]:
                di = 2
            else:
                di = 0
        match_dis.append(di)
    return match_rows, match_cols, match_dis


def print_structure():
    """
    This function prints the basic structure of the input, not including matchsticks' directions
    """
    im = Image.open('./sum_con.jpg')
    a = np.asarray(im)
    im = Image.fromarray(a)
    im.show()
    print """              _____________________________________________________________________________________________
             |                                                                                             |
             |              THE BASIC STRUCTURE: 24 MATCHSTICKS, INDEXED 0 - 23.                           |
             |                                                                                             |
             |              FOR EACH MATCHSTICK, YOU NEED TO CHOOSE AN INITIAL DIRECTION:                  |
             |                                                                                             |
             |              FOR INDICES: 0 - 2, 7 - 9, 14 - 16, 21 - 23: CHOOSE RIGHT - 'R' OR LEFT - 'L'  |
             |              FOR INDICES: 3 - 6, 10 - 13, 17 - 20: CHOOSE 'U' - UP OR 'D' - DOWN            |
             |                                                                                             |
              _____________________________________________________________________________________________
    """


def sum_in_out(j):
    match_rows, match_cols, match_dis = matchsticks_input()
    print_match_cons_sum(match_rows, match_cols, 'THE INPUT\n')
    times, flag_solved, run_time = mathead_code_proj.solve_rid_input(j, match_rows, match_cols, match_dis)
    if flag_solved == 1:
        print colored("""                                NO SOLUTION                               """, 'red')

    elif flag_solved == 2:
        arr_rows, arr_cols, arr_dis = mathead_code_proj.find_info(j)
        print_match_cons_sum(arr_rows, arr_cols, 'THE SOLUTION\n')

    else:
        print colored("""                                NO SOLUTION                               """, 'red')


def sum_generated_in_out(j):
    times, flag_solved, run_time, arr_rows, arr_cols, arr_dis, old_rows, old_cols, old_dis = \
        mathead_code_proj.solve_rid_input_gen(j)

    if flag_solved == 1:
        print colored("""                                NO SOLUTION                               """, 'red')

    elif flag_solved == 2:
        print """
YOU NEED TO MOVE THE MATCHSTICKS TO GET 6 MATCHSTICK HEADS IN EACH ROW, COLUMN AND DIAGONAL. 
THE INITIAL CONSTRUCTION APPEARS ON THE SCREEN NOW."""
        print_match_cons_sum(old_rows, old_cols, "THE INPUT")

        print_match_cons_sum(arr_rows, arr_cols, "THE OUTPUT")
    else:
        print colored("""                                NO SOLUTION                               """, 'red')


def solve_sum(j, gen='N'):
    if gen == 'N':
        sum_in_out(j)
    elif gen == 'Y':
        sum_generated_in_out(j)


def menu_sum(j):
    """
    User menu for solving sum of matchstick heads riddles - infinite loop
    (until the user enters N - does not want to continue solving these riddles)

    It gets j - the initial input/output file's index

    It receives input from the user - the matchsticks' directions

    It prints the input riddle on the screen
    It solves the riddle and prints the solution

    It returns the last input/output file's index
    """
    print """
    
    WELCOME TO OUR RIDDLES SOLVER!
    
    HERE YOU CAN SOLVE SUM OF MATCHSTICK HEADS RIDDLES.
    
    A SOLUTION IS: A MATCHSTICK CONFIGURATION WHICH HAS 6 MATCHSTICK HEADS IN EVERY ROW, COLUMN AND DIAGONAL.
    
    A MATCHSTICKS CONSTRUCTION WILL BE SOON PRINTED ON THE SCREEN. 
    YOU NEED TO CHOOSE A DIRECTION FOR EACH MATCHSTICK HEAD FOR THE INITIAL INPUT: UP/DOWN/LEFT/RIGHT.
    THIS PROGRAM CHANGES SOME MATCHSTICK DIRECTIONS IN ORDER TO FIND A CORRECT SOLUTION. 
    FOR EACH INPUT, A CORRECT OUTPUT - SOLUTION - WILL BE PRINTED.
    
    
    """
    print_structure()
    while True:
        cont = cont_run_rid()  # continue solving this type of riddles - 'Y' or 'N'
        if cont == 'N':
            return j
        j += 1
        gen = gen_input()
        solve_sum(j, gen)

"""
-----------------------------------------------------------------------------------------------------------
                            SQUARE RIDDLES GUI FUNCTIONS
-----------------------------------------------------------------------------------------------------------
"""


def sq1_input():
    """
    This function receives input - the 1-match-length squares that the user wants to appear on the screen
    The squares are indexed: 0-8
    A picture of the squares indexing in the matchsticks construction is printed on the screen.
    For each index: the user enters 'T' - the square appears
                                    'F' - the square does not appear
    :return: arr_dir - an array of strings ('T' / 'F') which represents the 1-match-length squares that
     will appear on the screen as input.
    """
    im = Image.open('./1-sqr.jpg')
    a = np.asarray(im)
    im = Image.fromarray(a)
    im.show()
    print """
    NOW, YOU NEED TO DECIDE WHICH 1-MATCH-LENGTH SQUARES YOU WANT TO APPEAR ON YOUR SCREEN.
    THE 1-MATCH-LENGTH SQUARES INDEXING APPEARS ON YOUR SCREEN. 
    FOR EACH INDEX: ENTER 'T' - IF YOU WANT THE SQUARE TO APPEAR, 'F' - OTHERWISE
    """
    arr_dir = []
    for i in range(0, 9):
        while True:
            direction = raw_input("INDEX " + str(i) + " - ENTER APPEARS - 'T' OR DOESN'T APPEAR - 'F': ")
            if direction == 'T' or direction == 'F':
                arr_dir.append(direction)
                break
    return arr_dir


def sq2_input():
    """
        This function receives input - the 2-match-length squares that the user wants to appear on the screen
        The squares are indexed: 0-3
        A picture of the squares indexing in the matchsticks construction is printed on the screen.
        For each index: the user enters 'T' - the square appears
                                        'F' - the square does not appear
        :return: arr_dir - an array of strings ('T' / 'F') which represents the 2-match-length squares that
         will appear on the screen as input.
        """
    im = Image.open('./2-sqr.jpg')
    a = np.asarray(im)
    im = Image.fromarray(a)
    im.show()
    print """
        NOW, YOU NEED TO DECIDE WHICH 2-MATCH-LENGTH SQUARES YOU WANT TO APPEAR ON YOUR SCREEN.
        THE 2-MATCH-LENGTH SQUARES INDEXING APPEARS ON YOUR SCREEN. 
        FOR EACH INDEX: ENTER 'T' - IF YOU WANT THE SQUARE TO APPEAR, 'F' - OTHERWISE
        """
    arr_dir = []
    for i in range(0, 4):
        while True:
            direction = raw_input("INDEX " + str(i) + " - ENTER APPEARS - 'T' OR DOESN'T APPEAR - 'F': ")
            if direction == 'T' or direction == 'F':
                arr_dir.append(direction)
                break
    return arr_dir


def sq3_input():
    """
        This function receives input -
        A picture of the 3-match-length squares indexing in the matchsticks construction is printed on the screen.
        For the 3-match-length square: the user enters 'T' - the square appears
                                                       'F' - the square does not appear
        :return: direction - a string ('T' / 'F') which represents the 3-match-length square:
         will appear / will not appear on the screen as input.
        """
    im = Image.open('./3-sqr.jpg')
    a = np.asarray(im)
    im = Image.fromarray(a)
    im.show()
    print """
        NOW, YOU NEED TO DECIDE IF YOU WANT THE 3-MATCH-LENGTH SQUARE TO APPEAR ON YOUR SCREEN AS AN INITIAL INPUT
        FOR THE RIDDLE.
        THE 1-MATCH-LENGTH SQUARES INDEXING APPEARS ON YOUR SCREEN. 
        FOR EACH INDEX: ENTER 'T' - IF YOU WANT THE SQUARE TO APPEAR, 'F' - OTHERWISE
        """
    while True:
        direction = raw_input("ENTER APPEARS - 'T' OR DOESN'T APPEAR - 'F': ")
        if direction == 'T' or direction == 'F':
            break
    return direction


def to_bool(arr_sq_1, arr_sq_2, sq3):
    """
    This function gets:
    :param arr_sq_1: an array of strings ('T' / 'F') which represents the 1-match-length squares that
     will appear on the screen as input.
    :param arr_sq_2: an array of strings ('T' / 'F') which represents the 2-match-length squares that
     will appear on the screen as input.
    :param sq3: a string ('T' / 'F') which represents the 3-match-length square that
     will appear / will not appear on the screen as input.

     It transforms the arrays into Boolean arrays.

    :return: sq_1_bool, sq_2_bool - Boolean arrays which represent the 1 / 2 - match - length squares that will appear
    on the screen as input.

    sq_3_bool - Boolean variable which represent the 3 - match - length square that will appear / will not appear
    on the screen as input.

    matchsticks - the matchsticks configuration, calculated by the Boolean arrays.
    The matchsticks are indexed: 0 - 23;
    True - the matchstick appears on the screen
    False - the matchstick does not appear on the screen
    """
    sq_1_bool = [True if item == 'T' else False for item in arr_sq_1]
    sq_2_bool = [True if item == 'T' else False for item in arr_sq_2]
    sq_3_bool = True if sq3 == 'T' else False
    matchsticks = [False] * 24

    list_square_1, list_square_2, list_square_3 = sqr_code_proj.get_list_sq()

    for index in range(0, 9):
        if sq_1_bool[index]:
            for item in list_square_1[index]:
                matchsticks[item] = True

    for index in range(0, 4):
        if sq_2_bool[index]:
            for item in list_square_2[index]:
                matchsticks[item] = True

    if sq_3_bool:
        for item in list_square_3:
            matchsticks[item] = True

    return sq_1_bool, sq_2_bool, sq_3_bool, matchsticks


def num_sqr_end_input():
    """
    This function receives user input: Y - the final number of squares which
    will be created by moving X matchsticks.
    """
    while True:
        num_sq_end = raw_input("ENTER THE FINAL NUMBER OF SQUARES: ")
        if num_sq_end.isdigit():
            if 0 <= int(num_sq_end) <= 14:
                break
    return int(num_sq_end)


def num_allowed_sq_input():
    """
    This function receives user input: X - the number of matchsticks to move.
    """
    while True:
        num_allowed = raw_input("ENTER THE NUMBER OF MATCHSTICKS TO MOVE: ")
        if num_allowed.isdigit():
            if 0 <= int(num_allowed) <= 24:
                break
    return int(num_allowed)


def print_sq(matchsticks, title, input_mat=None):
    """
    This function gets:
    :param matchsticks:a Boolean array which represents the current matchsticks configuration:
    Each matchstick is indexed 0 - 23.
    True - the matchstick appears, False - the matchstick does not appear.
    This function prints the current matchsticks configuration.
    If this is the output: the removed matchsticks will be printed in grey, the added ones will be printed in green
    :param title: the title that will be printed: 'The input' / 'The solution'
    :param input_mat: if the input is printed - 'None'
                      if the output is printed - the original input
    :return:
    """
    font = {'family': 'serif',
            'color': 'darkred',
            'weight': 'bold',
            'size': 26,
            }

    rows = 4
    cols = 7
    fig = plt.figure(figsize=(6, 6))
    plt.title(title, fontdict=font)
    plt.axis('off')
    for i in range(1, rows * cols + 1):
        if i <= 21 or i == 23 or i == 25 or i == 27:
            if (i % 7) % 2 == 0 and i % 7 != 0:
                img = mpimg.imread('./match2.jpg')
                plt.axis('off')
            else:
                img = mpimg.imread('./match5.jpg')
                plt.axis('off')
        else:
            img = mpimg.imread('./white.jpg')
            plt.axis('off')
        fig.add_subplot(rows, cols, i)

        if i % 7 == 2:
            if not matchsticks[i - 2]:
                if not input_mat or not input_mat[i - 2]:
                    img = mpimg.imread('./white.jpg')
                    plt.axis('off')
                elif input_mat[i - 2]:
                    img = mpimg.imread('./removed2.jpg')
                    plt.axis('off')
            else:
                if input_mat and not input_mat[i - 2]:
                    img = mpimg.imread('./added2.jpg')
                    plt.axis('off')

        elif i % 7 == 4:
            if not matchsticks[i - 3]:
                if not input_mat or not input_mat[i - 3]:
                    img = mpimg.imread('./white.jpg')
                    plt.axis('off')
                elif input_mat[i - 3]:
                    img = mpimg.imread('./removed2.jpg')
                    plt.axis('off')
            else:
                if input_mat and not input_mat[i - 3]:
                    img = mpimg.imread('./added2.jpg')
                    plt.axis('off')

        elif i % 7 == 6:
            if not matchsticks[i - 4]:
                if not input_mat or not input_mat[i - 4]:
                    img = mpimg.imread('./white.jpg')
                    plt.axis('off')
                elif input_mat[i - 4]:
                    img = mpimg.imread('./removed2.jpg')
                    plt.axis('off')
            else:
                if input_mat and not input_mat[i - 4]:
                    img = mpimg.imread('./added2.jpg')
                    plt.axis('off')

        elif i != 22 and i % 7 == 1:
            if not matchsticks[i + 2]:
                if not input_mat or not input_mat[i + 2]:
                    img = mpimg.imread('./white.jpg')
                    img = ndimage.rotate(img, 90)
                    plt.axis('off')
                elif input_mat[i + 2]:
                    img = mpimg.imread('./removed5.jpg')
                    plt.axis('off')
            else:
                if input_mat and not input_mat[i + 2]:
                    img = mpimg.imread('./added5.jpg')
                    plt.axis('off')

        elif i != 24 and i % 7 == 3:
            if not matchsticks[i + 1]:
                if not input_mat or not input_mat[i + 1]:
                    img = mpimg.imread('./white.jpg')
                    img = ndimage.rotate(img, 90)
                    plt.axis('off')
                elif input_mat[i + 1]:
                    img = mpimg.imread('./removed5.jpg')
                    plt.axis('off')
            else:
                if input_mat and not input_mat[i + 1]:
                    img = mpimg.imread('./added5.jpg')
                    plt.axis('off')

        elif i != 26 and i % 7 == 5:
            if not matchsticks[i]:
                if not input_mat or not input_mat[i]:
                    img = mpimg.imread('./white.jpg')
                    img = ndimage.rotate(img, 90)
                    plt.axis('off')
                elif input_mat[i]:
                    img = mpimg.imread('./removed5.jpg')
                    plt.axis('off')
            else:
                if input_mat and not input_mat[i]:
                    img = mpimg.imread('./added5.jpg')
                    plt.axis('off')

        elif i != 28 and i % 7 == 0:
            if not matchsticks[i - 1]:
                if not input_mat or not input_mat[i - 1]:
                    img = mpimg.imread('./white.jpg')
                    img = ndimage.rotate(img, 90)
                    plt.axis('off')
                elif input_mat[i - 1]:
                    img = mpimg.imread('./removed5.jpg')
                    plt.axis('off')
            else:
                if input_mat and not input_mat[i - 1]:
                    img = mpimg.imread('./added5.jpg')
                    plt.axis('off')
        plt.axis('off')
        plt.imshow(img)
    plt.subplots_adjust(left=0.1,
                        bottom=0.14,
                        right=0.9,
                        top=0.79,
                        wspace=0,
                        hspace=0.05)
    plt.show()


def cont_run_rid():
    """
    This function receives input from the user -
    'N' - does not want to continue solving the current riddle type (math / sum / square / shape)
    'Y' - otherwise
    It returns the user's answer
    """
    cont = ''
    while True:
        cont = raw_input("DO YOU WANT TO CONTINUE SOLVING THIS TYPE OF RIDDLES? ENTER Y / N: ")
        if cont == 'Y' or cont == 'N':
            break
    return cont


def gen_input():
    while True:
        gen = raw_input("""DO YOU WANT THE INPUT TO BE AUTOMATICALLY GENERATED? ENTER Y / N: """)
        if gen == 'Y' or gen == 'N':
            return gen


def menu_sqr(j):
    """
    User menu for solving square riddles - infinite loop (until the user enters N - does not want to continue solving
    this type of riddles)

    It gets j - the initial input/output file's index

    It receives input from the user - the riddle type (normal/optimization) and the
    riddle's parameters

    It prints the input riddle on the screen
    It solves the riddle (considering its type) and prints the solution

    It returns the last input/output file's index
    """
    print """

        WELCOME TO OUR RIDDLES SOLVER!

        HERE YOU CAN SOLVE SQUARE RIDDLES.
        
        ------------------------------------------ RIDDLE DEFINITION: -----------------------------------------------
        
        GIVEN AN INITIAL SQUARES CONSTRUCTION, X - A NUMBER OF MATCHSTICKS TO MOVE AND Y - A FINAL TOTAL NUMBER OF SQUARES:
        A SOLUTION IS - A NEW CONSTRUCTION WHICH INCLUDES EXACTLY Y SQUARES AND X MATCHSTICKS ARE MOVED 
        (THE OTHER MATCHSTICKS' LOCATIONS REMAIN THE SAME)
        
        -------------------------------------------------------------------------------------------------------------
        
        THERE ARE 14 SQUARES: 1-MATCH-LENGTH, 2-MATCH-LENGTH AND 3-MATCH-LENGTH SQUARES.
        
        1-MATCH-LENGTH SQUARES: INDEXED - 0-8
        2-MATCH-LENGTH SQUARES: INDEXED 0-3
        3-MATCH-LENGTH SQUARE
        
        YOU NEED TO CHOOSE Y - THE TOTAL NUMBER OF SQUARES THAT YOU WANT TO CREATE BY MOVING X MATCHSTICKS.
        THEN, YOU NEED TO CHOOSE X - THE NUMBER OF MATCHSTICKS TO MOVE.
        FINALLY, YOU NEED TO CHOOSE THE SQUARES THAT YOU WANT TO APPEAR ON THE SCREEN.
        
        THIS PROGRAM MOVES X MATCHSTICKS (IF POSSIBLE) IN ORDER TO FIND A CORRECT SOLUTION. 
        FOR EACH INPUT, A CORRECT OUTPUT - SOLUTION - WILL BE PRINTED.

        """

    while True:
        cont = cont_run_rid()  # continue solving this type of riddles - 'Y' or 'N'
        if cont == 'N':
            return j
        normal_or_optimal = normal_or_optimal_input()
        gen = gen_input()
        solve_sq(j, normal_or_optimal, gen)
        j += 1


def solve_sq(j, normal_or_optimal, gen='N'):
    """
        This function gets:
        :param j: The index of the input/output files
        :param normal_or_optimal: 'O' - optimization riddle, 'N' - normal squares riddle

        It receives user input - riddle's parameters, considering its type (optimization / normal)

        It solves the squares riddle (normal / optimization), the input and output (solution) are printed on the screen
        """
    if gen == 'N':
        if normal_or_optimal == 'N':
            sq_in_out(j)
        else:  # optimal output
            sq_optimal_in_out(j)
    elif gen == 'Y':
        sq_gen_in_out(j, normal_or_optimal)


def sq_gen_in_out(j, normal_or_optimal):
    if normal_or_optimal == 'N':
        sq_normal_generate_in_out(j)
    elif normal_or_optimal == 'O':
        sq_optimal_generate_in_out(j)


def sq_normal_generate_in_out(j):

    times, flag_solved, run_time, matchsticks, bool1, num_sqr_end, num_allowed = \
            sqr_code_proj.solve_rid_input_gen(j)

    if flag_solved == 1:
        print colored("""                                NO SOLUTION                               """, 'red')

    elif flag_solved == 2:
        print """
YOU NEED TO MOVE: """ + str(num_allowed) + """ MATCHSTICKS
TO GET """ + str(num_sqr_end) + """ SQUARES. THE INITIAL CONSTRUCTION APPEARS ON THE SCREEN NOW."""
        print_sq(bool1, 'THE INPUT')

        print_sq(matchsticks, 'THE SOLUTION', bool1)
    else:
        print colored("""                                NO SOLUTION                               """, 'red')


def sq_optimal_generate_in_out(j):
    times, flag_solved, run_time, matchsticks, bool1, num_sqr_end, num_allowed = \
        sqr_code_proj.solve_rid_input_gen(j)
    num_sqr_beg, num_sqr_1_beg, num_sqr_2_beg, num_sqr_3_beg, sq_1_bool, sq_2_bool, sq_3_bool = \
        sqr_code_proj.transform_match_to_sq_arrays(bool1)
    if flag_solved == 1:
        print colored("""                                NO SOLUTION                               """, 'red')

    elif flag_solved == 2:
        par = opt_par_input()
        if par == 'num_allowed':
            print """YOU NEED TO MOVE A MINIMAL NUMBER OF MATCHSTICKS
TO GET """ + str(num_sqr_end) + """ SQUARES. THE INITIAL CONSTRUCTION APPEARS ON THE SCREEN NOW."""
            print_sq(bool1, 'THE INPUT')
            times, flag_solved, run_time, matchsticks2, current_min = sqr_code_proj.solve_rid_opt_input(j, num_sqr_beg, num_sqr_1_beg, num_sqr_2_beg, num_sqr_3_beg, bool1,
                                              sq_1_bool, sq_2_bool, sq_3_bool, num_sqr_end)
            print_sq(matchsticks2, 'THE OUTPUT', bool1)

        elif par == 'num_sqr_end':
            print """YOU NEED TO MOVE """ + str(num_allowed) + """ MATCHSTICKS
            TO GET A MINIMAL NUMBER OF SQUARES. THE INITIAL CONSTRUCTION APPEARS ON THE SCREEN NOW."""
            print_sq(bool1, 'THE INPUT')
            times, flag_solved, run_time, matchsticks2, current_min = sqr_code_proj.solve_rid_opt_input(j, num_sqr_beg, num_sqr_1_beg, num_sqr_2_beg, num_sqr_3_beg, bool1,
                                              sq_1_bool, sq_2_bool, sq_3_bool, -1, num_allowed)
            print_sq(matchsticks2, 'THE OUTPUT', bool1)


def sq_in_out(j):
    """
     This function gets:
     :param j: Index of the input / output file

     It receives input from the user (normal riddle):
     The existing squares, the number of final squares, the number of matchsticks to move

     It prints the input on the screen
     It solves the normal squares riddle and prints the solution

     """
    num_sqr_end = num_sqr_end_input()
    num_allowed = num_allowed_sq_input()

    arr_sq_1 = sq1_input()
    arr_sq_2 = sq2_input()
    sq_3 = sq3_input()
    sq_1_bool, sq_2_bool, sq_3_bool, matchsticks = to_bool(arr_sq_1, arr_sq_2, sq_3)

    num_sqr_1_beg = sum(sq_1_bool)
    num_sqr_2_beg = sum(sq_2_bool)
    num_sqr_3_beg = sum([sq_3_bool])
    num_sqr_beg = num_sqr_1_beg + num_sqr_2_beg + num_sqr_3_beg

    valid = sqr_code_proj.check_valid(num_sqr_beg, num_sqr_1_beg, num_sqr_2_beg, num_sqr_3_beg, matchsticks, sq_1_bool,
                                      sq_2_bool, sq_3_bool, num_sqr_end,
                                      num_allowed)
    if valid:
        print_sq(matchsticks, 'THE INPUT\n')
        times, flag_solved, run_time = sqr_code_proj.solve_rid_input(j, num_sqr_beg, num_sqr_1_beg, num_sqr_2_beg,
                                                                     num_sqr_3_beg, matchsticks,
                                                                     sq_1_bool, sq_2_bool, sq_3_bool, num_sqr_end,
                                                                     num_allowed)
        if flag_solved == 1:
            print colored("""                                NO SOLUTION                               """, 'red')

        elif flag_solved == 2:
            matchsticks2 = sqr_code_proj.find_info(j)
            print_sq(matchsticks2, 'THE SOLUTION\n', matchsticks)

        else:
            print colored("""                                NO SOLUTION                               """, 'red')

    else:
        print """------------------------------------ERROR - INVALID INPUT----------------------------------------------
                                        SOMETHING IS WRONG WITH THE SQUARES INPUT. 
                                        MAYBE YOU HAVE FORGOTTEN SOME EXISTING SQUARES...
                                        MAYBE THE INTEGER PARAMETERS' VALUES ARE INVALID... 
                                        ENTER YOUR INPUT AGAIN.
    -------------------------------------------------------------------------------------------------------
        """


def opt_par_input():
    """
    This function receives input from the user - which parameter should be optimized while solving the squares riddle
    '1' - minimal number of matchsticks to move (the number of final squares is constant)
    '2' - minimal number of final squares (the number of matchsticks to move is constant)
    It returns the user's answer - the optimized parameter
    """
    while True:
        print """
ENTER THE PARAMETER THAT YOU WANT TO OPTIMIZE:
1 - THE NUMBER OF MATCHSTICKS TO MOVE
2 - THE NUMBER OF TOTAL SQUARES IN THE END OF THE EXECUTION PROCESS
        """
        option = raw_input("ENTER YOUR DECISION HERE: ")
        if option == '1':
            return 'num_allowed'
        elif option == '2':
            return 'num_sqr_end'


def sq_optimal_in_out(j):
    """
     This function gets:
     :param j: Index of the input / output file

     It receives input from the user (optimization riddle):
     The optimized parameter (num_allowed / num_sqr_end)
     The second (constant) parameter's value
     The initial existing squares
     It prints the input on the screen

     It solves the squares optimization riddle and prints the solution with the minimal number of: squares / matchstick
     'move' operations (considering the user's previous choice) on the screen

     """
    opt_parameter = opt_par_input()
    num_allowed, num_sqr_end = (-1, -1)
    if opt_parameter == 'num_sqr_end':
        num_allowed = num_allowed_sq_input()

    elif opt_parameter == 'num_allowed':
        num_sqr_end = num_sqr_end_input()

    arr_sq_1 = sq1_input()
    arr_sq_2 = sq2_input()
    sq_3 = sq3_input()
    sq_1_bool, sq_2_bool, sq_3_bool, matchsticks = to_bool(arr_sq_1, arr_sq_2, sq_3)

    num_sqr_1_beg = sum(sq_1_bool)
    num_sqr_2_beg = sum(sq_2_bool)
    num_sqr_3_beg = sum([sq_3_bool])
    num_sqr_beg = num_sqr_1_beg + num_sqr_2_beg + num_sqr_3_beg

    valid = sqr_code_proj.check_valid(num_sqr_beg, num_sqr_1_beg, num_sqr_2_beg, num_sqr_3_beg, matchsticks, sq_1_bool,
                                      sq_2_bool, sq_3_bool, num_sqr_end,
                                      num_allowed, True, opt_parameter)
    if valid:
        print_sq(matchsticks, 'THE INPUT\n')
        times, flag_solved, run_time, matchsticks2, current_min = sqr_code_proj.solve_rid_opt_input(j, num_sqr_beg,
                                                                                                    num_sqr_1_beg,
                                                                                                    num_sqr_2_beg,
                                                                                                    num_sqr_3_beg,
                                                                                                    matchsticks,
                                                                                                    sq_1_bool,
                                                                                                    sq_2_bool,
                                                                                                    sq_3_bool,
                                                                                                    num_sqr_end,
                                                                                                    num_allowed)
        if flag_solved == 1:
            print colored("""                                NO SOLUTION                               """, 'red')

        elif flag_solved == 0 and opt_parameter == 'num_allowed' and num_sqr_end != num_sqr_beg:
            print colored("""                                NO SOLUTION                               """, 'red')

        elif flag_solved == 0 and opt_parameter == 'num_sqr_end' and num_allowed != 0:

            print colored("""                                NO SOLUTION                               """, 'red')

        elif flag_solved == 2:
            print_sq(matchsticks2, 'THE SOLUTION\n', matchsticks)

        else:
            print_sq(matchsticks2, 'THE SOLUTION\n', matchsticks)

    else:
        print """------------------------------------ERROR - INVALID INPUT----------------------------------------------
                                        SOMETHING IS WRONG WITH THE SQUARES INPUT. 
                                        YOU HAVE FORGOTTEN SOME EXISTING SQUARES...
                                        ENTER YOUR INPUT AGAIN.
    -------------------------------------------------------------------------------------------------------
        """


"""
-----------------------------------------------------------------------------------------------------------
                            SHAPE DIVISION RIDDLES GUI FUNCTIONS
-----------------------------------------------------------------------------------------------------------
"""


def tri_or_sq_input():
    """
    This function receives input from the user -
    'T' - basic area unit: 1-match-length triangle
    'S' - basic area unit: 1-match-length square
    It returns the user's answer
    """
    while True:
        tri_or_sq = raw_input("ENTER 'T' - TRIANGLE OR 'S' - SQUARE: ")
        if tri_or_sq == 'S' or tri_or_sq == 'T':
            return tri_or_sq
        else:
            print "ERROR - INVALID INPUT"


def num_angles_input():
    """
        This function receives input from the user -
        The total number of angles (an angle can be also 180 deg) in the shape
        (1 - match - length edges)
        It returns the user's answer
        """
    while True:
        num_ang = raw_input("ENTER THE TOTAL NUMBER OF ANGLES: ")
        if num_ang.isdigit() and int(num_ang) >= 3:
            return int(num_ang)


def shape_sq_input():
    """
        This function receives input from the user -
        The total number of angles (an angle can be also 180 deg) in the shape
        (1 - match - length edges)
        manual shape input / random shape input / a shape which is a part of a series of polygons
        The angles (if the input is manual) - can be 90, 180, 270
        It returns the user's shape: a 2D array:
        format example - [[1, 90, 2], [2, 180, 3], [3, 90, 4], [4, 90, 5], [5, 180,6], [6, 90, 1]]
    """
    count_edges = 1
    shape = []
    num_angles = num_angles_input()
    man_rnd_con = man_rnd_con_input()
    if man_rnd_con == 'M':
        while True:
            ang = raw_input("ENTER AN ANGLE - 90, 180, 270: ")
            if ang.isdigit() and 0 < int(ang) < 360 and int(ang) % 90 == 0:
                shape.append([count_edges, int(ang), count_edges + 1])
                if count_edges == num_angles:
                    shape[count_edges - 1][2] = 1
                    return shape
                count_edges += 1
            else:
                print "ERROR - INVALID ANGLE INPUT"

    elif man_rnd_con == 'C':
        shape = areanew_proj.create_shape2(num_angles)
        return shape


def man_rnd_con_input():
    """
        This function receives input from the user -
        'M' - manual input
        'R' - random input
        'C' - constant input (available for shape riddles: a shape which is a part of a series)

        It returns the user's answer
    """
    print """
NOW, YOU CAN CHOOSE:
MANUAL INPUT - ENTER 'M'
RANDOM INPUT - ENTER 'R'
CONSTANT GENERATED INPUT - ENTER 'C'
    """
    while True:
        man_rnd_con = raw_input("CHOOSE THE DESIRED OPTION: ")
        if man_rnd_con == 'M' or man_rnd_con == 'R' or man_rnd_con == 'C':
            break
    return man_rnd_con


def shape_tri_input():
    """
            This function receives input from the user -
            The total number of angles (an angle can be also 180 deg) in the shape
            (1 - match - length edges)
            manual shape input / random shape input / a shape which is a part of a series of polygons
            The angles (if the input is manual) - can be 60, 120, 180, 240, 300
            It returns the user's shape: a 2D array:
            format example - [[1, 60, 2], [2, 60, 3], [3, 60, 1]]
    """
    count_edges = 1
    shape = []
    num_angles = num_angles_input()
    man_rnd_con = man_rnd_con_input()
    if man_rnd_con == 'M':
        while True:
            ang = raw_input("ENTER AN ANGLE - 60, 120, 180, 240, 300: ")
            if ang.isdigit() and 0 < int(ang) < 360 and int(ang) % 60 == 0:
                shape.append([count_edges, int(ang), count_edges + 1])
                if count_edges == num_angles:
                    shape[count_edges - 1][2] = 1
                    return shape
                count_edges += 1
            else:
                print "ERROR - INVALID ANGLE INPUT"

    elif man_rnd_con == 'C':
        shape = areanew_proj.create_shape(num_angles)
        return shape


def polygon_input():
    """
        General polygon input function:
        The user enters the shape type (basic area unit: square / triangle) and gets a shape (2D array) for the riddle
        This function returns the shape type and the polygon for the riddle
    """
    original = []
    tri_or_sq = tri_or_sq_input()
    if tri_or_sq == 'S':
        original = shape_sq_input()
    elif tri_or_sq == 'T':
        original = shape_tri_input()
    return original, tri_or_sq


def num_allowed_shape_input():
    """
            This function receives input from the user -
            The total number of matchsticks for division
            It returns the user's input
        """
    while True:
        num_allowed_s = raw_input("ENTER THE NUMBER OF MATCHSTICKS FOR DIVISION: ")
        if num_allowed_s.isdigit():
            return int(num_allowed_s)


def draw(original, title, color='yellow'):
    """
    This function gets:
    :param original: the shape for division
    :param title: 'THE INPUT' / 'THE SOLUTION'
    :param color: relevant only for printing a half of the shape (output), default - yellow
    It prints the shape by calculating its vertices
    """
    font = {'family': 'serif',
            'color': 'darkred',
            'weight': 'bold',
            'size': 18,
            }
    plt.title(title, fontdict=font)
    list_points = check_close.list_points(original, areanew_proj.build_dir(original))
    x_values = [x for x, y in list_points]
    y_values = [y for x, y in list_points]
    plt.plot(x_values, y_values, 'wo', zorder=2)
    for i in range(0, len(x_values) - 1, 1):
        if color == 'yellow':
            plt.plot(x_values[i:i + 2], y_values[i:i + 2], 'y-', zorder=1)
        elif color == 'black':
            plt.plot(x_values[i:i + 2], y_values[i:i + 2], 'k-', zorder=1)
        else:
            plt.plot(x_values[i:i + 2], y_values[i:i + 2], color[0] + '-', zorder=1)
    plt.axis('equal')
    plt.axis('off')


def print_shape(original, title, shape1=None, shape2=None):
    """
    This function gets:
    :param original: the shape for division
    :param title: 'THE INPUT' / 'THE SOLUTION'
    :param shape1: relevant only for printing a half of the shape (output)
    :param shape2: relevant only for printing the other half of the shape (output)
    If this is the input: it prints the original shape by calculating its vertices
    If this is the output: it prints the original shape and a half of it by calculating their vertices
    """

    def foo1(values):
        return values[0]

    def foo2(values):
        for i in range(1, len(values)):
            values[i - 1] = values[i]

    def foo3(values, c):
        values[len(values) - 1] = c

    draw(original, title)

    k = 0  # index of [1, ang, m]
    sh = 1  # default, can be 1 or 2

    if shape1 or shape2:

        for i in range(0, len(shape1)):

            if shape1[i][0] == 1:
                sh = 1
                k = i
            elif shape2[i][0] == 1:
                sh = 2
                k = i

        if sh == 1:
            for r in range(k):
                a = foo1(shape1)
                foo2(shape1)
                foo3(shape1, a)
            draw(shape1, title, 'cyan')

        elif sh == 2:
            for r in range(k):
                a = foo1(shape2)
                foo2(shape2)
                foo3(shape2, a)
            draw(shape2, title, 'cyan')

    plt.show()
    print '1'


def menu_shape(j):
    """
     User menu for solving shape division riddles - infinite loop (until the user enters N - does not want to continue solving
     this type of riddles)

     It gets j - the initial input/output file's index

     It receives input from the user - the riddle's parameters

     It prints the input riddle on the screen
     It solves the riddle (considering its type) and prints the solution

     It returns the last input/output file's index
     """
    print """

            WELCOME TO OUR RIDDLES SOLVER!

            HERE YOU CAN SOLVE SHAPE DIVISION RIDDLES.

            ------------------------------------------ RIDDLE DEFINITION: -----------------------------------------------

            GIVEN AN INITIAL MATCHSTICKS POLYGON AND X - A NUMBER OF MATCHSTICKS TO ADD.
            A SOLUTION IS - THE ORIGINAL POLYGON, DIVIDED BY X MATCHSTICKS INTO 2 IDENTICAL POLYGONS.
            LEGAL POLYGONS:
            BASIC AREA UNIT: 1-MATCH-LENGTH TRIANGLE (LEGAL ANGLES 60, 120, 180, 240, 300)
            BASIC AREA UNIT: 1-MATCH-LENGTH SQUARE (LEGAL ANGLES 90, 180, 270)

            -------------------------------------------------------------------------------------------------------------

            YOU NEED TO INSERT THE POLYGON'S ANGLES.
            THEN, YOU NEED TO CHOOSE X - THE NUMBER OF MATCHSTICKS FOR THE DIVISION.

            THIS PROGRAM ADDS X MATCHSTICKS (IF POSSIBLE) IN ORDER TO DIVIDE THE POLYGON. 
            FOR EACH INPUT, A CORRECT OUTPUT - SOLUTION - WILL BE PRINTED.

            """
    while True:
        cont = cont_run_rid()
        if cont == 'N':
            return j

        polygon, tri_or_sq = polygon_input()
        num_allowed = num_allowed_shape_input()
        valid = areanew_proj.check_valid(polygon, num_allowed)

        if valid:

            print_shape(polygon, 'THE INPUT\n')
            times, flag_solved, run_time, shape1, shape2 = areanew_proj.solve_rid_input(j, polygon, num_allowed,
                                                                                        tri_or_sq)
            if flag_solved == 1:
                print colored("""                                NO SOLUTION                               """, 'red')

            elif flag_solved == 2:
                print_shape(polygon, 'THE SOLUTION\n', shape1, shape2)
                print shape1, shape2

            else:
                print colored("""                                NO SOLUTION                               """, 'red')

        else:
            print """------------------------------------ERROR - INVALID INPUT----------------------------------------------
                                            
                                            YOUR SHAPE IS NOT A POLYGON.
                                    
        -------------------------------------------------------------------------------------------------------
            """

        j += 1


def main_option_input():
    """
        This function receives input from the user -
        '1' - mathematical equation riddles
        '2' - square riddles
        '3' - sum of matchstick heads riddles
        '4' - shape division riddles
        It returns the user's answer
    """
    option = ""
    while True:
        option = raw_input("ENTER YOUR CHOICE HERE (0, 1, 2, 3 OR 4): ")
        if option.isdigit() and 0 <= int(option) <= 4:
            break
    return option


def menu_all():
    """
    General menu for solving all the riddle types
    """
    j = 0
    while True:
        print """
    
WELCOME TO OUR RIDDLES SOLVER!
HERE YOU CAN SOLVE SEVERAL TYPES OF MATCHSTICK RIDDLES.

CHOOSE THE RIDDLES THAT YOU WANT TO SOLVE:
*************************************************************************
*                                                                       *
*                       THE AVAILABLE RIDDLES ARE:                      *
*                                                                       *
*************************************************************************
*                                                                       *
*                MATHEMATICAL RIDDLES (ENTER '1')                       *
*                SQUARE RIDDLES  (ENTER '2')                            *
*                SUM OF MATCHSTICK HEADS RIDDLES  (ENTER '3')           *
*                SHAPE DIVISION RIDDLES (ENTER '4')                     *
*                                                                       *
*************************************************************************    

IF YOU WANT TO EXIT, ENTER '0'.
    """
        option = main_option_input()  # must be 0, 1, 2 or 3
        if option == '1':
            j = menu_math(j)
            continue
        elif option == '2':
            j = menu_sqr(j)
            continue
        elif option == '3':
            j = menu_sum(j)
            continue
        elif option == '4':
            j = menu_shape(j)
            continue
        else:
            print 'Bye'
            break


def main():
    menu_all()


if __name__ == '__main__':
    main()
