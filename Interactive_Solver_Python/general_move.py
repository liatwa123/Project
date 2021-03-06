import copy
import time
import timeit
import os
import subprocess
import random
import math
from multiprocessing import Pool
from multiprocessing import freeze_support
import threading
import math


def read_math_riddle(j, dig1, dig2, result, plus_or_minus, N, num_allowed=-1, lower=-1, upper=-1):
    """
    This function gets:
    j - index of an input/output file
    dig1 - operand 1
    dig2 - operand 2
    result - the 3rd number
    plus_or_minus - operator, must be 'plus' or 'minus'
    If the riddle is not an optimization problem: num_allowed - number of matchsticks required for solving the riddle
    N - number of digits per operand
    If the riddle is an optimization problem: lower, upper - search limits for the minimal solution
    It checks if the input equation is valid.
    If yes - it writes a model file and runs it
    Else - returns -1
    """
    if num_allowed != -1:
        if check_valid(dig1, dig2, result, plus_or_minus):
            return write_model(j, dig1, dig2, result, plus_or_minus, N, num_allowed)
        else:
            return -1
    else:
        return write_model(j, dig1, dig2, result, plus_or_minus, N, -1, lower, upper)


def check_valid(dig1, dig2, result, plus_or_minus):
    """
        this function gets a string and returns true if it is a legal mathematical equation.
        a legal mathematical equation is:
        x+y=z or x-y=z
        x,y,z are natural numbers
        num_allowed is an integer - the number of add/remove operations allowed by the user
        add_remove must be 'add' or 'remove'
        else, it returns false.
        """
    if not (str(dig1).isdigit() and str(dig2).isdigit() and str(result).isdigit()):
        return False
    elif not (plus_or_minus == 'minus' or plus_or_minus == 'plus'):
        return False
    return True


def find_info(j, find_min=False, find_input=False):
    """
        This function gets:
        j - index of an input/output file
        find_min - True: optimization riddle, False otherwise
        It returns:
        The correct equation - normal riddle
        The correct equation and the minimal number of matchsticks for the operation(move) - optimization riddle
    """
    f = open('output' + str(j) + '.txt', 'r')
    text = f.read()
    while "Execution time: " not in text:
        time.sleep(1)
        f = open('output' + str(j) + '.txt', 'r')
        text = f.read()

    rows = text.split('\n')
    list_dig1 = []
    dig1 = []
    list_dig2 = []
    dig2 = []
    list_result = []
    result = []
    list_dig1_in = []
    dig1_in = []
    list_dig2_in = []
    dig2_in = []
    list_result_in = []
    result_in = []
    num_allowed = 0
    for row in rows:
        if 'digits[0]' in row and 'specification' not in row:
            st, val = row.split(' = ')
            if st not in list_dig1:
                list_dig1.append(st)
                dig1.append(int(val))
            else:
                txt, ind = st.split('s[0][')
                ind = ind[:-1]
                dig1[int(ind)] = int(val)

        elif 'digits[1]' in row and 'specification' not in row:
            st, val = row.split(' = ')
            if st not in list_dig2:
                list_dig2.append(st)
                dig2.append(int(val))
            else:
                txt, ind = st.split('s[1][')
                ind = ind[:-1]
                dig2[int(ind)] = int(val)

        elif 'digits[2]' in row and 'specification' not in row:
            st, val = row.split(' = ')
            if st not in list_result:
                list_result.append(st)
                result.append(int(val))
            else:
                txt, ind = st.split('s[2][')
                ind = ind[:-1]
                result[int(ind)] = int(val)

        if 'init_digs[0]' in row and 'specification' not in row:
            st, val = row.split(' = ')
            if st not in list_dig1_in:
                list_dig1_in.append(st)
                dig1_in.append(int(val))
            else:
                txt, ind = st.split('s[0][')
                ind = ind[:-1]
                dig1_in[int(ind)] = int(val)

        elif 'init_digs[1]' in row and 'specification' not in row:
            st, val = row.split(' = ')
            if st not in list_dig2_in:
                list_dig2_in.append(st)
                dig2_in.append(int(val))
            else:
                txt, ind = st.split('s[1][')
                ind = ind[:-1]
                dig2_in[int(ind)] = int(val)

        elif 'init_digs[2]' in row and 'specification' not in row:
            st, val = row.split(' = ')
            if st not in list_result_in:
                list_result_in.append(st)
                result_in.append(int(val))
            else:
                txt, ind = st.split('s[2][')
                ind = ind[:-1]
                result_in[int(ind)] = int(val)

        elif 'num_allowed' in row and '>' not in row and '!' not in row:
            st, val = row.split(' = ')
            num_allowed = int(val)

    num_dig1, num_dig2, num_result = to_numbers(dig1, dig2, result)
    num_dig1_or, num_dig2_or, num_result_or = to_numbers(dig1_in, dig2_in, result_in)

    if not find_min and not find_input:
        return num_dig1, num_dig2, num_result
    if find_input:
        return num_dig1, num_dig2, num_result, num_dig1_or, num_dig2_or, num_result_or, num_allowed
    if not find_input and find_min:
        return num_dig1, num_dig2, num_result, num_allowed


