import os
import subprocess
import time
import random
import timeit

text_var = "MODULE main\n\
/--state variables--/\n\
VAR\n\
count_row1:0..14;\n\
count_row2:0..14;\n\
count_row3:0..14;\n\
count_row4:0..14;\n\
\n\n\
count_col1:0..14;\n\
count_col2:0..14;\n\
count_col3:0..14;\n\
count_col4:0..14;\n\
\n\n\
count_di1:0..10;\n\
count_di2:0..10;\n\
num_allowed:0..14;\n\
\n\n\
row1: 0..7;\n\
row2: 3..14;\n\
row3: 10..21;\n\
row4: 17..24;\n\
\n\n\
rows_equal: boolean;\n\
cols_equal: boolean;\n\
dis_equal: boolean;\n\
finished_count: boolean;\n\
\n\n\
col1: {0,3,7,10,14,17,21,22};\n\
col2: {0,1,4,7,8,11,14,15,18,21,22,23};\n\
col3: {1,2,5,8,9,12,15,16,19,22,23,24};\n\
col4: {2,6,9,13,16,20,23,24};\n\
\n\n\
di1: {0,3,4,7,8,11,12,15,16,19,20,23,24};\n\
di2: {2,5,6,8,9,11,12,15,14,17,18,21,22};\n\
\n\n\
arr_rows:array 0..23 of 1..4;\n\
arr_cols:array 0..23 of 1..4;\n\
arr_dis:array 0..23 of 0..2;\n\
state:{initial, calc_cons, correct, guess};\n"

