import inline as inline
import matplotlib as matplotlib
from matplotlib import transforms
from termcolor import colored, cprint
import general_move
import general2
import mathead_code_proj
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import scipy.misc
from scipy import ndimage
import numpy as np
from PIL import Image

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
    fig = plt.figure(figsize=(18, 18))
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
    plt.show()


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


def equation_input(num_digits):
    """
    This function gets the number of digits per operand - num_digits.
    It receives an operand input from the user.
    It receives a string as an input for the riddle's operator. The operator must be 'minus' or 'plus'.
    It checks that the operands are natural numbers (including 0) and each operand includes maximum (num_digits) digits.
    It checks that the operand string equals 'plus' or 'minus'.
    If the inputs are valid - it returns the equation for the riddle.
    Else - it continues receiving inputs.
    """

    # first operand input
    dig1 = operand_input(num_digits, 1)

    # second operand input
    dig2 = operand_input(num_digits, 2)

    # result input
    result = operand_input(num_digits, 3)

    plus_or_minus = operator_input()

    return dig1, dig2, result, plus_or_minus


def equation_print(dig1, dig2, result, plus_or_minus, num_digits, num_allowed, operation):
    """
    This function prints a riddle's equation. (The equation may be an input or an output)
    """
    st11, st12, st13 = print_number(num_digits, dig1).split('\n')
    st21, st22, st23 = print_number(num_digits, dig2).split('\n')
    st31, st32, st33 = print_number(num_digits, result).split('\n')
    op1, op2, op3 = digits_dict[plus_or_minus].split('\n')
    eq1, eq2, eq3 = digits_dict['='].split('\n')
    print colored(st11 + op1 + st21 + eq1 + st31, 'yellow')
    print colored(st12 + op2 + st22 + eq2 + st32, 'yellow')
    print colored(st13 + op3 + st23 + eq3 + st33, 'yellow')
    print colored("""
                                   NUMBER OF MATCHSTICKS TO """ + operation + """: """ + num_allowed, 'yellow')


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


def general_input(num_digits, operation):
    """
    This function gets num_digits - the number of digits per operand, and operation - add, move or remove.
    It receives input from the user - the riddle's equation and the number of matchsticks required for solving the riddle.
    It prints the input by 7-segment format.
    """
    dig1, dig2, result, plus_or_minus = equation_input(num_digits)
    num_allowed = num_allowed_input(num_digits, operation)
    print """

    ---------------------------------------------------------------------------------------------------------
                                                 YOUR INPUT IS:
                """
    equation_print(dig1, dig2, result, plus_or_minus, num_digits, num_allowed, operation)
    print """---------------------------------------------------------------------------------------------------------"""
    return dig1, dig2, result, plus_or_minus, num_allowed


def general_output(dig1, dig2, result, plus_or_minus, num_digits, num_allowed, operation):
    """
    This function gets num_digits - the number of digits per operand
                       operation - add, move or remove
                       the output equation
    It prints the output equation on the screen.
    """
    print """

    ---------------------------------------------------------------------------------------------------------
                                                 YOUR OUTPUT IS:
                """
    equation_print(dig1, dig2, result, plus_or_minus, num_digits, num_allowed, operation)
    print """---------------------------------------------------------------------------------------------------------"""


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
    :return:
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


def menu_math():
    """
    User menu for solving mathematical equations riddles
    """
    print """Welcome to our matchstick riddles solver!
You can solve: mathematical equations"""
    j = 0
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

        if operation == 'ADD':
            num_digits = add()
            dig1, dig2, result, plus_or_minus, num_allowed = general_input(num_digits, operation)
            times, flag_solved, run_time = general2.solve_equation_input(j, int(dig1), int(dig2), int(result),
                                                                         plus_or_minus, int(num_allowed), 'add',
                                                                         int(num_digits))
            if flag_solved == 1:
                print colored("""                                NO SOLUTION                               """, 'red')
            elif flag_solved == 2:
                dig1, dig2, result = general2.find_info(j)
                general_output(dig1, dig2, result, plus_or_minus, num_digits, num_allowed, 'ADD')
            else:
                print colored("""                                NO SOLUTION                               """, 'red')

        elif operation == 'REMOVE':
            num_digits = remove()
            dig1, dig2, result, plus_or_minus, num_allowed = general_input(num_digits, operation)
            times, flag_solved, run_time = general2.solve_equation_input(j, int(dig1), int(dig2), int(result),
                                                                         plus_or_minus, int(num_allowed), 'remove',
                                                                         int(num_digits))
            if flag_solved == 1:
                print colored("""                                NO SOLUTION                               """, 'red')
            elif flag_solved == 2:
                dig1, dig2, result = general2.find_info(j)
                general_output(dig1, dig2, result, plus_or_minus, num_digits, num_allowed, 'REMOVE')
            else:
                print colored("""                                NO SOLUTION                               """, 'red')

        elif operation == 'MOVE':
            num_digits = move()
            dig1, dig2, result, plus_or_minus, num_allowed = general_input(num_digits, operation)
            times, flag_solved, run_time = general_move.solve_equation_input(j, int(dig1), int(dig2), int(result),
                                                                         plus_or_minus, int(num_allowed),
                                                                         int(num_digits))
            if flag_solved == 1:
                print colored("""                                NO SOLUTION                               """, 'red')
            elif flag_solved == 2:
                dig1, dig2, result = general_move.find_info(j)
                general_output(dig1, dig2, result, plus_or_minus, num_digits, num_allowed, 'MOVE')
            else:
                print colored("""                                NO SOLUTION                               """, 'red')

        elif operation == 'EXIT':
            print 'Bye'
            break
        else:
            print 'Error! Invalid operation.'


def menu_sum():
    j = 0
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
        j += 1
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


def main():
    # menu_math()
    menu_sum()




if __name__ == '__main__':
    main()
