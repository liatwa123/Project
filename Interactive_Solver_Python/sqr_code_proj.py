import os
import subprocess
import time
import timeit
import random

text_var = "MODULE main\n\
\n\
/--state variables--/\n\
VAR\n\
num_squares_beginning:0..14;\n\
num_squares_end:0..14;\n\
num_allowed:0..24;\n\
num_move:0..24;\n\
\n\n\
num_squares_1_beg:0..9;\n\
num_squares_1_end:0..9;\n\
last_in_1:0..9;\n\
\n\n\
num_squares_2_beg:0..4;\n\
num_squares_2_end:0..4;\n\
last_in_2:0..4;\n\
\n\n\
num_squares_3_beg:0..1;\n\
num_squares_3_end:0..1;\n\
last_in_3:{0,1};\n\
\n\n\
matchsticks:array 0..23 of boolean;\n\
match_index: 0..24;\n\
xor_arr:array 0..23 of boolean;\n\
state:{initial, calc_cons, correct, guess, check_free};\n\
free: boolean;\n\
fin_free: boolean;\n\
finished_count: boolean;\n\
sq_1_bool: array 0..8 of boolean;\n\
sq_2_bool: array 0..3 of boolean;\n\
sq_3_bool: boolean;\n\
num_match_beg: 0..24;\n\
num_match_end:0..24;\n"

