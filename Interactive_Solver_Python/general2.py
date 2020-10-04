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

max_allowed_add = {0: 1, 1: 5, 2: 2, 3: 4, 4: 3, 5: 2, 6: 1, 7: 4, 8: 0, 9: 1}
max_allowed_remove = {0: 4, 1: 0, 2: 0, 3: 3, 4: 2, 5: 0, 6: 1, 7: 1, 8: 5, 9: 4}

text_define = "DEFINE\n\
/--digit_bool:=[[TRUE,TRUE,TRUE,TRUE,TRUE,FALSE,TRUE],[FALSE,FALSE,FALSE,TRUE,TRUE,FALSE,FALSE]," \
              "[TRUE,FALSE,TRUE,TRUE,FALSE,TRUE,TRUE],[FALSE,FALSE,TRUE,TRUE,TRUE,TRUE,TRUE]," \
              "[FALSE,TRUE,FALSE,TRUE,TRUE,TRUE,FALSE],[FALSE,TRUE,TRUE,FALSE,TRUE,TRUE,TRUE]," \
              "[TRUE,TRUE,TRUE,FALSE,TRUE,TRUE,TRUE],[FALSE,FALSE,TRUE,TRUE,TRUE,FALSE,FALSE]," \
              "[TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE],[FALSE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE]];--/\n\
\n\
/--transformations available from every digit, based on num_op of the digit--/\n\
/--the rows are the original digit value, the lists are the transformations and the index of every list is the num_op of" \
              " the digit--/\n\
\n\
/--add transformation--/\n\
arr_trans_add:=[[{0},{8},{0},{0},{0},{0}],\n\
[{1},{7},{4},{3},{9,0},{8}],\n\
[{2},{2},{8},{2},{2},{2}],\n\
[{3},{9},{8},{3},{3},{3}],\n\
[{4},{4},{9},{8},{4},{4}],\n\
[{5},{6,9},{8},{5},{5},{5}],\n\
[{6},{8},{6},{6},{6},{6}],\n\
[{7},{7},{3},{0,9},{8},{7}],\n\
[{8},{8},{8},{8},{8},{8}],\n\
[{9},{8},{9},{9},{9},{9}]];\n\
\n\
/--remove transformation--/\n\
arr_trans_remove:=[[{0},{0},{0},{7},{1},{0}],\n\
[{1},{1},{1},{1},{1},{1}],\n\
[{2},{2},{2},{2},{2},{2}],\n\
[{3},{3},{7},{1},{3},{3}],\n\
[{4},{4},{1},{4},{4},{4}],\n\
[{5},{5},{5},{5},{5},{5}],\n\
[{6},{5},{6},{6},{6},{6}],\n\
[{7},{1},{7},{7},{7},{7}],\n\
[{8},{9,0,6},{3,2,5},{4},{7},{1}],\n\
[{9},{3,5},{4},{7},{1},{9}]];\n\
"

"""
The following functions generate the content of the riddle's NuSMV file
"""


def create_plus_add_next(N, num_allowed=-1, lower=-1, upper=-1):
    text_plus_add_next = "/--next values--/\n\
        /--constants--/\n\
        \n\
        next(plus_or_minus):=plus_or_minus;\n\
        next(num_allowed):=num_allowed;\n\
        next(remove_or_add):=remove_or_add;\n"

    for i in range(1, N + 1):
        text_plus_add_next += "next(dig1_" + str(i) + "_in) := dig1_" + str(i) + "_in;\n"
        text_plus_add_next += "next(dig2_" + str(i) + "_in) := dig2_" + str(i) + "_in;\n"
        text_plus_add_next += "next(result_" + str(i) + "_in) := result_" + str(i) + "_in;\n"

    text_plus_add_next += "next(state) := case\n\
                state = zeros & !is_sol: guess;\n\
                state = zeros & legal & is_sol: correct;\n\
                state = guess & next(is_sol): correct;\n\
                state = guess & !next(is_sol): zeros;\n\
                state = correct: correct;\n \
                TRUE: zeros;\n \
                esac;\n \
                \n\
                next(legal) := case\n \
                state = guess & ("
    for k in range(1, N + 1):
        text_plus_add_next += "num_op_dig1_" + str(k) + " != 0 & dig1_" + str(k) + "=dig1_" + str(k) + "_in | "
        text_plus_add_next += "num_op_dig2_" + str(k) + " != 0 & dig2_" + str(k) + "=dig2_" + str(k) + "_in | "
        text_plus_add_next += "num_op_dig3_" + str(k) + " != 0 & result_" + str(k) + "=result_" + str(k) + "_in | "
    text_plus_add_next = text_plus_add_next[:-2]
    text_plus_add_next += "): FALSE;\n\
                state = zeros: legal; \n \
                state = correct: TRUE;\n \
                state = guess & !("
    for l in range(1, N + 1):
        text_plus_add_next += "num_op_dig1_" + str(l) + " != 0 & dig1_" + str(l) + "=dig1_" + str(l) + "_in | "
        text_plus_add_next += "num_op_dig2_" + str(l) + " != 0 & dig2_" + str(l) + "=dig2_" + str(l) + "_in | "
        text_plus_add_next += "num_op_dig3_" + str(l) + " != 0 & result_" + str(l) + "=result_" + str(l) + "_in | "
    text_plus_add_next = text_plus_add_next[:-2]
    text_plus_add_next += "): TRUE;\n\
                TRUE: legal;\n \
                esac;\n \
                \n \
                next(is_sol) := case\n \
                state = zeros: is_sol;\n \
                state = guess: next(legal) & "
    for s in range(1, N + 1):
        text_plus_add_next += "num_op_dig1_" + str(s) + " + num_op_dig2_" + str(s) + " + num_op_dig3_" + str(s) + " + "
    text_plus_add_next = text_plus_add_next[:-2]
    text_plus_add_next += " = num_allowed & "

    text_num1 = ""
    text_num2 = ""
    text_num3 = ""

    for t in range(1, N + 1):
        text_num1 += "dig1_" + str(t) + " * " + str(10 ** (N - t)) + " + "
        text_num2 += "dig2_" + str(t) + " * " + str(10 ** (N - t)) + " + "
        text_num3 += "result_" + str(t) + " * " + str(10 ** (N - t)) + " + "

    text_num1 = text_num1[:-2]
    text_num2 = text_num2[:-2]
    text_num3 = text_num3[:-2]

    text_plus_add_next += text_num1 + " + (" + text_num2 + ") = " + text_num3 + ";\n\
                state = correct: TRUE;\n \
                TRUE: TRUE;\n \
                esac;\n \
                \n \
                \n "

    for r in range(1, N + 1):
        text_plus_add_next += "next(num_op_dig1_" + str(r) + ") := case\n \
                state = zeros & next(state) = guess: {0, 1, 2, 3, 4, 5};\n \
                state = zeros & next(state) = correct: 0;\n \
                state = guess & next(state) = correct: num_op_dig1_" + str(r) + ";\n \
                state = guess & next(state) = zeros: 0;\n \
                state = correct: num_op_dig1_" + str(r) + ";\n \
                TRUE: {0, 1, 2, 3, 4, 5};\n \
                esac;\n \
                \n \
                next(num_op_dig2_" + str(r) + ") := case\n \
                state = zeros & next(state) = guess: {0, 1, 2, 3, 4, 5};\n \
                state = zeros & next(state) = correct: 0;\n \
                state = guess & next(state) = correct: num_op_dig2_" + str(r) + ";\n \
                state = guess & next(state) = zeros: 0;\n \
                state = correct: num_op_dig2_" + str(r) + ";\n \
                TRUE: {0, 1, 2, 3, 4, 5};\n \
                esac;\n \
                \n \
                next(num_op_dig3_" + str(r) + ") := case\n \
                state = zeros & next(state) = guess: {0, 1, 2, 3, 4, 5};\n \
                state = zeros & next(state) = correct: 0;\n \
                state = guess & next(state) = correct: num_op_dig3_" + str(r) + ";\n \
                state = guess & next(state) = zeros: 0;\n \
                state = correct: num_op_dig3_" + str(r) + ";\n \
                TRUE: {0, 1, 2, 3, 4, 5};\n \
                esac;\n \
                \n \
                next(dig1_" + str(r) + ") := case\n \
                state = zeros & next(state) = guess: arr_trans_add[dig1_" + str(r) + "_in][next(num_op_dig1_" + str(r) + ")];\n \
                state = zeros & next(state) = correct: dig1_" + str(r) + "_in;\n \
                state = guess & next(state) = correct: dig1_" + str(r) + ";\n \
                state = guess & next(state) = zeros: dig1_" + str(r) + "_in;\n \
                state = correct: dig1_" + str(r) + ";\n \
                TRUE: arr_trans_add[dig1_" + str(r) + "_in][next(num_op_dig1_" + str(r) + ")];\n \
                esac;\n \
                \n \
                next(dig2_" + str(r) + ") := case\n \
                state = zeros & next(state) = guess: arr_trans_add[dig2_" + str(r) + "_in][next(num_op_dig2_" + str(r) + ")];\n \
                state = zeros & next(state) = correct: dig2_" + str(r) + "_in;\n \
                state = guess & next(state) = correct: dig2_" + str(r) + ";\n \
                state = guess & next(state) = zeros: dig2_" + str(r) + "_in;\n \
                state = correct: dig2_" + str(r) + ";\n \
                TRUE: arr_trans_add[dig2_" + str(r) + "_in][next(num_op_dig2_" + str(r) + ")];\n \
                esac;\n \
                \n \
                next(result_" + str(r) + ") := case\n \
                state = zeros & next(state) = guess: arr_trans_add[result_" + str(r) + "_in][next(num_op_dig3_" + str(
            r) + ")];\n \
                state = zeros & next(state) = correct: result_" + str(r) + "_in;\n \
                state = guess & next(state) = correct: result_" + str(r) + ";\n \
                state = guess & next(state) = zeros: result_" + str(r) + "_in;\n \
                state = correct: result_" + str(r) + ";\n \
                TRUE: arr_trans_add[result_" + str(r) + "_in][next(num_op_dig3_" + str(r) + ")];\n \
                esac;\n \
                \n"
    if num_allowed != -1:
        text_plus_add_next += "LTLSPEC\n \
        G ! (state=correct)\n"
    else:
        text_plus_add_next += "LTLSPEC\n \
        G ! (state=correct & num_allowed >= " + str(lower) + " & num_allowed <= " + str(upper) + ")\n"
    """
    text_plus_add_next += "SPEC\n \
            EF !(state=correct)\n"
            """
    return text_plus_add_next