def to_numbers(li_dig1, li_dig2, li_result):
    """
    This function gets 3 lists of numbers which represent the operands' digits
    It returns the operands as integers
    """
    dig1 = li_dig1[0]
    dig2 = li_dig2[0]
    result = li_result[0]
    for i in range(0, len(li_dig1) - 1):
        dig1 = dig1 * 10 + li_dig1[i + 1]
        dig2 = dig2 * 10 + li_dig2[i + 1]
        result = result * 10 + li_result[i + 1]
    return dig1, dig2, result


def solve_equation_input(j, dig1, dig2, result, plus_or_minus, num_allowed, num_digits):
    """
        This function gets:
        j - index of an input/output file
        dig1 - operand 1
        dig2 - operand 2
        result - the 3rd number
        plus_or_minus - operator, must be 'plus' or 'minus'
        num_allowed - number of matchsticks required for solving the riddle
        num_digits - number of digits per operand
        It checks if the input equation is valid.
        If yes - it writes a model file and runs it
        It returns:
        times - if this parameter equals -1: invalid riddle input
        flag_solved - 1 represents 'no-solution', 2 represents 'solved'
        run_time - the riddle's execution time
    """
    flag_solved = 0
    run_time = -1
    times = read_math_riddle(j, dig1, dig2, result, plus_or_minus, num_digits, num_allowed)
    if times != -1:
        flag_solved, run_time = find_solution(j)
    return times, flag_solved, run_time


def solve_equation_gen(j, plus_or_minus, N):
    flag_solved = 0
    run_time = -1
    dig1, dig2, result, dig1_or, dig2_or, dig3_or, num_allowed = (0, 0, 0, 0, 0, 0, 0)
    times = write_gen_model(j, plus_or_minus, N)
    if times:
        flag_solved, run_time = find_solution(j)
        dig1, dig2, result, dig1_or, dig2_or, dig3_or, num_allowed = find_info(j, False, True)
    return times, flag_solved, run_time, dig1, dig2, result, dig1_or, dig2_or, dig3_or, num_allowed