num_squares_beginning_str = ""
num_squares_1_beg_str = ""
num_squares_2_beg_str = ""
num_squares_3_beg_str = ""
num_squares_end_str = ""
num_allowed_str = ""
text_assign_2 = "init(num_squares_1_end):=0;\n\
init(num_squares_2_end):=0;\n\
init(num_squares_3_end):=0;\n\
init(xor_arr):=falsarr;\n\
init(free):=FALSE;\n\
init(fin_free):=FALSE;\n\
init(last_in_1):=0;\n\
init(last_in_2):=0;\n\
init(last_in_3):=0;\n\
init(num_move):=0;\n\
\n\n\
init(match_index):=0;\n\
init(state):=initial;\n\
init(finished_count):=FALSE;\n\
init(num_match_beg):=count(bool1[0]) + count(bool1[1]) + count(bool1[2]) + count(bool1[3]) + count(bool1[4]) + count(bool1[5]) + count(bool1[6]) + count(bool1[7]) + count(bool1[8]) + count(bool1[9]) + count(bool1[10]) + count(bool1[11]) + count(bool1[12]) + count(bool1[13]) + count(bool1[14]) + count(bool1[15]) + count(bool1[16]) + count(bool1[17]) + count(bool1[18]) + count(bool1[19]) + count(bool1[20]) + count(bool1[21]) + count(bool1[22]) + count(bool1[23]);\n\
init(num_match_end):=0;\n\
/--next values--/\n\
/--constants--/\n\
next(num_squares_beginning):=num_squares_beginning;\n\
next(num_squares_1_beg):=num_squares_1_beg;\n\
next(num_squares_2_beg):=num_squares_2_beg;\n\
next(num_squares_3_beg):=num_squares_3_beg;\n\
next(num_squares_end):=num_squares_end;\n\
next(num_allowed):=num_allowed;\n\
next(finished_count):=last_in_1=9 & last_in_2=4 & last_in_3=1;\n\
next(num_match_beg):=num_match_beg;\n\
/--non constants--/\n\
next(state):=case\n\
finished_count & state = check_free & !free & fin_free & num_squares_1_end + num_squares_2_end + num_squares_3_end = num_squares_end & num_move = 2*num_allowed & num_match_beg = num_match_end: correct;\n\
state = calc_cons & finished_count & (num_squares_1_end + num_squares_2_end + num_squares_3_end != num_squares_end | num_move!=2*num_allowed | num_match_beg != num_match_end): guess;\n\
state = calc_cons & finished_count & (num_squares_1_end + num_squares_2_end + num_squares_3_end = num_squares_end & num_move=2*num_allowed & num_match_beg = num_match_end): check_free;\n\
state = check_free & !fin_free: check_free;\n\
state = check_free & fin_free & free: guess;\n\
state = guess & num_squares_1_end != 0: guess;\n\
state = correct: correct;\n\
TRUE: calc_cons;\n\
esac;\n\
\n\n\
next(match_index):=case\n\
state = check_free: (match_index + 1)mod(25);\n\
TRUE: 0;\n\
esac;\n\
\n\n\
next(fin_free):=(next(match_index) = 24);\n\
\n\n\
next(last_in_1):=case\n\
state = calc_cons & next(state) = calc_cons & last_in_1 < 9: (last_in_1 + 1)mod(10);\n\
state = calc_cons & last_in_1 = 9 & next(state) = calc_cons: 9;\n\
state = calc_cons & last_in_1 = 9 & next(state) = guess: 0;\n\
state = calc_cons & last_in_1 = 9 & next(state) = correct: 9;\n\
state = guess: 0;\n\
state = correct: 9;\n\
state = initial: 0;\n\
TRUE: 9;\n\
esac;\n\
\n\n\
next(last_in_2):=case\n\
state = calc_cons & next(state) = calc_cons & last_in_2 < 4: (last_in_2 + 1)mod(5);\n\
state = calc_cons & last_in_2 = 4 & next(state) = calc_cons: 4;\n\
state = calc_cons & last_in_2 = 4 & next(state) = guess: 0;\n\
state = calc_cons & last_in_2 = 4 & next(state) = correct: 4;\n\
state = guess: 0;\n\
state = correct: 4;\n\
state = initial: 0;\n\
TRUE: 4;\n\
esac;\n\
\n\n\
next(last_in_3):=case\n\
state = calc_cons & next(state) = calc_cons & last_in_3 < 1: (last_in_3 + 1)mod(2);\n\
state = calc_cons & last_in_3 = 1 & next(state) = calc_cons: 1;\n\
state = calc_cons & last_in_3 = 1 & next(state) = guess: 0;\n\
state = calc_cons & last_in_3 = 1 & next(state) = correct: 1;\n\
state = guess: 0;\n\
state = correct: 1;\n\
state = initial: 0;\n\
TRUE: 1;\n\
esac;\n\
\n\n\
next(matchsticks[0]):=case\n\
next(state) = calc_cons: matchsticks[0];\n\
next(state) = correct: matchsticks[0];\n\
next(state) = guess & state = calc_cons:{TRUE, FALSE};\n\
TRUE:matchsticks[0];\n\
esac;\n\
\n\n\
next(matchsticks[1]):=case\n\
next(state) = calc_cons: matchsticks[1];\n\
next(state) = correct: matchsticks[1];\n\
next(state) = guess & state = calc_cons:{TRUE, FALSE};\n\
TRUE:matchsticks[1];\n\
esac;\n\
\n\n\
next(matchsticks[2]):=case\n\
next(state) = calc_cons: matchsticks[2];\n\
next(state) = correct: matchsticks[2];\n\
next(state) = guess & state = calc_cons:{TRUE, FALSE};\n\
TRUE:matchsticks[2];\n\
esac;\n\
\n\n\
next(matchsticks[3]):=case\n\
next(state) = calc_cons: matchsticks[3];\n\
next(state) = correct: matchsticks[3];\n\
next(state) = guess & state = calc_cons:{TRUE, FALSE};\n\
TRUE:matchsticks[3];\n\
esac;\n\
\n\n\
next(matchsticks[4]):=case\n\
next(state) = calc_cons: matchsticks[4];\n\
next(state) = correct: matchsticks[4];\n\
next(state) = guess & state = calc_cons:{TRUE, FALSE};\n\
TRUE:matchsticks[4];\n\
esac;\n\
\n\n\
next(matchsticks[5]):=case\n\
next(state) = calc_cons: matchsticks[5];\n\
next(state) = correct: matchsticks[5];\n\
next(state) = guess & state = calc_cons:{TRUE, FALSE};\n\
TRUE:matchsticks[5];\n\
esac;\n\
\n\n\
next(matchsticks[6]):=case\n\
next(state) = calc_cons: matchsticks[6];\n\
next(state) = correct: matchsticks[6];\n\
next(state) = guess & state = calc_cons:{TRUE, FALSE};\n\
TRUE:matchsticks[6];\n\
esac;\n\
\n\n\
next(matchsticks[7]):=case\n\
next(state) = calc_cons: matchsticks[7];\n\
next(state) = correct: matchsticks[7];\n\
next(state) = guess & state = calc_cons:{TRUE, FALSE};\n\
TRUE:matchsticks[7];\n\
esac;\n\
\n\n\
next(matchsticks[8]):=case\n\
next(state) = calc_cons: matchsticks[8];\n\
next(state) = correct: matchsticks[8];\n\
next(state) = guess & state = calc_cons:{TRUE, FALSE};\n\
TRUE:matchsticks[8];\n\
esac;\n\
\n\n\
next(matchsticks[9]):=case\n\
next(state) = calc_cons: matchsticks[9];\n\
next(state) = correct: matchsticks[9];\n\
next(state) = guess & state = calc_cons:{TRUE, FALSE};\n\
TRUE:matchsticks[9];\n\
esac;\n\
\n\n\
next(matchsticks[10]):=case\n\
next(state) = calc_cons: matchsticks[10];\n\
next(state) = correct: matchsticks[10];\n\
next(state) = guess & state = calc_cons:{TRUE, FALSE};\n\
TRUE:matchsticks[10];\n\
esac;\n\
\n\n\
next(matchsticks[11]):=case\n\
next(state) = calc_cons: matchsticks[11];\n\
next(state) = correct: matchsticks[11];\n\
next(state) = guess & state = calc_cons:{TRUE, FALSE};\n\
TRUE:matchsticks[11];\n\
esac;\n\
\n\n\
next(matchsticks[12]):=case\n\
next(state) = calc_cons: matchsticks[12];\n\
next(state) = correct: matchsticks[12];\n\
next(state) = guess & state = calc_cons:{TRUE, FALSE};\n\
TRUE:matchsticks[12];\n\
esac;\n\
\n\n\
next(matchsticks[13]):=case\n\
next(state) = calc_cons: matchsticks[13];\n\
next(state) = correct: matchsticks[13];\n\
next(state) = guess & state = calc_cons:{TRUE, FALSE};\n\
TRUE:matchsticks[13];\n\
esac;\n\
\n\n\
next(matchsticks[14]):=case\n\
next(state) = calc_cons: matchsticks[14];\n\
next(state) = correct: matchsticks[14];\n\
next(state) = guess & state = calc_cons:{TRUE, FALSE};\n\
TRUE:matchsticks[14];\n\
esac;\n\
\n\n\
next(matchsticks[15]):=case\n\
next(state) = calc_cons: matchsticks[15];\n\
next(state) = correct: matchsticks[15];\n\
next(state) = guess & state = calc_cons:{TRUE, FALSE};\n\
TRUE:matchsticks[15];\n\
esac;\n\
\n\n\
next(matchsticks[16]):=case\n\
next(state) = calc_cons: matchsticks[16];\n\
next(state) = correct: matchsticks[16];\n\
next(state) = guess & state = calc_cons:{TRUE, FALSE};\n\
TRUE:matchsticks[16];\n\
esac;\n\
\n\n\
next(matchsticks[17]):=case\n\
next(state) = calc_cons: matchsticks[17];\n\
next(state) = correct: matchsticks[17];\n\
next(state) = guess & state = calc_cons:{TRUE, FALSE};\n\
TRUE:matchsticks[17];\n\
esac;\n\
\n\n\
next(matchsticks[18]):=case\n\
next(state) = calc_cons: matchsticks[18];\n\
next(state) = correct: matchsticks[18];\n\
next(state) = guess & state = calc_cons:{TRUE, FALSE};\n\
TRUE:matchsticks[18];\n\
esac;\n\
\n\n\
next(matchsticks[19]):=case\n\
next(state) = calc_cons: matchsticks[19];\n\
next(state) = correct: matchsticks[19];\n\
next(state) = guess & state = calc_cons:{TRUE, FALSE};\n\
TRUE:matchsticks[19];\n\
esac;\n\
\n\n\
next(matchsticks[20]):=case\n\
next(state) = calc_cons: matchsticks[20];\n\
next(state) = correct: matchsticks[20];\n\
next(state) = guess & state = calc_cons:{TRUE, FALSE};\n\
TRUE:matchsticks[20];\n\
esac;\n\
\n\n\
next(matchsticks[21]):=case\n\
next(state) = calc_cons: matchsticks[21];\n\
next(state) = correct: matchsticks[21];\n\
next(state) = guess & state = calc_cons:{TRUE, FALSE};\n\
TRUE:matchsticks[21];\n\
esac;\n\
\n\n\
next(matchsticks[22]):=case\n\
next(state) = calc_cons: matchsticks[22];\n\
next(state) = correct: matchsticks[22];\n\
next(state) = guess & state = calc_cons:{TRUE, FALSE};\n\
TRUE:matchsticks[22];\n\
esac;\n\
\n\n\
next(matchsticks[23]):=case\n\
next(state) = calc_cons: matchsticks[23];\n\
next(state) = correct: matchsticks[23];\n\
next(state) = guess & state = calc_cons:{TRUE, FALSE};\n\
TRUE:matchsticks[23];\n\
esac;\n\
\n\n\
next(xor_arr[0]):=case\n\
next(state)=calc_cons:(bool1[0])xor(matchsticks[0]);\n\
TRUE:xor_arr[0];\n\
esac;\n\
\n\n\
next(xor_arr[1]):=case\n\
next(state)=calc_cons:(bool1[1])xor(matchsticks[1]);\n\
TRUE:xor_arr[1];\n\
esac;\n\
\n\n\
next(xor_arr[2]):=case\n\
next(state)=calc_cons:(bool1[2])xor(matchsticks[2]);\n\
TRUE:xor_arr[2];\n\
esac;\n\
\n\n\
next(xor_arr[3]):=case\n\
next(state)=calc_cons:(bool1[3])xor(matchsticks[3]);\n\
TRUE:xor_arr[3];\n\
esac;\n\
\n\n\
next(xor_arr[4]):=case\n\
next(state)=calc_cons:(bool1[4])xor(matchsticks[4]);\n\
TRUE:xor_arr[4];\n\
esac;\n\
\n\n\
next(xor_arr[5]):=case\n\
next(state)=calc_cons:(bool1[5])xor(matchsticks[5]);\n\
TRUE:xor_arr[5];\n\
esac;\n\
\n\n\
next(xor_arr[6]):=case\n\
next(state)=calc_cons:(bool1[6])xor(matchsticks[6]);\n\
TRUE:xor_arr[6];\n\
esac;\n\
\n\n\
next(xor_arr[7]):=case\n\
next(state)=calc_cons:(bool1[7])xor(matchsticks[7]);\n\
TRUE:xor_arr[7];\n\
esac;\n\
\n\n\
next(xor_arr[8]):=case\n\
next(state)=calc_cons:(bool1[8])xor(matchsticks[8]);\n\
TRUE:xor_arr[8];\n\
esac;\n\
\n\n\
next(xor_arr[9]):=case\n\
next(state)=calc_cons:(bool1[9])xor(matchsticks[9]);\n\
TRUE:xor_arr[9];\n\
esac;\n\
\n\n\
next(xor_arr[10]):=case\n\
next(state)=calc_cons:(bool1[10])xor(matchsticks[10]);\n\
TRUE:xor_arr[10];\n\
esac;\n\
\n\n\
next(xor_arr[11]):=case\n\
next(state)=calc_cons:(bool1[11])xor(matchsticks[11]);\n\
TRUE:xor_arr[11];\n\
esac;\n\
\n\n\
next(xor_arr[12]):=case\n\
next(state)=calc_cons:(bool1[12])xor(matchsticks[12]);\n\
TRUE:xor_arr[12];\n\
esac;\n\
\n\n\
next(xor_arr[13]):=case\n\
next(state)=calc_cons:(bool1[13])xor(matchsticks[13]);\n\
TRUE:xor_arr[13];\n\
esac;\n\
\n\n\
next(xor_arr[14]):=case\n\
next(state)=calc_cons:(bool1[14])xor(matchsticks[14]);\n\
TRUE:xor_arr[14];\n\
esac;\n\
\n\n\
next(xor_arr[15]):=case\n\
next(state)=calc_cons:(bool1[15])xor(matchsticks[15]);\n\
TRUE:xor_arr[15];\n\
esac;\n\
\n\n\
next(xor_arr[16]):=case\n\
next(state)=calc_cons:(bool1[16])xor(matchsticks[16]);\n\
TRUE:xor_arr[16];\n\
esac;\n\
\n\n\
next(xor_arr[17]):=case\n\
next(state)=calc_cons:(bool1[17])xor(matchsticks[17]);\n\
TRUE:xor_arr[17];\n\
esac;\n\
\n\
next(xor_arr[18]):=case\n\
next(state)=calc_cons:(bool1[18])xor(matchsticks[18]);\n\
TRUE:xor_arr[18];\n\
esac;\n\
\n\
next(xor_arr[19]):=case\n\
next(state)=calc_cons:(bool1[19])xor(matchsticks[19]);\n\
TRUE:xor_arr[19];\n\
esac;\n\
\n\n\
next(xor_arr[20]):=case\n\
next(state)=calc_cons:(bool1[20])xor(matchsticks[20]);\n\
TRUE:xor_arr[20];\n\
esac;\n\
\n\n\
next(xor_arr[21]):=case\n\
next(state)=calc_cons:(bool1[21])xor(matchsticks[21]);\n\
TRUE:xor_arr[21];\n\
esac;\n\
\n\n\
next(xor_arr[22]):=case\n\
next(state)=calc_cons:(bool1[22])xor(matchsticks[22]);\n\
TRUE:xor_arr[22];\n\
esac;\n\
\n\n\
next(xor_arr[23]):=case\n\
next(state)=calc_cons:(bool1[23])xor(matchsticks[23]);\n\
TRUE:xor_arr[23];\n\
esac;\n\
\n\n\
next(sq_1_bool[0]):=case\n\
matchsticks[0] & matchsticks[4] & matchsticks[7] & matchsticks[3]: TRUE;\n\
TRUE: FALSE;\n\
esac;\n\
\n\n\
next(sq_1_bool[1]):=case\n\
matchsticks[1] & matchsticks[4] & matchsticks[5] & matchsticks[8]: TRUE;\n\
TRUE: FALSE;\n\
esac;\n\
\n\n\
next(sq_1_bool[2]):=case\n\
matchsticks[2] & matchsticks[5] & matchsticks[9] & matchsticks[6]: TRUE;\n\
TRUE: FALSE;\n\
esac;\n\
\n\n\
next(sq_1_bool[3]):=case\n\
matchsticks[7] & matchsticks[10] & matchsticks[11] & matchsticks[14]: TRUE;\n\
TRUE: FALSE;\n\
esac;\n\
\n\n\
next(sq_1_bool[4]):=case\n\
matchsticks[8] & matchsticks[11] & matchsticks[15] & matchsticks[12]: TRUE;\n\
TRUE: FALSE;\n\
esac;\n\
\n\n\
next(sq_1_bool[5]):=case\n\
matchsticks[16] & matchsticks[13] & matchsticks[12] & matchsticks[9]: TRUE;\n\
TRUE: FALSE;\n\
esac;\n\
\n\n\
next(sq_1_bool[6]):=case\n\
matchsticks[14] & matchsticks[17] & matchsticks[18] & matchsticks[21]: TRUE;\n\
TRUE: FALSE;\n\
esac;\n\
\n\n\
next(sq_1_bool[7]):=case\n\
matchsticks[15] & matchsticks[18] & matchsticks[19] & matchsticks[22]: TRUE;\n\
TRUE: FALSE;\n\
esac;\n\
\n\n\
next(sq_1_bool[8]):=case\n\
matchsticks[16] & matchsticks[19] & matchsticks[20] & matchsticks[23]: TRUE;\n\
TRUE: FALSE;\n\
esac;\n\
\n\
next(sq_2_bool[0]):=case\n\
matchsticks[0] & matchsticks[1] & matchsticks[5] & matchsticks[12] & matchsticks[15] & matchsticks[14] & matchsticks[10] & matchsticks[3]: TRUE;\n\
TRUE: FALSE;\n\
esac;\n\
\n\n\
next(sq_2_bool[1]):=case\n\
matchsticks[1] & matchsticks[2] & matchsticks[6] & matchsticks[13] & matchsticks[16] & matchsticks[15] & matchsticks[11] & matchsticks[4]: TRUE;\n\
TRUE: FALSE;\n\
esac;\n\
\n\
next(sq_2_bool[2]):=case\n\
matchsticks[7] & matchsticks[8] & matchsticks[12] & matchsticks[19] & matchsticks[22] & matchsticks[21] & matchsticks[17] & matchsticks[10]: TRUE;\n\
TRUE: FALSE;\n\
esac;\n\
\n\n\
next(sq_2_bool[3]):=case\n\
matchsticks[8] & matchsticks[9] & matchsticks[13] & matchsticks[20] & matchsticks[23] & matchsticks[22] & matchsticks[18] & matchsticks[11]: TRUE;\n\
TRUE: FALSE;\n\
esac;\n\
\n\n\
next(sq_3_bool):=case\n\
matchsticks[0] & matchsticks[1] & matchsticks[2] & matchsticks[6] & matchsticks[13] & matchsticks[20] & matchsticks[23] & matchsticks[22] & matchsticks[21] & matchsticks[17] & matchsticks[10] & matchsticks[3]: TRUE;\n\
TRUE: FALSE;\n\
esac;\n\
\n\n\
next(num_move):=case\n\
state = guess: count(next(xor_arr[0])) + count(next(xor_arr[1])) + count(next(xor_arr[2])) + count(next(xor_arr[3])) + count(next(xor_arr[4])) + count(next(xor_arr[5])) + count(next(xor_arr[6])) + count(next(xor_arr[7])) + count(next(xor_arr[8])) + count(next(xor_arr[9])) + count(next(xor_arr[10])) + count(next(xor_arr[11])) + count(next(xor_arr[12])) + count(next(xor_arr[13])) + count(next(xor_arr[14])) + count(next(xor_arr[15])) + count(next(xor_arr[16])) + count(next(xor_arr[17])) + count(next(xor_arr[18])) + count(next(xor_arr[19])) + count(next(xor_arr[20])) + count(next(xor_arr[21])) + count(next(xor_arr[22])) + count(next(xor_arr[23]));\n\
TRUE: num_move;\n\
esac;\n\
\n\n\
next(num_match_end):= count(matchsticks[0]) +  count(matchsticks[1]) + count(matchsticks[2]) + count(matchsticks[3]) + count(matchsticks[4]) + count(matchsticks[5]) + count(matchsticks[6]) + count(matchsticks[7]) + count(matchsticks[8]) + count(matchsticks[9]) + count(matchsticks[10]) + count(matchsticks[11]) + count(matchsticks[12]) + count(matchsticks[13]) + count(matchsticks[14]) + count(matchsticks[15]) + count(matchsticks[16]) + count(matchsticks[17]) + count(matchsticks[18]) + count(matchsticks[19]) + count(matchsticks[20]) + count(matchsticks[21]) + count(matchsticks[22]) + count(matchsticks[23]);\n\
\n\
next(free):=case\n\
state = check_free & match_index = 0 & matchsticks[0]: !(sq_1_bool[0] | sq_2_bool[0] | sq_3_bool);\n\
state = check_free & match_index = 0 & !matchsticks[0]: FALSE;\n\
state = check_free & match_index = 1 & matchsticks[1]: !(sq_1_bool[1] | sq_2_bool[0] | sq_2_bool[1] | sq_3_bool) | free;\n\
state = check_free & match_index = 1 & !matchsticks[1]: free;\n\
state = check_free & match_index = 2 & matchsticks[2]: !(sq_1_bool[2] | sq_2_bool[1] | sq_3_bool) | free;\n\
state = check_free & match_index = 2 & !matchsticks[2]: free;\n\
state = check_free & match_index = 3 & matchsticks[3]: !(sq_1_bool[0] | sq_2_bool[0] | sq_3_bool) | free;\n\
state = check_free & match_index = 3 & !matchsticks[3]: free;\n\
state = check_free & match_index = 4 & matchsticks[4]: !(sq_1_bool[0] | sq_1_bool[1] | sq_2_bool[1]) | free;\n\
state = check_free & match_index = 4 & !matchsticks[4]: free;\n\
state = check_free & match_index = 5 & matchsticks[5]: !(sq_1_bool[1] | sq_1_bool[2] | sq_2_bool[0]) | free;\n\
state = check_free & match_index = 5 & !matchsticks[5]: free;\n\
state = check_free & match_index = 6 & matchsticks[6]: !(sq_1_bool[2] | sq_2_bool[1] | sq_3_bool) | free;\n\
state = check_free & match_index = 6 & !matchsticks[6]: free;\n\
state = check_free & match_index = 7 & matchsticks[7]: !(sq_1_bool[0] | sq_1_bool[3] | sq_2_bool[2]) | free;\n\
state = check_free & match_index = 7 & !matchsticks[7]: free;\n\
state = check_free & match_index = 8 & matchsticks[8]: !(sq_1_bool[1] | sq_1_bool[4] | sq_2_bool[2] | sq_2_bool[3]) | free;\n\
state = check_free & match_index = 8 & !matchsticks[8]: free;\n\
state = check_free & match_index = 9 & matchsticks[9]: !(sq_1_bool[2] | sq_1_bool[5] | sq_2_bool[3]) | free;\n\
state = check_free & match_index = 9 & !matchsticks[9]: free;\n\
state = check_free & match_index = 10 & matchsticks[10]: !(sq_1_bool[3] | sq_2_bool[2] | sq_2_bool[0] | sq_3_bool) | free;\n\
state = check_free & match_index = 10 & !matchsticks[10]: free;\n\
state = check_free & match_index = 11 & matchsticks[11]: !(sq_1_bool[3] | sq_1_bool[4] | sq_2_bool[3]) | free;\n\
state = check_free & match_index = 11 & !matchsticks[11]: free;\n\
state = check_free & match_index = 12 & matchsticks[12]: !(sq_1_bool[5] | sq_1_bool[4] | sq_2_bool[2]) | free;\n\
state = check_free & match_index = 12 & !matchsticks[12]: free;\n\
state = check_free & match_index = 13 & matchsticks[13]: !(sq_1_bool[5] | sq_2_bool[3] | sq_3_bool) | free;\n\
state = check_free & match_index = 13 & !matchsticks[13]: free;\n\
state = check_free & match_index = 14 & matchsticks[14]: !(sq_1_bool[3] | sq_1_bool[6] | sq_2_bool[0]) | free;\n\
state = check_free & match_index = 14 & !matchsticks[14]: free;\n\
state = check_free & match_index = 15 & matchsticks[15]: !(sq_1_bool[4] | sq_1_bool[7] | sq_2_bool[0]) | free;\n\
state = check_free & match_index = 15 & !matchsticks[15]: free;\n\
state = check_free & match_index = 16 & matchsticks[16]: !(sq_1_bool[5] | sq_1_bool[8] | sq_2_bool[1]) | free;\n\
state = check_free & match_index = 16 & !matchsticks[16]: free;\n\
state = check_free & match_index = 17 & matchsticks[17]: !(sq_1_bool[6] | sq_2_bool[2] | sq_3_bool) | free;\n\
state = check_free & match_index = 17 & !matchsticks[17]: free;\n\
state = check_free & match_index = 18 & matchsticks[18]: !(sq_1_bool[6] | sq_1_bool[7] | sq_2_bool[3]) | free;\n\
state = check_free & match_index = 18 & !matchsticks[18]: free;\n\
state = check_free & match_index = 19 & matchsticks[19]: !(sq_1_bool[7] | sq_1_bool[8] | sq_2_bool[2]) | free;\n\
state = check_free & match_index = 19 & !matchsticks[19]: free;\n\
state = check_free & match_index = 20 & matchsticks[20]: !(sq_1_bool[8] | sq_2_bool[3] | sq_3_bool) | free;\n\
state = check_free & match_index = 20 & !matchsticks[20]: free;\n\
state = check_free & match_index = 21 & matchsticks[21]: !(sq_1_bool[6] | sq_2_bool[2] | sq_3_bool) | free;\n\
state = check_free & match_index = 21 & !matchsticks[21]: free;\n\
state = check_free & match_index = 22 & matchsticks[22]: !(sq_1_bool[7] | sq_2_bool[2] | sq_2_bool[3] | sq_3_bool) | free;\n\
state = check_free & match_index = 22 & !matchsticks[22]: free;\n\
state = check_free & match_index = 23 & !matchsticks[23]: free;\n\
state = check_free & match_index = 23 & matchsticks[23]: !(sq_1_bool[8] | sq_2_bool[3] | sq_3_bool) | free;\n\
state = check_free & match_index = 24: free;\n\
TRUE: FALSE;\n\
esac;\n\
\n\n\
next(num_squares_1_end):=case\n\
!(finished_count) & state = calc_cons & sq_1_bool[last_in_1] & last_in_1 < 9: (num_squares_1_end+1)mod(10) ;\n\
state = guess: 0;\n\
TRUE: num_squares_1_end;\n\
esac;\n\
\n\n\
next(num_squares_2_end):=case\n\
!(finished_count) & state = calc_cons & sq_2_bool[last_in_2] & last_in_2 < 4: (num_squares_2_end+1)mod(5) ;\n\
state = guess: 0;\n\
TRUE: num_squares_2_end;\n\
esac;\n\
\n\n\
next(num_squares_3_end):=case\n\
!(finished_count) & state = calc_cons & sq_3_bool & last_in_3 < 1: (num_squares_3_end+1)mod(2) ;\n\
state = guess: 0;\n\
TRUE: num_squares_3_end;\n\
esac;\n\
\n\n"