def create_plus_remove_next(N, num_allowed=-1, lower=-1, upper=-1):
    text_plus_remove_next = "/--next values--/\n\
        /--constants--/\n\
        \n\
        next(plus_or_minus):=plus_or_minus;\n\
        next(num_allowed):=num_allowed;\n\
        next(remove_or_add):=remove_or_add;\n"

    for i in range(1, N + 1):
        text_plus_remove_next += "next(dig1_" + str(i) + "_in) := dig1_" + str(i) + "_in;\n"
        text_plus_remove_next += "next(dig2_" + str(i) + "_in) := dig2_" + str(i) + "_in;\n"
        text_plus_remove_next += "next(result_" + str(i) + "_in) := result_" + str(i) + "_in;\n"

    text_plus_remove_next += "next(state) := case\n\
                state = zeros & !is_sol: guess;\n\
                state = zeros & legal & is_sol: correct;\n\
                state = guess & next(is_sol): correct;\n\
                state = guess & !next(is_sol): zeros;\n\
                state = correct: correct;\n \
                TRUE: zeros;\n \
                esac;\n \
                \n\
                next(legal) := case\n \
                state = guess & ("
    for k in range(1, N + 1):
        text_plus_remove_next += "num_op_dig1_" + str(k) + " != 0 & dig1_" + str(k) + "=dig1_" + str(k) + "_in | "
        text_plus_remove_next += "num_op_dig2_" + str(k) + " != 0 & dig2_" + str(k) + "=dig2_" + str(k) + "_in | "
        text_plus_remove_next += "num_op_dig3_" + str(k) + " != 0 & result_" + str(k) + "=result_" + str(k) + "_in | "
    text_plus_remove_next = text_plus_remove_next[:-2]
    text_plus_remove_next += "): FALSE;\n\
                state = zeros: legal; \n \
                state = correct: TRUE;\n \
                state = guess & !("
    for l in range(1, N + 1):
        text_plus_remove_next += "num_op_dig1_" + str(l) + " != 0 & dig1_" + str(l) + "=dig1_" + str(l) + "_in | "
        text_plus_remove_next += "num_op_dig2_" + str(l) + " != 0 & dig2_" + str(l) + "=dig2_" + str(l) + "_in | "
        text_plus_remove_next += "num_op_dig3_" + str(l) + " != 0 & result_" + str(l) + "=result_" + str(l) + "_in | "
    text_plus_remove_next = text_plus_remove_next[:-2]
    text_plus_remove_next += "): TRUE;\n\
                TRUE: legal;\n \
                esac;\n \
                \n \
                next(is_sol) := case\n \
                state = zeros: is_sol;\n \
                state = guess: next(legal) & "
    for s in range(1, N + 1):
        text_plus_remove_next += "num_op_dig1_" + str(s) + " + num_op_dig2_" + str(s) + " + num_op_dig3_" + str(s) + " + "
    text_plus_remove_next = text_plus_remove_next[:-2]
    text_plus_remove_next += " = num_allowed & "

    text_num1 = ""
    text_num2 = ""
    text_num3 = ""

    for t in range(1, N + 1):
        text_num1 += "dig1_" + str(t) + " * " + str(10 ** (N - t)) + " + "
        text_num2 += "dig2_" + str(t) + " * " + str(10 ** (N - t)) + " + "
        text_num3 += "result_" + str(t) + " * " + str(10 ** (N - t)) + " + "

    text_num1 = text_num1[:-2]
    text_num2 = text_num2[:-2]
    text_num3 = text_num3[:-2]

    text_plus_remove_next += text_num1 + " + (" + text_num2 + ") = " + text_num3 + ";\n\
                state = correct: TRUE;\n \
                TRUE: TRUE;\n \
                esac;\n \
                \n \
                \n "

    for r in range(1, N + 1):
        text_plus_remove_next += "next(num_op_dig1_" + str(r) + ") := case\n \
                state = zeros & next(state) = guess: {0, 1, 2, 3, 4, 5};\n \
                state = zeros & next(state) = correct: 0;\n \
                state = guess & next(state) = correct: num_op_dig1_" + str(r) + ";\n \
                state = guess & next(state) = zeros: 0;\n \
                state = correct: num_op_dig1_" + str(r) + ";\n \
                TRUE: {0, 1, 2, 3, 4, 5};\n \
                esac;\n \
                \n \
                next(num_op_dig2_" + str(r) + ") := case\n \
                state = zeros & next(state) = guess: {0, 1, 2, 3, 4, 5};\n \
                state = zeros & next(state) = correct: 0;\n \
                state = guess & next(state) = correct: num_op_dig2_" + str(r) + ";\n \
                state = guess & next(state) = zeros: 0;\n \
                state = correct: num_op_dig2_" + str(r) + ";\n \
                TRUE: {0, 1, 2, 3, 4, 5};\n \
                esac;\n \
                \n \
                next(num_op_dig3_" + str(r) + ") := case\n \
                state = zeros & next(state) = guess: {0, 1, 2, 3, 4, 5};\n \
                state = zeros & next(state) = correct: 0;\n \
                state = guess & next(state) = correct: num_op_dig3_" + str(r) + ";\n \
                state = guess & next(state) = zeros: 0;\n \
                state = correct: num_op_dig3_" + str(r) + ";\n \
                TRUE: {0, 1, 2, 3, 4, 5};\n \
                esac;\n \
                \n \
                next(dig1_" + str(r) + ") := case\n \
                state = zeros & next(state) = guess: arr_trans_remove[dig1_" + str(r) + "_in][next(num_op_dig1_" + str(r) + ")];\n \
                state = zeros & next(state) = correct: dig1_" + str(r) + "_in;\n \
                state = guess & next(state) = correct: dig1_" + str(r) + ";\n \
                state = guess & next(state) = zeros: dig1_" + str(r) + "_in;\n \
                state = correct: dig1_" + str(r) + ";\n \
                TRUE: arr_trans_remove[dig1_" + str(r) + "_in][next(num_op_dig1_" + str(r) + ")];\n \
                esac;\n \
                \n \
                next(dig2_" + str(r) + ") := case\n \
                state = zeros & next(state) = guess: arr_trans_remove[dig2_" + str(r) + "_in][next(num_op_dig2_" + str(r) + ")];\n \
                state = zeros & next(state) = correct: dig2_" + str(r) + "_in;\n \
                state = guess & next(state) = correct: dig2_" + str(r) + ";\n \
                state = guess & next(state) = zeros: dig2_" + str(r) + "_in;\n \
                state = correct: dig2_" + str(r) + ";\n \
                TRUE: arr_trans_remove[dig2_" + str(r) + "_in][next(num_op_dig2_" + str(r) + ")];\n \
                esac;\n \
                \n \
                next(result_" + str(r) + ") := case\n \
                state = zeros & next(state) = guess: arr_trans_remove[result_" + str(r) + "_in][next(num_op_dig3_" + str(
            r) + ")];\n \
                state = zeros & next(state) = correct: result_" + str(r) + "_in;\n \
                state = guess & next(state) = correct: result_" + str(r) + ";\n \
                state = guess & next(state) = zeros: result_" + str(r) + "_in;\n \
                state = correct: result_" + str(r) + ";\n \
                TRUE: arr_trans_remove[result_" + str(r) + "_in][next(num_op_dig3_" + str(r) + ")];\n \
                esac;\n \
                \n"
    if num_allowed != -1:
        text_plus_remove_next += "LTLSPEC\n \
         G ! (state=correct)\n"
    else:
        text_plus_remove_next += "LTLSPEC\n \
         G ! (state=correct & num_allowed >= " + str(lower) + " & num_allowed <= " + str(upper) + ")\n"
    """
    text_plus_remove_next += "SPEC\n \
            EF !(state=correct)\n"
    """
    return text_plus_remove_next