text_assign = "ASSIGN\n\
init(finished_count):=FALSE;\n\
init(count_row1):=0;\n\
init(count_row2):=0;\n\
init(count_row3):=0;\n\
init(count_row4):=0;\n\
\n\n\
init(count_col1):=0;\n\
init(count_col2):=0;\n\
init(count_col3):=0;\n\
init(count_col4):=0;\n\
\n\n\
init(count_di1):=0;\n\
init(count_di2):=0;\n\
\n\n\
init(row1):=0;\n\
init(row2):=3;\n\
init(row3):=10;\n\
init(row4):=17;\n\
\n\n\
init(col1):=0;\n\
init(col2):=0;\n\
init(col3):=1;\n\
init(col4):=2;\n\
\n\n\
init(di1):=0;\n\
init(di2):=2;\n\
\n\n\
init(num_allowed):=6;\n\
init(arr_rows):=match_rows;\n\
init(arr_cols):=match_cols;\n\
init(arr_dis):=match_dis;\n\
init(state):=initial;\n\
\n\n\
init(rows_equal):=count_row1 = num_allowed & count_row2 = num_allowed & count_row3 = num_allowed & count_row4 = num_allowed;\n\
init(cols_equal):=count_col1 = num_allowed & count_col2 = num_allowed & count_col3 = num_allowed & count_col4 = num_allowed;\n\
init(dis_equal):=count_di1 = num_allowed & count_di2 = num_allowed;\n\
\n\n\
next(finished_count) := row1 = 7 & row2 = 14 & row3 = 21 & row4 = 24 & col1 = 22 & col2 = 23 & col3 = 24 & col4 = 24 & di1 = 24 & di2 = 22;\n\
next(num_allowed):=num_allowed;\n\
\n\n\
next(state):=case\n\
finished_count & rows_equal & cols_equal & dis_equal: correct;\n\
state = calc_cons & next(finished_count) & !(next(rows_equal) & next(cols_equal) & next(dis_equal)): guess;\n\
state = guess & count_row1 != 0: guess;\n\
state = correct: correct;\n\
TRUE: calc_cons;\n\
esac;\n\
\n\n\
next(row1):=case\n\
state = calc_cons & next(state) = calc_cons & row1 < 7: (row1 + 1)mod(8);\n\
state = calc_cons & row1 = 7 & next(state) = calc_cons: 7;\n\
state = calc_cons & row1 = 7 & next(state) = guess: 0;\n\
state = calc_cons & row1 = 7 & next(state) = correct: 7;\n\
state = guess: 0;\n\
state = correct: 7;\n\
state = initial: 0;\n\
TRUE: 7;\n\
esac;\n\
\n\n\
next(row2):=case\n\
state = calc_cons & next(state) = calc_cons & row2 < 14: 4 + (row2 - 3)mod(11);\n\
state = calc_cons & row2 = 14 & next(state) = calc_cons: 14;\n\
state = calc_cons & row2 = 14 & next(state) = guess: 3;\n\
state = calc_cons & row2 = 14 & next(state) = correct: 14;\n\
state = guess: 3;\n\
state = correct: 14;\n\
state = initial: 3;\n\
TRUE: 14;\n\
esac;\n\
\n\
next(row3):=case\n\
state = calc_cons & next(state) = calc_cons & row3 < 21: 10 + (row3 - 9)mod(12);\n\
state = calc_cons & row3 = 21 & next(state) = calc_cons: 21;\n\
state = calc_cons & row3 = 21 & next(state) = guess: 10;\n\
state = calc_cons & row3 = 21 & next(state) = correct: 21;\n\
state = guess: 10;\n\
state = correct: 21;\n\
state = initial: 10;\n\
TRUE: 21;\n\
esac;\n\
\n\n\
next(row4):=case\n\
state = calc_cons & next(state) = calc_cons & row4 < 24: 17 + (row4 - 16)mod(8);\n\
state = calc_cons & row4 = 24 & next(state) = calc_cons: 24;\n\
state = calc_cons & row4 = 24 & next(state) = guess: 17;\n\
state = calc_cons & row4 = 24 & next(state) = correct: 24;\n\
state = guess: 17;\n\
state = correct: 24;\n\
state = initial: 17;\n\
TRUE: 24;\n\
esac;\n\
\n\n\
/--0,3,7,10,14,17,21,22--/\n\
next(col1):=case\n\
state = calc_cons & next(state) = calc_cons & col1 = 0: 3;\n\
state = calc_cons & next(state) = calc_cons & col1 = 3: 7;\n\
state = calc_cons & next(state) = calc_cons & col1 = 7: 10;\n\
state = calc_cons & next(state) = calc_cons & col1 = 10: 14;\n\
state = calc_cons & next(state) = calc_cons & col1 = 14: 17;\n\
state = calc_cons & next(state) = calc_cons & col1 = 17: 21;\n\
state = calc_cons & col1 = 21 & next(state) = calc_cons: 22;\n\
state = calc_cons & col1 = 22 & next(state) = guess: 0;\n\
state = calc_cons & col1 = 22 & next(state) = correct: 22;\n\
state = guess: 0;\n\
state = correct: 22;\n\
state = initial: 0;\n\
TRUE: 22;\n\
esac;\n\
\n\n\
/--0,1,4,7,8,11,14,15,18,21,22,23--/\n\
next(col2):=case\n\
state = calc_cons & next(state) = calc_cons & col2 = 0: 1;\n\
state = calc_cons & next(state) = calc_cons & col2 = 1: 4;\n\
state = calc_cons & next(state) = calc_cons & col2 = 4: 7;\n\
state = calc_cons & next(state) = calc_cons & col2 = 7: 8;\n\
state = calc_cons & next(state) = calc_cons & col2 = 8: 11;\n\
state = calc_cons & next(state) = calc_cons & col2 = 11: 14;\n\
state = calc_cons & next(state) = calc_cons & col2 = 14: 15;\n\
state = calc_cons & next(state) = calc_cons & col2 = 15: 18;\n\
state = calc_cons & next(state) = calc_cons & col2 = 18: 21;\n\
state = calc_cons & next(state) = calc_cons & col2 = 21: 22;\n\
state = calc_cons & col2 = 22 & next(state) = calc_cons: 23;\n\
state = calc_cons & col2 = 23 & next(state) = guess: 0;\n\
state = calc_cons & col2 = 23 & next(state) = correct: 23;\n\
state = guess: 0;\n\
state = correct: 23;\n\
state = initial: 0;\n\
TRUE: 23;\n\
esac;\n\
\n\n\
/--1,2,5,8,9,12,15,16,19,22,23,24--/\n\
next(col3):=case\n\
state = calc_cons & next(state) = calc_cons & col3 = 1: 2;\n\
state = calc_cons & next(state) = calc_cons & col3 = 2: 5;\n\
state = calc_cons & next(state) = calc_cons & col3 = 5: 8;\n\
state = calc_cons & next(state) = calc_cons & col3 = 8: 9;\n\
state = calc_cons & next(state) = calc_cons & col3 = 9: 12;\n\
state = calc_cons & next(state) = calc_cons & col3 = 12: 15;\n\
state = calc_cons & next(state) = calc_cons & col3 = 15: 16;\n\
state = calc_cons & next(state) = calc_cons & col3 = 16: 19;\n\
state = calc_cons & next(state) = calc_cons & col3 = 19: 22;\n\
state = calc_cons & next(state) = calc_cons & col3 = 22: 23;\n\
state = calc_cons & col3 = 23 & next(state) = calc_cons: 24;\n\
state = calc_cons & col3 = 24 & next(state) = guess: 1;\n\
state = calc_cons & col3 = 24 & next(state) = correct: 24;\n\
state = guess: 1;\n\
state = correct: 24;\n\
state = initial: 1;\n\
TRUE: 24;\n\
esac;\n\
\n\n\
/--2,6,9,13,16,20,23,24--/\n\
next(col4):=case\n\
state = calc_cons & next(state) = calc_cons & col4 = 2: 6;\n\
state = calc_cons & next(state) = calc_cons & col4 = 6: 9;\n\
state = calc_cons & next(state) = calc_cons & col4 = 9: 13;\n\
state = calc_cons & next(state) = calc_cons & col4 = 13: 16;\n\
state = calc_cons & next(state) = calc_cons & col4 = 16: 20;\n\
state = calc_cons & next(state) = calc_cons & col4 = 20: 23;\n\
state = calc_cons & col4 = 23 & next(state) = calc_cons: 24;\n\
state = calc_cons & col4 = 24 & next(state) = guess: 2;\n\
state = calc_cons & col4 = 24 & next(state) = correct: 24;\n\
state = guess: 2;\n\
state = correct: 24;\n\
state = initial: 2;\n\
TRUE: 24;\n\
esac;\n\
\n\n\
/--0,3,4,7,8,11,12,15,16,19,20,23,24--/\n\
next(di1):=case\n\
state = calc_cons & next(state) = calc_cons & di1 = 0: 3;\n\
state = calc_cons & next(state) = calc_cons & di1 = 3: 4;\n\
state = calc_cons & next(state) = calc_cons & di1 = 4: 7;\n\
state = calc_cons & next(state) = calc_cons & di1 = 7: 8;\n\
state = calc_cons & next(state) = calc_cons & di1 = 8: 11;\n\
state = calc_cons & next(state) = calc_cons & di1 = 11: 12;\n\
state = calc_cons & next(state) = calc_cons & di1 = 12: 15;\n\
state = calc_cons & next(state) = calc_cons & di1 = 15: 16;\n\
state = calc_cons & next(state) = calc_cons & di1 = 16: 19;\n\
state = calc_cons & next(state) = calc_cons & di1 = 19: 20;\n\
state = calc_cons & next(state) = calc_cons & di1 = 20: 23;\n\
state = calc_cons & di1 = 23 & next(state) = calc_cons: 24;\n\
state = calc_cons & di1 = 24 & next(state) = guess: 0;\n\
state = calc_cons & di1 = 24 & next(state) = correct: 24;\n\
state = guess: 0;\n\
state = correct: 24;\n\
state = initial: 0;\n\
TRUE: 24;\n\
esac;\n\
\n\n\
/--2,5,6,8,9,11,12,14,15,17,18,21,22--/\n\
next(di2):=case\n\
state = calc_cons & next(state) = calc_cons & di2 = 2: 5;\n\
state = calc_cons & next(state) = calc_cons & di2 = 5: 6;\n\
state = calc_cons & next(state) = calc_cons & di2 = 6: 8;\n\
state = calc_cons & next(state) = calc_cons & di2 = 7: 8;\n\
state = calc_cons & next(state) = calc_cons & di2 = 8: 9;\n\
state = calc_cons & next(state) = calc_cons & di2 = 9: 11;\n\
state = calc_cons & next(state) = calc_cons & di2 = 11: 12;\n\
state = calc_cons & next(state) = calc_cons & di2 = 12: 14;\n\
state = calc_cons & next(state) = calc_cons & di2 = 14: 15;\n\
state = calc_cons & next(state) = calc_cons & di2 = 15: 17;\n\
state = calc_cons & next(state) = calc_cons & di2 = 17: 18;\n\
state = calc_cons & next(state) = calc_cons & di2 = 18: 21;\n\
state = calc_cons & di2 = 21 & next(state) = calc_cons: 22;\n\
state = calc_cons & di2 = 22 & next(state) = guess: 2;\n\
state = calc_cons & di2 = 22 & next(state) = correct: 22;\n\
state = guess: 2;\n\
state = correct: 22;\n\
state = initial: 2;\n\
TRUE: 22;\n\
esac;\n\
\n\n\
next(rows_equal):=next(count_row1) = next(num_allowed) & next(count_row2) = next(num_allowed) & next(count_row3) = next(num_allowed) & next(count_row4) = next(num_allowed);\n\
next(cols_equal):=next(count_col1) = next(num_allowed) & next(count_col2) = next(num_allowed) & next(count_col3) = next(num_allowed) & next(count_col4) = next(num_allowed);\n\
next(dis_equal):=next(count_di1) = next(num_allowed) & next(count_di2) = next(num_allowed);\n\
\n\n\
next(arr_rows[0]):=case\n\
next(state) = calc_cons: arr_rows[0];\n\
next(state) = correct: arr_rows[0];\n\
next(state) = guess & state = calc_cons:row_options[0];\n\
TRUE:arr_rows[0];\n\
esac;\n\
\n\
next(arr_cols[0]):=case\n\
next(state) = calc_cons: arr_cols[0];\n\
next(state) = correct: arr_cols[0];\n\
next(state) = guess & state = calc_cons:col_options[1];\n\
TRUE:arr_cols[0];\n\
esac;\n\
\n\n\
next(arr_dis[0]):=case\n\
next(state) = calc_cons: arr_dis[0];\n\
next(state) = correct: arr_dis[0];\n\
next(state) = guess & state = calc_cons & next(arr_cols[0]) = 1: 1;\n\
next(state) = guess & next(arr_cols[0]) = 2: 0;\n\
TRUE:arr_dis[0];\n\
esac;\n\
\n\n\
next(arr_rows[1]):=case\n\
next(state) = calc_cons: arr_rows[1];\n\
next(state) = correct: arr_rows[1];\n\
next(state) = guess & state = calc_cons:row_options[0];\n\
TRUE:arr_rows[1];\n\
esac;\n\
\n\n\
next(arr_cols[1]):=case\n\
next(state) = calc_cons: arr_cols[1];\n\
next(state) = correct: arr_cols[1];\n\
next(state) = guess & state = calc_cons:col_options[3];\n\
TRUE:arr_cols[1];\n\
esac;\n\
\n\n\
next(arr_dis[1]):=0;\n\
\n\n\
next(arr_rows[2]):=case\n\
next(state) = calc_cons: arr_rows[2];\n\
next(state) = correct: arr_rows[2];\n\
next(state) = guess & state = calc_cons:row_options[0];\n\
TRUE:arr_rows[2];\n\
esac;\n\
\n\n\
next(arr_cols[2]):=case\n\
next(state) = calc_cons: arr_cols[2];\n\
next(state) = correct: arr_cols[2];\n\
next(state) = guess & state = calc_cons:col_options[5];\n\
TRUE:arr_cols[2];\n\
esac;\n\
\n\n\
next(arr_dis[2]):=case\n\
next(state) = calc_cons: arr_dis[2];\n\
next(state) = correct: arr_dis[2];\n\
next(state) = guess & state = calc_cons & next(arr_cols[2]) = 3: 0;\n\
next(state) = guess & state = calc_cons & next(arr_cols[2]) = 4: 2;\n\
TRUE:arr_dis[2];\n\
esac;\n\
\n\n\
next(arr_rows[3]):=case\n\
next(state) = calc_cons: arr_rows[3];\n\
next(state) = correct: arr_rows[3];\n\
next(state) = guess & state = calc_cons:row_options[1];\n\
TRUE:arr_rows[3];\n\
esac;\n\
\n\n\
next(arr_cols[3]):=1;\n\
\n\
next(arr_dis[3]):=case\n\
next(state) = calc_cons: arr_dis[3];\n\
next(state) = correct: arr_dis[3];\n\
next(state) = guess & state = calc_cons & next(arr_rows[3]) = 1: 1;\n\
next(state) = guess & state = calc_cons & next(arr_rows[3]) = 2: 0;\n\
TRUE:arr_dis[3];\n\
esac;\n\
\n\n\
next(arr_rows[4]):=case\n\
next(state) = calc_cons: arr_rows[4];\n\
next(state) = correct: arr_rows[4];\n\
next(state) = guess & state = calc_cons:row_options[1];\n\
TRUE:arr_rows[4];\n\
esac;\n\
\n\n\
next(arr_dis[4]):=case\n\
next(state) = calc_cons: arr_dis[4];\n\
next(state) = correct: arr_dis[4];\n\
next(state) = guess & state = calc_cons & next(arr_rows[4]) = 2: 1;\n\
next(state) = guess & state = calc_cons & next(arr_rows[4]) = 1: 0;\n\
TRUE:arr_dis[4];\n\
esac;\n\
\n\n\
next(arr_cols[4]):=2;\n\
\n\n\
next(arr_rows[5]):=case\n\
next(state) = calc_cons: arr_rows[5];\n\
next(state) = correct: arr_rows[5];\n\
next(state) = guess & state = calc_cons:row_options[1];\n\
TRUE:arr_rows[5];\n\
esac;\n\
\n\n\
next(arr_cols[5]):=3;\n\
\n\n\
next(arr_dis[5]):=case\n\
next(state) = calc_cons: arr_dis[5];\n\
next(state) = correct: arr_dis[5];\n\
next(state) = guess & state = calc_cons & next(arr_rows[5]) = 2: 2;\n\
next(state) = guess & state = calc_cons & next(arr_rows[5]) = 1: 0;\n\
TRUE:arr_dis[5];\n\
esac;\n\
\n\n\
next(arr_rows[6]):=case\n\
next(state) = calc_cons: arr_rows[6];\n\
next(state) = correct: arr_rows[6];\n\
next(state) = guess & state = calc_cons:row_options[1];\n\
TRUE:arr_rows[6];\n\
esac;\n\
\n\n\
next(arr_cols[6]):=4;\n\
\n\n\
next(arr_dis[6]):=case\n\
next(state) = calc_cons: arr_dis[6];\n\
next(state) = correct: arr_dis[6];\n\
next(state) = guess & state = calc_cons & next(arr_rows[6]) = 1: 2;\n\
next(state) = guess & state = calc_cons & next(arr_rows[6]) = 2: 0;\n\
TRUE:arr_dis[6];\n\
esac;\n\
\n\n\
next(arr_rows[7]):=case\n\
next(state) = calc_cons: arr_rows[7];\n\
next(state) = correct: arr_rows[7];\n\
next(state) = guess & state = calc_cons:row_options[2];\n\
TRUE:arr_rows[7];\n\
esac;\n\
\n\n\
next(arr_cols[7]):=case\n\
next(state) = calc_cons: arr_cols[7];\n\
next(state) = correct: arr_cols[7];\n\
next(state) = guess & state = calc_cons:col_options[1];\n\
TRUE:arr_cols[7];\n\
esac;\n\
\n\n\
next(arr_dis[7]):=case\n\
next(state) = calc_cons: arr_dis[7];\n\
next(state) = correct: arr_dis[7];\n\
next(state) = guess & state = calc_cons & next(arr_cols[7]) = 1: 0;\n\
next(state) = guess & state = calc_cons & next(arr_cols[7]) = 2: 1;\n\
TRUE:arr_dis[7];\n\
esac;\n\
\n\n\
next(arr_rows[8]):=case\n\
next(state) = calc_cons: arr_rows[8];\n\
next(state) = correct: arr_rows[8];\n\
next(state) = guess & state = calc_cons:row_options[2];\n\
TRUE:arr_rows[8];\n\
esac;\n\
\n\n\
next(arr_cols[8]):=case\n\
next(state) = calc_cons: arr_cols[8];\n\
next(state) = correct: arr_cols[8];\n\
next(state) = guess & state = calc_cons:col_options[3];\n\
TRUE:arr_cols[8];\n\
esac;\n\
\n\n\
next(arr_dis[8]):=case\n\
next(state) = calc_cons: arr_dis[8];\n\
next(state) = correct: arr_dis[8];\n\
next(state) = guess & state = calc_cons & next(arr_cols[8]) = 2: 1;\n\
next(state) = guess & state = calc_cons & next(arr_cols[8]) = 3: 2;\n\
TRUE:arr_dis[8];\n\
esac;\n\
\n\n\
next(arr_rows[9]):=case\n\
next(state) = calc_cons: arr_rows[9];\n\
next(state) = correct: arr_rows[9];\n\
next(state) = guess & state = calc_cons:row_options[2];\n\
TRUE:arr_rows[9];\n\
esac;\n\
\n\n\
next(arr_cols[9]):=case\n\
next(state) = calc_cons: arr_cols[9];\n\
next(state) = correct: arr_cols[9];\n\
next(state) = guess & state = calc_cons:col_options[5];\n\
TRUE:arr_cols[9];\n\
esac;\n\
\n\n\
next(arr_dis[9]):=case\n\
next(state) = calc_cons: arr_dis[9];\n\
next(state) = correct: arr_dis[9];\n\
next(state) = guess & state = calc_cons & next(arr_cols[9]) = 3: 2;\n\
next(state) = guess & state = calc_cons & next(arr_cols[9]) = 4: 0;\n\
TRUE:arr_dis[9];\n\
esac;\n\
\n\n\
next(arr_rows[10]):=case\n\
next(state) = calc_cons: arr_rows[10];\n\
next(state) = correct: arr_rows[10];\n\
next(state) = guess & state = calc_cons:row_options[3];\n\
TRUE:arr_rows[10];\n\
esac;\n\
\n\n\
next(arr_cols[10]):=1;\n\
\n\n\
next(arr_dis[10]):=0;\n\
\n\n\
next(arr_rows[11]):=case\n\
next(state) = calc_cons: arr_rows[11];\n\
next(state) = correct: arr_rows[11];\n\
next(state) = guess & state = calc_cons:row_options[3];\n\
TRUE:arr_rows[11];\n\
esac;\n\
\n\n\
next(arr_cols[11]):=2;\n\
\n\n\
next(arr_dis[11]):=case\n\
next(state) = calc_cons: arr_dis[11];\n\
next(state) = correct: arr_dis[11];\n\
next(state) = guess & state = calc_cons & next(arr_rows[11]) = 2: 1;\n\
next(state) = guess & state = calc_cons & next(arr_rows[11]) = 3: 2;\n\
TRUE:arr_dis[11];\n\
esac;\n\
\n\n\
next(arr_rows[12]):=case\n\
next(state) = calc_cons: arr_rows[12];\n\
next(state) = correct: arr_rows[12];\n\
next(state) = guess & state = calc_cons:row_options[3];\n\
TRUE:arr_rows[12];\n\
esac;\n\
\n\n\
next(arr_cols[12]):=3;\n\
\n\n\
next(arr_dis[12]):=case\n\
next(state) = calc_cons: arr_dis[12];\n\
next(state) = correct: arr_dis[12];\n\
next(state) = guess & state = calc_cons & next(arr_rows[12]) = 2: 2;\n\
next(state) = guess & state = calc_cons & next(arr_rows[12]) = 3: 1;\n\
TRUE:arr_dis[12];\n\
esac;\n\
\n\n\
next(arr_rows[13]):=case\n\
next(state) = calc_cons: arr_rows[13];\n\
next(state) = correct: arr_rows[13];\n\
next(state) = guess & state = calc_cons:row_options[3];\n\
TRUE:arr_rows[13];\n\
esac;\n\
\n\n\
next(arr_cols[13]):=4;\n\
\n\n\
next(arr_dis[13]):=0;\n\
\n\n\
next(arr_rows[14]):=case\n\
next(state) = calc_cons: arr_rows[14];\n\
next(state) = correct: arr_rows[14];\n\
next(state) = guess & state = calc_cons:row_options[4];\n\
TRUE:arr_rows[14];\n\
esac;\n\
\n\n\
next(arr_cols[14]):=case\n\
next(state) = calc_cons: arr_cols[14];\n\
next(state) = correct: arr_cols[14];\n\
next(state) = guess & state = calc_cons:col_options[1];\n\
TRUE:arr_cols[14];\n\
esac;\n\
\n\n\
next(arr_dis[14]):=case\n\
next(state) = calc_cons: arr_dis[14];\n\
next(state) = correct: arr_dis[14];\n\
next(state) = guess & state = calc_cons & next(arr_cols[14]) = 1: 0;\n\
next(state) = guess & state = calc_cons & next(arr_cols[14]) = 2: 2;\n\
TRUE:arr_dis[14];\n\
esac;\n\
\n\n\
next(arr_rows[15]):=case\n\
next(state) = calc_cons: arr_rows[15];\n\
next(state) = correct: arr_rows[15];\n\
next(state) = guess & state = calc_cons:row_options[4];\n\
TRUE:arr_rows[15];\n\
esac;\n\
\n\n\
next(arr_cols[15]):=case\n\
next(state) = calc_cons: arr_cols[15];\n\
next(state) = correct: arr_cols[15];\n\
next(state) = guess & state = calc_cons:col_options[3];\n\
TRUE:arr_cols[15];\n\
esac;\n\
\n\n\
next(arr_dis[15]):=case\n\
next(state) = calc_cons: arr_dis[15];\n\
next(state) = correct: arr_dis[15];\n\
next(state) = guess & state = calc_cons & next(arr_cols[15]) = 2: 2;\n\
next(state) = guess & state = calc_cons & next(arr_cols[15]) = 3: 1;\n\
TRUE:arr_dis[15];\n\
esac;\n\
\n\n\
next(arr_rows[16]):=case\n\
next(state) = calc_cons: arr_rows[16];\n\
next(state) = correct: arr_rows[16];\n\
next(state) = guess & state = calc_cons:row_options[4];\n\
TRUE:arr_rows[16];\n\
esac;\n\
\n\n\
next(arr_cols[16]):=case\n\
next(state) = calc_cons: arr_cols[16];\n\
next(state) = correct: arr_cols[16];\n\
next(state) = guess & state = calc_cons:col_options[5];\n\
TRUE:arr_cols[16];\n\
esac;\n\
\n\n\
next(arr_dis[16]):=case\n\
next(state) = calc_cons: arr_dis[16];\n\
next(state) = correct: arr_dis[16];\n\
next(state) = guess & state = calc_cons & next(arr_cols[16]) = 3: 1;\n\
next(state) = guess & state = calc_cons & next(arr_cols[16]) = 4: 0;\n\
TRUE:arr_dis[16];\n\
esac;\n\
\n\n\
next(arr_rows[17]):=case\n\
next(state) = calc_cons: arr_rows[17];\n\
next(state) = correct: arr_rows[17];\n\
next(state) = guess & state = calc_cons:row_options[5];\n\
TRUE:arr_rows[17];\n\
esac;\n\
\n\n\
next(arr_cols[17]):=1;\n\
\n\n\
next(arr_dis[17]):=case\n\
next(state) = calc_cons: arr_dis[17];\n\
next(state) = correct: arr_dis[17];\n\
next(state) = guess & state = calc_cons & next(arr_rows[17]) = 3: 0;\n\
next(state) = guess & state = calc_cons & next(arr_rows[17]) = 4: 2;\n\
TRUE:arr_dis[17];\n\
esac;\n\
\n\n\
next(arr_rows[18]):=case\n\
next(state) = calc_cons: arr_rows[18];\n\
next(state) = correct: arr_rows[18];\n\
next(state) = guess & state = calc_cons:row_options[5];\n\
TRUE:arr_rows[18];\n\
esac;\n\
\n\n\
next(arr_cols[18]):=2;\n\
\n\n\
next(arr_dis[18]):=case\n\
next(state) = calc_cons: arr_dis[18];\n\
next(state) = correct: arr_dis[18];\n\
next(state) = guess & state = calc_cons & next(arr_rows[18]) = 3: 2;\n\
next(state) = guess & state = calc_cons & next(arr_rows[18]) = 4: 0;\n\
TRUE:arr_dis[18];\n\
esac;\n\
\n\n\
next(arr_rows[19]):=case\n\
next(state) = calc_cons: arr_rows[19];\n\
next(state) = correct: arr_rows[19];\n\
next(state) = guess & state = calc_cons:row_options[5];\n\
TRUE:arr_rows[19];\n\
esac;\n\
\n\n\
next(arr_cols[19]):=3;\n\
\n\n\
next(arr_dis[19]):=case\n\
next(state) = calc_cons: arr_dis[19];\n\
next(state) = correct: arr_dis[19];\n\
next(state) = guess & state = calc_cons & next(arr_rows[19]) = 3: 1;\n\
next(state) = guess & state = calc_cons & next(arr_rows[19]) = 4: 0;\n\
TRUE:arr_dis[19];\n\
esac;\n\
\n\n\
next(arr_rows[20]):=case\n\
next(state) = calc_cons: arr_rows[20];\n\
next(state) = correct: arr_rows[20];\n\
next(state) = guess & state = calc_cons:row_options[5];\n\
TRUE:arr_rows[20];\n\
esac;\n\
\n\n\
next(arr_cols[20]):=4;\n\
\n\n\
next(arr_dis[20]):=case\n\
next(state) = calc_cons: arr_dis[20];\n\
next(state) = correct: arr_dis[20];\n\
next(state) = guess & state = calc_cons & next(arr_cols[20]) = 4: 1;\n\
next(state) = guess & state = calc_cons & next(arr_cols[20]) = 3: 0;\n\
TRUE:arr_dis[20];\n\
esac;\n\
\n\n\
next(arr_rows[21]):=case\n\
next(state) = calc_cons: arr_rows[21];\n\
next(state) = correct: arr_rows[21];\n\
next(state) = guess & state = calc_cons:row_options[6];\n\
TRUE:arr_rows[21];\n\
esac;\n\
\n\n\
next(arr_cols[21]):=case\n\
next(state) = calc_cons: arr_cols[21];\n\
next(state) = correct: arr_cols[21];\n\
next(state) = guess & state = calc_cons:col_options[1];\n\
TRUE:arr_cols[21];\n\
esac;\n\
\n\n\
next(arr_dis[21]):=case\n\
next(state) = calc_cons: arr_dis[21];\n\
next(state) = correct: arr_dis[21];\n\
next(state) = guess & state = calc_cons & next(arr_cols[21]) = 1: 2;\n\
next(state) = guess & state = calc_cons & next(arr_cols[21]) = 2: 0;\n\
TRUE:arr_dis[21];\n\
esac;\n\
\n\n\
next(arr_rows[22]):=case\n\
next(state) = calc_cons: arr_rows[22];\n\
next(state) = correct: arr_rows[22];\n\
next(state) = guess & state = calc_cons:row_options[6];\n\
TRUE:arr_rows[22];\n\
esac;\n\
\n\n\
next(arr_cols[22]):=case\n\
next(state) = calc_cons: arr_cols[22];\n\
next(state) = correct: arr_cols[22];\n\
next(state) = guess & state = calc_cons:col_options[3];\n\
TRUE:arr_cols[22];\n\
esac;\n\
\n\n\
next(arr_dis[22]):=0;\n\
\n\n\
next(arr_rows[23]):=case\n\
next(state) = calc_cons: arr_rows[23];\n\
next(state) = correct: arr_rows[23];\n\
next(state) = guess & state = calc_cons:row_options[6];\n\
TRUE:arr_rows[23];\n\
esac;\n\
\n\n\
next(arr_cols[23]):=case\n\
next(state) = calc_cons: arr_cols[23];\n\
next(state) = correct: arr_cols[23];\n\
next(state) = guess & state = calc_cons:col_options[5];\n\
TRUE:arr_cols[23];\n\
esac;\n\
\n\n\
next(arr_dis[23]):=case\n\
next(state) = calc_cons: arr_dis[23];\n\
next(state) = correct: arr_dis[23];\n\
next(state) = guess & state = calc_cons & next(arr_cols[23]) = 4: 1;\n\
next(state) = guess & state = calc_cons & next(arr_cols[23]) = 3: 0;\n\
TRUE:arr_dis[23];\n\
esac;\n\
\n\n\
next(count_row1):=case\n\
!(finished_count) & state = calc_cons & arr_rows[row1] = 1 & row1 < 7: (count_row1+1)mod(15) ;\n\
state = guess: 0;\n\
TRUE: count_row1;\n\
esac;\n\
\n\n\
next(count_row2):=case\n\
!(finished_count) & state = calc_cons & arr_rows[row2] = 2 & row2 < 14: (count_row2+1)mod(15) ;\n\
state = guess: 0;\n\
TRUE: count_row2;\n\
esac;\n\
\n\n\
next(count_row3):=case\n\
!(finished_count) & state = calc_cons & arr_rows[row3] = 3 & row3 < 21: (count_row3+1)mod(15) ;\n\
state = guess: 0;\n\
TRUE: count_row3;\n\
esac;\n\
\n\n\
next(count_row4):=case\n\
!(finished_count) & state = calc_cons & arr_rows[row4] = 4 & row4 < 24: (count_row4+1)mod(15) ;\n\
state = guess: 0;\n\
TRUE: count_row4;\n\
esac;\n\
\n\n\
next(count_col1):=case\n\
!(finished_count) & state = calc_cons & arr_cols[col1] = 1 & col1 < 22: (count_col1+1)mod(15) ;\n\
state = guess: 0;\n\
TRUE: count_col1;\n\
esac;\n\
\n\n\
next(count_col2):=case\n\
!(finished_count) & state = calc_cons & arr_cols[col2] = 2 & col2 < 23: (count_col2+1)mod(15) ;\n\
state = guess: 0;\n\
TRUE: count_col2;\n\
esac;\n\
\n\n\
next(count_col3):=case\n\
!(finished_count) & state = calc_cons & arr_cols[col3] = 3 & col3 < 24: (count_col3+1)mod(15) ;\n\
state = guess: 0;\n\
TRUE: count_col3;\n\
esac;\n\
\n\n\
next(count_col4):=case\n\
!(finished_count) & state = calc_cons & arr_cols[col4] = 4 & col4 < 24: (count_col4+1)mod(15) ;\n\
state = guess: 0;\n\
TRUE: count_col4;\n\
esac;\n\
\n\n\
next(count_di1):=case\n\
!(finished_count) & state = calc_cons & arr_dis[di1] = 1 & di1 < 24: (count_di1+1)mod(11) ;\n\
state = guess: 0;\n\
TRUE: count_di1;\n\
esac;\n\
\n\n\
next(count_di2):=case\n\
!(finished_count) & state = calc_cons & arr_dis[di2] = 2 & di2 < 22: (count_di2+1)mod(11) ;\n\
state = guess: 0;\n\
TRUE: count_di2;\n\
esac;\n\
\n\n\
/--need to count cols and dis--/\n\
LTLSPEC\n\
G !(state = correct)"