def write_gen_model(j, plus_or_minus, N):
    text_var = """MODULE main

    				/--state variables--/
    				VAR
    				num_move:0..""" + str(N * 7 * 3) + """;

    				digits: array 0..2 of array 0..""" + str(N - 1) + """ of 0..9;
    				init_digs: array 0..2 of array 0..""" + str(N - 1) + """ of 0..9;

    				xor_arr:array 0..2 of array 0..""" + str(N - 1) + """ of array 0..6 of boolean;
                    init_xor:array 0..2 of array 0..""" + str(N - 1) + """ of array 0..6 of boolean;
                    
    				state:{initial, calc_cons, correct, guess};

    				num_match_beg: 0..""" + str(N * 7 * 3) + """;
    				num_match_end: 0..""" + str(N * 7 * 3) + """;
    				"""


    text_var += """num_allowed:0..""" + str(15 * N) + """;"""

    text_define = """DEFINE
    				/--7-segment representation array--/
    				digit_bool:=[[TRUE,TRUE,TRUE,TRUE,TRUE,FALSE,TRUE],[FALSE,FALSE,FALSE,TRUE,TRUE,FALSE,FALSE],[TRUE,FALSE,TRUE,TRUE,FALSE,TRUE,TRUE],[FALSE,FALSE,TRUE,TRUE,TRUE,TRUE,TRUE],[FALSE,TRUE,FALSE,TRUE,TRUE,TRUE,FALSE],[FALSE,TRUE,TRUE,FALSE,TRUE,TRUE,TRUE],[TRUE,TRUE,TRUE,FALSE,TRUE,TRUE,TRUE],[FALSE,FALSE,TRUE,TRUE,TRUE,FALSE,FALSE],[TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE],[FALSE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE]];
    
    """
    text_assign = """ASSIGN
    """
    for k in range(0, 3):
        for l in range(0, N):
            text_assign += """init(init_digs[""" + str(k) + """][""" + str(l) + """]):=digits[""" + str(k) + """][""" + str(l)+ """];
            """

    for k in range(0, 3):
        for l in range(0, N):
            for m in range(0, 7):
                text_assign += """init(init_xor[""" + str(k) + """][""" + str(l) + """][""" + str(m) + """]) := digit_bool[init_digs[""" + str(k) + """][""" + str(l) + """]][""" + str(m) + """];
                init(xor_arr[""" + str(k) + """][""" + str(l) + """][""" + str(m) + """]):=digit_bool[init_digs[""" + str(k) + """][""" + str(l) + """]][""" + str(m) + """];
                """

    text_assign += """init(state):=initial;
    
    init(num_match_beg):="""
    for i in range(0, 3):
        for j1 in range(0, N):
            for k in range(0, 7):
                text_assign += """count(init_xor[""" + str(i) + """][""" + str(j1) + """][""" + str(k) + """]) + """
    text_assign = text_assign[:-3]
    text_assign += """;
    init(num_match_end):=0;
    init(num_move):=0;"""
    for k in range(0, 3):
        for l in range(0, N):
            text_assign += """next(init_digs[""" + str(k) + """][""" + str(l) + """]):=init_digs[""" + str(k) + """][""" + str(l) + """];
            next(init_xor[""" + str(k) + """][""" + str(l) + """]):=init_xor[""" + str(k) + """][""" + str(l) + """];"""
    text_assign += """
        next(num_allowed):=num_allowed;	
    	next(state):=case
    	state = initial: guess;
    	"""
    text_num1 = """"""
    text_num2 = """"""
    text_num3 = """"""
    for k in range(1, N + 1):
        text_num1 += "digits[0][" + str(k - 1) + "] * " + str(10 ** (N - k)) + " + "
        text_num2 += "digits[1][" + str(k - 1) + "] * " + str(10 ** (N - k)) + " + "
        text_num3 += "digits[2][" + str(k - 1) + "] * " + str(10 ** (N - k)) + " + "

    text_num1 = text_num1[:-2]
    text_num2 = text_num2[:-2]
    text_num3 = text_num3[:-2]
    if plus_or_minus == 'minus':
        text_assign += """state = calc_cons & num_move = 2*num_allowed & num_match_beg = num_match_end & """ + text_num1 + """ - (""" + text_num2 + """) = """ + text_num3 + """: correct;
                          state = calc_cons & !(num_move = 2*num_allowed & num_match_beg = num_match_end & """ + text_num1 + """ - (""" + text_num2 + """) = """ + text_num3 + """): guess;
    				      state = correct: correct;
    				      TRUE: calc_cons;
    				      esac;

    				      next(num_match_beg):=num_match_beg;
    				      next(num_match_end):="""
    elif plus_or_minus == 'plus':
        text_assign += """state = calc_cons & num_move = 2*num_allowed & num_match_beg = num_match_end & """ + text_num1 + """ + (""" + text_num2 + """) = """ + text_num3 + """: correct;
                                  state = calc_cons & !(num_move = 2*num_allowed & num_match_beg = num_match_end & """ + text_num1 + """ + (""" + text_num2 + """) = """ + text_num3 + """): guess;
            				      state = correct: correct;
            				      TRUE: calc_cons;
            				      esac;

            				      next(num_match_beg):=num_match_beg;
            				      next(num_match_end):="""
    for i in range(0, 3):
        for j1 in range(0, N):
            for k in range(0, 7):
                text_assign += """count(digit_bool[digits[""" + str(i) + """][""" + str(j1) + """]][""" + str(
                    k) + """]) + """
    text_assign = text_assign[:-3]
    text_assign += """;

        next(num_move):=case
    	state = guess: """
    for i in range(0, 3):
        for j1 in range(0, N):
            for k in range(0, 7):
                text_assign += """count(next(xor_arr[""" + str(i) + """][""" + str(j1) + """][""" + str(
                    k) + """])) + """
    text_assign = text_assign[:-3]
    text_assign += """;
        TRUE: num_move;
    	esac;

    	"""
    for i in range(0, 3):
        for j1 in range(0, N):
            for k in range(0, 7):
                text_assign += """next(xor_arr[""" + str(i) + """][""" + str(j1) + """][""" + str(k) + """]):=case
                    next(state)=calc_cons:(init_xor[""" + str(i) + """][""" + str(j1) + """][""" + str(
                    k) + """])xor(digit_bool[digits[""" + str(i) + """][""" + str(j1) + """]][""" + str(k) + """]);
                    TRUE:xor_arr[""" + str(i) + """][""" + str(j1) + """][""" + str(k) + """];
                    esac;

                    """
    for i in range(0, 3):
        for j1 in range(0, N):
            text_assign += """
                next(digits[""" + str(i) + """][""" + str(j1) + """]):=case
                next(state)=calc_cons | next(state) = correct: digits[""" + str(i) + """][""" + str(j1) + """];
                TRUE: {0,1,2,3,4,5,6,7,8,9};
                esac;
                """

    text_assign += """LTLSPEC
        G ! (state=correct & num_allowed != 0)"""

    os.chdir(r'C:\Users\liatw\OneDrive\Desktop\NuSMV-'
             r''
             r'2.6.0-win64\bin')

    code = ''''''
    if plus_or_minus == 'minus':
        open('minus_move' + str(j) + ".smv", 'w').close()
        code = '''
j = ''' + str(j) + '''
text_var = """''' + str(text_var) + '''"""
text_define = """''' + str(text_define) + '''"""
text_assign = """''' + str(text_assign) + '''"""
f = open('minus_move' + str(j) + '.smv', 'a')
print >> f, text_var
print >> f, text_define
print >> f, text_assign
f.close()
            '''
    elif plus_or_minus == 'plus':
        open('plus_move' + str(j) + ".smv", 'w').close()
        code = '''
j = ''' + str(j) + '''
text_var = """''' + str(text_var) + '''"""
text_define = """''' + str(text_define) + '''"""
text_assign = """''' + str(text_assign) + '''"""
f = open('plus_move' + str(j) + '.smv', 'a')
print >> f, text_var
print >> f, text_define
print >> f, text_assign
f.close()
            '''
    build_time = timeit.timeit(code, number=1)
    run_model(plus_or_minus + '_move' + str(j) + '.smv', j)  # runs the model
    return build_time