def create_minus_add_next(N, num_allowed=-1, lower=-1, upper=-1):
    text_minus_add_next = "/--next values--/\n\
    /--constants--/\n\
    \n\
    next(plus_or_minus):=plus_or_minus;\n\
    next(num_allowed):=num_allowed;\n\
    next(remove_or_add):=remove_or_add;\n"

    for i in range(1, N+1):
        text_minus_add_next += "next(dig1_" + str(i) + "_in) := dig1_" + str(i) + "_in;\n"
        text_minus_add_next += "next(dig2_" + str(i) + "_in) := dig2_" + str(i) + "_in;\n"
        text_minus_add_next += "next(result_" + str(i) + "_in) := result_" + str(i) + "_in;\n"

    text_minus_add_next += "next(state) := case\n\
            state = zeros & !is_sol: guess;\n\
            state = zeros & legal & is_sol: correct;\n\
            state = guess & next(is_sol): correct;\n\
            state = guess & !next(is_sol): zeros;\n\
            state = correct: correct;\n \
            TRUE: zeros;\n \
            esac;\n \
            \n\
            next(legal) := case\n \
            state = guess & ("
    for k in range(1, N+1):
        text_minus_add_next += "num_op_dig1_" + str(k) + " != 0 & dig1_" + str(k) + "=dig1_" + str(k) + "_in | "
        text_minus_add_next += "num_op_dig2_" + str(k) + " != 0 & dig2_" + str(k) + "=dig2_" + str(k) + "_in | "
        text_minus_add_next += "num_op_dig3_" + str(k) + " != 0 & result_" + str(k) + "=result_" + str(k) + "_in | "
    text_minus_add_next = text_minus_add_next[:-2]
    text_minus_add_next += "): FALSE;\n\
            state = zeros: legal; \n \
            state = correct: TRUE;\n \
            state = guess & !("
    for l in range(1, N+1):
        text_minus_add_next += "num_op_dig1_" + str(l) + " != 0 & dig1_" + str(l) + "=dig1_" + str(l) + "_in | "
        text_minus_add_next += "num_op_dig2_" + str(l) + " != 0 & dig2_" + str(l) + "=dig2_" + str(l) + "_in | "
        text_minus_add_next += "num_op_dig3_" + str(l) + " != 0 & result_" + str(l) + "=result_" + str(l) + "_in | "
    text_minus_add_next = text_minus_add_next[:-2]
    text_minus_add_next += "): TRUE;\n\
            TRUE: legal;\n \
            esac;\n \
            \n \
            next(is_sol) := case\n \
            state = zeros: is_sol;\n \
            state = guess: next(legal) & "
    for s in range(1, N+1):
        text_minus_add_next += "num_op_dig1_" + str(s) + " + num_op_dig2_" + str(s) + " + num_op_dig3_" + str(s) +" + "
    text_minus_add_next = text_minus_add_next[:-2]
    text_minus_add_next += " = num_allowed & "

    text_num1 = ""
    text_num2 = ""
    text_num3 = ""

    for t in range(1, N + 1):
        text_num1 += "dig1_" + str(t) + " * " + str(10 ** (N - t)) + " + "
        text_num2 += "dig2_" + str(t) + " * " + str(10 ** (N - t)) + " + "
        text_num3 += "result_" + str(t) + " * " + str(10 ** (N - t)) + " + "

    text_num1 = text_num1[:-2]
    text_num2 = text_num2[:-2]
    text_num3 = text_num3[:-2]

    text_minus_add_next += text_num1 + " - (" + text_num2 + ") = " + text_num3 + ";\n\
            state = correct: TRUE;\n \
            TRUE: TRUE;\n \
            esac;\n \
            \n \
            \n "

    for r in range(1, N+1):
        text_minus_add_next += "next(num_op_dig1_" + str(r) +") := case\n \
            state = zeros & next(state) = guess: {0, 1, 2, 3, 4, 5};\n \
            state = zeros & next(state) = correct: 0;\n \
            state = guess & next(state) = correct: num_op_dig1_" +  str(r) + ";\n \
            state = guess & next(state) = zeros: 0;\n \
            state = correct: num_op_dig1_" +  str(r) + ";\n \
            TRUE: {0, 1, 2, 3, 4, 5};\n \
            esac;\n \
            \n \
            next(num_op_dig2_" + str(r) +") := case\n \
            state = zeros & next(state) = guess: {0, 1, 2, 3, 4, 5};\n \
            state = zeros & next(state) = correct: 0;\n \
            state = guess & next(state) = correct: num_op_dig2_" +  str(r) + ";\n \
            state = guess & next(state) = zeros: 0;\n \
            state = correct: num_op_dig2_" +  str(r) + ";\n \
            TRUE: {0, 1, 2, 3, 4, 5};\n \
            esac;\n \
            \n \
            next(num_op_dig3_" + str(r) +") := case\n \
            state = zeros & next(state) = guess: {0, 1, 2, 3, 4, 5};\n \
            state = zeros & next(state) = correct: 0;\n \
            state = guess & next(state) = correct: num_op_dig3_" +  str(r) + ";\n \
            state = guess & next(state) = zeros: 0;\n \
            state = correct: num_op_dig3_" +  str(r) + ";\n \
            TRUE: {0, 1, 2, 3, 4, 5};\n \
            esac;\n \
            \n \
            next(dig1_" + str(r) +") := case\n \
            state = zeros & next(state) = guess: arr_trans_add[dig1_"+ str(r) +"_in][next(num_op_dig1_" + str(r) +")];\n \
            state = zeros & next(state) = correct: dig1_" + str(r) + "_in;\n \
            state = guess & next(state) = correct: dig1_" + str(r) + ";\n \
            state = guess & next(state) = zeros: dig1_" + str(r) +"_in;\n \
            state = correct: dig1_" + str(r) + ";\n \
            TRUE: arr_trans_add[dig1_" + str(r) + "_in][next(num_op_dig1_" + str(r) + ")];\n \
            esac;\n \
            \n \
            next(dig2_" + str(r) + ") := case\n \
            state = zeros & next(state) = guess: arr_trans_add[dig2_" + str(r) + "_in][next(num_op_dig2_" + str(r) +")];\n \
            state = zeros & next(state) = correct: dig2_" + str(r) + "_in;\n \
            state = guess & next(state) = correct: dig2_" + str(r) + ";\n \
            state = guess & next(state) = zeros: dig2_" + str(r) + "_in;\n \
            state = correct: dig2_" + str(r) + ";\n \
            TRUE: arr_trans_add[dig2_" + str(r) + "_in][next(num_op_dig2_" + str(r) + ")];\n \
            esac;\n \
            \n \
            next(result_"+ str(r) + ") := case\n \
            state = zeros & next(state) = guess: arr_trans_add[result_" + str(r) + "_in][next(num_op_dig3_"+ str(r) +")];\n \
            state = zeros & next(state) = correct: result_" + str(r)+ "_in;\n \
            state = guess & next(state) = correct: result_"+ str(r) +";\n \
            state = guess & next(state) = zeros: result_" + str(r) + "_in;\n \
            state = correct: result_" + str(r) + ";\n \
            TRUE: arr_trans_add[result_" + str(r) + "_in][next(num_op_dig3_"+ str(r) + ")];\n \
            esac;\n \
            \n"

    if num_allowed != -1:
        text_minus_add_next += "LTLSPEC\n \
         G ! (state=correct)\n"
    else:
        text_minus_add_next += "LTLSPEC\n \
         G ! (state=correct & num_allowed >= " + str(lower) + " & num_allowed <= " + str(upper) + ")\n"
    """
    text_minus_add_next += "SPEC\n \
        EF !(state=correct)\n"
        """
    return text_minus_add_next