def solve_rid_input(j, match_rows, match_cols, match_dis):
    """
    This function gets:
    :param j: a starting index for input/output files
    :param match_rows: integers input array - the rows that the matchsticks point to (must be 1 - 4)
    :param match_cols: integers input array - the columns that the matchsticks point to (must be 1 - 4)
    :param match_dis: integers input array - the diagonals that the matchsticks point to (must be 1 - 2, 0:
     no diagonal was pointed by this match)

     It solves the riddle

    :return: flag_solved - 1: no solution, 2: solved
    run_time - execution time
    times - if the input is invalid: -1
    """
    flag_solved = 0
    run_time = -1
    times = read_sq_riddle(match_rows, match_cols, match_dis, j)
    if times != -1:
        flag_solved, run_time = find_solution(j)
    return times, flag_solved, run_time


def solve_rid_input_gen(j):
    flag_solved = 0
    run_time = -1
    times, flag_solved, run_time, arr_rows, arr_cols, arr_dis, old_rows, old_cols, old_dis = (0, 0, 0, [], [], [], [], [], [])
    times = write_gen_model(j)
    if times != -1:
        flag_solved, run_time = find_solution(j)
        arr_rows, arr_cols, arr_dis, old_rows, old_cols, old_dis = find_info(j, True)
    return times, flag_solved, run_time, arr_rows, arr_cols, arr_dis, old_rows, old_cols, old_dis