def write_model(j, num1, num2, num3, plus_or_minus, N, num_allowed=-1, lower=-1, upper=-1):
    """
        This function gets the user's input and writes a model according to these values.
        If this is a normal riddle: num_allowed must be entered.
        If this is an optimization riddle: lower and upper (search limits) must be entered.
    """

    text_var = """MODULE main
        
				/--state variables--/
				VAR
				num_move:0..""" + str(N * 7 * 3) + """;
               
				digits: array 0..2 of array 0..""" + str(N - 1) + """ of 0..9;
		
				xor_arr:array 0..2 of array 0..""" + str(N - 1) + """ of array 0..6 of boolean;
		
				state:{initial, calc_cons, correct, guess};
        
				num_match_beg: 0..""" + str(N * 7 * 3) + """;
				num_match_end: 0..""" + str(N * 7 * 3) + """;
				"""

    if num_allowed == -1:
        text_var += """num_allowed:0..""" + str(15 * N) + """;"""

    text_define = """DEFINE
				/--7-segment representation array--/
				digit_bool:=[[TRUE,TRUE,TRUE,TRUE,TRUE,FALSE,TRUE],[FALSE,FALSE,FALSE,TRUE,TRUE,FALSE,FALSE],[TRUE,FALSE,TRUE,TRUE,FALSE,TRUE,TRUE],[FALSE,FALSE,TRUE,TRUE,TRUE,TRUE,TRUE],[FALSE,TRUE,FALSE,TRUE,TRUE,TRUE,FALSE],[FALSE,TRUE,TRUE,FALSE,TRUE,TRUE,TRUE],[TRUE,TRUE,TRUE,FALSE,TRUE,TRUE,TRUE],[FALSE,FALSE,TRUE,TRUE,TRUE,FALSE,FALSE],[TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE],[FALSE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE]];
        
				/--user input--/
				init_digs := """

    num1_arr = []
    num2_arr = []
    num3_arr = []
    num1_cp = num1
    num2_cp = num2
    num3_cp = num3

    for i in range(N, 0, -1):
        num1_arr.append(num1_cp % 10)
        num2_arr.append(num2_cp % 10)
        num3_arr.append(num3_cp % 10)
        num1_cp = num1_cp / 10
        num2_cp = num2_cp / 10
        num3_cp = num3_cp / 10
    num1_arr.reverse()
    num2_arr.reverse()
    num3_arr.reverse()
    arr_tot = [num1_arr, num2_arr, num3_arr]  # these lists represent the digits in each operand

    digits_arr = ["""[TRUE,TRUE,TRUE,TRUE,TRUE,FALSE,TRUE]""", """[FALSE,FALSE,FALSE,TRUE,TRUE,FALSE,FALSE]""",
                  """[TRUE,FALSE,TRUE,TRUE,FALSE,TRUE,TRUE]""", """[FALSE,FALSE,TRUE,TRUE,TRUE,TRUE,TRUE]""",
                  """[FALSE,TRUE,FALSE,TRUE,TRUE,TRUE,FALSE]""", """[FALSE,TRUE,TRUE,FALSE,TRUE,TRUE,TRUE]""",
                  """[TRUE,TRUE,TRUE,FALSE,TRUE,TRUE,TRUE]""", """[FALSE,FALSE,TRUE,TRUE,TRUE,FALSE,FALSE]""",
                  """[TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE]""", """[FALSE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE]"""]
    text_define += str(arr_tot) + """;
    init_xor := ["""
    arr_cp = []

    for element in arr_tot:
        text_define += """["""
        for dig in element:
            text_define += digits_arr[int(dig)] + """, """

        text_define = text_define[:-2]
        text_define += """], """

    text_define = text_define[:-2]
    text_define += """];
    """
    if num_allowed != -1:
        text_define += """num_allowed:=""" + str(num_allowed) + """;"""

    text_define += """/--end-input--/
    """
    text_assign = """ASSIGN
		
				init(digits):=init_digs;
				init(xor_arr):=init_xor;
				init(state):=initial;
		
				init(num_match_beg):="""
    for i in range(0, 3):
        for j1 in range(0, N):
            for k in range(0, 7):
                text_assign += """count(init_xor[""" + str(i) + """][""" + str(j1) + """][""" + str(k) + """]) + """
    text_assign = text_assign[:-3]
    text_assign += """;
    
    init(num_match_end):=0;
	init(num_move):=0;
	"""

    if num_allowed == -1:
        text_assign += """next(num_allowed):=num_allowed;"""

    text_assign += """	
	next(state):=case
	state = initial: guess;
	"""
    text_num1 = """"""
    text_num2 = """"""
    text_num3 = """"""
    for k in range(1, N + 1):
        text_num1 += "digits[0][" + str(k - 1) + "] * " + str(10 ** (N - k)) + " + "
        text_num2 += "digits[1][" + str(k - 1) + "] * " + str(10 ** (N - k)) + " + "
        text_num3 += "digits[2][" + str(k - 1) + "] * " + str(10 ** (N - k)) + " + "

    text_num1 = text_num1[:-2]
    text_num2 = text_num2[:-2]
    text_num3 = text_num3[:-2]
    if plus_or_minus == 'minus':
        text_assign += """state = calc_cons & num_move = 2*num_allowed & num_match_beg = num_match_end & """ + text_num1 + """ - (""" + text_num2 + """) = """ + text_num3 + """: correct;
                      state = calc_cons & !(num_move = 2*num_allowed & num_match_beg = num_match_end & """ + text_num1 + """ - (""" + text_num2 + """) = """ + text_num3 + """): guess;
				      state = correct: correct;
				      TRUE: calc_cons;
				      esac;
				      
				      next(num_match_beg):=num_match_beg;
				      next(num_match_end):="""
    elif plus_or_minus == 'plus':
        text_assign += """state = calc_cons & num_move = 2*num_allowed & num_match_beg = num_match_end & """ + text_num1 + """ + (""" + text_num2 + """) = """ + text_num3 + """: correct;
                              state = calc_cons & !(num_move = 2*num_allowed & num_match_beg = num_match_end & """ + text_num1 + """ + (""" + text_num2 + """) = """ + text_num3 + """): guess;
        				      state = correct: correct;
        				      TRUE: calc_cons;
        				      esac;

        				      next(num_match_beg):=num_match_beg;
        				      next(num_match_end):="""
    for i in range(0, 3):
        for j1 in range(0, N):
            for k in range(0, 7):
                text_assign += """count(digit_bool[digits[""" + str(i) + """][""" + str(j1) + """]][""" + str(
                    k) + """]) + """
    text_assign = text_assign[:-3]
    text_assign += """;
    
    next(num_move):=case
	state = guess: """
    for i in range(0, 3):
        for j1 in range(0, N):
            for k in range(0, 7):
                text_assign += """count(next(xor_arr[""" + str(i) + """][""" + str(j1) + """][""" + str(
                    k) + """])) + """
    text_assign = text_assign[:-3]
    text_assign += """;
    TRUE: num_move;
	esac;
	
	"""
    for i in range(0, 3):
        for j1 in range(0, N):
            for k in range(0, 7):
                text_assign += """next(xor_arr[""" + str(i) + """][""" + str(j1) + """][""" + str(k) + """]):=case
                next(state)=calc_cons:(init_xor[""" + str(i) + """][""" + str(j1) + """][""" + str(
                    k) + """])xor(digit_bool[digits[""" + str(i) + """][""" + str(j1) + """]][""" + str(k) + """]);
                TRUE:xor_arr[""" + str(i) + """][""" + str(j1) + """][""" + str(k) + """];
                esac;
                
                """
    for i in range(0, 3):
        for j1 in range(0, N):
            text_assign += """
            next(digits[""" + str(i) + """][""" + str(j1) + """]):=case
            next(state)=calc_cons | next(state) = correct: digits[""" + str(i) + """][""" + str(j1) + """];
            TRUE: {0,1,2,3,4,5,6,7,8,9};
            esac;
            """
    if num_allowed != -1:
        text_assign += """LTLSPEC
          G ! (state=correct)"""
    else:
        text_assign += """LTLSPEC
         G ! (state=correct & num_allowed >= """ + str(lower) + """ & num_allowed <= """ + str(upper) + """)"""

    os.chdir(r'C:\Users\liatw\OneDrive\Desktop\NuSMV-'
             r''
             r'2.6.0-win64\bin')

    code = ''''''
    if plus_or_minus == 'minus':
        open('minus_move' + str(j) + ".smv", 'w').close()
        code = '''
j = ''' + str(j) + '''
text_var = """''' + str(text_var) + '''"""
text_define = """''' + str(text_define) + '''"""
text_assign = """''' + str(text_assign) + '''"""
f = open('minus_move' + str(j) + '.smv', 'a')
print >> f, text_var
print >> f, text_define
print >> f, text_assign
f.close()
        '''
    elif plus_or_minus == 'plus':
        open('plus_move' + str(j) + ".smv", 'w').close()
        code = '''
j = ''' + str(j) + '''
text_var = """''' + str(text_var) + '''"""
text_define = """''' + str(text_define) + '''"""
text_assign = """''' + str(text_assign) + '''"""
f = open('plus_move' + str(j) + '.smv', 'a')
print >> f, text_var
print >> f, text_define
print >> f, text_assign
f.close()
        '''
    build_time = timeit.timeit(code, number=1)
    run_model(plus_or_minus + '_move' + str(j) + '.smv', j)  # runs the model
    return build_time