# squares' matchstick indices.

list_square_1 = [[0, 3, 4, 7], [1, 4, 5, 8], [5, 2, 6, 9], [10, 7, 11, 14], [11, 8, 12, 15], [12, 13, 16, 9],
                 [17, 14, 18, 21], [18, 15, 19, 22],
                 [19, 20, 16, 23]]
list_square_2 = [[0, 3, 10, 14, 15, 12, 5, 1], [1, 2, 6, 13, 16, 15, 11, 4], [7, 8, 12, 19, 22, 21, 17, 10],
                 [8, 9, 13, 20, 22, 23, 18, 11]]
list_square_3 = [0, 1, 2, 6, 13, 20, 23, 22, 21, 17, 10, 3]

# input arrays initialization

init_sq1 = [True, False, False, True, True, False, False, True, True]
init_sq2 = [False, False, False, False]

bool1 = [True, False, False, True, True, False, False, True, True, False, True, True, True, False, True, True, True,
         False, True, True, True
    , False, True, True]


def transform_match_to_sq_arrays(bool2):
    num_sqr_beg, num_sqr_1_beg, num_sqr_2_beg, num_sqr_3_beg = (0, 0, 0, 0)
    sq_1_bool = [True if bool2[list_square_1[i][0]] and bool2[list_square_1[i][1]] and bool2[list_square_1[i][2]] and
                         bool2[list_square_1[i][3]] else False for i in range(0, 9)]

    sq_2_bool = [True if bool2[list_square_2[i][0]] and bool2[list_square_2[i][1]] and bool2[list_square_2[i][2]] and
                         bool2[list_square_2[i][3]] and bool2[list_square_2[i][4]] and bool2[list_square_2[i][5]] and
                         bool2[list_square_2[i][6]] and bool2[list_square_2[i][7]] else False for i in range(0, 4)]

    sq_3_bool = True
    for k in range(0, 12):
        sq_3_bool = sq_3_bool and bool2[list_square_3[k]]

    if sq_3_bool:
        num_sqr_3_beg = 1

    num_sqr_1_beg = sum(sq_1_bool)
    num_sqr_2_beg = sum(sq_2_bool)
    num_sqr_beg = num_sqr_1_beg + num_sqr_2_beg + num_sqr_3_beg

    return num_sqr_beg, num_sqr_1_beg, num_sqr_2_beg, num_sqr_3_beg, sq_1_bool, sq_2_bool, sq_3_bool


def solve_rid(i, num_allowed):
    """
        This function gets i - file index and num_allowed - the number of matchsticks to move
        It generates a random input for the squares riddle
        It checks if the input is valid if it is, generates an input - model file and runs it
    """

    # generating the input
    num_squares_1_beg = random.randint(0, 9)
    num_squares_3_beg = random.randint(0, 1)
    num_squares_2_beg = random.randint(0, 4)
    num_squares_beginning = num_squares_1_beg + num_squares_3_beg + num_squares_2_beg
    num_squares_end = random.randint(0, 14)

    sq_1_bool = [False] * 9
    sq_2_bool = [False] * 4
    matchsticks = [False] * 24
    for k in range(0, num_squares_1_beg):
        index = random.randint(0, 8)
        sq_1_bool[index] = True
        for item in list_square_1[index]:
            matchsticks[item] = True
    for m in range(0, num_squares_2_beg):
        index2 = random.randint(0, 3)
        sq_2_bool[index2] = True
        for item2 in list_square_2[index2]:
            matchsticks[item2] = True
    if num_squares_3_beg == 0:
        sq_3_bool = False
    else:
        sq_3_bool = True
        for item3 in list_square_3:
            matchsticks[item3] = True

    flag_solved = 0
    run_time = -1

    # checking if the input is valid, if it is - generating an input - model file and running it
    times = read_sq_riddle(i, num_squares_beginning, num_squares_1_beg, num_squares_2_beg, num_squares_3_beg,
                           matchsticks, sq_1_bool, sq_2_bool, sq_3_bool, num_squares_end, num_allowed)

    if times != -1:  # valid input
        flag_solved, run_time = find_solution(i)
    return times, flag_solved, run_time