def solve_rid(j):
    """
    This function gets:
    :param j: a starting index for input/output files

    This function chooses randomly:

    :param match_rows: integers input array - the rows that the matchsticks point to (must be 1 - 4)
    :param match_cols: integers input array - the columns that the matchsticks point to (must be 1 - 4)
    :param match_dis: integers input array - the diagonals that the matchsticks point to (must be 1 - 2, 0:
     no diagonal was pointed by this match)

     It solves the riddle

    :return: flag_solved - 1: no solution, 2: solved
    run_time - execution time
    times - if the input is invalid: -1
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
           row = random.randint(1,2)
        if 7 <= i <= 9:
            row = 2
        if 10 <= i <= 13:
            row = random.randint(2,3)
        if 14 <= i <= 16:
           row = 3
        if 17 <= i <= 20:
            row = random.randint(3,4)
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
            col = random.randint(1, 2)
        if i % 7 == 1:
            col = random.randint(2, 3)
        if i % 7 == 2:
            col = random.randint(3, 4)
        match_cols.append(col)
        if i == 1 or i == 10 or i == 13 or i == 22:
            di = 0
        if i == 8 or i == 11 or i == 12 or i == 15:
            di = random.randint(1, 2)
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
    flag_solved = 0
    run_time = -1
    times = read_sq_riddle(match_rows, match_cols, match_dis, j)
    if times != -1:
        flag_solved, run_time = find_solution(j)
    return times, flag_solved, run_time


def read_sq_riddle(match_rows, match_cols, match_dis, j):
    """
       this function: gets a riddle
       encodes the riddle in NuSMV and runs NuSMV to find a solution
       writes the NuSMV output in a file
       """
    if check_valid(match_rows, match_cols, match_dis):
        return write_model(match_rows, match_cols, match_dis, j)
    else:
        return -1


def check_valid(match_rows, match_cols, match_dis):
    """

    This function gets:

    :param match_rows: integers input array - the rows that the matchsticks point to (must be 1 - 4)
    :param match_cols: integers input array - the columns that the matchsticks point to (must be 1 - 4)
    :param match_dis: integers input array - the diagonals that the matchsticks point to (must be 1 - 2, 0:
     no diagonal was pointed by this match)

    :return: True - the input is valid, False otherwise

    """
    row_options = [[1], [1, 2], [2], [2, 3], [3], [3, 4], [4]]
    col_options = [[1, 2], [2, 3], [3, 4], [1], [2], [3], [4]]
    di_options = [[0, 1], [0], [0, 2], [1, 2]]
    if len(match_cols) != 24 or len(match_dis) != 24 or len(match_rows) != 24:
        return False
    for i in range(0, 24):
        if 0 <= i <= 2:
            if match_rows[i] not in row_options[0]:
                return False
        if 3 <= i <= 6:
            if match_rows[i] not in row_options[1]:
                return False
        if 7 <= i <= 9:
            if match_rows[i] not in row_options[2]:
                return False
        if 10 <= i <= 13:
            if match_rows[i] not in row_options[3]:
                return False
        if 14 <= i <= 16:
            if match_rows[i] not in row_options[4]:
                return False
        if 17 <= i <= 20:
            if match_rows[i] not in row_options[5]:
                return False
        if 21 <= i <= 23:
            if match_rows[i] not in row_options[6]:
                return False
        if i % 7 == 3 and match_cols[i] != col_options[3][0]:
            return False
        if i % 7 == 4 and match_cols[i] != col_options[4][0]:
            return False
        if i % 7 == 5 and match_cols[i] != col_options[5][0]:
            return False
        if i % 7 == 6 and match_cols[i] != col_options[6][0]:
            return False
        if i % 7 == 0 and match_cols[i] not in col_options[0]:
            return False
        if i % 7 == 1 and match_cols[i] not in col_options[1]:
            return False
        if i % 7 == 2 and match_cols[i] not in col_options[2]:
            return False
        if (i == 1 or i == 10 or i == 13 or i == 22) and match_dis[i] != di_options[1][0]:
            return False

        if i == 8 or i == 11 or i == 12 or i == 15:
            if match_dis[i] not in di_options[3]:
                return False
            else:
                if not check_di(match_rows, match_cols, match_dis, i):
                    return False

        if i in [0, 3, 4, 7, 16, 19, 20, 23]:
            if match_dis[i] not in di_options[0]:
                return False
            else:
                if not check_di(match_rows, match_cols, match_dis, i):
                    return False

        if i in [2, 5, 6, 9, 14, 17, 18, 21]:
            if match_dis[i] not in di_options[2]:
                return False
            else:
                if not check_di(match_rows, match_cols, match_dis, i):
                    return False

    return True


def check_di(match_rows, match_cols, match_dis, k):
    if k == 1 or k == 10 or k == 13 or k == 22:
        return True
    else:
        if match_rows[k] == match_cols[k] and match_dis[k] != 1:
            return False
        if match_rows[k] == 5 - match_cols[k] and match_dis[k] != 2:
            return False
    return True

def write_gen_model(j):
    text = """
MODULE main
        /--state variables--/
        VAR
        count_row1:0..14;
        count_row2:0..14;
        count_row3:0..14;
        count_row4:0..14;
        count_col1:0..14;
        count_col2:0..14;
        count_col3:0..14;
        count_col4:0..14;
        count_di1:0..10;
        count_di2:0..10;
        num_allowed:0..14;
        row1: 0..7;
        row2: 3..14;
        row3: 10..21;
        row4: 17..24;
        rows_equal: boolean;
        cols_equal: boolean;
        dis_equal: boolean;
        finished_count: boolean;
        col1: {0,3,7,10,14,17,21,22};
        col2: {0,1,4,7,8,11,14,15,18,21,22,23};
        col3: {1,2,5,8,9,12,15,16,19,22,23,24};
        col4: {2,6,9,13,16,20,23,24};
        di1: {0,3,4,7,8,11,12,15,16,19,20,23,24};
        di2: {2,5,6,8,9,11,12,15,14,17,18,21,22};
        arr_rows:array 0..23 of 1..4;
        arr_cols:array 0..23 of 1..4;
        arr_dis:array 0..23 of 0..2;
		match_rows:array 0..23 of 1..4;
        match_cols:array 0..23 of 1..4;
        match_dis:array 0..23 of 0..2;
        state:{initial, calc_cons, correct, guess};
DEFINE
            row_options:=[1,{1,2},2,{2,3},3,{3,4},4];
            col_options:=row_options;
            di_options:=[0,{0,1},{0,2},{1,2}];
ASSIGN
        init(finished_count):=FALSE;
        init(count_row1):=0;
        init(count_row2):=0;
        init(count_row3):=0;
        init(count_row4):=0;
        init(count_col1):=0;
        init(count_col2):=0;
        init(count_col3):=0;
        init(count_col4):=0;
        init(count_di1):=0;
        init(count_di2):=0;
        init(row1):=0;
        init(row2):=3;
        init(row3):=10;
        init(row4):=17;
        init(col1):=0;
        init(col2):=0;
        init(col3):=1;
        init(col4):=2;
        init(di1):=0;
        init(di2):=2;
        init(num_allowed):=6;
        init(arr_rows):=match_rows;
        init(arr_cols):=match_cols;
        init(arr_dis):=match_dis;
        init(state):=initial;