def create_minus_remove_next(N, num_allowed=-1, lower=-1, upper=-1):
    text_minus_remove_next = "/--next values--/\n\
        /--constants--/\n\
        \n\
        next(plus_or_minus):=plus_or_minus;\n\
        next(num_allowed):=num_allowed;\n\
        next(remove_or_add):=remove_or_add;\n"

    for i in range(1, N + 1):
        text_minus_remove_next += "next(dig1_" + str(i) + "_in) := dig1_" + str(i) + "_in;\n"
        text_minus_remove_next += "next(dig2_" + str(i) + "_in) := dig2_" + str(i) + "_in;\n"
        text_minus_remove_next += "next(result_" + str(i) + "_in) := result_" + str(i) + "_in;\n"

    text_minus_remove_next += "next(state) := case\n\
                state = zeros & !is_sol: guess;\n\
                state = zeros & legal & is_sol: correct;\n\
                state = guess & next(is_sol): correct;\n\
                state = guess & !next(is_sol): zeros;\n\
                state = correct: correct;\n \
                TRUE: zeros;\n \
                esac;\n \
                \n\
                next(legal) := case\n \
                state = guess & ("
    for k in range(1, N + 1):
        text_minus_remove_next += "num_op_dig1_" + str(k) + " != 0 & dig1_" + str(k) + "=dig1_" + str(k) + "_in | "
        text_minus_remove_next += "num_op_dig2_" + str(k) + " != 0 & dig2_" + str(k) + "=dig2_" + str(k) + "_in | "
        text_minus_remove_next += "num_op_dig3_" + str(k) + " != 0 & result_" + str(k) + "=result_" + str(k) + "_in | "
    text_minus_remove_next = text_minus_remove_next[:-2]
    text_minus_remove_next += "): FALSE;\n\
                state = zeros: legal; \n \
                state = correct: TRUE;\n \
                state = guess & !("
    for l in range(1, N + 1):
        text_minus_remove_next += "num_op_dig1_" + str(l) + " != 0 & dig1_" + str(l) + "=dig1_" + str(l) + "_in | "
        text_minus_remove_next += "num_op_dig2_" + str(l) + " != 0 & dig2_" + str(l) + "=dig2_" + str(l) + "_in | "
        text_minus_remove_next += "num_op_dig3_" + str(l) + " != 0 & result_" + str(l) + "=result_" + str(l) + "_in | "
    text_minus_remove_next = text_minus_remove_next[:-2]
    text_minus_remove_next += "): TRUE;\n\
                TRUE: legal;\n \
                esac;\n \
                \n \
                next(is_sol) := case\n \
                state = zeros: is_sol;\n \
                state = guess: next(legal) & "
    for s in range(1, N + 1):
        text_minus_remove_next += "num_op_dig1_" + str(s) + " + num_op_dig2_" + str(s) + " + num_op_dig3_" + str(s) + " + "
    text_minus_remove_next = text_minus_remove_next[:-2]
    text_minus_remove_next += " = num_allowed & "

    text_num1 = ""
    text_num2 = ""
    text_num3 = ""

    for t in range(1, N + 1):
        text_num1 += "dig1_" + str(t) + " * " + str(10 ** (N - t)) + " + "
        text_num2 += "dig2_" + str(t) + " * " + str(10 ** (N - t)) + " + "
        text_num3 += "result_" + str(t) + " * " + str(10 ** (N - t)) + " + "

    text_num1 = text_num1[:-2]
    text_num2 = text_num2[:-2]
    text_num3 = text_num3[:-2]

    text_minus_remove_next += text_num1 + " - (" + text_num2 + ") = " + text_num3 + ";\n\
                state = correct: TRUE;\n \
                TRUE: TRUE;\n \
                esac;\n \
                \n \
                \n "

    for r in range(1, N + 1):
        text_minus_remove_next += "next(num_op_dig1_" + str(r) + ") := case\n \
                state = zeros & next(state) = guess: {0, 1, 2, 3, 4, 5};\n \
                state = zeros & next(state) = correct: 0;\n \
                state = guess & next(state) = correct: num_op_dig1_" + str(r) + ";\n \
                state = guess & next(state) = zeros: 0;\n \
                state = correct: num_op_dig1_" + str(r) + ";\n \
                TRUE: {0, 1, 2, 3, 4, 5};\n \
                esac;\n \
                \n \
                next(num_op_dig2_" + str(r) + ") := case\n \
                state = zeros & next(state) = guess: {0, 1, 2, 3, 4, 5};\n \
                state = zeros & next(state) = correct: 0;\n \
                state = guess & next(state) = correct: num_op_dig2_" + str(r) + ";\n \
                state = guess & next(state) = zeros: 0;\n \
                state = correct: num_op_dig2_" + str(r) + ";\n \
                TRUE: {0, 1, 2, 3, 4, 5};\n \
                esac;\n \
                \n \
                next(num_op_dig3_" + str(r) + ") := case\n \
                state = zeros & next(state) = guess: {0, 1, 2, 3, 4, 5};\n \
                state = zeros & next(state) = correct: 0;\n \
                state = guess & next(state) = correct: num_op_dig3_" + str(r) + ";\n \
                state = guess & next(state) = zeros: 0;\n \
                state = correct: num_op_dig3_" + str(r) + ";\n \
                TRUE: {0, 1, 2, 3, 4, 5};\n \
                esac;\n \
                \n \
                next(dig1_" + str(r) + ") := case\n \
                state = zeros & next(state) = guess: arr_trans_remove[dig1_" + str(r) + "_in][next(num_op_dig1_" + str(r) + ")];\n \
                state = zeros & next(state) = correct: dig1_" + str(r) + "_in;\n \
                state = guess & next(state) = correct: dig1_" + str(r) + ";\n \
                state = guess & next(state) = zeros: dig1_" + str(r) + "_in;\n \
                state = correct: dig1_" + str(r) + ";\n \
                TRUE: arr_trans_remove[dig1_" + str(r) + "_in][next(num_op_dig1_" + str(r) + ")];\n \
                esac;\n \
                \n \
                next(dig2_" + str(r) + ") := case\n \
                state = zeros & next(state) = guess: arr_trans_remove[dig2_" + str(r) + "_in][next(num_op_dig2_" + str(r) + ")];\n \
                state = zeros & next(state) = correct: dig2_" + str(r) + "_in;\n \
                state = guess & next(state) = correct: dig2_" + str(r) + ";\n \
                state = guess & next(state) = zeros: dig2_" + str(r) + "_in;\n \
                state = correct: dig2_" + str(r) + ";\n \
                TRUE: arr_trans_remove[dig2_" + str(r) + "_in][next(num_op_dig2_" + str(r) + ")];\n \
                esac;\n \
                \n \
                next(result_" + str(r) + ") := case\n \
                state = zeros & next(state) = guess: arr_trans_remove[result_" + str(r) + "_in][next(num_op_dig3_" + str(
            r) + ")];\n \
                state = zeros & next(state) = correct: result_" + str(r) + "_in;\n \
                state = guess & next(state) = correct: result_" + str(r) + ";\n \
                state = guess & next(state) = zeros: result_" + str(r) + "_in;\n \
                state = correct: result_" + str(r) + ";\n \
                TRUE: arr_trans_remove[result_" + str(r) + "_in][next(num_op_dig3_" + str(r) + ")];\n \
                esac;\n \
                \n"

    if num_allowed != -1:
        text_minus_remove_next += "LTLSPEC\n \
         G ! (state=correct)\n"
    else:
        text_minus_remove_next += "LTLSPEC\n \
         G ! (state=correct & num_allowed >= " + str(lower) + " & num_allowed <= " + str(upper) + ")\n"
    """
    text_minus_remove_next += "SPEC\n \
        EF !(state=correct)\n"
        """
    return text_minus_remove_next