def solve_rid_input(i, num_squares_beginning, num_squares_1_beg, num_squares_2_beg, num_squares_3_beg, matchsticks,
                    sq_1_bool, sq_2_bool, sq_3_bool, num_squares_end, num_allowed):
    """
    This function gets:
    :param i: a starting index for input/output files
    :param num_squares_beginning: the initial total number of squares
    :param num_squares_1_beg: the initial number of 1-match-length squares
    :param num_squares_2_beg: the initial number of 2-match-length squares
    :param num_squares_3_beg: the initial number of 3-match-length squares
    :param num_squares_end: the final (desired) total number of squares
    :param num_allowed: the number of matchsticks to move (in order to create the desired number of squares)
    :param matchsticks: a Boolean array representing the matchsticks configuration.
    The matchsticks are indexed: 0-23.
    True - the matchstick exists (appears on the screen), False- otherwise.

    :param sq_1_bool: a Boolean array which represents the 1 - match - length squares that will appear
    on the screen as input.
    :param sq_2_bool: a Boolean array which represents the 2 - match - length squares that will appear
    on the screen as input.
    :param sq_3_bool: Boolean variable which represent the 3 - match - length square that will appear / will not appear
    on the screen as input.
    True - the square exists, False - otherwise.

    It solves the riddle

    :return: flag_solved - 1: no solution, 2: solved
    run_time - execution time
    times - if the input is invalid: -1
    """
    flag_solved = 0
    run_time = -1
    times = read_sq_riddle(i, num_squares_beginning, num_squares_1_beg, num_squares_2_beg, num_squares_3_beg,
                           matchsticks, sq_1_bool, sq_2_bool, sq_3_bool, num_squares_end, num_allowed)
    if times != -1:
        flag_solved, run_time = find_solution(i)
    return times, flag_solved, run_time


def solve_rid_input_gen(i):
    flag_solved = 0
    run_time = -1
    matchsticks, bool1, num_sqr_end, num_allowed = ([], [], 0, 0)
    times = write_gen_model(i)
    if times != -1:
        flag_solved, run_time = find_solution(i)
        matchsticks, bool1, num_sqr_end, num_allowed = find_info(i, False, -1, -1, True)
    return times, flag_solved, run_time, matchsticks, bool1, num_sqr_end, num_allowed


def solve_rid_opt_input(j, num_squares_beginning, num_squares_1_beg, num_squares_2_beg, num_squares_3_beg, matchsticks,
                        sq_1_bool, sq_2_bool, sq_3_bool, num_squares_end=-1, num_allowed=-1):
    """
    This function gets:
    :param j: a starting index for input/output files
    :param num_squares_beginning: the initial total number of squares
    :param num_squares_1_beg: the initial number of 1-match-length squares
    :param num_squares_2_beg: the initial number of 2-match-length squares
    :param num_squares_3_beg: the initial number of 3-match-length squares
    :param num_squares_end: the final (desired) total number of squares
    :param num_allowed: the number of matchsticks to move (in order to create the desired number of squares)
    :param matchsticks: a Boolean array representing the matchsticks configuration.
    The matchsticks are indexed: 0-23.
    True - the matchstick exists (appears on the screen), False- otherwise.

    :param sq_1_bool: a Boolean array which represents the 1 - match - length squares that will appear
    on the screen as input.
    :param sq_2_bool: a Boolean array which represents the 2 - match - length squares that will appear
    on the screen as input.
    :param sq_3_bool: Boolean variable which represent the 3 - match - length square that will appear / will not appear
    on the screen as input.
    True - the square exists, False - otherwise.

    It solves the riddle

    :return: flag_solved - 1: no solution, 2: solved
    run_time - execution time
    times - if the input is invalid: -1
    """
    flag_solved = 0
    flag_solved1 = 0  # draft for computations of the minimal num_allowed
    run_time = -1
    total = 0
    times = 0

    matchsticks2, current_min = (matchsticks, 0)
    lower, upper, mid_or_last_sol = limits(num_squares_beginning, num_squares_1_beg, num_squares_2_beg,
                                           num_squares_3_beg, matchsticks, sq_1_bool, sq_2_bool, sq_3_bool,
                                           num_squares_end, num_allowed)

    if (lower, upper, mid_or_last_sol) != (None, None, None):
        flag_solved = 1

    while (lower, upper, mid_or_last_sol) != (None, None, None):
        times = read_sq_riddle(j, num_squares_beginning, num_squares_1_beg, num_squares_2_beg, num_squares_3_beg,
                               matchsticks, sq_1_bool, sq_2_bool, sq_3_bool, num_squares_end, num_allowed, lower, upper)
        flag_solved1, run_time = find_solution(j)
        total += run_time
        if flag_solved1 == 2:
            flag_solved = 2
            matchsticks2, current_min = find_info(j, True, num_allowed, num_squares_end)
        lower, upper, mid_or_last_sol = limits(num_squares_beginning, num_squares_1_beg, num_squares_2_beg,
                                               num_squares_3_beg,
                                               matchsticks,
                                               sq_1_bool, sq_2_bool, sq_3_bool, num_squares_end, num_allowed,
                                               mid_or_last_sol,
                                               lower, upper, current_min, flag_solved1)
    return times, flag_solved, run_time, matchsticks2, current_min


def read_sq_riddle(i, num_squares_beginning, num_squares_1_beg, num_squares_2_beg, num_squares_3_beg, matchsticks,
                   sq_1_bool, sq_2_bool, sq_3_bool, num_squares_end=-1, num_allowed=-1, lower=-1, upper=-1):
    """
       this function: gets a squares riddle
       encodes the riddle in NuSMV and runs NuSMV to find a solution
       writes the NuSMV output in a file
       """
    if num_allowed != -1 and num_squares_end != -1:
        if check_valid(num_squares_beginning, num_squares_1_beg, num_squares_2_beg, num_squares_3_beg, matchsticks,
                       sq_1_bool,
                       sq_2_bool, sq_3_bool, num_squares_end,
                       num_allowed):
            return write_model(i, num_squares_beginning, num_squares_1_beg, num_squares_2_beg, num_squares_3_beg,
                               matchsticks,
                               sq_1_bool, sq_2_bool, sq_3_bool, num_squares_end, num_allowed)
        else:
            return -1

    else:
        return write_model(i, num_squares_beginning, num_squares_1_beg, num_squares_2_beg, num_squares_3_beg,
                           matchsticks,
                           sq_1_bool, sq_2_bool, sq_3_bool, num_squares_end, num_allowed, lower, upper)


def get_list_sq():
    return list_square_1, list_square_2, list_square_3


def check_valid(num_squares_beginning, num_squares_1_beg, num_squares_2_beg, num_squares_3_beg, matchsticks, sq_1_bool,
                sq_2_bool, sq_3_bool, num_squares_end=-1,
                num_allowed=-1, opt=False, opt_parameter=''):
    """
    This function gets the input parameters and determines their validity.
    """
    if not opt:
        if num_squares_end > 14 or num_squares_end <= 0:
            return False

        if num_allowed > 24 or num_allowed < 0 or num_allowed > sum(matchsticks):
            return False

    else:
        if opt_parameter == 'num_allowed':
            if num_squares_end > 14 or num_squares_end <= 0:
                return False

            if opt_parameter == 'num_squares_end':
                if num_allowed > 24 or num_allowed < 0 or num_allowed > sum(matchsticks):
                    return False

    if num_squares_beginning > 14 or num_squares_beginning <= 0:
        return False
    if num_squares_beginning != num_squares_1_beg + num_squares_2_beg + num_squares_3_beg:
        return False
    if sum(sq_1_bool) != num_squares_1_beg:
        return False
    if sum(sq_2_bool) != num_squares_2_beg:
        return False
    if sum([sq_3_bool]) != num_squares_3_beg:
        return False
    if sum(sq_2_bool) + sum(sq_1_bool) + sum([sq_3_bool]) != num_squares_beginning:
        return False

    # checks that all the squares from the boolean squares arrays appear in the matchsticks configuration
    for i in range(0, 9):
        if sq_1_bool[i] and (not matchsticks[list_square_1[i][0]] or not matchsticks[list_square_1[i][1]] or
                             not matchsticks[list_square_1[i][2]] or not matchsticks[list_square_1[i][3]]):
            return False
        if not sq_1_bool[i] and (matchsticks[list_square_1[i][0]] and matchsticks[list_square_1[i][1]] and
                                 matchsticks[list_square_1[i][2]] and matchsticks[list_square_1[i][3]]):
            return False

    for k in range(0, 4):
        if sq_2_bool[k]:
            for m in range(0, 8):
                if not matchsticks[list_square_2[k][m]]:
                    return False
        else:
            for m in range(0, 8):
                if not matchsticks[list_square_2[k][m]]:
                    break
                if m == 7 and matchsticks[list_square_2[k][m]]:
                    return False

    if sq_3_bool:
        for t in range(0, 12):
            if not matchsticks[list_square_3[t]]:
                return False
    else:
        for t in range(0, 12):
            if not matchsticks[list_square_3[t]]:
                break
            if t == 11 and matchsticks[list_square_3[t]]:
                return False

    # checks that there are no free matchsticks which do not belong to any square
    for s in range(0, 24):
        if matchsticks[s] and not is_in_sq1(s, sq_1_bool) and not is_in_sq2(s, sq_2_bool) and not is_in_sq3(s,
                                                                                                            sq_3_bool):
            return False

    return True


def is_in_sq1(s, sq_1_bool):
    """
      This function gets the list of existing 1-match-length squares and a matchstick's index - s
      It checks that the matchstick indexed s belongs to a 1-match-length square
    """
    for k in range(0, 9):
        if sq_1_bool[k] and s in list_square_1[k]:
            return True
    return False


def is_in_sq2(s, sq_2_bool):
    """
     This function gets the list of existing 2-match-length squares and a matchstick's index - s
     It checks that the matchstick indexed s belongs to a 2-match-length square
     """
    for k in range(0, 4):
        if sq_2_bool[k] and s in list_square_2[k]:
            return True
    return False


def is_in_sq3(s, sq_3_bool):
    """
     This function gets the list of existing 3-match-length squares and a matchstick's index - s
     It checks that the matchstick indexed s belongs to a 3-match-length square
     """
    if sq_3_bool and s in list_square_3:
        return True
    return False