def run_model(file_model, j):
    """
    This function gets:
    file_model: name of an input file
    j: index of its matching output file
    It runs the model file in NuSMV
    """
    f = open(str(file_model), 'a')
    open('output' + str(j) + '.txt', 'w').close()
    output_f = open('output' + str(j) + '.txt', 'a')
    subprocess.Popen("ptime.exe NuSMV -bmc -bmc_length 10 " + str(file_model), stdout=output_f, stderr=output_f)
    output_f.close()
    f.close()


def solve_equation(j, plus_or_minus, num_allowed, N):
    """
    This function gets:
    j - index of an input/output file
    dig1 - operand 1
    dig2 - operand 2
    result - the 3rd number
    plus_or_minus - operator, must be 'plus' or 'minus'
    num_allowed - number of matchsticks required for solving the riddle
    N - number of digits per operand
    It checks if the input equation is valid.
    If yes - it writes a model file and runs it
    It returns:
    times - if this parameter equals -1: invalid riddle input
    flag_solved - 1 represents 'no-solution', 2 represents 'solved'
    run_time - the riddle's execution time
    """

    dig1 = random.randint(0, 10 ** N - 1)
    dig2 = random.randint(0, 10 ** N - 1)
    result = random.randint(0, 10 ** N - 1)

    flag_solved = 0
    run_time = -1
    times = read_math_riddle(j, dig1, dig2, result, plus_or_minus, N, num_allowed)
    if times != -1:
        flag_solved, run_time = find_solution(j)
    return times, flag_solved, run_time


