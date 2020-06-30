from termcolor import colored, cprint
import general_move
import general2

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
    # first operand input
    dig1 = operand_input(num_digits, 1)

    # second operand input
    dig2 = operand_input(num_digits, 2)

    # result input
    result = operand_input(num_digits, 3)

    plus_or_minus = operator_input()

    return dig1, dig2, result, plus_or_minus


def equation_print(dig1, dig2, result, plus_or_minus, num_digits, num_allowed, operation):
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
    print """

    ---------------------------------------------------------------------------------------------------------
                                                 YOUR OUTPUT IS:
                """
    equation_print(dig1, dig2, result, plus_or_minus, num_digits, num_allowed, operation)
    print """---------------------------------------------------------------------------------------------------------"""


def menu():
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


def main():
    menu()


if __name__ == '__main__':
    main()