def write_model(j, num_squares_beginning, num_squares_1_beg, num_squares_2_beg, num_squares_3_beg,
                matchsticks,
                sq_1_bool, sq_2_bool, sq_3_bool, num_squares_end=-1, num_allowed=-1, lower=-1, upper=-1):
    """
       This funcion gets the riddle's input parameters and writes a model file indexed j for the riddle
       It runs the model file in NuSMV and prints the output to the output file indexed j
    """
    text_assign2 = text_assign_2
    if num_allowed != -1 and num_squares_end != -1:
        text_assign2 += "LTLSPEC\n \
                G !(state = correct)"
    elif num_allowed == -1:
        text_assign2 += "LTLSPEC\n \
                G !(state = correct & num_allowed >= """ + str(lower) + """ & num_allowed <= """ + str(upper) + """)"""
    elif num_squares_end == -1:
        text_assign2 += "LTLSPEC\n \
                        G !(state = correct & num_squares_end >= """ + str(lower) + """ & num_squares_end <= """ + str(
            upper) + """)"""
    matchsticks_str = ""
    sq_1_bool_str = ""
    sq_2_bool_str = ""

    for i in range(0, 24):
        matchsticks_str = matchsticks_str + "," + str(matchsticks[i]).upper()

    matchsticks_str = matchsticks_str[1:]

    for i in range(0, 9):
        sq_1_bool_str = sq_1_bool_str + "," + str(sq_1_bool[i]).upper()

    sq_1_bool_str = sq_1_bool_str[1:]

    for i in range(0, 4):
        sq_2_bool_str = sq_2_bool_str + "," + str(sq_2_bool[i]).upper()

    sq_2_bool_str = sq_2_bool_str[1:]

    text_define = "DEFINE\n\
    list_square_1:=[[0,3,4,7],[1,4,5,8],[5,2,6,9],[10,7,11,14],[11,8,12,15],[12,13,16,9],[17,14,18,21],[18,15,19,22],[19,20,16,23]];\n\
    list_square_2:=[[0,3,10,14,15,12,5,1],[1,2,6,13,16,15,11,4],[7,8,12,19,22,21,17,10],[8,9,13,20,22,23,18,11]];\n\
    list_square_3:=[0,1,2,6,13,20,23,22,21,17,10,3];\n\
    init_sq1:=[" + sq_1_bool_str + "];\n\
    init_sq2:=[" + sq_2_bool_str + "];\n\
    bool1:=[" + matchsticks_str + "];\n\
    falsarr:=[FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE];\n"

    text_assign = "ASSIGN\n\
    /--user input--/\n\
    init(num_squares_beginning):=" + str(num_squares_beginning) + ";\n\
    init(num_squares_1_beg):=" + str(num_squares_1_beg) + ";\n\
    init(num_squares_2_beg):=" + str(num_squares_2_beg) + ";\n\
    init(num_squares_3_beg):=" + str(num_squares_3_beg) + ";\n\
    init(matchsticks):=bool1;\n\
    init(sq_1_bool):=init_sq1;\n\
    init(sq_2_bool):=init_sq2;\n\
    init(sq_3_bool):=" + str(sq_3_bool).upper() + ";\n"
    if num_allowed != -1:
        text_assign += "init(num_allowed) := " + str(num_allowed) + ";\n"
    if num_squares_end != -1:
        text_assign += "init(num_squares_end):=" + str(num_squares_end) + ";\n"

    os.chdir(r'C:\Users\liatw\OneDrive\Desktop\NuSMV-2.6.0-win64\bin')  # change to your NuSMV bin directory
    open('sq' + str(j) + ".smv", 'w').close()
    code = '''j = ''' + str(j) + '''
text_var = """''' + text_var + '''"""
text_define = """''' + text_define + '''"""
text_assign = """''' + text_assign + '''"""
text_assign_2 = """''' + text_assign2 + '''"""
f = open('sq' + str(j) + '.smv', 'a')
print >> f, text_var
print >> f, text_define
print >> f, text_assign
print >> f, text_assign_2
f.close()'''
    build_time = timeit.timeit(code, number=1)
    run_model('sq' + str(j) + '.smv', j)
    return build_time