def solve_equation_opt_input(j, dig1, dig2, result, plus_or_minus, N):
    """
            This function gets:
            j - index of an input/output file
            dig1 - operand 1
            dig2 - operand 2
            result - the 3rd number
            plus_or_minus - operator, must be 'plus' or 'minus'
            N - number of digits per operand
            It checks if the input equation is valid.
            If yes - it writes a model file and runs it
            It returns:
            times - if this parameter equals -1: invalid riddle input
            flag_solved - 1 represents 'no-solution', 2 represents 'solved'
            run_time - the riddle's execution time
            sol1, sol2, sol3, current_min - the operands and the minimal number of move operations
    """
    flag_solved = 0
    flag_solved1 = 0  # draft for computations of the minimal num_allowed
    run_time = -1
    total = 0
    times = 0
    sol1, sol2, sol3, current_min = (dig1, dig2, result, 0)
    lower, upper, mid_or_last_sol = limits( dig1, dig2, result, N, plus_or_minus)
    if (lower, upper, mid_or_last_sol) != (None, None, None):
        flag_solved = 1
    while (lower, upper, mid_or_last_sol) != (None, None, None):
        times = read_math_riddle(j, dig1, dig2, result, plus_or_minus, N, -1, lower, upper)
        flag_solved1, run_time = find_solution(j)
        total += run_time
        if flag_solved1 == 2:
            flag_solved = 2
            sol1, sol2, sol3, current_min = find_info(j, True)
        lower, upper, mid_or_last_sol = limits(dig1, dig2, result, N, plus_or_minus,
                                                                 mid_or_last_sol, lower, upper,
                                                                 sol1, sol2, sol3, current_min, flag_solved1)
    return times, flag_solved, run_time, sol1, sol2, sol3, current_min