init(match_rows[0]):=row_options[0];
init(match_rows[1]):=row_options[0];
init(match_rows[2]):=row_options[0];
init(match_rows[3]):=row_options[1];
init(match_rows[4]):=row_options[1];
init(match_rows[5]):=row_options[1];
init(match_rows[6]):=row_options[1];
init(match_rows[7]):=row_options[2];
init(match_rows[8]):=row_options[2];
init(match_rows[9]):=row_options[2];
init(match_rows[10]):=row_options[3];
init(match_rows[11]):=row_options[3];
init(match_rows[12]):=row_options[3];
init(match_rows[13]):=row_options[3];
init(match_rows[14]):=row_options[4];
init(match_rows[15]):=row_options[4];
init(match_rows[16]):=row_options[4];
init(match_rows[17]):=row_options[5];
init(match_rows[18]):=row_options[5];
init(match_rows[19]):=row_options[5];
init(match_rows[20]):=row_options[5];
init(match_rows[21]):=row_options[6];
init(match_rows[22]):=row_options[6];
init(match_rows[23]):=row_options[6];
init(match_cols[0]):=col_options[1];
init(match_cols[1]):=col_options[3];
init(match_cols[2]):=col_options[5];
init(match_cols[3]):=col_options[0];
init(match_cols[4]):=col_options[2];
init(match_cols[5]):=col_options[4];
init(match_cols[6]):=col_options[6];
init(match_cols[7]):=col_options[1];
init(match_cols[8]):=col_options[3];
init(match_cols[9]):=col_options[5];
init(match_cols[10]):=col_options[0];
init(match_cols[11]):=col_options[2];
init(match_cols[12]):=col_options[4];
init(match_cols[13]):=col_options[6];
init(match_cols[14]):=col_options[1];
init(match_cols[15]):=col_options[3];
init(match_cols[16]):=col_options[5];
init(match_cols[17]):=col_options[0];
init(match_cols[18]):=col_options[2];
init(match_cols[19]):=col_options[4];
init(match_cols[20]):=col_options[6];
init(match_cols[21]):=col_options[1];
init(match_cols[22]):=col_options[3];
init(match_cols[23]):=col_options[5];
init(match_dis[0]):=case
match_cols[0] = 1: 1;
match_cols[0] = 2: 0;
esac;
init(match_dis[1]):=0;
init(match_dis[2]):=case
match_cols[2] = 3: 0;
match_cols[2] = 4: 2;
esac;
init(match_dis[3]):=case
match_rows[3] = 1: 1;
match_rows[3] = 2: 0;
esac;
init(match_dis[4]):=case
match_rows[4] = 2: 1;
match_rows[4] = 1: 0;
esac;
init(match_dis[5]):=case
match_rows[5] = 2: 2;
match_rows[5] = 1: 0;
esac;
init(match_dis[6]):=case
match_rows[6] = 1: 2;
match_rows[6] = 2: 0;
esac;
init(match_dis[7]):=case
match_cols[7] = 1: 0;
match_cols[7] = 2: 1;
esac;
init(match_dis[8]):=case
match_cols[8] = 2: 1;
match_cols[8] = 3: 2;
esac;
init(match_dis[9]):=case
match_cols[9] = 3: 2;
match_cols[9] = 4: 0;
esac;
init(match_dis[10]):=0;
init(match_dis[11]):=case
match_rows[11] = 2: 1;
match_rows[11] = 3: 2;
esac;
init(match_dis[12]):=case
match_rows[12] = 2: 2;
match_rows[12] = 3: 1;
esac;
init(match_dis[13]):=0;
init(match_dis[14]):=case
match_cols[14] = 1: 0;
match_cols[14] = 2: 2;
esac;
init(match_dis[15]):=case
match_cols[15] = 2: 2;
match_cols[15] = 3: 1;
esac;
init(match_dis[16]):=case
match_cols[16] = 3: 1;
match_cols[16] = 4: 0;
esac;
init(match_dis[17]):=case
match_rows[17] = 3: 0;
match_rows[17] = 4: 2;
esac;
init(match_dis[18]):=case
match_rows[18] = 3: 2;
match_rows[18] = 4: 0;
esac;
init(match_dis[19]):=case
match_rows[19] = 3: 1;
match_rows[19] = 4: 0;
esac;
init(match_dis[20]):=case
match_rows[20] = 4: 1;
match_rows[20] = 3: 0;
esac;
init(match_dis[21]):=case
match_cols[21] = 1: 2;
match_cols[21] = 2: 0;
esac;
init(match_dis[22]):=0;
init(match_dis[23]):=case
match_cols[23] = 4: 1;
match_cols[23] = 3: 0;
esac;
        init(rows_equal):=count_row1 = num_allowed & count_row2 = num_allowed & count_row3 = num_allowed & count_row4 = num_allowed;
        init(cols_equal):=count_col1 = num_allowed & count_col2 = num_allowed & count_col3 = num_allowed & count_col4 = num_allowed;
        init(dis_equal):=count_di1 = num_allowed & count_di2 = num_allowed;
		next(match_rows[0]):=match_rows[0];