def write_gen_model(j):
    text = """MODULE main
        /--state variables--/
        VAR
        num_squares_beginning:0..14;
        num_squares_end:0..14;
        num_allowed:0..24;
        num_move:0..24;
        
        
        num_squares_1_beg:0..9;
        num_squares_1_end:0..9;
        last_in_1:0..9;
        
        
        num_squares_2_beg:0..4;
        num_squares_2_end:0..4;
        last_in_2:0..4;
        
        
        num_squares_3_beg:0..1;
        num_squares_3_end:0..1;
        last_in_3:{0,1};
        
        
        matchsticks:array 0..23 of boolean;
        match_index: 0..24;
        xor_arr:array 0..23 of boolean;
        state:{initial, calc_cons, correct, guess, check_free};
        free: boolean;
        fin_free: boolean;
        finished_count: boolean;
        sq_1_bool: array 0..8 of boolean;
        sq_2_bool: array 0..3 of boolean;
        sq_3_bool: boolean;
        num_match_beg: 0..24;
        num_match_end:0..24;
        init_sq1:array 0..8 of boolean;
        init_sq2:array 0..3 of boolean;
		init_sq3:boolean;
        bool1:array 0..23 of boolean;
            
DEFINE
            list_square_1:=[[0,3,4,7],[1,4,5,8],[5,2,6,9],[10,7,11,14],[11,8,12,15],[12,13,16,9],[17,14,18,21],[18,15,19,22],[19,20,16,23]];
            list_square_2:=[[0,3,10,14,15,12,5,1],[1,2,6,13,16,15,11,4],[7,8,12,19,22,21,17,10],[8,9,13,20,22,23,18,11]];
            list_square_3:=[0,1,2,6,13,20,23,22,21,17,10,3];
            falsarr:=[FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE];
        
ASSIGN
            /--user input--/
            init(num_squares_beginning):=num_squares_1_beg  + num_squares_2_beg + num_squares_3_beg;
			
            init(num_squares_1_beg):= count(init_sq1[0]) + count(init_sq1[1]) + count(init_sq1[2]) + count(init_sq1[3]) + count(init_sq1[4]) + count(init_sq1[5]) + count(init_sq1[6]) + count(init_sq1[7]) + count(init_sq1[8]);
			
			init(num_squares_2_beg):= count(init_sq2[0]) + count(init_sq2[1]) + count(init_sq2[2]) + count(init_sq2[3]);
			
            init(num_squares_3_beg):=count(sq_3_bool);
			
            init(matchsticks):=bool1;
			init(sq_1_bool[0]):=matchsticks[0] & matchsticks[3] & matchsticks[4] & matchsticks[7];
			init(sq_1_bool[1]):=matchsticks[1] & matchsticks[4] & matchsticks[5] & matchsticks[8];
			init(sq_1_bool[2]):=matchsticks[2] & matchsticks[5] & matchsticks[9] & matchsticks[6];
			init(sq_1_bool[3]):=matchsticks[7] & matchsticks[10] & matchsticks[11] & matchsticks[14];
			init(sq_1_bool[4]):=matchsticks[8] & matchsticks[11] & matchsticks[15] & matchsticks[12];
			init(sq_1_bool[5]):=matchsticks[16] & matchsticks[13] & matchsticks[12] & matchsticks[9];
			init(sq_1_bool[6]):=matchsticks[14] & matchsticks[17] & matchsticks[18] & matchsticks[21];
			init(sq_1_bool[7]):=matchsticks[15] & matchsticks[18] & matchsticks[19] & matchsticks[22];
			init(sq_1_bool[8]):=matchsticks[16] & matchsticks[19] & matchsticks[20] & matchsticks[23];
			
			init(init_sq1):=sq_1_bool;
			init(init_sq2):=sq_2_bool;
			init(init_sq3):=sq_3_bool;
			
			init(sq_2_bool[0]):=matchsticks[0] & matchsticks[1] & matchsticks[5] & matchsticks[12] & matchsticks[15] & matchsticks[14] & matchsticks[10] & matchsticks[3];
			init(sq_2_bool[1]):= matchsticks[1] & matchsticks[2] & matchsticks[6] & matchsticks[13] & matchsticks[16] & matchsticks[15] & matchsticks[11] & matchsticks[4];
			init(sq_2_bool[2]):=matchsticks[7] & matchsticks[8] & matchsticks[12] & matchsticks[19] & matchsticks[22] & matchsticks[21] & matchsticks[17] & matchsticks[10];
			init(sq_2_bool[3]):=matchsticks[8] & matchsticks[9] & matchsticks[13] & matchsticks[20] & matchsticks[23] & matchsticks[22] & matchsticks[18] & matchsticks[11];
			init(sq_3_bool):=matchsticks[0] & matchsticks[1] & matchsticks[2] & matchsticks[6] & matchsticks[13] & matchsticks[20] & matchsticks[23] & matchsticks[22] & matchsticks[21] & matchsticks[17] & matchsticks[10] & matchsticks[3];
			
        
        
init(num_squares_1_end):=0;
        init(num_squares_2_end):=0;
        init(num_squares_3_end):=0;
        init(xor_arr):=falsarr;
        
		init(free):=(matchsticks[0] & !(sq_1_bool[0] | sq_2_bool[0] | sq_3_bool))|(matchsticks[1] & !(sq_1_bool[1] | sq_2_bool[0] | sq_2_bool[1] | sq_3_bool))|(matchsticks[2] & !(sq_1_bool[2] | sq_2_bool[1] | sq_3_bool))|(matchsticks[3] & !(sq_1_bool[0] | sq_2_bool[0] | sq_3_bool))|(matchsticks[4] & !(sq_1_bool[0] | sq_1_bool[1] | sq_2_bool[1]))|(matchsticks[5] & !(sq_1_bool[1] | sq_1_bool[2] | sq_2_bool[0]))|(matchsticks[6] & !(sq_1_bool[2] | sq_2_bool[1] | sq_3_bool))|(matchsticks[7] & !(sq_1_bool[0] | sq_1_bool[3] | sq_2_bool[2]) )|(matchsticks[8] & !(sq_1_bool[1] | sq_1_bool[4] | sq_2_bool[2] | sq_2_bool[3]))|(matchsticks[9] & !(sq_1_bool[2] | sq_1_bool[5] | sq_2_bool[3]) )|(matchsticks[10] & !(sq_1_bool[3] | sq_2_bool[2] | sq_2_bool[0] | sq_3_bool))|(matchsticks[11] & !(sq_1_bool[3] | sq_1_bool[4] | sq_2_bool[3]))|(matchsticks[12] & !(sq_1_bool[5] | sq_1_bool[4] | sq_2_bool[2]))|(matchsticks[13] & !(sq_1_bool[5] | sq_2_bool[3] | sq_3_bool))|(matchsticks[14] & !(sq_1_bool[3] | sq_1_bool[6] | sq_2_bool[0]))|(matchsticks[15] &  !(sq_1_bool[4] | sq_1_bool[7] | sq_2_bool[0]) )|(matchsticks[16] &  !(sq_1_bool[5] | sq_1_bool[8] | sq_2_bool[1]))|(matchsticks[17] & !(sq_1_bool[6] | sq_2_bool[2] | sq_3_bool))|(matchsticks[18] & !(sq_1_bool[6] | sq_1_bool[7] | sq_2_bool[3]) )|(matchsticks[19] & !(sq_1_bool[7] | sq_1_bool[8] | sq_2_bool[2]))|(matchsticks[20] & !(sq_1_bool[8] | sq_2_bool[3] | sq_3_bool))|(matchsticks[21] &  !(sq_1_bool[6] | sq_2_bool[2] | sq_3_bool))|(matchsticks[22] & !(sq_1_bool[7] | sq_2_bool[2] | sq_2_bool[3] | sq_3_bool))|(matchsticks[23] & !(sq_1_bool[8] | sq_2_bool[3] | sq_3_bool));
		
        init(fin_free):=FALSE;
        init(last_in_1):=0;
        init(last_in_2):=0;
        init(last_in_3):=0;
        init(num_move):=0;
        
        
        init(match_index):=0;
        init(state):=initial;
        init(finished_count):=FALSE;
        init(num_match_beg):=count(bool1[0]) + count(bool1[1]) + count(bool1[2]) + count(bool1[3]) + count(bool1[4]) + count(bool1[5]) + count(bool1[6]) + count(bool1[7]) + count(bool1[8]) + count(bool1[9]) + count(bool1[10]) + count(bool1[11]) + count(bool1[12]) + count(bool1[13]) + count(bool1[14]) + count(bool1[15]) + count(bool1[16]) + count(bool1[17]) + count(bool1[18]) + count(bool1[19]) + count(bool1[20]) + count(bool1[21]) + count(bool1[22]) + count(bool1[23]);
        init(num_match_end):=0;
		
		
        /--next values--/
        /--constants--/
		next(bool1):=bool1;
        next(num_squares_beginning):=num_squares_beginning;
        next(num_squares_1_beg):=num_squares_1_beg;
        next(num_squares_2_beg):=num_squares_2_beg;
        next(num_squares_3_beg):=num_squares_3_beg;
		
		next(init_sq1):=init_sq1;
		next(init_sq2):=init_sq2;
		next(init_sq3):=init_sq3;
        next(num_squares_end):=num_squares_end;
        next(num_allowed):=num_allowed;
        next(finished_count):=last_in_1=9 & last_in_2=4 & last_in_3=1;
        next(num_match_beg):=num_match_beg;
		
        /--non constants--/
        next(state):=case
        finished_count & state = check_free & !free & fin_free & num_squares_1_end + num_squares_2_end + num_squares_3_end = num_squares_end & num_move = 2*num_allowed & num_match_beg = num_match_end: correct;
        state = calc_cons & finished_count & (num_squares_1_end + num_squares_2_end + num_squares_3_end != num_squares_end | num_move!=2*num_allowed | num_match_beg != num_match_end): guess;
        state = calc_cons & finished_count & (num_squares_1_end + num_squares_2_end + num_squares_3_end = num_squares_end & num_move=2*num_allowed & num_match_beg = num_match_end): check_free;
        state = check_free & !fin_free: check_free;
        state = check_free & fin_free & free: guess;
        state = guess & num_squares_1_end != 0: guess;
        state = correct: correct;
        TRUE: calc_cons;
        esac;
		
        
        
        next(match_index):=case
        state = check_free: (match_index + 1)mod(25);
        TRUE: 0;
        esac;
        
        
        next(fin_free):=(next(match_index) = 24);
        
        
        next(last_in_1):=case
        state = calc_cons & next(state) = calc_cons & last_in_1 < 9: (last_in_1 + 1)mod(10);
        state = calc_cons & last_in_1 = 9 & next(state) = calc_cons: 9;
        state = calc_cons & last_in_1 = 9 & next(state) = guess: 0;
        state = calc_cons & last_in_1 = 9 & next(state) = correct: 9;
        state = guess: 0;
        state = correct: 9;
        state = initial: 0;
        TRUE: 9;
        esac;
        
        
        next(last_in_2):=case
        state = calc_cons & next(state) = calc_cons & last_in_2 < 4: (last_in_2 + 1)mod(5);
        state = calc_cons & last_in_2 = 4 & next(state) = calc_cons: 4;
        state = calc_cons & last_in_2 = 4 & next(state) = guess: 0;
        state = calc_cons & last_in_2 = 4 & next(state) = correct: 4;
        state = guess: 0;
        state = correct: 4;
        state = initial: 0;
        TRUE: 4;
        esac;
        
        
        next(last_in_3):=case
        state = calc_cons & next(state) = calc_cons & last_in_3 < 1: (last_in_3 + 1)mod(2);
        state = calc_cons & last_in_3 = 1 & next(state) = calc_cons: 1;
        state = calc_cons & last_in_3 = 1 & next(state) = guess: 0;
        state = calc_cons & last_in_3 = 1 & next(state) = correct: 1;
        state = guess: 0;
        state = correct: 1;
        state = initial: 0;
        TRUE: 1;
        esac;
        
        
        next(matchsticks[0]):=case
        next(state) = calc_cons: matchsticks[0];
        next(state) = correct: matchsticks[0];
        next(state) = guess & state = calc_cons:{TRUE, FALSE};
        TRUE:matchsticks[0];
        esac;
        
        
        next(matchsticks[1]):=case
        next(state) = calc_cons: matchsticks[1];
        next(state) = correct: matchsticks[1];
        next(state) = guess & state = calc_cons:{TRUE, FALSE};
        TRUE:matchsticks[1];
        esac;
        
        
        next(matchsticks[2]):=case
        next(state) = calc_cons: matchsticks[2];
        next(state) = correct: matchsticks[2];
        next(state) = guess & state = calc_cons:{TRUE, FALSE};
        TRUE:matchsticks[2];
        esac;
        
        
        next(matchsticks[3]):=case
        next(state) = calc_cons: matchsticks[3];
        next(state) = correct: matchsticks[3];
        next(state) = guess & state = calc_cons:{TRUE, FALSE};
        TRUE:matchsticks[3];
        esac;
        
        
        next(matchsticks[4]):=case
        next(state) = calc_cons: matchsticks[4];
        next(state) = correct: matchsticks[4];
        next(state) = guess & state = calc_cons:{TRUE, FALSE};
        TRUE:matchsticks[4];
        esac;
        
        
        next(matchsticks[5]):=case
        next(state) = calc_cons: matchsticks[5];
        next(state) = correct: matchsticks[5];
        next(state) = guess & state = calc_cons:{TRUE, FALSE};
        TRUE:matchsticks[5];
        esac;
        
        
        next(matchsticks[6]):=case
        next(state) = calc_cons: matchsticks[6];
        next(state) = correct: matchsticks[6];
        next(state) = guess & state = calc_cons:{TRUE, FALSE};
        TRUE:matchsticks[6];
        esac;
        
        
        next(matchsticks[7]):=case
        next(state) = calc_cons: matchsticks[7];
        next(state) = correct: matchsticks[7];
        next(state) = guess & state = calc_cons:{TRUE, FALSE};
        TRUE:matchsticks[7];
        esac;
        
        
        next(matchsticks[8]):=case
        next(state) = calc_cons: matchsticks[8];
        next(state) = correct: matchsticks[8];
        next(state) = guess & state = calc_cons:{TRUE, FALSE};
        TRUE:matchsticks[8];
        esac;
        
        
        next(matchsticks[9]):=case
        next(state) = calc_cons: matchsticks[9];
        next(state) = correct: matchsticks[9];
        next(state) = guess & state = calc_cons:{TRUE, FALSE};
        TRUE:matchsticks[9];
        esac;
        
        
        next(matchsticks[10]):=case
        next(state) = calc_cons: matchsticks[10];
        next(state) = correct: matchsticks[10];
        next(state) = guess & state = calc_cons:{TRUE, FALSE};
        TRUE:matchsticks[10];
        esac;
        
        
        next(matchsticks[11]):=case
        next(state) = calc_cons: matchsticks[11];
        next(state) = correct: matchsticks[11];
        next(state) = guess & state = calc_cons:{TRUE, FALSE};
        TRUE:matchsticks[11];
        esac;
        
        
        next(matchsticks[12]):=case
        next(state) = calc_cons: matchsticks[12];
        next(state) = correct: matchsticks[12];
        next(state) = guess & state = calc_cons:{TRUE, FALSE};
        TRUE:matchsticks[12];
        esac;
        
        
        next(matchsticks[13]):=case
        next(state) = calc_cons: matchsticks[13];
        next(state) = correct: matchsticks[13];
        next(state) = guess & state = calc_cons:{TRUE, FALSE};
        TRUE:matchsticks[13];
        esac;
        
        
        next(matchsticks[14]):=case
        next(state) = calc_cons: matchsticks[14];
        next(state) = correct: matchsticks[14];
        next(state) = guess & state = calc_cons:{TRUE, FALSE};
        TRUE:matchsticks[14];
        esac;
        
        
        next(matchsticks[15]):=case
        next(state) = calc_cons: matchsticks[15];
        next(state) = correct: matchsticks[15];
        next(state) = guess & state = calc_cons:{TRUE, FALSE};
        TRUE:matchsticks[15];
        esac;
        
        
        next(matchsticks[16]):=case
        next(state) = calc_cons: matchsticks[16];
        next(state) = correct: matchsticks[16];
        next(state) = guess & state = calc_cons:{TRUE, FALSE};
        TRUE:matchsticks[16];
        esac;
        
        
        next(matchsticks[17]):=case
        next(state) = calc_cons: matchsticks[17];
        next(state) = correct: matchsticks[17];
        next(state) = guess & state = calc_cons:{TRUE, FALSE};
        TRUE:matchsticks[17];
        esac;
        
        
        next(matchsticks[18]):=case
        next(state) = calc_cons: matchsticks[18];
        next(state) = correct: matchsticks[18];
        next(state) = guess & state = calc_cons:{TRUE, FALSE};
        TRUE:matchsticks[18];
        esac;
        
        
        next(matchsticks[19]):=case
        next(state) = calc_cons: matchsticks[19];
        next(state) = correct: matchsticks[19];
        next(state) = guess & state = calc_cons:{TRUE, FALSE};
        TRUE:matchsticks[19];
        esac;
        
        
        next(matchsticks[20]):=case
        next(state) = calc_cons: matchsticks[20];
        next(state) = correct: matchsticks[20];
        next(state) = guess & state = calc_cons:{TRUE, FALSE};
        TRUE:matchsticks[20];
        esac;
        
        
        next(matchsticks[21]):=case
        next(state) = calc_cons: matchsticks[21];
        next(state) = correct: matchsticks[21];
        next(state) = guess & state = calc_cons:{TRUE, FALSE};
        TRUE:matchsticks[21];
        esac;
        
        
        next(matchsticks[22]):=case
        next(state) = calc_cons: matchsticks[22];
        next(state) = correct: matchsticks[22];
        next(state) = guess & state = calc_cons:{TRUE, FALSE};
        TRUE:matchsticks[22];
        esac;
        
        
        next(matchsticks[23]):=case
        next(state) = calc_cons: matchsticks[23];
        next(state) = correct: matchsticks[23];
        next(state) = guess & state = calc_cons:{TRUE, FALSE};
        TRUE:matchsticks[23];
        esac;
        
        
        next(xor_arr[0]):=case
        next(state)=calc_cons:(bool1[0])xor(matchsticks[0]);
        TRUE:xor_arr[0];
        esac;
        
        
        next(xor_arr[1]):=case
        next(state)=calc_cons:(bool1[1])xor(matchsticks[1]);
        TRUE:xor_arr[1];
        esac;
        
        
        next(xor_arr[2]):=case
        next(state)=calc_cons:(bool1[2])xor(matchsticks[2]);
        TRUE:xor_arr[2];
        esac;
        
        
        next(xor_arr[3]):=case
        next(state)=calc_cons:(bool1[3])xor(matchsticks[3]);
        TRUE:xor_arr[3];
        esac;
        
        
        next(xor_arr[4]):=case
        next(state)=calc_cons:(bool1[4])xor(matchsticks[4]);
        TRUE:xor_arr[4];
        esac;
        
        
        next(xor_arr[5]):=case
        next(state)=calc_cons:(bool1[5])xor(matchsticks[5]);
        TRUE:xor_arr[5];
        esac;
        
        
        next(xor_arr[6]):=case
        next(state)=calc_cons:(bool1[6])xor(matchsticks[6]);
        TRUE:xor_arr[6];
        esac;
        
        
        next(xor_arr[7]):=case
        next(state)=calc_cons:(bool1[7])xor(matchsticks[7]);
        TRUE:xor_arr[7];
        esac;
        
        
        next(xor_arr[8]):=case
        next(state)=calc_cons:(bool1[8])xor(matchsticks[8]);
        TRUE:xor_arr[8];
        esac;
        
        
        next(xor_arr[9]):=case
        next(state)=calc_cons:(bool1[9])xor(matchsticks[9]);
        TRUE:xor_arr[9];
        esac;
        
        
        next(xor_arr[10]):=case
        next(state)=calc_cons:(bool1[10])xor(matchsticks[10]);
        TRUE:xor_arr[10];
        esac;
        
        
        next(xor_arr[11]):=case
        next(state)=calc_cons:(bool1[11])xor(matchsticks[11]);
        TRUE:xor_arr[11];
        esac;
        
        
        next(xor_arr[12]):=case
        next(state)=calc_cons:(bool1[12])xor(matchsticks[12]);
        TRUE:xor_arr[12];
        esac;
        
        
        next(xor_arr[13]):=case
        next(state)=calc_cons:(bool1[13])xor(matchsticks[13]);
        TRUE:xor_arr[13];
        esac;
        
        
        next(xor_arr[14]):=case
        next(state)=calc_cons:(bool1[14])xor(matchsticks[14]);
        TRUE:xor_arr[14];
        esac;
        
        
        next(xor_arr[15]):=case
        next(state)=calc_cons:(bool1[15])xor(matchsticks[15]);
        TRUE:xor_arr[15];
        esac;
        
        
        next(xor_arr[16]):=case
        next(state)=calc_cons:(bool1[16])xor(matchsticks[16]);
        TRUE:xor_arr[16];
        esac;
        
        
        next(xor_arr[17]):=case
        next(state)=calc_cons:(bool1[17])xor(matchsticks[17]);
        TRUE:xor_arr[17];
        esac;
        
        next(xor_arr[18]):=case
        next(state)=calc_cons:(bool1[18])xor(matchsticks[18]);
        TRUE:xor_arr[18];
        esac;
        
        next(xor_arr[19]):=case
        next(state)=calc_cons:(bool1[19])xor(matchsticks[19]);
        TRUE:xor_arr[19];
        esac;
        
        
        next(xor_arr[20]):=case
        next(state)=calc_cons:(bool1[20])xor(matchsticks[20]);
        TRUE:xor_arr[20];
        esac;
        
        
        next(xor_arr[21]):=case
        next(state)=calc_cons:(bool1[21])xor(matchsticks[21]);
        TRUE:xor_arr[21];
        esac;
        
        
        next(xor_arr[22]):=case
        next(state)=calc_cons:(bool1[22])xor(matchsticks[22]);
        TRUE:xor_arr[22];
        esac;
        
        
        next(xor_arr[23]):=case
        next(state)=calc_cons:(bool1[23])xor(matchsticks[23]);
        TRUE:xor_arr[23];
        esac;
        
        
        next(sq_1_bool[0]):=case
        matchsticks[0] & matchsticks[4] & matchsticks[7] & matchsticks[3]: TRUE;
        TRUE: FALSE;
        esac;
        
        
        next(sq_1_bool[1]):=case
        matchsticks[1] & matchsticks[4] & matchsticks[5] & matchsticks[8]: TRUE;
        TRUE: FALSE;
        esac;
        
        
        next(sq_1_bool[2]):=case
        matchsticks[2] & matchsticks[5] & matchsticks[9] & matchsticks[6]: TRUE;
        TRUE: FALSE;
        esac;
        
        
        next(sq_1_bool[3]):=case
        matchsticks[7] & matchsticks[10] & matchsticks[11] & matchsticks[14]: TRUE;
        TRUE: FALSE;
        esac;
        
        
        next(sq_1_bool[4]):=case
        matchsticks[8] & matchsticks[11] & matchsticks[15] & matchsticks[12]: TRUE;
        TRUE: FALSE;
        esac;
        
        
        next(sq_1_bool[5]):=case
        matchsticks[16] & matchsticks[13] & matchsticks[12] & matchsticks[9]: TRUE;
        TRUE: FALSE;
        esac;
        
        
        next(sq_1_bool[6]):=case
        matchsticks[14] & matchsticks[17] & matchsticks[18] & matchsticks[21]: TRUE;
        TRUE: FALSE;
        esac;
        
        
        next(sq_1_bool[7]):=case
        matchsticks[15] & matchsticks[18] & matchsticks[19] & matchsticks[22]: TRUE;
        TRUE: FALSE;
        esac;
        
        
        next(sq_1_bool[8]):=case
        matchsticks[16] & matchsticks[19] & matchsticks[20] & matchsticks[23]: TRUE;
        TRUE: FALSE;
        esac;
        
        next(sq_2_bool[0]):=case
        matchsticks[0] & matchsticks[1] & matchsticks[5] & matchsticks[12] & matchsticks[15] & matchsticks[14] & matchsticks[10] & matchsticks[3]: TRUE;
        TRUE: FALSE;
        esac;
        
        
        next(sq_2_bool[1]):=case
        matchsticks[1] & matchsticks[2] & matchsticks[6] & matchsticks[13] & matchsticks[16] & matchsticks[15] & matchsticks[11] & matchsticks[4]: TRUE;
        TRUE: FALSE;
        esac;
        
        next(sq_2_bool[2]):=case
        matchsticks[7] & matchsticks[8] & matchsticks[12] & matchsticks[19] & matchsticks[22] & matchsticks[21] & matchsticks[17] & matchsticks[10]: TRUE;
        TRUE: FALSE;
        esac;
        
        
        next(sq_2_bool[3]):=case
        matchsticks[8] & matchsticks[9] & matchsticks[13] & matchsticks[20] & matchsticks[23] & matchsticks[22] & matchsticks[18] & matchsticks[11]: TRUE;
        TRUE: FALSE;
        esac;
        
        
        next(sq_3_bool):=case
        matchsticks[0] & matchsticks[1] & matchsticks[2] & matchsticks[6] & matchsticks[13] & matchsticks[20] & matchsticks[23] & matchsticks[22] & matchsticks[21] & matchsticks[17] & matchsticks[10] & matchsticks[3]: TRUE;
        TRUE: FALSE;
        esac;
        
        
        next(num_move):=case
        state = guess: count(next(xor_arr[0])) + count(next(xor_arr[1])) + count(next(xor_arr[2])) + count(next(xor_arr[3])) + count(next(xor_arr[4])) + count(next(xor_arr[5])) + count(next(xor_arr[6])) + count(next(xor_arr[7])) + count(next(xor_arr[8])) + count(next(xor_arr[9])) + count(next(xor_arr[10])) + count(next(xor_arr[11])) + count(next(xor_arr[12])) + count(next(xor_arr[13])) + count(next(xor_arr[14])) + count(next(xor_arr[15])) + count(next(xor_arr[16])) + count(next(xor_arr[17])) + count(next(xor_arr[18])) + count(next(xor_arr[19])) + count(next(xor_arr[20])) + count(next(xor_arr[21])) + count(next(xor_arr[22])) + count(next(xor_arr[23]));
        TRUE: num_move;
        esac;
        
        
        next(num_match_end):= count(matchsticks[0]) +  count(matchsticks[1]) + count(matchsticks[2]) + count(matchsticks[3]) + count(matchsticks[4]) + count(matchsticks[5]) + count(matchsticks[6]) + count(matchsticks[7]) + count(matchsticks[8]) + count(matchsticks[9]) + count(matchsticks[10]) + count(matchsticks[11]) + count(matchsticks[12]) + count(matchsticks[13]) + count(matchsticks[14]) + count(matchsticks[15]) + count(matchsticks[16]) + count(matchsticks[17]) + count(matchsticks[18]) + count(matchsticks[19]) + count(matchsticks[20]) + count(matchsticks[21]) + count(matchsticks[22]) + count(matchsticks[23]);
        
        next(free):=case
        state = check_free & match_index = 0 & matchsticks[0]: !(sq_1_bool[0] | sq_2_bool[0] | sq_3_bool);
        state = check_free & match_index = 0 & !matchsticks[0]: FALSE;
        state = check_free & match_index = 1 & matchsticks[1]: !(sq_1_bool[1] | sq_2_bool[0] | sq_2_bool[1] | sq_3_bool) | free;
        state = check_free & match_index = 1 & !matchsticks[1]: free;
        state = check_free & match_index = 2 & matchsticks[2]: !(sq_1_bool[2] | sq_2_bool[1] | sq_3_bool) | free;
        state = check_free & match_index = 2 & !matchsticks[2]: free;
        state = check_free & match_index = 3 & matchsticks[3]: !(sq_1_bool[0] | sq_2_bool[0] | sq_3_bool) | free;
        state = check_free & match_index = 3 & !matchsticks[3]: free;
        state = check_free & match_index = 4 & matchsticks[4]: !(sq_1_bool[0] | sq_1_bool[1] | sq_2_bool[1]) | free;
        state = check_free & match_index = 4 & !matchsticks[4]: free;
        state = check_free & match_index = 5 & matchsticks[5]: !(sq_1_bool[1] | sq_1_bool[2] | sq_2_bool[0]) | free;
        state = check_free & match_index = 5 & !matchsticks[5]: free;
        state = check_free & match_index = 6 & matchsticks[6]: !(sq_1_bool[2] | sq_2_bool[1] | sq_3_bool) | free;
        state = check_free & match_index = 6 & !matchsticks[6]: free;
        state = check_free & match_index = 7 & matchsticks[7]: !(sq_1_bool[0] | sq_1_bool[3] | sq_2_bool[2]) | free;
        state = check_free & match_index = 7 & !matchsticks[7]: free;
        state = check_free & match_index = 8 & matchsticks[8]: !(sq_1_bool[1] | sq_1_bool[4] | sq_2_bool[2] | sq_2_bool[3]) | free;
        state = check_free & match_index = 8 & !matchsticks[8]: free;
        state = check_free & match_index = 9 & matchsticks[9]: !(sq_1_bool[2] | sq_1_bool[5] | sq_2_bool[3]) | free;
        state = check_free & match_index = 9 & !matchsticks[9]: free;
        state = check_free & match_index = 10 & matchsticks[10]: !(sq_1_bool[3] | sq_2_bool[2] | sq_2_bool[0] | sq_3_bool) | free;
        state = check_free & match_index = 10 & !matchsticks[10]: free;
        state = check_free & match_index = 11 & matchsticks[11]: !(sq_1_bool[3] | sq_1_bool[4] | sq_2_bool[3]) | free;
        state = check_free & match_index = 11 & !matchsticks[11]: free;
        state = check_free & match_index = 12 & matchsticks[12]: !(sq_1_bool[5] | sq_1_bool[4] | sq_2_bool[2]) | free;
        state = check_free & match_index = 12 & !matchsticks[12]: free;
        state = check_free & match_index = 13 & matchsticks[13]: !(sq_1_bool[5] | sq_2_bool[3] | sq_3_bool) | free;
        state = check_free & match_index = 13 & !matchsticks[13]: free;
        state = check_free & match_index = 14 & matchsticks[14]: !(sq_1_bool[3] | sq_1_bool[6] | sq_2_bool[0]) | free;
        state = check_free & match_index = 14 & !matchsticks[14]: free;
        state = check_free & match_index = 15 & matchsticks[15]: !(sq_1_bool[4] | sq_1_bool[7] | sq_2_bool[0]) | free;
        state = check_free & match_index = 15 & !matchsticks[15]: free;
        state = check_free & match_index = 16 & matchsticks[16]: !(sq_1_bool[5] | sq_1_bool[8] | sq_2_bool[1]) | free;
        state = check_free & match_index = 16 & !matchsticks[16]: free;
        state = check_free & match_index = 17 & matchsticks[17]: !(sq_1_bool[6] | sq_2_bool[2] | sq_3_bool) | free;
        state = check_free & match_index = 17 & !matchsticks[17]: free;
        state = check_free & match_index = 18 & matchsticks[18]: !(sq_1_bool[6] | sq_1_bool[7] | sq_2_bool[3]) | free;
        state = check_free & match_index = 18 & !matchsticks[18]: free;
        state = check_free & match_index = 19 & matchsticks[19]: !(sq_1_bool[7] | sq_1_bool[8] | sq_2_bool[2]) | free;
        state = check_free & match_index = 19 & !matchsticks[19]: free;
        state = check_free & match_index = 20 & matchsticks[20]: !(sq_1_bool[8] | sq_2_bool[3] | sq_3_bool) | free;
        state = check_free & match_index = 20 & !matchsticks[20]: free;
        state = check_free & match_index = 21 & matchsticks[21]: !(sq_1_bool[6] | sq_2_bool[2] | sq_3_bool) | free;
        state = check_free & match_index = 21 & !matchsticks[21]: free;
        state = check_free & match_index = 22 & matchsticks[22]: !(sq_1_bool[7] | sq_2_bool[2] | sq_2_bool[3] | sq_3_bool) | free;
        state = check_free & match_index = 22 & !matchsticks[22]: free;
        state = check_free & match_index = 23 & !matchsticks[23]: free;
        state = check_free & match_index = 23 & matchsticks[23]: !(sq_1_bool[8] | sq_2_bool[3] | sq_3_bool) | free;
        state = check_free & match_index = 24: free;
        TRUE: FALSE;
        esac;
        
        
        next(num_squares_1_end):=case
        !(finished_count) & state = calc_cons & sq_1_bool[last_in_1] & last_in_1 < 9: (num_squares_1_end+1)mod(10) ;
        state = guess: 0;
        TRUE: num_squares_1_end;
        esac;
        
        
        next(num_squares_2_end):=case
        !(finished_count) & state = calc_cons & sq_2_bool[last_in_2] & last_in_2 < 4: (num_squares_2_end+1)mod(5) ;
        state = guess: 0;
        TRUE: num_squares_2_end;
        esac;
        
        
        next(num_squares_3_end):=case
        !(finished_count) & state = calc_cons & sq_3_bool & last_in_3 < 1: (num_squares_3_end+1)mod(2) ;
        state = guess: 0;
        TRUE: num_squares_3_end;
        esac;
        
        
        LTLSPEC
                         G !(state = initial & !free & num_allowed != 0 & num_squares_end != 0 & num_squares_beginning != 1 & F state = correct & num_squares_end != num_squares_beginning)
"""
    os.chdir(r'C:\Users\liatw\OneDrive\Desktop\NuSMV-2.6.0-win64\bin')  # change to your NuSMV bin directory
    open('sq' + str(j) + ".smv", 'w').close()
    code = '''j = ''' + str(j) + '''
text = """''' + text + '''"""
f = open('sq' + str(j) + '.smv', 'a')
print >> f, text
f.close()'''
    build_time = timeit.timeit(code, number=1)
    run_model('sq' + str(j) + '.smv', j)
    return build_time