def limits(num1, num2, result, N, plus_or_minus, mid_or_last_sol='', last_lower=-1, last_upper=-1,
           sol1=0, sol2=0, sol3=0, current_min=0, flag_solved=0):
    """
    This function gets:
    :param remove_or_add: remove / add matchsticks
    :param num1: 1st operand - input
    :param num2: 2nd operand - input
    :param result: 3rd number - input
    :param sol1: 1st operand - solution
    :param sol2: 2nd operand - solution
    :param sol3: 3rd number - solution
    :param N: number of digits in each operand
    :param plus_or_minus: operator
    :param mid_or_last_sol: last upper bound chosen - median or the last solution (what was the minimum)
    :param last_lower: last lower bound
    :param last_upper:last upper bound
    :param current_min: current minimal num_allowed
    :param flag_solved: 1 - no solution, 2 - solved
    This function returns: lower, upper, mid_or_last_sol
    """
    if last_lower == last_upper == -1:
        if plus_or_minus == 'plus':
            if num1 + num2 == result:
                return None, None, None# min found - stop changing limits
        else:
            if num1 - num2 == result:
                return None, None, None  # min found - stop changing limits
        return 1, 15 * N, ''

    elif current_min == 1 or last_upper < last_lower:
        return None, None, None

    elif flag_solved == 2:
        if last_lower == last_upper:
            return None, None, None
        if min((last_lower + last_upper) / 2, current_min) == current_min != (last_lower + last_upper) / 2:
            mid_or_last_sol = 'last'
        else:
            mid_or_last_sol = 'mid'
        return last_lower, min((last_lower + last_upper)/2, current_min - 1), mid_or_last_sol

    elif flag_solved == 1:

        if current_min == last_upper + 1:
            return None, None, None

        if mid_or_last_sol == 'last':
            return None, None, None

        elif mid_or_last_sol == '':  # first time running, no solutions -> stop searching
            return None, None, None

        elif mid_or_last_sol == 'mid':
            #  return (last_lower + last_upper) / 2, current_min - 1, mid_or_last_sol
            return last_upper + 1, current_min - 1, mid_or_last_sol


def find_solution(j):
    """
        This function gets:
        j - index of an input/output file
        It returns:
        flag_solved - 1: no solution, 2: solved
        run_time: the riddle's execution time
    """
    run_time = 0

    f = open('output' + str(j) + '.txt', 'r')
    text = f.read()
    while "Execution time: " not in text:
        time.sleep(1)
        f = open('output' + str(j) + '.txt', 'r')
        text = f.read()
    run_str = (text.split("Execution time: "))[1].split(" s")[0]
    run_time = float(run_str)

    if 'is false' in text:
        f.close()
        return 2, run_time
    else:
        f.close()
        return 1, run_time


def calculate_avg(plus_or_minus, num_allowed, N, index):
    """
       This function gets:
       index - starting index for the input/output files
       plus_or_minus - operator, must be 'plus' or 'minus'
       num_allowed - number of matchsticks required for solving the riddle
       N - number of digits per operand

       It randomly chooses:
       dig1 - operand 1
       dig2 - operand 2
       result - the 3rd number

       It checks if the input equation is valid.
       If yes - it writes a model file and runs it
       It calculates the average execution time for no-solution riddles
       """

    avg_build = 0
    avg_solved_run = 0
    avg_not_solved_run = 0
    count_solved = 0
    count_no_solution = 0

    for i in range(index, 120000 + index):  # you can choose a different number than 120000, this number depends on the
                                            # ratio between solved and no-solution riddles
                                            # it also depends on the number of measurements in the average
        times, flag_solved, run_time = solve_equation(i, plus_or_minus, num_allowed, N)
        # times: -1: invalid riddle, otherwise: valid.
        # flag_solved: 1 - no solution, 2 - solved, 0 - invalid
        # run_rime: riddle's execution time

        if times != -1:  # the riddle is valid
            avg_build = avg_build + times
            if flag_solved == 2:
                count_solved += 1
                avg_solved_run = avg_solved_run + run_time
            if flag_solved == 1:
                count_no_solution += 1
                avg_not_solved_run = avg_not_solved_run + run_time

            # number of measured no-solution cases (you can change this row to count_solved, and the number of
            # measurements is up to your choice)
            if count_no_solution == 1:
                return avg_not_solved_run / count_no_solution  # change this to avg_solved_run / count_solved if you want to
                                                               # calculate the average execution time for solved riddles
    return 0