def limits(remove_or_add, num1, num2, result, N, plus_or_minus, mid_or_last_sol='', last_lower=-1, last_upper=-1,
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
        max_sum = 0
        if plus_or_minus == 'plus':
            if num1 + num2 == result:
                return None, None, None# min found - stop changing limits
        else:
            if num1 - num2 == result:
                return None, None, None  # min found - stop changing limits

        if remove_or_add == 'add':
            # calculate the max number for add
            for k in range(1, N + 1):
                max_sum += max_allowed_add[num1 % 10] + max_allowed_add[num2 % 10] + max_allowed_add[result % 10]
                num1 = num1 / 10
                num2 = num2 / 10
                result = result / 10

        else:
            for k in range(1, N + 1):
                max_sum += max_allowed_remove[num1 % 10] + max_allowed_remove[num2 % 10] + max_allowed_remove[
                    result % 10]
                num1 = num1 / 10
                num2 = num2 / 10
                result = result / 10

        if max_sum == 0:
            return None, None, None
        return 1, max_sum, ''

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
            return (last_lower + last_upper) / 2, current_min - 1, mid_or_last_sol




def read_math_riddle(j, dig1, dig2, result, plus_or_minus, remove_or_add, N, num_allowed=-1, lower=-1, upper=-1):
    """
    This function gets:
    j - index of an input/output file
    dig1 - operand 1
    dig2 - operand 2
    result - the 3rd number
    plus_or_minus - operator, must be 'plus' or 'minus'
    If the riddle is not an optimization problem: num_allowed - number of matchsticks required for solving the riddle
    remove_or_add - operation: must be 'add' or 'remove'
    N - number of digits per operand
    If the riddle is an optimization problem: lower, upper - search limits for the minimal solution
    It checks if the input equation is valid.
    If yes - it writes a model file and runs it
    Else - returns -1
    """
    if num_allowed != -1:
        if check_valid(dig1, dig2, result, plus_or_minus, num_allowed, remove_or_add, N):
            return write_model(j, dig1, dig2, result, plus_or_minus, remove_or_add, N, num_allowed)
        else:
            return -1
    else:
        return write_model(j, dig1, dig2, result, plus_or_minus, remove_or_add, N, -1, lower, upper)


def write_model(j, num1, num2, num3, plus_or_minus, remove_or_add, N, num_allowed=-1, lower=-1, upper=-1):
    """
        This function gets the user's input and writes a model according to these values.
        If this is a normal riddle: num_allowed must be entered.
        If this is an optimization riddle: lower and upper (search limits) must be entered.
    """

    text_var = "MODULE main\n\
    \n\
    /--state variables--/ \n\
    VAR\n"
    for m in range(1, 4):
        if m < 3:
            for i in range(1, N+1):
                text_var += "dig" + str(m) + "_" + str(i) + ":0..9;\n"
                text_var += "dig" + str(m) + "_" + str(i) + "_in:0..9;\n"
                text_var += "num_op_dig" + str(m) + "_" + str(i) + ":0..5;\n"
        else:
            for i in range(1, N+1):
                text_var += "result" + "_" + str(i) + ":0..9;\n"
                text_var += "result" + "_" + str(i) + "_in:0..9;\n"
                text_var += "num_op_dig" + str(m) + "_" + str(i) + ":0..5;\n"

    text_var += "num_allowed:0.." + str(15 * N) + ";\n"
    text_var += "plus_or_minus:{plus,minus};\n\
    remove_or_add:{remove,add};\n\
    \n\
    /--legal checks if num_op_dig1, num_op_dig2 and num_op_dig3 are legal, meaning:--/ \n\
    /--these values are the solution of the riddle--/ \n\
    /--or: any transformation to different dig1, dig2 and dig3 is available using num_op_dig1, num_op_dig2 and num_op_dig3--/ \n\
    legal:boolean;\n\
    is_sol:boolean;\n\
    state:{zeros, guess, correct};\n"

    text_num1 = ""
    text_num2 = ""
    text_num3 = ""

    for k in range(1, N+1):
        text_num1 += "dig1_" + str(k) + " * " + str(10 ** (N-k)) + " + "
        text_num2 += "dig2_" + str(k) + " * " + str(10 ** (N - k)) + " + "
        text_num3 += "result_" + str(k) + " * " + str(10 ** (N - k)) + " + "

    text_num1 = text_num1[:-2]
    text_num2 = text_num2[:-2]
    text_num3 = text_num3[:-2]
    text_minus_add_init = "ASSIGN\n\
/--initial values: user input--/\n"
    num1_str = str(num1)
    num2_str = str(num2)
    num3_str = str(num3)
    if len(num1_str) < N:
        num1_str = '0' * (N-len(str(num1))) + num1_str

    if len(num2_str) < N:
        num2_str = '0' * (N-len(str(num2))) + num2_str

    if len(num3_str) < N:
        num3_str = '0' * (N-len(str(num3))) + num3_str

    for i in range(1, N+1):
        text_minus_add_init += "init(dig1_" + str(i) + ") := " + num1_str[i-1] + ";\n"
        text_minus_add_init += "init(dig2_" + str(i) + ") := " + num2_str[i-1] + ";\n"
        text_minus_add_init += "init(result_" + str(i) + ") := " + num3_str[i-1] + ";\n"
        text_minus_add_init += "init(dig1_" + str(i) + "_in) := " + num1_str[i-1] + ";\n"
        text_minus_add_init += "init(dig2_" + str(i) + "_in) := " + num2_str[i-1] + ";\n"
        text_minus_add_init += "init(result_" + str(i) + "_in) := " + num3_str[i-1] + ";\n"
        text_minus_add_init += "init(num_op_dig1_" + str(i) + ") := 0;\n"
        text_minus_add_init += "init(num_op_dig2_" + str(i) + ") := 0;\n"
        text_minus_add_init += "init(num_op_dig3_" + str(i) + ") := 0;\n"

    text_minus_add_init += "init(state):=zeros;\n\
/--initial values: user input--/\n\
init(plus_or_minus):=" + plus_or_minus + ";\n\
init(remove_or_add):=" + remove_or_add + ";\n\
init(legal):=" + text_num1 + " - ( " + text_num2 + " ) = " + text_num3 + "& num_allowed = 0;\n\
init(is_sol):=" + text_num1 + " - ( " + text_num2 + " ) = " + text_num3 + "& num_allowed = 0;\n"
    if num_allowed != -1:
        text_minus_add_init += "init(num_allowed) := " + str(num_allowed) + ";\n"
    text_minus_remove_init = "ASSIGN\n\
/--initial values: user input--/\n"
    num1_str = str(num1)
    num2_str = str(num2)
    num3_str = str(num3)
    if len(num1_str) < N:
        num1_str = '0' * (N - len(str(num1))) + num1_str

    if len(num2_str) < N:
        num2_str = '0' * (N - len(str(num2))) + num2_str

    if len(num3_str) < N:
        num3_str = '0' * (N - len(str(num3))) + num3_str

    for i in range(1, N+1):
        text_minus_remove_init += "init(dig1_" + str(i) + ") := " + num1_str[i-1] + ";\n"
        text_minus_remove_init += "init(dig2_" + str(i) + ") := " + num2_str[i-1] + ";\n"
        text_minus_remove_init += "init(result_" + str(i) + ") := " + num3_str[i-1] + ";\n"
        text_minus_remove_init += "init(dig1_" + str(i) + "_in) := " + num1_str[i-1] + ";\n"
        text_minus_remove_init += "init(dig2_" + str(i) + "_in) := " + num2_str[i-1] + ";\n"
        text_minus_remove_init += "init(result_" + str(i) + "_in) := " + num3_str[i-1] + ";\n"
        text_minus_remove_init += "init(num_op_dig1_" + str(i) + ") := 0;\n"
        text_minus_remove_init += "init(num_op_dig2_" + str(i) + ") := 0;\n"
        text_minus_remove_init += "init(num_op_dig3_" + str(i) + ") := 0;\n"

    text_minus_remove_init += "init(state):=zeros;\n\
/--initial values: user input--/\n\
init(plus_or_minus):=" + plus_or_minus + ";\n\
init(remove_or_add):=" + remove_or_add + ";\n\
init(legal):=" + text_num1 + " - ( " + text_num2 + " ) = " + text_num3 + "& num_allowed = 0;\n\
init(is_sol):=" + text_num1 + " - ( " + text_num2 + " ) = " + text_num3 + "& num_allowed = 0;\n"
    if num_allowed != -1:
        text_minus_remove_init += "init(num_allowed) := " + str(num_allowed) + ";\n"

    text_plus_add_init = "ASSIGN\n\
/--initial values: user input--/\n"
    num1_str = str(num1)
    num2_str = str(num2)
    num3_str = str(num3)
    if len(num1_str) < N:
        num1_str = '0' * (N - len(str(num1))) + num1_str

    if len(num2_str) < N:
        num2_str = '0' * (N - len(str(num2))) + num2_str

    if len(num3_str) < N:
        num3_str = '0' * (N - len(str(num3))) + num3_str

    for i in range(1, N+1):
        text_plus_add_init += "init(dig1_" + str(i) + ") := " + num1_str[i-1] + ";\n"
        text_plus_add_init += "init(dig2_" + str(i) + ") := " + num2_str[i-1] + ";\n"
        text_plus_add_init += "init(result_" + str(i) + ") := " + num3_str[i-1] + ";\n"
        text_plus_add_init += "init(dig1_" + str(i) + "_in) := " + num1_str[i-1] + ";\n"
        text_plus_add_init += "init(dig2_" + str(i) + "_in) := " + num2_str[i-1] + ";\n"
        text_plus_add_init += "init(result_" + str(i) + "_in) := " + num3_str[i-1] + ";\n"
        text_plus_add_init += "init(num_op_dig1_" + str(i) + ") := 0;\n"
        text_plus_add_init += "init(num_op_dig2_" + str(i) + ") := 0;\n"
        text_plus_add_init += "init(num_op_dig3_" + str(i) + ") := 0;\n"

    text_plus_add_init += "init(state):=zeros;\n\
/--initial values: user input--/\n\
init(plus_or_minus):=" + plus_or_minus + ";\n\
init(remove_or_add):=" + remove_or_add + ";\n\
init(legal):=" + text_num1 + " + ( " + text_num2 + " ) = " + text_num3 + "& num_allowed = 0;\n\
init(is_sol):=" + text_num1 + " + ( " + text_num2 + " ) = " + text_num3 + "& num_allowed = 0;\n"
    if num_allowed != -1:
        text_plus_add_init += "init(num_allowed) := " + str(num_allowed) + ";\n"

    text_plus_remove_init = "ASSIGN\n\
/--initial values: user input--/\n"
    num1_str = str(num1)
    num2_str = str(num2)
    num3_str = str(num3)
    if len(num1_str) < N:
        num1_str = '0' * (N - len(str(num1))) + num1_str

    if len(num2_str) < N:
        num2_str = '0' * (N - len(str(num2))) + num2_str

    if len(num3_str) < N:
        num3_str = '0' * (N - len(str(num3))) + num3_str

    for i in range(1, N+1):
        text_plus_remove_init += "init(dig1_" + str(i) + ") := " + num1_str[i-1] + ";\n"
        text_plus_remove_init += "init(dig2_" + str(i) + ") := " + num2_str[i-1] + ";\n"
        text_plus_remove_init += "init(result_" + str(i) + ") := " + num3_str[i-1] + ";\n"
        text_plus_remove_init += "init(dig1_" + str(i) + "_in) := " + num1_str[i-1] + ";\n"
        text_plus_remove_init += "init(dig2_" + str(i) + "_in) := " + num2_str[i-1] + ";\n"
        text_plus_remove_init += "init(result_" + str(i) + "_in) := " + num3_str[i-1] + ";\n"
        text_plus_remove_init += "init(num_op_dig1_" + str(i) + ") := 0;\n"
        text_plus_remove_init += "init(num_op_dig2_" + str(i) + ") := 0;\n"
        text_plus_remove_init += "init(num_op_dig3_" + str(i) + ") := 0;\n"

    text_plus_remove_init += "init(state):=zeros;\n\
/--initial values: user input--/\n\
init(plus_or_minus):=" + plus_or_minus + ";\n\
init(remove_or_add):=" + remove_or_add + ";\n\
init(legal):=" + text_num1 + " + ( " + text_num2 + " ) = " + text_num3 + "& num_allowed = 0;\n\
init(is_sol):=" + text_num1 + " + ( " + text_num2 + " ) = " + text_num3 + "& num_allowed = 0;\n"
    if num_allowed != -1:
        text_plus_remove_init += "init(num_allowed) := " + str(num_allowed) + ";\n"

    os.chdir(r'C:\Users\liatw\OneDrive\Desktop\NuSMV-'
             r''
             r'2.6.0-win64\bin')
    if plus_or_minus == 'minus' and remove_or_add == 'add':
        text_minus_add_next = create_minus_add_next(N, num_allowed, lower, upper)
        open('minus_add' + str(j) + ".smv", 'w').close()
        code = '''
j = ''' + str(j) + '''
text_var = """''' + str(text_var) + '''"""
text_define = """''' + str(text_define) + '''"""
text_minus_add_init = """''' + str(text_minus_add_init) + '''"""
text_minus_add_next = """''' + str(text_minus_add_next) + '''"""
f = open('minus_add' + str(j) + '.smv', 'a')
print >> f, text_var
print >> f, text_define
print >> f, text_minus_add_init
print >> f, text_minus_add_next
f.close()
        '''
        build_time = timeit.timeit(code, number=1)
        run_model('minus_add' + str(j) + '.smv', j)
        return build_time

    elif plus_or_minus == 'minus' and remove_or_add == 'remove':
        open('minus_remove' + str(j) + ".smv", 'w').close()
        text_minus_remove_next = create_minus_remove_next(N, num_allowed, lower, upper)
        code = '''
j = ''' + str(j) + '''
text_var = """''' + str(text_var) + '''"""
text_define = """''' + str(text_define) + '''"""
text_minus_remove_init = """''' + str(text_minus_remove_init) + '''"""
text_minus_remove_next = """''' + str(text_minus_remove_next) + '''"""
f = open('minus_remove' + str(j) + '.smv', 'a')
print >> f, text_var
print >> f, text_define
print >> f, text_minus_remove_init
print >> f, text_minus_remove_next
f.close()
                '''
        build_time = timeit.timeit(code, number=1)
        run_model('minus_remove' + str(j) + '.smv', j)
        return build_time

    elif plus_or_minus == 'plus' and remove_or_add == 'add':
        open('plus_add' + str(j) + ".smv", 'w').close()
        text_plus_add_next = create_plus_add_next(N, num_allowed, lower, upper)
        code = '''
j = ''' + str(j) + '''
text_var = """''' + str(text_var) + '''"""
text_define = """''' + str(text_define) + '''"""
text_plus_add_init = """''' + str(text_plus_add_init) + '''"""
text_plus_add_next = """''' + str(text_plus_add_next) + '''"""
f = open('plus_add' + str(j) + '.smv', 'a')
print >> f, text_var
print >> f, text_define
print >> f, text_plus_add_init
print >> f, text_plus_add_next
f.close()
                                '''
        build_time = timeit.timeit(code, number=1)
        run_model('plus_add' + str(j) + '.smv', j)
        return build_time

    elif plus_or_minus == 'plus' and remove_or_add == 'remove':
        open('plus_remove' + str(j) + ".smv", 'w').close()
        text_plus_remove_next = create_plus_remove_next(N, num_allowed, lower, upper)
        code = '''
j = ''' + str(j) + '''
text_var = """''' + str(text_var) + '''"""
text_define = """''' + str(text_define) + '''"""
text_plus_remove_init = """''' + str(text_plus_remove_init) + '''"""
text_plus_remove_next = """''' + str(text_plus_remove_next) + '''"""
f = open('plus_remove' + str(j) + '.smv', 'a')
print >> f, text_var
print >> f, text_define
print >> f, text_plus_remove_init
print >> f, text_plus_remove_next
f.close()
                                '''
        build_time = timeit.timeit(code, number=1)
        run_model('plus_remove' + str(j) + '.smv', j)
        return build_time
    else:
        print "error"


def check_valid(dig1, dig2, result, plus_or_minus, num_allowed, remove_or_add, N):
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
    elif not (remove_or_add == "add" or remove_or_add == "remove"):
        return False
    else:
        return check_num_allowed(dig1, dig2, result, remove_or_add, num_allowed, N)


def check_num_allowed(num1, num2, result, remove_or_add, num_allowed, N):
    """
    this function returns:
    True if the max allowed matchsticks for 'add'/'remove' >= num_allowed
    False otherwise
    """

    if remove_or_add == 'add':
        # calculate the max number for add
        max_sum = 0
        for k in range(1, N+1):
            max_sum += max_allowed_add[num1 % 10] + max_allowed_add[num2 % 10] + max_allowed_add[result % 10]
            num1 = num1 / 10
            num2 = num2 / 10
            result = result / 10
        if max_sum >= num_allowed:
            return True
        else:
            return False
    else:
        max_sum = 0
        for k in range(1, N + 1):
            max_sum += max_allowed_remove[num1 % 10] + max_allowed_remove[num2 % 10] + max_allowed_remove[result % 10]
            num1 = num1 / 10
            num2 = num2 / 10
            result = result / 10
        if max_sum >= num_allowed:
            return True
        else:
            return False


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


def solve_equation(j, plus_or_minus, num_allowed, remove_or_add, N):
    """
    This function gets:
    j - index of an input/output file
    plus_or_minus - operator, must be 'plus' or 'minus'
    num_allowed - number of matchsticks required for solving the riddle
    N - number of digits per operand
    remove_or_add - operation: remove or add matchsticks (must be 'remove' or 'add')

    It randomly chooses:
    dig1 - operand 1
    dig2 - operand 2
    result - the 3rd number

    It checks if the input equation is valid.
    If yes - it writes a model file and runs it
    It returns:
    times - if this parameter equals -1: invalid riddle input
    flag_solved - 1 represents 'no-solution', 2 represents 'solved'
    run_time - the riddle's execution time
    """

    dig1 = random.randint(0, 10**N - 1)
    dig2 = random.randint(0, 10**N - 1)
    result = random.randint(0, 10**N - 1)

    flag_solved = 0
    run_time = -1
    times = read_math_riddle(j, dig1, dig2, result, plus_or_minus, remove_or_add, N, num_allowed)
    if times != -1:
        flag_solved, run_time = find_solution(j)
    return times, flag_solved, run_time


def solve_equation_input(j, dig1, dig2, result, plus_or_minus, num_allowed, remove_or_add, N):
    """
    This function gets:
    j - index of an input/output file
    dig1 - operand 1
    dig2 - operand 2
    result - the 3rd number
    plus_or_minus - operator, must be 'plus' or 'minus'
    num_allowed - number of matchsticks required for solving the riddle
    N - number of digits per operand
    remove_or_add - operation: remove or add matchsticks (must be 'remove' or 'add')
    It checks if the input equation is valid.
    If yes - it writes a model file and runs it
    It returns:
    times - if this parameter equals -1: invalid riddle input
    flag_solved - 1 represents 'no-solution', 2 represents 'solved'
    run_time - the riddle's execution time
    """

    flag_solved = 0
    run_time = -1
    times = read_math_riddle(j, dig1, dig2, result, plus_or_minus, remove_or_add, N, num_allowed)
    if times != -1:
        flag_solved, run_time = find_solution(j)
    return times, flag_solved, run_time


def solve_equation_opt_input(j, dig1, dig2, result, plus_or_minus, remove_or_add, N):
    """
        This function gets:
        j - index of an input/output file
        dig1 - operand 1
        dig2 - operand 2
        result - the 3rd number
        plus_or_minus - operator, must be 'plus' or 'minus'
        N - number of digits per operand
        remove_or_add - operation: remove or add matchsticks (must be 'remove' or 'add')
        It checks if the input equation is valid.
        If yes - it writes a model file and runs it
        It returns:
        times - if this parameter equals -1: invalid riddle input
        flag_solved - 1 represents 'no-solution', 2 represents 'solved'
        run_time - the riddle's execution time
        sol1, sol2, sol3, current_min - the operands and the minimal number of add/remove operations
        """
    flag_solved = 0
    flag_solved1 = 0  # draft for computations of the minimal num_allowed
    run_time = -1
    total = 0
    times = 0
    sol1, sol2, sol3, current_min = (dig1, dig2, result, 0)
    lower, upper, mid_or_last_sol = limits(remove_or_add, dig1, dig2, result, N, plus_or_minus)
    if (lower, upper, mid_or_last_sol) != (None, None, None):
        flag_solved = 1
    while (lower, upper, mid_or_last_sol) != (None, None, None):
        times = read_math_riddle(j, dig1, dig2, result, plus_or_minus, remove_or_add, N, -1, lower, upper)
        flag_solved1, run_time = find_solution(j)
        total += run_time
        if flag_solved1 == 2:
            flag_solved = 2
            sol1, sol2, sol3, current_min = find_info(j, True)
        lower, upper, mid_or_last_sol = limits(remove_or_add, dig1, dig2, result, N, plus_or_minus,
                                                                 mid_or_last_sol, lower, upper,
                                                                 sol1, sol2, sol3, current_min, flag_solved1)
    return times, flag_solved, run_time, sol1, sol2, sol3, current_min


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


def find_info(j, find_min=False):
    """
        This function gets:
        j - index of an input/output file
        find_min - True: optimization riddle, False otherwise
        It returns:
        The correct equation - normal riddle
        The correct equation and the minimal number of matchsticks for the operation(add/remove) - optimization riddle
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
    num_allowed = 0
    for row in rows:
        if 'dig1' in row and 'specification' not in row and 'in' not in row and 'op' not in row:
            st, val = row.split(' = ')
            if st not in list_dig1:
                list_dig1.append(st)
                dig1.append(int(val))
            else:
                txt, ind = st.split('1_')
                dig1[int(ind) - 1] = int(val)

        elif 'dig2' in row and 'specification' not in row and 'in' not in row and 'op' not in row:
            st, val = row.split(' = ')
            if st not in list_dig2:
                list_dig2.append(st)
                dig2.append(int(val))
            else:
                txt, ind = st.split('2_')
                dig2[int(ind) - 1] = int(val)

        elif 'result' in row and 'specification' not in row and 'might' not in row and 'in' not in row and 'op' not in row:
            st, val = row.split(' = ')
            if st not in list_result:
                list_result.append(st)
                result.append(int(val))
            else:
                txt, ind = st.split('_')
                result[int(ind) - 1] = int(val)

        elif 'num_allowed' in row and '>' not in row:
            st, val = row.split(' = ')
            num_allowed = int(val)

    num_dig1, num_dig2, num_result = to_numbers(dig1, dig2, result)
    if find_min:
        return num_dig1, num_dig2, num_result, num_allowed
    return num_dig1, num_dig2, num_result


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


def calculate_avg(plus_or_minus, num_allowed, remove_or_add, N, index):
    """
           This function gets:
           index - starting index for the input/output files
           plus_or_minus - operator, must be 'plus' or 'minus'
           num_allowed - number of matchsticks required for solving the riddle
           N - number of digits per operand
           remove_or_add - operation: remove or add matchsticks (must be 'remove' or 'add')
           It randomly chooses:
           dig1 - operand 1
           dig2 - operand 2
           result - the 3rd number

           It checks if the input equation is valid.
           If yes - it writes a model file and runs it
           It calculates the average execution time for solved riddles
    """
    avg_build = 0
    avg_solved_run = 0
    avg_not_solved_run = 0
    count_solved = 0
    count_no_solution = 0

    for i in range(index, 120000 + index):
        times, flag_solved, run_time = solve_equation(i, plus_or_minus, num_allowed, remove_or_add, N)

        if times != -1:
            avg_build = avg_build + times
            if flag_solved == 2:
                count_solved += 1
                avg_solved_run = avg_solved_run + run_time
            if flag_solved == 1:
                count_no_solution += 1
                avg_not_solved_run = avg_not_solved_run + run_time
            if count_solved == 1:
                break
    return avg_solved_run / count_solved


def main():
    """
    print str(calculate_avg('minus', 0, 'remove', 3, 0 * 10 ** 7))
    print str(calculate_avg('minus', 1, 'remove', 3, 1 * 10 ** 7))

    print str(calculate_avg('minus', 2, 'remove', 3, 2 * 10 ** 7))

    print str(calculate_avg('minus', 3, 'remove', 3, 3 * 10 ** 7))

    print str(calculate_avg('minus', 4, 'remove', 3, 4 * 10 ** 7))

    print str(calculate_avg('minus', 5, 'remove', 3, 4 * 10 ** 7))
    print str(calculate_avg('minus', 6, 'remove', 3, 6 * 10 ** 7))
    print str(calculate_avg('minus', 7, 'remove', 3, 7 * 10 ** 7))

    print str(calculate_avg('minus', 8, 'remove', 3, 8 * 10 ** 7))
     print str(calculate_avg('minus', 9, 'remove', 1, 9 * 10 ** 7))

    print str(calculate_avg('minus', 10, 'remove', 3, 10 * 10 ** 7))
    print str(calculate_avg('minus', 11, 'remove', 3, 11 * 10 ** 7))

    print str(calculate_avg('minus', 12, 'remove', 3, 12 * 10 ** 7))
    print str(calculate_avg('minus', 13, 'remove', 3, 13 * 10 ** 7))
    print str(calculate_avg('minus', 14, 'remove', 3, 14 * 10 ** 7))
    """
    os.chdir(r'C:\Users\liatw\OneDrive\Desktop\NuSMV-'
             r''
             r'2.6.0-win64\bin')
    run_model('minus_add2.smv', 2)




if __name__ == '__main__':
    main()