def limits(num_squares_beginning, num_squares_1_beg, num_squares_2_beg, num_squares_3_beg,
           matchsticks,
           sq_1_bool, sq_2_bool, sq_3_bool, num_squares_end=-1, num_allowed=-1, mid_or_last_sol='',
           last_lower=-1, last_upper=- 1, current_min=0, flag_solved=0):
    if last_lower == last_upper == -1:
        if num_allowed == -1:  # need to find optimal num_allowed, num_squares_end is constant
            if num_squares_beginning == num_squares_end:
                return None, None, None  # min found - stop changing limits
            return 1, min(sum(matchsticks), 24 - sum(matchsticks)), ''

        elif num_squares_end == -1:  # need to find optimal num_squares_end, num_allowed is constant
            if num_allowed == 0:
                return None, None, None  # min found - stop changing limits
            return 1, 14, ''

    elif current_min == 1 or last_upper < last_lower:
        return None, None, None

    elif flag_solved == 2:
        if last_lower == last_upper:
            return None, None, None
        if min((last_lower + last_upper) / 2, current_min) == current_min != (last_lower + last_upper) / 2:
            mid_or_last_sol = 'last'
        else:
            mid_or_last_sol = 'mid'
        return last_lower, min((last_lower + last_upper) / 2, current_min - 1), mid_or_last_sol

    elif flag_solved == 1:

        if current_min == last_upper + 1:
            return None, None, None

        if mid_or_last_sol == 'last':
            return None, None, None

        elif mid_or_last_sol == '':  # first time running, no solutions -> stop searching
            return None, None, None

        elif mid_or_last_sol == 'mid':
            return (last_lower + last_upper) / 2, current_min - 1, mid_or_last_sol