next(match_rows[1]):=match_rows[1];
next(match_rows[2]):=match_rows[2];
next(match_rows[3]):=match_rows[3];
next(match_rows[4]):=match_rows[4];
next(match_rows[5]):=match_rows[5];
next(match_rows[6]):=match_rows[6];
next(match_rows[7]):=match_rows[7];
next(match_rows[8]):=match_rows[8];
next(match_rows[9]):=match_rows[9];
next(match_rows[10]):=match_rows[10];
next(match_rows[11]):=match_rows[11];
next(match_rows[12]):=match_rows[12];
next(match_rows[13]):=match_rows[13];
next(match_rows[14]):=match_rows[14];
next(match_rows[15]):=match_rows[15];
next(match_rows[16]):=match_rows[16];
next(match_rows[17]):=match_rows[17];
next(match_rows[18]):=match_rows[18];
next(match_rows[19]):=match_rows[19];
next(match_rows[20]):=match_rows[20];
next(match_rows[21]):=match_rows[21];
next(match_rows[22]):=match_rows[22];
next(match_rows[23]):=match_rows[23];
next(match_cols[0]):=match_cols[0];
next(match_cols[1]):=match_cols[1];
next(match_cols[2]):=match_cols[2];
next(match_cols[3]):=match_cols[3];
next(match_cols[4]):=match_cols[4];
next(match_cols[5]):=match_cols[5];
next(match_cols[6]):=match_cols[6];
next(match_cols[7]):=match_cols[7];
next(match_cols[8]):=match_cols[8];
next(match_cols[9]):=match_cols[9];
next(match_cols[10]):=match_cols[10];
next(match_cols[11]):=match_cols[11];
next(match_cols[12]):=match_cols[12];
next(match_cols[13]):=match_cols[13];
next(match_cols[14]):=match_cols[14];
next(match_cols[15]):=match_cols[15];
next(match_cols[16]):=match_cols[16];
next(match_cols[17]):=match_cols[17];
next(match_cols[18]):=match_cols[18];
next(match_cols[19]):=match_cols[19];
next(match_cols[20]):=match_cols[20];
next(match_cols[21]):=match_cols[21];
next(match_cols[22]):=match_cols[22];
next(match_cols[23]):=match_cols[23];
next(match_dis[0]):=match_dis[0];
next(match_dis[1]):=match_dis[1];
next(match_dis[2]):=match_dis[2];
next(match_dis[3]):=match_dis[3];
next(match_dis[4]):=match_dis[4];
next(match_dis[5]):=match_dis[5];
next(match_dis[6]):=match_dis[6];
next(match_dis[7]):=match_dis[7];
next(match_dis[8]):=match_dis[8];
next(match_dis[9]):=match_dis[9];
next(match_dis[10]):=match_dis[10];
next(match_dis[11]):=match_dis[11];
next(match_dis[12]):=match_dis[12];
next(match_dis[13]):=match_dis[13];
next(match_dis[14]):=match_dis[14];
next(match_dis[15]):=match_dis[15];
next(match_dis[16]):=match_dis[16];
next(match_dis[17]):=match_dis[17];
next(match_dis[18]):=match_dis[18];
next(match_dis[19]):=match_dis[19];
next(match_dis[20]):=match_dis[20];
next(match_dis[21]):=match_dis[21];
next(match_dis[22]):=match_dis[22];
next(match_dis[23]):=match_dis[23];
        next(finished_count) := row1 = 7 & row2 = 14 & row3 = 21 & row4 = 24 & col1 = 22 & col2 = 23 & col3 = 24 & col4 = 24 & di1 = 24 & di2 = 22;
        next(num_allowed):=num_allowed;
        next(state):=case
        finished_count & rows_equal & cols_equal & dis_equal: correct;
        state = calc_cons & next(finished_count) & !(next(rows_equal) & next(cols_equal) & next(dis_equal)): guess;
        state = guess & count_row1 != 0: guess;
        state = correct: correct;
        TRUE: calc_cons;
        esac;
        next(row1):=case
        state = calc_cons & next(state) = calc_cons & row1 < 7: (row1 + 1)mod(8);
        state = calc_cons & row1 = 7 & next(state) = calc_cons: 7;
        state = calc_cons & row1 = 7 & next(state) = guess: 0;
        state = calc_cons & row1 = 7 & next(state) = correct: 7;
        state = guess: 0;
        state = correct: 7;
        state = initial: 0;
        TRUE: 7;
        esac;
        next(row2):=case
        state = calc_cons & next(state) = calc_cons & row2 < 14: 4 + (row2 - 3)mod(11);
        state = calc_cons & row2 = 14 & next(state) = calc_cons: 14;
        state = calc_cons & row2 = 14 & next(state) = guess: 3;
        state = calc_cons & row2 = 14 & next(state) = correct: 14;
        state = guess: 3;
        state = correct: 14;
        state = initial: 3;
        TRUE: 14;
        esac;
        next(row3):=case
        state = calc_cons & next(state) = calc_cons & row3 < 21: 10 + (row3 - 9)mod(12);
        state = calc_cons & row3 = 21 & next(state) = calc_cons: 21;
        state = calc_cons & row3 = 21 & next(state) = guess: 10;
        state = calc_cons & row3 = 21 & next(state) = correct: 21;
        state = guess: 10;
        state = correct: 21;
        state = initial: 10;
        TRUE: 21;
        esac;
        next(row4):=case
        state = calc_cons & next(state) = calc_cons & row4 < 24: 17 + (row4 - 16)mod(8);
        state = calc_cons & row4 = 24 & next(state) = calc_cons: 24;
        state = calc_cons & row4 = 24 & next(state) = guess: 17;
        state = calc_cons & row4 = 24 & next(state) = correct: 24;
        state = guess: 17;
        state = correct: 24;
        state = initial: 17;
        TRUE: 24;
        esac;
        /--0,3,7,10,14,17,21,22--/
        next(col1):=case
        state = calc_cons & next(state) = calc_cons & col1 = 0: 3;
        state = calc_cons & next(state) = calc_cons & col1 = 3: 7;
        state = calc_cons & next(state) = calc_cons & col1 = 7: 10;
        state = calc_cons & next(state) = calc_cons & col1 = 10: 14;
        state = calc_cons & next(state) = calc_cons & col1 = 14: 17;
        state = calc_cons & next(state) = calc_cons & col1 = 17: 21;
        state = calc_cons & col1 = 21 & next(state) = calc_cons: 22;
        state = calc_cons & col1 = 22 & next(state) = guess: 0;
        state = calc_cons & col1 = 22 & next(state) = correct: 22;
        state = guess: 0;
        state = correct: 22;
        state = initial: 0;
        TRUE: 22;
        esac;
        /--0,1,4,7,8,11,14,15,18,21,22,23--/
        next(col2):=case
        state = calc_cons & next(state) = calc_cons & col2 = 0: 1;
        state = calc_cons & next(state) = calc_cons & col2 = 1: 4;
        state = calc_cons & next(state) = calc_cons & col2 = 4: 7;
        state = calc_cons & next(state) = calc_cons & col2 = 7: 8;
        state = calc_cons & next(state) = calc_cons & col2 = 8: 11;
        state = calc_cons & next(state) = calc_cons & col2 = 11: 14;
        state = calc_cons & next(state) = calc_cons & col2 = 14: 15;
        state = calc_cons & next(state) = calc_cons & col2 = 15: 18;
        state = calc_cons & next(state) = calc_cons & col2 = 18: 21;
        state = calc_cons & next(state) = calc_cons & col2 = 21: 22;
        state = calc_cons & col2 = 22 & next(state) = calc_cons: 23;
        state = calc_cons & col2 = 23 & next(state) = guess: 0;
        state = calc_cons & col2 = 23 & next(state) = correct: 23;
        state = guess: 0;
        state = correct: 23;
        state = initial: 0;
        TRUE: 23;
        esac;
        /--1,2,5,8,9,12,15,16,19,22,23,24--/
        next(col3):=case
        state = calc_cons & next(state) = calc_cons & col3 = 1: 2;
        state = calc_cons & next(state) = calc_cons & col3 = 2: 5;
        state = calc_cons & next(state) = calc_cons & col3 = 5: 8;
        state = calc_cons & next(state) = calc_cons & col3 = 8: 9;
        state = calc_cons & next(state) = calc_cons & col3 = 9: 12;
        state = calc_cons & next(state) = calc_cons & col3 = 12: 15;
        state = calc_cons & next(state) = calc_cons & col3 = 15: 16;
        state = calc_cons & next(state) = calc_cons & col3 = 16: 19;
        state = calc_cons & next(state) = calc_cons & col3 = 19: 22;
        state = calc_cons & next(state) = calc_cons & col3 = 22: 23;
        state = calc_cons & col3 = 23 & next(state) = calc_cons: 24;
        state = calc_cons & col3 = 24 & next(state) = guess: 1;
        state = calc_cons & col3 = 24 & next(state) = correct: 24;
        state = guess: 1;
        state = correct: 24;
        state = initial: 1;
        TRUE: 24;
        esac;
        /--2,6,9,13,16,20,23,24--/
        next(col4):=case
        state = calc_cons & next(state) = calc_cons & col4 = 2: 6;
        state = calc_cons & next(state) = calc_cons & col4 = 6: 9;
        state = calc_cons & next(state) = calc_cons & col4 = 9: 13;
        state = calc_cons & next(state) = calc_cons & col4 = 13: 16;
        state = calc_cons & next(state) = calc_cons & col4 = 16: 20;
        state = calc_cons & next(state) = calc_cons & col4 = 20: 23;
        state = calc_cons & col4 = 23 & next(state) = calc_cons: 24;
        state = calc_cons & col4 = 24 & next(state) = guess: 2;
        state = calc_cons & col4 = 24 & next(state) = correct: 24;
        state = guess: 2;
        state = correct: 24;
        state = initial: 2;
        TRUE: 24;
        esac;
        /--0,3,4,7,8,11,12,15,16,19,20,23,24--/
        next(di1):=case
        state = calc_cons & next(state) = calc_cons & di1 = 0: 3;
        state = calc_cons & next(state) = calc_cons & di1 = 3: 4;
        state = calc_cons & next(state) = calc_cons & di1 = 4: 7;
        state = calc_cons & next(state) = calc_cons & di1 = 7: 8;
        state = calc_cons & next(state) = calc_cons & di1 = 8: 11;
        state = calc_cons & next(state) = calc_cons & di1 = 11: 12;
        state = calc_cons & next(state) = calc_cons & di1 = 12: 15;
        state = calc_cons & next(state) = calc_cons & di1 = 15: 16;
        state = calc_cons & next(state) = calc_cons & di1 = 16: 19;
        state = calc_cons & next(state) = calc_cons & di1 = 19: 20;
        state = calc_cons & next(state) = calc_cons & di1 = 20: 23;
        state = calc_cons & di1 = 23 & next(state) = calc_cons: 24;
        state = calc_cons & di1 = 24 & next(state) = guess: 0;
        state = calc_cons & di1 = 24 & next(state) = correct: 24;
        state = guess: 0;
        state = correct: 24;
        state = initial: 0;
        TRUE: 24;
        esac;
        /--2,5,6,8,9,11,12,14,15,17,18,21,22--/
        next(di2):=case
        state = calc_cons & next(state) = calc_cons & di2 = 2: 5;
        state = calc_cons & next(state) = calc_cons & di2 = 5: 6;
        state = calc_cons & next(state) = calc_cons & di2 = 6: 8;
        state = calc_cons & next(state) = calc_cons & di2 = 7: 8;
        state = calc_cons & next(state) = calc_cons & di2 = 8: 9;
        state = calc_cons & next(state) = calc_cons & di2 = 9: 11;
        state = calc_cons & next(state) = calc_cons & di2 = 11: 12;
        state = calc_cons & next(state) = calc_cons & di2 = 12: 14;
        state = calc_cons & next(state) = calc_cons & di2 = 14: 15;
        state = calc_cons & next(state) = calc_cons & di2 = 15: 17;
        state = calc_cons & next(state) = calc_cons & di2 = 17: 18;
        state = calc_cons & next(state) = calc_cons & di2 = 18: 21;
        state = calc_cons & di2 = 21 & next(state) = calc_cons: 22;
        state = calc_cons & di2 = 22 & next(state) = guess: 2;
        state = calc_cons & di2 = 22 & next(state) = correct: 22;
        state = guess: 2;
        state = correct: 22;
        state = initial: 2;
        TRUE: 22;
        esac;
        next(rows_equal):=next(count_row1) = next(num_allowed) & next(count_row2) = next(num_allowed) & next(count_row3) = next(num_allowed) & next(count_row4) = next(num_allowed);
        next(cols_equal):=next(count_col1) = next(num_allowed) & next(count_col2) = next(num_allowed) & next(count_col3) = next(num_allowed) & next(count_col4) = next(num_allowed);
        next(dis_equal):=next(count_di1) = next(num_allowed) & next(count_di2) = next(num_allowed);
        next(arr_rows[0]):=case
        next(state) = calc_cons: arr_rows[0];
        next(state) = correct: arr_rows[0];
        next(state) = guess & state = calc_cons:row_options[0];
        TRUE:arr_rows[0];
        esac;
        next(arr_cols[0]):=case
        next(state) = calc_cons: arr_cols[0];
        next(state) = correct: arr_cols[0];
        next(state) = guess & state = calc_cons:col_options[1];
        TRUE:arr_cols[0];
        esac;
        next(arr_dis[0]):=case
        next(state) = calc_cons: arr_dis[0];
        next(state) = correct: arr_dis[0];
        next(state) = guess & state = calc_cons & next(arr_cols[0]) = 1: 1;
        next(state) = guess & next(arr_cols[0]) = 2: 0;
        TRUE:arr_dis[0];
        esac;
        next(arr_rows[1]):=case
        next(state) = calc_cons: arr_rows[1];
        next(state) = correct: arr_rows[1];
        next(state) = guess & state = calc_cons:row_options[0];
        TRUE:arr_rows[1];
        esac;
        next(arr_cols[1]):=case
        next(state) = calc_cons: arr_cols[1];
        next(state) = correct: arr_cols[1];
        next(state) = guess & state = calc_cons:col_options[3];
        TRUE:arr_cols[1];
        esac;
        next(arr_dis[1]):=0;
        next(arr_rows[2]):=case
        next(state) = calc_cons: arr_rows[2];
        next(state) = correct: arr_rows[2];
        next(state) = guess & state = calc_cons:row_options[0];
        TRUE:arr_rows[2];
        esac;
        next(arr_cols[2]):=case
        next(state) = calc_cons: arr_cols[2];
        next(state) = correct: arr_cols[2];
        next(state) = guess & state = calc_cons:col_options[5];
        TRUE:arr_cols[2];
        esac;
        next(arr_dis[2]):=case
        next(state) = calc_cons: arr_dis[2];
        next(state) = correct: arr_dis[2];
        next(state) = guess & state = calc_cons & next(arr_cols[2]) = 3: 0;
        next(state) = guess & state = calc_cons & next(arr_cols[2]) = 4: 2;
        TRUE:arr_dis[2];
        esac;
        next(arr_rows[3]):=case
        next(state) = calc_cons: arr_rows[3];
        next(state) = correct: arr_rows[3];
        next(state) = guess & state = calc_cons:row_options[1];
        TRUE:arr_rows[3];
        esac;
        next(arr_cols[3]):=1;
        next(arr_dis[3]):=case
        next(state) = calc_cons: arr_dis[3];
        next(state) = correct: arr_dis[3];
        next(state) = guess & state = calc_cons & next(arr_rows[3]) = 1: 1;
        next(state) = guess & state = calc_cons & next(arr_rows[3]) = 2: 0;
        TRUE:arr_dis[3];
        esac;
        next(arr_rows[4]):=case
        next(state) = calc_cons: arr_rows[4];
        next(state) = correct: arr_rows[4];
        next(state) = guess & state = calc_cons:row_options[1];
        TRUE:arr_rows[4];
        esac;
        next(arr_dis[4]):=case
        next(state) = calc_cons: arr_dis[4];
        next(state) = correct: arr_dis[4];
        next(state) = guess & state = calc_cons & next(arr_rows[4]) = 2: 1;
        next(state) = guess & state = calc_cons & next(arr_rows[4]) = 1: 0;
        TRUE:arr_dis[4];
        esac;
        next(arr_cols[4]):=2;
        next(arr_rows[5]):=case
        next(state) = calc_cons: arr_rows[5];
        next(state) = correct: arr_rows[5];
        next(state) = guess & state = calc_cons:row_options[1];
        TRUE:arr_rows[5];
        esac;
        next(arr_cols[5]):=3;
        next(arr_dis[5]):=case
        next(state) = calc_cons: arr_dis[5];
        next(state) = correct: arr_dis[5];
        next(state) = guess & state = calc_cons & next(arr_rows[5]) = 2: 2;
        next(state) = guess & state = calc_cons & next(arr_rows[5]) = 1: 0;
        TRUE:arr_dis[5];
        esac;
        next(arr_rows[6]):=case
        next(state) = calc_cons: arr_rows[6];
        next(state) = correct: arr_rows[6];
        next(state) = guess & state = calc_cons:row_options[1];
        TRUE:arr_rows[6];
        esac;
        next(arr_cols[6]):=4;
        next(arr_dis[6]):=case
        next(state) = calc_cons: arr_dis[6];
        next(state) = correct: arr_dis[6];
        next(state) = guess & state = calc_cons & next(arr_rows[6]) = 1: 2;
        next(state) = guess & state = calc_cons & next(arr_rows[6]) = 2: 0;
        TRUE:arr_dis[6];
        esac;
        next(arr_rows[7]):=case
        next(state) = calc_cons: arr_rows[7];
        next(state) = correct: arr_rows[7];
        next(state) = guess & state = calc_cons:row_options[2];
        TRUE:arr_rows[7];
        esac;
        next(arr_cols[7]):=case
        next(state) = calc_cons: arr_cols[7];
        next(state) = correct: arr_cols[7];
        next(state) = guess & state = calc_cons:col_options[1];
        TRUE:arr_cols[7];
        esac;
        next(arr_dis[7]):=case
        next(state) = calc_cons: arr_dis[7];
        next(state) = correct: arr_dis[7];
        next(state) = guess & state = calc_cons & next(arr_cols[7]) = 1: 0;
        next(state) = guess & state = calc_cons & next(arr_cols[7]) = 2: 1;
        TRUE:arr_dis[7];
        esac;
        next(arr_rows[8]):=case
        next(state) = calc_cons: arr_rows[8];
        next(state) = correct: arr_rows[8];
        next(state) = guess & state = calc_cons:row_options[2];
        TRUE:arr_rows[8];
        esac;
        next(arr_cols[8]):=case
        next(state) = calc_cons: arr_cols[8];
        next(state) = correct: arr_cols[8];
        next(state) = guess & state = calc_cons:col_options[3];
        TRUE:arr_cols[8];
        esac;
        next(arr_dis[8]):=case
        next(state) = calc_cons: arr_dis[8];
        next(state) = correct: arr_dis[8];
        next(state) = guess & state = calc_cons & next(arr_cols[8]) = 2: 1;
        next(state) = guess & state = calc_cons & next(arr_cols[8]) = 3: 2;
        TRUE:arr_dis[8];
        esac;
        next(arr_rows[9]):=case
        next(state) = calc_cons: arr_rows[9];
        next(state) = correct: arr_rows[9];
        next(state) = guess & state = calc_cons:row_options[2];
        TRUE:arr_rows[9];
        esac;
        next(arr_cols[9]):=case
        next(state) = calc_cons: arr_cols[9];
        next(state) = correct: arr_cols[9];
        next(state) = guess & state = calc_cons:col_options[5];
        TRUE:arr_cols[9];
        esac;
        next(arr_dis[9]):=case
        next(state) = calc_cons: arr_dis[9];
        next(state) = correct: arr_dis[9];
        next(state) = guess & state = calc_cons & next(arr_cols[9]) = 3: 2;
        next(state) = guess & state = calc_cons & next(arr_cols[9]) = 4: 0;
        TRUE:arr_dis[9];
        esac;
        next(arr_rows[10]):=case
        next(state) = calc_cons: arr_rows[10];
        next(state) = correct: arr_rows[10];
        next(state) = guess & state = calc_cons:row_options[3];
        TRUE:arr_rows[10];
        esac;
        next(arr_cols[10]):=1;
        next(arr_dis[10]):=0;
        next(arr_rows[11]):=case
        next(state) = calc_cons: arr_rows[11];
        next(state) = correct: arr_rows[11];
        next(state) = guess & state = calc_cons:row_options[3];
        TRUE:arr_rows[11];
        esac;
        next(arr_cols[11]):=2;
        next(arr_dis[11]):=case
        next(state) = calc_cons: arr_dis[11];
        next(state) = correct: arr_dis[11];
        next(state) = guess & state = calc_cons & next(arr_rows[11]) = 2: 1;
        next(state) = guess & state = calc_cons & next(arr_rows[11]) = 3: 2;
        TRUE:arr_dis[11];
        esac;
        next(arr_rows[12]):=case
        next(state) = calc_cons: arr_rows[12];
        next(state) = correct: arr_rows[12];
        next(state) = guess & state = calc_cons:row_options[3];
        TRUE:arr_rows[12];
        esac;
        next(arr_cols[12]):=3;
        next(arr_dis[12]):=case
        next(state) = calc_cons: arr_dis[12];
        next(state) = correct: arr_dis[12];
        next(state) = guess & state = calc_cons & next(arr_rows[12]) = 2: 2;
        next(state) = guess & state = calc_cons & next(arr_rows[12]) = 3: 1;
        TRUE:arr_dis[12];
        esac;
        next(arr_rows[13]):=case
        next(state) = calc_cons: arr_rows[13];
        next(state) = correct: arr_rows[13];
        next(state) = guess & state = calc_cons:row_options[3];
        TRUE:arr_rows[13];
        esac;
        next(arr_cols[13]):=4;
        next(arr_dis[13]):=0;
        next(arr_rows[14]):=case
        next(state) = calc_cons: arr_rows[14];
        next(state) = correct: arr_rows[14];
        next(state) = guess & state = calc_cons:row_options[4];
        TRUE:arr_rows[14];
        esac;
        next(arr_cols[14]):=case
        next(state) = calc_cons: arr_cols[14];
        next(state) = correct: arr_cols[14];
        next(state) = guess & state = calc_cons:col_options[1];
        TRUE:arr_cols[14];
        esac;
        next(arr_dis[14]):=case
        next(state) = calc_cons: arr_dis[14];
        next(state) = correct: arr_dis[14];
        next(state) = guess & state = calc_cons & next(arr_cols[14]) = 1: 0;
        next(state) = guess & state = calc_cons & next(arr_cols[14]) = 2: 2;
        TRUE:arr_dis[14];
        esac;
        next(arr_rows[15]):=case
        next(state) = calc_cons: arr_rows[15];
        next(state) = correct: arr_rows[15];
        next(state) = guess & state = calc_cons:row_options[4];
        TRUE:arr_rows[15];
        esac;
        next(arr_cols[15]):=case
        next(state) = calc_cons: arr_cols[15];
        next(state) = correct: arr_cols[15];
        next(state) = guess & state = calc_cons:col_options[3];
        TRUE:arr_cols[15];
        esac;
        next(arr_dis[15]):=case
        next(state) = calc_cons: arr_dis[15];
        next(state) = correct: arr_dis[15];
        next(state) = guess & state = calc_cons & next(arr_cols[15]) = 2: 2;
        next(state) = guess & state = calc_cons & next(arr_cols[15]) = 3: 1;
        TRUE:arr_dis[15];
        esac;
        next(arr_rows[16]):=case
        next(state) = calc_cons: arr_rows[16];
        next(state) = correct: arr_rows[16];
        next(state) = guess & state = calc_cons:row_options[4];
        TRUE:arr_rows[16];
        esac;
        next(arr_cols[16]):=case
        next(state) = calc_cons: arr_cols[16];
        next(state) = correct: arr_cols[16];
        next(state) = guess & state = calc_cons:col_options[5];
        TRUE:arr_cols[16];
        esac;
        next(arr_dis[16]):=case
        next(state) = calc_cons: arr_dis[16];
        next(state) = correct: arr_dis[16];
        next(state) = guess & state = calc_cons & next(arr_cols[16]) = 3: 1;
        next(state) = guess & state = calc_cons & next(arr_cols[16]) = 4: 0;
        TRUE:arr_dis[16];
        esac;
        next(arr_rows[17]):=case
        next(state) = calc_cons: arr_rows[17];
        next(state) = correct: arr_rows[17];
        next(state) = guess & state = calc_cons:row_options[5];
        TRUE:arr_rows[17];
        esac;
        next(arr_cols[17]):=1;
        next(arr_dis[17]):=case
        next(state) = calc_cons: arr_dis[17];
        next(state) = correct: arr_dis[17];
        next(state) = guess & state = calc_cons & next(arr_rows[17]) = 3: 0;
        next(state) = guess & state = calc_cons & next(arr_rows[17]) = 4: 2;
        TRUE:arr_dis[17];
        esac;
        next(arr_rows[18]):=case
        next(state) = calc_cons: arr_rows[18];
        next(state) = correct: arr_rows[18];
        next(state) = guess & state = calc_cons:row_options[5];
        TRUE:arr_rows[18];
        esac;
        next(arr_cols[18]):=2;
        next(arr_dis[18]):=case
        next(state) = calc_cons: arr_dis[18];
        next(state) = correct: arr_dis[18];
        next(state) = guess & state = calc_cons & next(arr_rows[18]) = 3: 2;
        next(state) = guess & state = calc_cons & next(arr_rows[18]) = 4: 0;
        TRUE:arr_dis[18];
        esac;
        next(arr_rows[19]):=case
        next(state) = calc_cons: arr_rows[19];
        next(state) = correct: arr_rows[19];
        next(state) = guess & state = calc_cons:row_options[5];
        TRUE:arr_rows[19];
        esac;
        next(arr_cols[19]):=3;
        next(arr_dis[19]):=case
        next(state) = calc_cons: arr_dis[19];
        next(state) = correct: arr_dis[19];
        next(state) = guess & state = calc_cons & next(arr_rows[19]) = 3: 1;
        next(state) = guess & state = calc_cons & next(arr_rows[19]) = 4: 0;
        TRUE:arr_dis[19];
        esac;
        next(arr_rows[20]):=case
        next(state) = calc_cons: arr_rows[20];
        next(state) = correct: arr_rows[20];
        next(state) = guess & state = calc_cons:row_options[5];
        TRUE:arr_rows[20];
        esac;
        next(arr_cols[20]):=4;
        next(arr_dis[20]):=case
        next(state) = calc_cons: arr_dis[20];
        next(state) = correct: arr_dis[20];
        next(state) = guess & state = calc_cons & next(arr_cols[20]) = 4: 1;
        next(state) = guess & state = calc_cons & next(arr_cols[20]) = 3: 0;
        TRUE:arr_dis[20];
        esac;
        next(arr_rows[21]):=case
        next(state) = calc_cons: arr_rows[21];
        next(state) = correct: arr_rows[21];
        next(state) = guess & state = calc_cons:row_options[6];
        TRUE:arr_rows[21];
        esac;
        next(arr_cols[21]):=case
        next(state) = calc_cons: arr_cols[21];
        next(state) = correct: arr_cols[21];
        next(state) = guess & state = calc_cons:col_options[1];
        TRUE:arr_cols[21];
        esac;
        next(arr_dis[21]):=case
        next(state) = calc_cons: arr_dis[21];
        next(state) = correct: arr_dis[21];
        next(state) = guess & state = calc_cons & next(arr_cols[21]) = 1: 2;
        next(state) = guess & state = calc_cons & next(arr_cols[21]) = 2: 0;
        TRUE:arr_dis[21];
        esac; 
        next(arr_rows[22]):=case
        next(state) = calc_cons: arr_rows[22];
        next(state) = correct: arr_rows[22];
        next(state) = guess & state = calc_cons:row_options[6];
        TRUE:arr_rows[22];
        esac;
        next(arr_cols[22]):=case
        next(state) = calc_cons: arr_cols[22];
        next(state) = correct: arr_cols[22];
        next(state) = guess & state = calc_cons:col_options[3];
        TRUE:arr_cols[22];
        esac;
        next(arr_dis[22]):=0;
        next(arr_rows[23]):=case
        next(state) = calc_cons: arr_rows[23];
        next(state) = correct: arr_rows[23];
        next(state) = guess & state = calc_cons:row_options[6];
        TRUE:arr_rows[23];
        esac;
        next(arr_cols[23]):=case
        next(state) = calc_cons: arr_cols[23];
        next(state) = correct: arr_cols[23];
        next(state) = guess & state = calc_cons:col_options[5];
        TRUE:arr_cols[23];
        esac;
        next(arr_dis[23]):=case
        next(state) = calc_cons: arr_dis[23];
        next(state) = correct: arr_dis[23];
        next(state) = guess & state = calc_cons & next(arr_cols[23]) = 4: 1;
        next(state) = guess & state = calc_cons & next(arr_cols[23]) = 3: 0;
        TRUE:arr_dis[23];
        esac;
        next(count_row1):=case
        !(finished_count) & state = calc_cons & arr_rows[row1] = 1 & row1 < 7: (count_row1+1)mod(15) ;
        state = guess: 0;
        TRUE: count_row1;
        esac;
        next(count_row2):=case
        !(finished_count) & state = calc_cons & arr_rows[row2] = 2 & row2 < 14: (count_row2+1)mod(15) ;
        state = guess: 0;
        TRUE: count_row2;
        esac;
        next(count_row3):=case
        !(finished_count) & state = calc_cons & arr_rows[row3] = 3 & row3 < 21: (count_row3+1)mod(15) ;
        state = guess: 0;
        TRUE: count_row3;
        esac;
        next(count_row4):=case
        !(finished_count) & state = calc_cons & arr_rows[row4] = 4 & row4 < 24: (count_row4+1)mod(15) ;
        state = guess: 0;
        TRUE: count_row4;
        esac;
        next(count_col1):=case
        !(finished_count) & state = calc_cons & arr_cols[col1] = 1 & col1 < 22: (count_col1+1)mod(15) ;
        state = guess: 0;
        TRUE: count_col1;
        esac;
        next(count_col2):=case
        !(finished_count) & state = calc_cons & arr_cols[col2] = 2 & col2 < 23: (count_col2+1)mod(15) ;
        state = guess: 0;
        TRUE: count_col2;
        esac;
        next(count_col3):=case
        !(finished_count) & state = calc_cons & arr_cols[col3] = 3 & col3 < 24: (count_col3+1)mod(15) ;
        state = guess: 0;
        TRUE: count_col3;
        esac;
        next(count_col4):=case
        !(finished_count) & state = calc_cons & arr_cols[col4] = 4 & col4 < 24: (count_col4+1)mod(15) ;
        state = guess: 0;
        TRUE: count_col4;
        esac;
        next(count_di1):=case
        !(finished_count) & state = calc_cons & arr_dis[di1] = 1 & di1 < 24: (count_di1+1)mod(11) ;
        state = guess: 0;
        TRUE: count_di1;
        esac;
        next(count_di2):=case
        !(finished_count) & state = calc_cons & arr_dis[di2] = 2 & di2 < 22: (count_di2+1)mod(11) ;
        state = guess: 0;
        TRUE: count_di2;
        esac;
        /--need to count cols and dis--/
        LTLSPEC
        G !(state = guess & F state = correct)
    """
    os.chdir(r'C:\Users\liatw\OneDrive\Desktop\NuSMV-2.6.0-win64\bin')
    code = '''
j = ''' + str(j) + '''
text = """''' + text + '''"""
f = open('mat_h' + str(j) + '.smv', 'a')
print >> f, text
f.close()
'''
    build_time = timeit.timeit(code, number=1)
    run_model('mat_h' + str(j) + '.smv', j)
    return build_time


def write_model(match_rows, match_cols, match_dis, j):
    """
        This function writes the input into the model file indexed j.
        Then, it runs the model file in NuSMV
    """

    text_define = "DEFINE\n\
    row_options:=[1,{1,2},2,{2,3},3,{3,4},4];\n\
    col_options:=row_options;\n\
    di_options:=[0,{0,1},{0,2},{1,2}];\n\
    \n\n\
    match_rows:=" + str(match_rows) + ";\n\
    match_cols:=" + str(match_cols) + ";\n\
    match_dis:=" + str(match_dis) + ";"
    os.chdir(r'C:\Users\liatw\OneDrive\Desktop\NuSMV-2.6.0-win64\bin')
    code = '''
j = ''' + str(j) + '''
text_var = """''' + text_var + '''"""
text_define = """''' + text_define + '''"""
text_assign = """''' + text_assign + '''"""
f = open('mat_h' + str(j) + '.smv', 'a')
print >> f, text_var
print >> f, text_define
print >> f, text_assign
f.close()
'''
    build_time = timeit.timeit(code, number=1)
    run_model('mat_h' + str(j) + '.smv', j)
    return build_time


def run_model(file_model, j):
    """
        This function runs the model file indexed j with NuSMV and prints the results into the output file indexed j.
    """
    f = open(str(file_model), 'a')
    output_f = open('output_head' + str(j) + '.txt', 'a')
    subprocess.Popen("ptime.exe NuSMV.exe -bmc -bmc_length 31 " + str(file_model), stdout=output_f, stderr=output_f)
    output_f.close()
    f.close()


def find_solution(j):
    """
    This function reads the relevant file according to the operations
    It finds the solution in the file and prints it
    """
    f = open('output_head' + str(j) + '.txt', 'r')
    text = f.read()
    while "Execution time: " not in text:
        time.sleep(1)
        f = open('output_head' + str(j) + '.txt', 'r')
        text = f.read()
    run_str = (text.split("Execution time: "))[1].split(" s")[0]
    run_time = float(run_str)

    if 'is false' in text:
        f.close()
        return 2, run_time
    else:
        f.close()
        return 1, run_time


def find_info(j, find_input=False):
    """
        This function gets:
        j - index of an input/output file
        It returns the riddle's solution:
        arr_rows: integers input array - the rows that the matchsticks point to (must be 1 - 4)
        arr_cols: integers input array - the columns that the matchsticks point to (must be 1 - 4)
        arr_dis: integers input array - the diagonals that the matchsticks point to (must be 1 - 2, 0:
        no diagonal was pointed by this match)

    """
    f = open('output_head' + str(j) + '.txt', 'r')
    text = f.read()
    while "Execution time: " not in text:
        time.sleep(1)
        f = open('output_head' + str(j) + '.txt', 'r')
        text = f.read()

    rows = text.split('\n')
    list_rows_ind = []
    arr_rows = []
    list_cols_ind = []
    arr_cols = []
    list_dis_ind = []
    arr_dis = []
    list_rows2_ind = []
    old_rows = []
    list_cols2_ind = []
    old_cols = []
    list_dis2_ind = []
    old_dis = []

    for row in rows:
        if 'arr_rows' in row and 'specification' not in row:
            st, val = row.split(' = ')

            if st not in list_rows_ind:
                list_rows_ind.append(st)
                arr_rows.append(int(val))

            else:
                st = st.replace(']', '[')
                var, ind, var2 = st.split('[')
                arr_rows[int(ind)] = int(val)

        if 'arr_cols' in row and 'specification' not in row:
            st, val = row.split(' = ')

            if st not in list_cols_ind:
                list_cols_ind.append(st)
                arr_cols.append(int(val))

            else:
                st = st.replace(']', '[')
                var, ind, var2 = st.split('[')
                arr_cols[int(ind)] = int(val)

        if 'arr_dis' in row and 'specification' not in row:
            st, val = row.split(' = ')

            if st not in list_dis_ind:
                list_dis_ind.append(st)
                arr_dis.append(int(val))

            else:
                st = st.replace(']', '[')
                var, ind, var2 = st.split('[')
                arr_dis[int(ind)] = int(val)

        if 'match_rows' in row and 'specification' not in row:
            st, val = row.split(' = ')

            if st not in list_rows_ind:
                list_rows2_ind.append(st)
                old_rows.append(int(val))

            else:
                st = st.replace(']', '[')
                var, ind, var2 = st.split('[')
                old_rows[int(ind)] = int(val)

        if 'match_cols' in row and 'specification' not in row:
            st, val = row.split(' = ')

            if st not in list_cols_ind:
                list_cols2_ind.append(st)
                old_cols.append(int(val))

            else:
                st = st.replace(']', '[')
                var, ind, var2 = st.split('[')
                old_cols[int(ind)] = int(val)

        if 'match_dis' in row and 'specification' not in row:
            st, val = row.split(' = ')

            if st not in list_dis_ind:
                list_dis2_ind.append(st)
                old_dis.append(int(val))

            else:
                st = st.replace(']', '[')
                var, ind, var2 = st.split('[')
                old_dis[int(ind)] = int(val)

    if find_input:
        return arr_rows, arr_cols, arr_dis, old_rows, old_cols, old_dis
    else:
        return arr_rows, arr_cols, arr_dis


def calculate_avg(index):
    avg_build = 0
    avg_solved_run = 0
    avg_not_solved_run = 0
    count_solved = 0
    count_no_solution = 0

    for i in range(index, 1200000 + index):    # you can choose a different number than 1200000, this number depends on the
                                               # ratio between solved and no-solution riddles
                                               # it also depends on the number of measurements in the average
        times, flag_solved, run_time = solve_rid(i)
        # times: -1: invalid riddle, otherwise: valid.
        # flag_solved: 1 - no solution, 2 - solved, 0 - invalid
        # run_rime: riddle's execution time

        if times != -1:  # the riddle is valid
            avg_build = avg_build + times
            if flag_solved == 2:
                count_solved += 1
                avg_solved_run += run_time
            if flag_solved == 1:
                count_no_solution += 1
                avg_not_solved_run += run_time
            if count_solved == 20:  # number of measured solved cases
                break
    return avg_solved_run / count_solved


def main():
    os.chdir(r'C:\Users\liatw\OneDrive\Desktop\NuSMV-2.6.0-win64\bin')
    run_model('mat_h1.smv', 1)


if __name__ == '__main__':
    main()