def find_all(j, plus_or_minus, num_allowed, N):
    """
           This function gets:
           j - an index of an input/output file
           plus_or_minus - operator, must be 'plus' or 'minus'
           num_allowed - number of matchsticks required for solving the riddle
           N - number of digits per operand
           It checks if the input equation is valid.
           If yes - it writes a model file and runs it.
           It finds all the possible solutions for the riddle.
           """
    times, flag_solved, run_time = solve_equation(j, plus_or_minus, num_allowed, N)
    while flag_solved != 1:
        update_assertion(j, plus_or_minus)
        j += 1
        run_model(plus_or_minus + "_move" + str(j) + '.smv', j)
        flag_solved, run_time = find_solution(j)


def input_find_all(j, dig1, dig2, result, plus_or_minus, num_allowed, N):
    """
           This function gets:
           j - an index of an input/output file
           plus_or_minus - operator, must be 'plus' or 'minus'
           num_allowed - number of matchsticks required for solving the riddle
           N - number of digits per operand
           It checks if the input equation is valid.
           If yes - it writes a model file and runs it.
           It finds all the possible solutions for the riddle.
           """
    flag_solved = 0
    times, flag_solved1, run_time = solve_equation_input(j, dig1, dig2, result, plus_or_minus, num_allowed, N)

    if flag_solved1 != 0:
        flag_solved = flag_solved1

    while flag_solved1 != 1 and flag_solved1 != 0:
        update_assertion(j, plus_or_minus)
        j += 1
        run_model(plus_or_minus + "_move" + str(j) + '.smv', j)
        flag_solved1, run_time = find_solution(j)
        if flag_solved1 == 2:
            flag_solved = flag_solved1
    return j, flag_solved


def update_assertion(j, plus_or_minus):
    """
        This function gets:
        j - an index of an input/output file
        plus_or_minus - operator, must be 'plus' or 'minus'
        It creates a new input file indexed j + 1
        There, it updates the riddle's assertion in the input file indexed j in order to find new solutions (different
        from the previous ones)
    """
    str_another_sol = ""
    os.chdir(r'C:\Users\liatw\OneDrive\Desktop\NuSMV-2.6.0-win64\bin')
    out = open('output' + str(j) + '.txt', 'r')
    lines_out = out.readlines()

    m = open(plus_or_minus + "_move" + str(j) + '.smv', 'r')

    j += 1

    model = open(plus_or_minus + "_move" + str(j) + '.smv', 'w')
    lines = m.readlines()

    arr_digits = []

    for line in reversed(lines_out):
        if 'digits' in line and 'specification' not in line:
            str_arr, val = line.split(' = ')
            if str_arr not in arr_digits:
                str_another_sol += str_arr + ' = ' + val.strip('\n') + ' &'
                arr_digits.append(str_arr)
    str_another_sol = str_another_sol[:-2]

    for line in lines:
        if 'G ! (state=correct' not in line:
            model.write(line)
        else:
            if 'G ! (state=correct)' in line:
                model.write(line[:-2] + ' & !(' + str_another_sol + '))')
            else:
                imp, rest = line.split('))')
                model.write(imp + ') & !(' + str_another_sol + '))')


def main():
    """
    print str(calculate_avg('minus', 0, 2, 0 * 10 ** 7))
    print str(calculate_avg('minus', 1, 2, 1 * 10 ** 7))
    print str(calculate_avg('minus', 2, 2, 2 * 10 ** 7))
    print str(calculate_avg('minus', 3, 2, 3 * 10 ** 7))
    print str(calculate_avg('minus', 4, 2, 4 * 10 ** 7))
    print str(calculate_avg('minus', 5, 2, 5 * 10 ** 7))
    print str(calculate_avg('minus', 6, 2, 6 * 10 ** 7))
    print str(calculate_avg('minus', 7, 2, 7 * 10 ** 7))
    """

    find_all(1, 'minus', 6, 2)

    """
    print str(calculate_avg('minus', 8, 2, 8 * 10 ** 7))
    print str(calculate_avg('minus', 9, 2, 9 * 10 ** 7))
    print str(calculate_avg('minus', 10, 2, 10 * 10 ** 7))
    print str(calculate_avg('minus', 11, 2, 11 * 10 ** 7))
    print str(calculate_avg('minus', 12, 2, 12 * 10 ** 7))
    print str(calculate_avg('minus', 13, 2, 13 * 10 ** 7))

    print str(calculate_avg('minus', 14, 2, 14 * 10 ** 7))
    print str(calculate_avg('minus', 15, 2, 9 * 10 ** 7))
    print str(calculate_avg('minus', 16, 2, 10 * 10 ** 7))
    print str(calculate_avg('minus', 17, 2, 11 * 10 ** 7))
    print str(calculate_avg('minus', 18, 2, 18 * 10 ** 7))
    print str(calculate_avg('minus', 19, 2, 19 * 10 ** 7))
    print str(calculate_avg('minus', 20, 2, 20 * 10 ** 7))
    print '1'
    """


if __name__ == '__main__':
    main()