def run_model(file_model, j):
    """
        This function runs the model file indexed j with NuSMV and prints the results into the output file indexed j.
    """
    f = open(str(file_model), 'a')
    open('output_sq' + str(j) + '.txt', 'w').close()
    output_f = open('output_sq' + str(j) + '.txt', 'a')
    subprocess.Popen("ptime.exe NuSMV -bmc -bmc_length 51 " + str(file_model), stdout=output_f, stderr=output_f)
    output_f.close()
    f.close()


def find_info(j, find_min=False, num_allowed=-1, num_sqr_end=-1, find_input=False):
    """
            This function gets:
            j - index of an input/output file
            It returns the riddle's solution:
            matchsticks - a Boolean array indexed 0 - 23 which represents the current matchsticks configuration:
            True - the indexed matchstick exists, False - the indexed matchstick does not exist.

        """
    par = ''
    if num_allowed == -1:
        par = 'num_allowed'
    elif num_sqr_end == -1:
        par = 'num_sqr_end'
    f = open('output_sq' + str(j) + '.txt', 'r')
    text = f.read()
    while "Execution time: " not in text:
        time.sleep(1)
        f = open('output_sq' + str(j) + '.txt', 'r')
        text = f.read()

    rows = text.split('\n')
    list_match_ind = []
    arr_match = []
    list_bool1_ind = []
    arr_bool1 = []

    for row in rows:
        if 'matchsticks' in row and 'specification' not in row:
            st, val = row.split(' = ')

            if st not in list_match_ind:
                list_match_ind.append(st)
                arr_match.append(val)

            else:
                st = st.replace(']', '[')
                var, ind, var2 = st.split('[')
                arr_match[int(ind)] = val

        if 'bool1' in row and 'specification' not in row:
            st, val = row.split(' = ')

            if st not in list_match_ind:
                list_bool1_ind.append(st)
                arr_bool1.append(val)

            else:
                st = st.replace(']', '[')
                var, ind, var2 = st.split('[')
                arr_bool1[int(ind)] = val

        elif num_allowed == -1 and 'num_allowed' in row and '>' not in row and '!' not in row:
            st, num_all = row.split(' = ')
            num_allowed = int(num_all)

        elif num_sqr_end == -1 and 'num_squares_end' in row and '>' not in row and '!' not in row:
            st, num_sq = row.split(' = ')
            num_sqr_end = int(num_sq)

    matchsticks = [True if item == 'TRUE' else False for item in arr_match]
    bool1 = [True if item == 'TRUE' else False for item in arr_bool1]
    if find_input:
        return matchsticks, bool1, num_sqr_end, num_allowed
    if not find_min:
        return matchsticks
    elif par == 'num_sqr_end':
        return matchsticks, num_sqr_end
    elif par == 'num_allowed':
        return matchsticks, num_allowed


def find_solution(j):
    """
    reads the relevant file according to the operations
    finds the solution in the file and prints it
    """
    f = open('output_sq' + str(j) + '.txt', 'r')
    text = f.read()
    while "Execution time: " not in text:
        time.sleep(1)
        f = open('output_sq' + str(j) + '.txt', 'r')
        text = f.read()
    run_str = (text.split("Execution time: "))[1].split(" s")[0]
    run_time = float(run_str)

    if 'is false' in text:
        f.close()
        return 2, run_time
    else:
        f.close()
        return 1, run_time


def calculate_avg(index, num_allowed):
    """
        This function calculates the average execution time
    """
    avg_build = 0
    avg_solved_run = 0
    avg_not_solved_run = 0
    count_solved = 0
    count_no_solution = 0

    for i in range(index, 120000000 + index):
        times, flag_solved, run_time = solve_rid(i, num_allowed)
        if times != -1:
            avg_build += times
            if flag_solved == 2:
                count_solved += 1
                avg_solved_run += run_time
            if flag_solved == 1:
                count_no_solution += 1
                avg_not_solved_run += run_time
            if count_solved == 1:
                break
    return avg_solved_run / count_solved


def main():
    os.chdir(r'C:\Users\liatw\OneDrive\Desktop\NuSMV-2.6.0-win64\bin')  # change to your NuSMV directory
    run_model('sq2.smv', 2)


if __name__ == '__main__':
    main()
