import copy
import os
import subprocess
import time
import timeit
import random
import check_close
import re


def read_riddle(i, shape, num_allowed): 
"""
This function gets a file index - i, a shape and the allowed number of matchsticks to add
It checks that the shape is a polygon. If it is - it encodes the riddle into a model file (with index i), else - it returns an error.
"""
    if check_valid(shape, num_allowed):
        return write_model_sq(i, shape, num_allowed) # in order to write a model file for the triangle area unit riddles - change this row to:
						     # write_model_tri(i, shape, num_allowed)
    else:
        return -1

# check if the input shape is a polygon
def check_valid(shape, num_allowed):
    return check_close.build_shape2(shape, build_dir(shape))


def write_model_sq(j, shape, num_allowed):
"""
This function gets a file index, the number of matchsticks for division and a shape (2D array)
It creates a model file of the riddle
Only basic area unit square is allowed here
"""
    half = str(len(shape) / 2 - 2)				# last index for storing the new part's original junctions (from the shape). There are len(shape) / 2 - 1 original junction indices for each part to store.
    half_1 = str(len(shape) / 2 - 1)				# first index for storing the new part's cut junctions (one matchstick is new, one matchstick is from the original shape). There are 2 junctions represented as [match1_index, ang1, match2_index] for each part to store.
    half_2 = str(len(shape) / 2)				# first index for storing the new part's new inner junctions (both matchsticks are new). There are num_allowed - 1 junctions represented as [match1_index, ang1, match2_index] for each part to store.
    half1_allowed = str(len(shape) / 2 - 1 + num_allowed)	# last index for storing the new part's cut junctions (one matchstick is new, one matchstick is from the original shape). There are 2 junctions represented as [match1_index, ang1, match2_index] for each part to store.
    half2_allowed = str(len(shape) / 2 - 2 + num_allowed)	# last index for storing the new part's new inner junctions (both matchsticks are new). There are num_allowed - 1 junctions represented as [match1_index, ang1, match2_index] for each part to store.
    last = str(len(shape) - 1)					# last original matchstick's index 
    text_var = """MODULE main

            VAR

            state:{initial, guess, calc_cons, correct};
            arr_junct_1: array 0..""" + half + """ of 0..""" + last + """;
            arr_junct_2: array 0..""" + half + """ of 0..""" + last + """;
            num_it: 0..""" + str(3 + len(shape) / 2 + num_allowed) + """;
            cuts1: array """ + half_1 + """..""" + half1_allowed + """ of array 0..2 of {90,180,0"""
    str_num = """"""
    for i in range(1, num_allowed + 1 + len(shape)):
        if i != 90 and i != 180 and i != 270:
            str_num += """,""" + str(i)

    str_new = """"""
    for i in range(len(shape) + 1, len(shape) + num_allowed + 1):
        if i != 90 and i != 180 and i != 270:
            str_new += """,""" + str(i)

    text_var += str_num + """};
        cuts2: array """ + half_1 + """..""" + half1_allowed + """ of array 0..2 of {90,180,0""" + str_num + """};
        """
    if len(shape) / 2 <= len(shape) / 2 - 2 + num_allowed:
        text_var += """inside1: array """ + half_2 + """..""" + half2_allowed + """ of array 0..2 of {90,180,270""" + str_new + """};
        inside2: array """ + half_2 + """..""" + half2_allowed + """ of array 0..2 of {90,180,270""" + str_new + """};
        """
    text_var += """
        equal1: boolean;
        equal2: boolean;
        legal: boolean;
        ind1: 0..""" + half1_allowed + """;
        ind2: 0..""" + half1_allowed + """;
        ind3: 0..""" + half1_allowed + """;
        init_ind1: 0..""" + half1_allowed + """;
        init_ind2: 0..""" + half1_allowed + """;
        finished: boolean; """

    text_define = """DEFINE	
        shape:=""" + str(shape) + """;
        cut_in:=[""" + """[""" + str(len(shape) + 1) + """,180,1]""" + str(
        """,[""" + str(len(shape) + 1) + """,180,1]""") * (len(shape) / 2 + num_allowed) + """];
        junct_in:=""" + str([1] * (len(shape) / 2 - 1)) + """;
        """
    if len(shape) / 2 <= len(shape) / 2 - 2 + num_allowed:
        text_define += """ins_in:=[""" + """[""" + str(len(shape) + 1) + """,180,""" + str(
            len(shape) + 2) + """]""" + str(
            """,[""" + str(len(shape) + 1) + """,180,""" + str(len(shape) + 2) + """]""") * (
                                   len(shape) / 2 - 2 + num_allowed) + """];
        """

    list_match = """"""
    for i in range(1, len(shape)):
        list_match += """, """ + str(i)

    text_assign = """ASSIGN
            """
    if len(shape) / 2 <= len(shape) / 2 - 2 + num_allowed:
        text_assign += """
            init(inside1):=ins_in;
            init(inside2):=ins_in;
            """
    text_assign += """init(arr_junct_1):=junct_in;
            init(arr_junct_2):=junct_in;
            init(cuts1):=cut_in;
            init(cuts2):=cut_in;
            init(state):=initial;
            init(ind1):= 0; 
            init(ind2):= 0; 
            init(ind3):=0;
            init(init_ind1):=0;
            init(init_ind2):= 0; 
            init(legal):=TRUE;
            init(equal1):=TRUE;
            init(equal2):=TRUE;
             init(num_it):=1;

            next(state):=case
            state = initial: guess; 
            state = guess: calc_cons;
            state = calc_cons & finished & (equal1 | equal2) & legal: correct;
            TRUE: calc_cons;
            esac;

             next(num_it):=(num_it + 1) mod (""" + str(3 + len(shape) / 2 + num_allowed + 1) + """);

            next(arr_junct_1[0]):=case
            next(state) = guess: {0""" + list_match + """};
            TRUE: arr_junct_1[0];
            esac;
        """
    for k in range(1, len(shape) / 2 - 1):
        text_assign += """next(arr_junct_1[""" + str(k) + """]):=case
            next(state) = guess: (next(arr_junct_1[""" + str(k - 1) + """]) + 1)mod(""" + str(len(shape)) + """);
            TRUE: arr_junct_1[""" + str(k) + """];
            esac;
            """

    text_assign += """next(arr_junct_2[0]):=case
            next(state) = guess: (next(arr_junct_1[""" + str(len(shape) / 2 - 2) + """]) + 2)mod(""" + str(len(shape)) + """);
            TRUE: arr_junct_2[0];
            esac;
            """

    for k in range(1, len(shape) / 2 - 1):
        text_assign += """next(arr_junct_2[""" + str(k) + """]):=case
                next(state) = guess: (next(arr_junct_2[""" + str(k - 1) + """]) + 1)mod(""" + str(len(shape)) + """);
                TRUE: arr_junct_2[""" + str(k) + """];
                esac;
                """

    list_options = """"""
    for l in range(0, len(shape) / 2 + num_allowed):
        list_options += str(l) + ","
    list_options = list_options[:-1]

    text_assign += """next(ind1):=case
                    state = initial: 0;
                                    state = guess & next(state) = calc_cons: next(init_ind1);
                                    state = calc_cons & !finished & ind1 < """ + half + """: (ind1 + 1)mod(""" + str(
        len(shape) / 2 + num_allowed) + """);
    								state = calc_cons & !finished & ind1 = """ + half + """ & cuts1[""" + half1_allowed + """][2] = (shape[(arr_junct_1[""" + half + """])mod(""" + str(
        len(shape)) + """)][2])mod(""" + str(len(shape) + 1) + """): """ + half1_allowed + """;
    								state = calc_cons & !finished & cuts1[""" + half1_allowed + """][2] = (shape[(arr_junct_1[""" + half + """])mod(""" + str(
        len(shape)) + """)][2])mod(""" + str(
        len(shape) + 1) + """) & ind1 > """ + half_1 + """ : (ind1 + """ + half1_allowed + """)mod(""" + str(
        len(shape) / 2 + num_allowed) + """);
    								state = calc_cons & !finished & cuts1[""" + half1_allowed + """][2] = (shape[(arr_junct_1[""" + half + """])mod(""" + str(
        len(shape)) + """)][2])mod(""" + str(len(shape) + 1) + """) & ind1 = """ + half_1 + """ : 0;
    								state = calc_cons & !finished & ind1 = """ + half + """ & cuts1[""" + half_1 + """][2] = (shape[(arr_junct_1[""" + half + """])mod(""" + str(
        len(shape)) + """)][2])mod(""" + str(len(shape) + 1) + """): """ + half_1 + """;
    								state = calc_cons & !finished & ind1 > """ + half + """ & cuts1[""" + half_1 + """][2] = (shape[(arr_junct_1[""" + half + """])mod(""" + str(
        len(shape)) + """)][2])mod(""" + str(len(shape) + 1) + """): (ind1 + 1)mod(""" + str(
        len(shape) / 2 + num_allowed) + """);
                                    state = calc_cons & next(state) = guess: 0;
                                    TRUE: ind1;
                                    esac;

                    next(ind3):=case
                    state = guess & next(state) = calc_cons: next(init_ind1);
                                    state = calc_cons & !finished & ind3 <= """ + half + """ & ind3 > 0: (ind3 + """ + half1_allowed + """)mod(""" + str(
        len(shape) / 2 + num_allowed) + """);
    								state = calc_cons & !finished & ind3 = 0 & cuts1[""" + half1_allowed + """][2] = (shape[(arr_junct_1[0])mod(""" + str(
        len(shape)) + """)][0])mod(""" + str(len(shape) + 1) + """): """ + half1_allowed + """;
    								state = calc_cons & !finished & cuts1[""" + half1_allowed + """][2] = (shape[(arr_junct_1[0])mod(""" + str(
        len(shape)) + """)][0])mod(""" + str(
        len(shape) + 1) + """) & ind3 > """ + half_1 + """ & ind3 < """ + half1_allowed + """ : (ind3 + 1)mod(""" + str(
        len(shape) / 2 + num_allowed) + """);
    								state = calc_cons & !finished & cuts1[""" + half1_allowed + """][2] = (shape[(arr_junct_1[0])mod(""" + str(
        len(shape)) + """)][0])mod(""" + str(len(shape) + 1) + """) & ind3 = """ + half1_allowed + """ : """ + half + """;
    								state = calc_cons & !finished & ind3 = 0 & cuts1[""" + half_1 + """][2] = (shape[(arr_junct_1[0])mod(""" + str(
        len(shape)) + """)][0])mod(""" + str(len(shape) + 1) + """): """ + half_1 + """;
    								state = calc_cons & !finished & ind3 >= """ + half_1 + """ & ind3 < """ + half1_allowed + """ & cuts1[""" + half_1 + """][2] = (shape[(arr_junct_1[0])mod(""" + str(
        len(shape)) + """)][0])mod(""" + str(len(shape) + 1) + """): (ind3 + 1)mod(""" + str(
        len(shape) / 2 + num_allowed) + """);
    								state = calc_cons & !finished & ind3 = """ + half1_allowed + """ & cuts1[""" + half_1 + """][2] = (shape[(arr_junct_1[0])mod(""" + str(
        len(shape)) + """)][0])mod(""" + str(len(shape) + 1) + """): """ + half + """;
                                    state = calc_cons & next(state) = guess: 0;
                                    TRUE: ind3;
                                    esac;

                    next(ind2):=case
                                    state = initial: 0;
                                    state = guess & next(state) = calc_cons: next(init_ind2);
                                    state = calc_cons & !finished & ind2 < """ + half + """: (ind2 + 1)mod(""" + str(
        len(shape) / 2 + num_allowed) + """);
    								state = calc_cons & !finished & ind2 = """ + half + """ & cuts2[""" + half1_allowed + """][2] = (shape[(arr_junct_2[""" + half + """])mod(""" + str(
        len(shape)) + """)][2])mod(""" + str(len(shape) + 1) + """): """ + half1_allowed + """;
    								state = calc_cons & !finished & cuts2[""" + half1_allowed + """][2] = (shape[(arr_junct_2[""" + half + """])mod(""" + str(
        len(shape)) + """)][2])mod(""" + str(
        len(shape) + 1) + """) & ind2 > """ + half_1 + """ : (ind2 + """ + half1_allowed + """)mod(""" + str(
        len(shape) / 2 + num_allowed) + """);
    								state = calc_cons & !finished & cuts2[""" + half1_allowed + """][2] = (shape[(arr_junct_2[""" + half + """])mod(""" + str(
        len(shape)) + """)][2])mod(""" + str(len(shape) + 1) + """) & ind2 = """ + half_1 + """ : 0;
    								state = calc_cons & !finished & ind2 = """ + half + """ & cuts2[""" + half_1 + """][2] = (shape[(arr_junct_2[""" + half + """])mod(""" + str(
        len(shape)) + """)][2])mod(""" + str(len(shape) + 1) + """): """ + half_1 + """;
    								state = calc_cons & !finished & ind2 > """ + half + """ & cuts2[""" + half_1 + """][2] = (shape[(arr_junct_2[""" + half + """])mod(""" + str(
        len(shape)) + """)][2])mod(""" + str(len(shape) + 1) + """): (ind2 + 1)mod(""" + str(
        len(shape) / 2 + num_allowed) + """);
                                    state = calc_cons & next(state) = guess: 0;
                                    TRUE: ind2;
                                    esac;

            next(init_ind1):=case
            state = initial: 0;
            state = guess & next(state) = calc_cons: {""" + list_options + """};
            state = calc_cons & next(state) = guess: 0;
            TRUE: init_ind1;
            esac;

            next(init_ind2):=case
            state = initial: 0;
            state = guess & next(state) = calc_cons: {""" + list_options + """};
            state = calc_cons & next(state) = guess: 0;
            TRUE: init_ind2;
            esac;

            next(finished):= num_it = """ + str(3 + len(shape) / 2 + num_allowed - 1) + """;

            next(equal1):=case
            state = calc_cons & next(state) = calc_cons & ind1 <= """ + str(
        len(shape) / 2 - 2) + """ & ind2 <= """ + str(len(shape) / 2 - 2) + """: equal1 & shape[arr_junct_1[ind1]][1] = shape[arr_junct_2[ind2]][1];
            state = calc_cons & next(state) = calc_cons & ind1 <= """ + str(
        len(shape) / 2 - 2) + """ & ind2 = """ + str(
        len(shape) / 2 - 1) + """: equal1 & shape[arr_junct_1[ind1]][1] = cuts2[""" + half_1 + """][1];
            """
    if len(shape) / 2 <= len(shape) / 2 - 2 + num_allowed:
        text_assign += """state = calc_cons & next(state) = calc_cons & ind1 <= """ + half + """ & ind2 > """ + str(
            len(shape) / 2 - 1) + """ & ind2 < """ + half1_allowed + """ : equal1 & shape[arr_junct_1[ind1]][1] = inside2[ind2][1];
            """

    text_assign += """state = calc_cons & next(state) = calc_cons & ind1 <= """ + half + """ & ind2 = """ + half1_allowed + """: equal1 & shape[arr_junct_1[ind1]][1] = cuts2[""" + half1_allowed + """][1];

            state = calc_cons & next(state) = calc_cons & ind1 = """ + half_1 + """ & ind2 <= """ + half + """: equal1 & shape[arr_junct_2[ind2]][1] = cuts1[""" + half_1 + """][1];
            state = calc_cons & next(state) = calc_cons & ind1 = """ + half_1 + """ & ind2 = """ + half_1 + """: equal1 & cuts1[""" + half_1 + """][1] = cuts2[""" + half_1 + """][1];
        """
    if len(shape) / 2 <= len(shape) / 2 - 2 + num_allowed:
        text_assign += """state = calc_cons & next(state) = calc_cons & ind1 = """ + half_1 + """ & ind2 > """ + half_1 + """ & ind2 < """ + half1_allowed + """: equal1 & cuts1[""" + half_1 + """][1] = inside2[ind2][1];
            """
    text_assign += """state = calc_cons & next(state) = calc_cons & ind1 = """ + half_1 + """ & ind2 = """ + half1_allowed + """: equal1 & cuts1[""" + half_1 + """][1] = cuts2[""" + half1_allowed + """][1];
        """
    if len(shape) / 2 <= len(shape) / 2 - 2 + num_allowed:
        text_assign += """state = calc_cons & next(state) = calc_cons & ind1 > """ + half_1 + """ & ind1 < """ + half1_allowed + """ & ind2 <= """ + half + """: equal1 & shape[arr_junct_2[ind2]][1] = inside1[ind1][1];
            state = calc_cons & next(state) = calc_cons & ind1 > """ + half_1 + """ & ind1 < """ + half1_allowed + """ & ind2 = """ + half_1 + """: equal1 & cuts2[""" + half_1 + """][1] = inside1[ind1][1];
            state = calc_cons & next(state) = calc_cons & ind1 > """ + half_1 + """ & ind1 < """ + half1_allowed + """ & ind2 > """ + half_1 + """ & ind2 < """ + half1_allowed + """: equal1 & inside1[ind1][1] = inside2[ind2][1];
            state = calc_cons & next(state) = calc_cons & ind1 > """ + half_1 + """ & ind1 < """ + half1_allowed + """ & ind2 = """ + half1_allowed + """: equal1 & inside1[ind1][1] = cuts2[""" + half1_allowed + """][1];
            """
    text_assign += """
            state = calc_cons & next(state) = calc_cons & ind1 = """ + half1_allowed + """ & ind2 <= """ + half + """: equal1 & shape[arr_junct_2[ind2]][1] = cuts1[""" + half1_allowed + """][1];
            state = calc_cons & next(state) = calc_cons & ind1 = """ + half1_allowed + """ & ind2 = """ + half_1 + """: equal1 & cuts1[""" + half1_allowed + """][1] = cuts2[""" + half_1 + """][1];
            """
    if len(shape) / 2 <= len(shape) / 2 - 2 + num_allowed:
        text_assign += """state = calc_cons & next(state) = calc_cons & ind1 = """ + half1_allowed + """ & ind2 > """ + half_1 + """ & ind2 < """ + half1_allowed + """: equal1 & cuts1[""" + half1_allowed + """][1] = inside2[ind2][1];
            """
    text_assign += """state = calc_cons & next(state) = calc_cons & ind1 = """ + half1_allowed + """ & ind2 = """ + half1_allowed + """: equal1 & cuts1[""" + half1_allowed + """][1] = cuts2[""" + half1_allowed + """][1];
            next(state) = guess: TRUE;
            TRUE: equal1;
            esac;

            next(equal2):=case
            state = calc_cons & next(state) = calc_cons & ind3 <= """ + half + """ & ind2 <= """ + half + """: equal2 & shape[arr_junct_1[ind3]][1] = shape[arr_junct_2[ind2]][1];
            state = calc_cons & next(state) = calc_cons & ind3 <= """ + half + """ & ind2 = """ + half_1 + """: equal2 & shape[arr_junct_1[ind3]][1] = cuts2[""" + half_1 + """][1];
        """
    if len(shape) / 2 <= len(shape) / 2 - 2 + num_allowed:
        text_assign += """state = calc_cons & next(state) = calc_cons & ind3 <= """ + half + """ & ind2 > """ + half_1 + """ & ind2 < """ + half1_allowed + """: equal2 & shape[arr_junct_1[ind3]][1] = inside2[ind2][1];
            """
    text_assign += """state = calc_cons & next(state) = calc_cons & ind3 <= """ + half + """ & ind2 = """ + half1_allowed + """: equal2 & shape[arr_junct_1[ind3]][1] = cuts2[""" + half1_allowed + """][1];

            state = calc_cons & next(state) = calc_cons & ind3 = """ + half_1 + """ & ind2 <= """ + half + """: equal2 & shape[arr_junct_2[ind2]][1] = cuts1[""" + half_1 + """][1];
            state = calc_cons & next(state) = calc_cons & ind3 = """ + half_1 + """ & ind2 = """ + half_1 + """: equal2 & cuts1[""" + half_1 + """][1] = cuts2[""" + half_1 + """][1];
            """
    if len(shape) / 2 <= len(shape) / 2 - 2 + num_allowed:
        text_assign += """state = calc_cons & next(state) = calc_cons & ind3 = """ + half_1 + """ & ind2 > """ + half_1 + """ & ind2 < """ + half1_allowed + """: equal2 & cuts1[""" + half_1 + """][1] = inside2[ind2][1];
            """
    text_assign += """state = calc_cons & next(state) = calc_cons & ind3 = """ + half_1 + """ & ind2 = """ + half1_allowed + """: equal2 & cuts1[""" + half_1 + """][1] = cuts2[""" + half1_allowed + """][1];
            """
    if len(shape) / 2 <= len(shape) / 2 - 2 + num_allowed:
        text_assign += """state = calc_cons & next(state) = calc_cons & ind3 > """ + half_1 + """ & ind3 < """ + half1_allowed + """ & ind2 <= """ + half + """: equal2 & shape[arr_junct_2[ind2]][1] = inside1[ind3][1];
            state = calc_cons & next(state) = calc_cons & ind3 > """ + half_1 + """ & ind3 < """ + half1_allowed + """ & ind2 = """ + half_1 + """: equal2 & cuts2[""" + half_1 + """][1] = inside1[ind3][1];
            state = calc_cons & next(state) = calc_cons & ind3 > """ + half_1 + """ & ind3 < """ + half1_allowed + """ & ind2 > """ + half_1 + """ & ind2 < """ + half1_allowed + """: equal2 & inside1[ind3][1] = inside2[ind2][1];
            state = calc_cons & next(state) = calc_cons & ind3 > """ + half_1 + """ & ind3 < """ + half1_allowed + """ & ind2 = """ + half1_allowed + """: equal2 & inside1[ind3][1] = cuts2[""" + half1_allowed + """][1];
            """
    text_assign += """state = calc_cons & next(state) = calc_cons & ind3 = """ + half1_allowed + """ & ind2 <= """ + half + """: equal2 & shape[arr_junct_2[ind2]][1] = cuts1[""" + half1_allowed + """][1];
            state = calc_cons & next(state) = calc_cons & ind3 = """ + half1_allowed + """ & ind2 = """ + half_1 + """: equal2 & cuts1[""" + half1_allowed + """][1] = cuts2[""" + half_1 + """][1];
            """
    if len(shape) / 2 <= len(shape) / 2 - 2 + num_allowed:
        text_assign += """state = calc_cons & next(state) = calc_cons & ind3 = """ + half1_allowed + """ & ind2 > """ + half_1 + """ & ind2 < """ + half1_allowed + """: equal2 & cuts1[""" + half1_allowed + """][1] = inside2[ind2][1];
            """
    text_assign += """
            state = calc_cons & next(state) = calc_cons & ind3 = """ + half1_allowed + """ & ind2 = """ + half1_allowed + """: equal2 & cuts1[""" + half1_allowed + """][1] = cuts2[""" + half1_allowed + """][1];
            next(state) = guess: TRUE;
            TRUE: equal2;
            esac;

            next(cuts1[""" + half_1 + """][0]):=""" + str(len(shape) + 1) + """;
            next(cuts1[""" + half1_allowed + """][0]):=""" + str(len(shape) + num_allowed) + """;

            next(cuts2[""" + half_1 + """][0]):=""" + str(len(shape) + 1) + """;
            next(cuts2[""" + half1_allowed + """][0]):=""" + str(len(shape) + num_allowed) + """;


            next(cuts1[""" + half_1 + """][2]):=next(shape[arr_junct_1[0]][0]);
            next(cuts1[""" + half1_allowed + """][2]):=next(shape[arr_junct_1[""" + half + """]][2]);

            next(cuts2[""" + half_1 + """][2]):=next(shape[arr_junct_2[""" + half + """]][2]);
            next(cuts2[""" + half1_allowed + """][2]):=next(shape[arr_junct_2[0]][0]);

    next(cuts1[""" + half_1 + """][1]) := case

            next(state) = guess & ((next(cuts1[""" + half_1 + """][2]))mod(""" + str(
        len(shape) + 1) + """) > (next(cuts2[""" + half_1 + """][2]))mod(""" + str(len(
        shape) + 1) + """) & !(next(cuts1[""" + half_1 + """][2]) = 1 & next(cuts2[""" + half_1 + """][2]) = """ + str(
        len(shape)) + """) | next(cuts1[""" + half_1 + """][2]) = 1 & next(cuts2[""" + half_1 + """][2]) = """ + str(
        len(shape)) + """) & next(shape[(abs(cuts2[""" + half_1 + """][2] + """ + str(
        len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) = 270: {90, 180};

            next(state) = guess & ((next(cuts1[""" + half_1 + """][2]))mod(""" + str(
        len(shape) + 1) + """) > (next(cuts2[""" + half_1 + """][2]))mod(""" + str(len(
        shape) + 1) + """) & !(next(cuts1[""" + half_1 + """][2]) = 1 & next(cuts2[""" + half_1 + """][2]) = """ + str(
        len(shape)) + """) | next(cuts1[""" + half_1 + """][2]) = 1 & next(cuts2[""" + half_1 + """][2]) = """ + str(
        len(shape)) + """) & next(shape[(abs(cuts2[""" + half_1 + """][2] + """ + str(
        len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) = 180: 90;


            next(state) = guess & ((next(cuts1[""" + half_1 + """][2]))mod(""" + str(
        len(shape) + 1) + """) <= (next(cuts2[""" + half_1 + """][2]))mod(""" + str(
        len(shape) + 1) + """)  & !(next(cuts1[""" + half_1 + """][2]) = """ + str(
        len(shape)) + """ & next(cuts2[""" + half_1 + """][2]) = 1) | next(cuts1[""" + half_1 + """][2]) = """ + str(
        len(
            shape)) + """ & next(cuts2[""" + half_1 + """][2]) = 1) & next(shape[(abs(cuts1[""" + half_1 + """][2] + """ + str(
        len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) = 180: 90;

            next(state) = guess & ((next(cuts1[""" + half_1 + """][2]))mod(""" + str(
        len(shape) + 1) + """) <= (next(cuts2[""" + half_1 + """][2]))mod(""" + str(
        len(shape) + 1) + """)  & !(next(cuts1[""" + half_1 + """][2]) = """ + str(
        len(shape)) + """ & next(cuts2[""" + half_1 + """][2]) = 1) | next(cuts1[""" + half_1 + """][2]) = """ + str(
        len(
            shape)) + """ & next(cuts2[""" + half_1 + """][2]) = 1) & next(shape[(abs(cuts1[""" + half_1 + """][2] + """ + str(
        len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) = 270: {90, 180};

            next(state) = calc_cons | next(state) = correct: cuts1[""" + half_1 + """][1];
            TRUE: 0;
            esac;

            next(cuts2[""" + half_1 + """][1]) := case

            next(state) = guess & ((next(cuts1[""" + half_1 + """][2]))mod(""" + str(
        len(shape) + 1) + """) > (next(cuts2[""" + half_1 + """][2]))mod(""" + str(len(
        shape) + 1) + """) & !(next(cuts1[""" + half_1 + """][2]) = 1 & next(cuts2[""" + half_1 + """][2]) = """ + str(
        len(shape)) + """)| next(cuts1[""" + half_1 + """][2]) = 1 & next(cuts2[""" + half_1 + """][2]) = """ + str(
        len(shape)) + """): next(shape[(abs(cuts2[""" + half_1 + """][2] + """ + str(
        len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) - next(cuts1[""" + half_1 + """][1]);

            next(state) = guess & ((next(cuts1[""" + half_1 + """][2]))mod(""" + str(
        len(shape) + 1) + """) <= (next(cuts2[""" + half_1 + """][2]))mod(""" + str(
        len(shape) + 1) + """) & !(next(cuts1[""" + half_1 + """][2]) = """ + str(
        len(shape)) + """ & next(cuts1[""" + half_1 + """][2]) = 1) | next(cuts1[""" + half_1 + """][2]) = """ + str(
        len(
            shape)) + """ & next(cuts2[""" + half_1 + """][2]) = 1): next(shape[(abs(cuts1[""" + half_1 + """][2] + """ + str(
        len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) - next(cuts1[""" + half_1 + """][1]);

            next(state) = calc_cons | next(state) = correct: cuts2[""" + half_1 + """][1];
            TRUE: 0;
            esac;

            next(cuts1[""" + half1_allowed + """][1]) := case

            next(state) = guess & ((next(cuts1[""" + half1_allowed + """][2]))mod(""" + str(
        len(shape) + 1) + """) > (next(cuts2[""" + half1_allowed + """][2]))mod(""" + str(len(
        shape) + 1) + """) & !(next(cuts1[""" + half1_allowed + """][2]) = 1 & next(cuts2[""" + half1_allowed + """][2]) = """ + str(
        len(
            shape)) + """)| next(cuts1[""" + half1_allowed + """][2]) = 1 & next(cuts2[""" + half1_allowed + """][2]) = """ + str(
        len(shape)) + """)& next(shape[(abs(cuts2[""" + half1_allowed + """][2] + """ + str(
        len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) = 270: {90, 180};

            next(state) = guess & ((next(cuts1[""" + half1_allowed + """][2]))mod(""" + str(
        len(shape) + 1) + """) > (next(cuts2[""" + half1_allowed + """][2]))mod(""" + str(len(
        shape) + 1) + """) & !(next(cuts1[""" + half1_allowed + """][2]) = 1 & next(cuts2[""" + half1_allowed + """][2]) = """ + str(
        len(
            shape)) + """)| next(cuts1[""" + half1_allowed + """][2]) = 1 & next(cuts2[""" + half1_allowed + """][2]) = """ + str(
        len(shape)) + """)& next(shape[(abs(cuts2[""" + half1_allowed + """][2] + """ + str(
        len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) = 180: 90;


            next(state) = guess & ((next(cuts1[""" + half1_allowed + """][2]))mod(""" + str(
        len(shape) + 1) + """) <= (next(cuts2[""" + half1_allowed + """][2]))mod(""" + str(
        len(shape) + 1) + """) & !(next(cuts1[""" + half1_allowed + """][2]) = """ + str(len(
        shape)) + """ & next(cuts2[""" + half1_allowed + """][2]) = 1)| next(cuts1[""" + half1_allowed + """][2]) = """ + str(
        len(
            shape)) + """ & next(cuts2[""" + half1_allowed + """][2]) = 1)& next(shape[(abs(cuts1[""" + half1_allowed + """][2] + """ + str(
        len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) = 180: 90;

            next(state) = guess & ((next(cuts1[""" + half1_allowed + """][2]))mod(""" + str(
        len(shape) + 1) + """) <= (next(cuts2[""" + half1_allowed + """][2]))mod(""" + str(
        len(shape) + 1) + """) & !(next(cuts1[""" + half1_allowed + """][2]) = """ + str(len(
        shape)) + """ & next(cuts2[""" + half1_allowed + """][2]) = 1)| next(cuts1[""" + half1_allowed + """][2]) = """ + str(
        len(
            shape)) + """ & next(cuts2[""" + half1_allowed + """][2]) = 1)& next(shape[(abs(cuts1[""" + half1_allowed + """][2] + """ + str(
        len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) = 270: {90, 180};

            next(state) = calc_cons | next(state) = correct: cuts1[""" + half1_allowed + """][1];
            TRUE: 0;
            esac;

            next(cuts2[""" + half1_allowed + """][1]) := case
            next(state) = guess & ((next(cuts1[""" + half1_allowed + """][2]))mod(""" + str(
        len(shape) + 1) + """) > (next(cuts2[""" + half1_allowed + """][2]))mod(""" + str(len(
        shape) + 1) + """) & !(next(cuts1[""" + half1_allowed + """][2]) = 1 & next(cuts2[""" + half1_allowed + """][2]) = """ + str(
        len(
            shape)) + """)| next(cuts1[""" + half1_allowed + """][2]) = 1 & next(cuts2[""" + half1_allowed + """][2]) = """ + str(
        len(shape)) + """): next(shape[(abs(cuts2[""" + half1_allowed + """][2] + """ + str(
        len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) - next(cuts1[""" + half1_allowed + """][1]);

            next(state) = guess & ((next(cuts1[""" + half1_allowed + """][2]))mod(""" + str(
        len(shape) + 1) + """) <= (next(cuts2[""" + half1_allowed + """][2]))mod(""" + str(
        len(shape) + 1) + """) & !(next(cuts1[""" + half1_allowed + """][2]) = """ + str(len(
        shape)) + """ & next(cuts2[""" + half1_allowed + """][2]) = 1)| next(cuts1[""" + half1_allowed + """][2]) = """ + str(
        len(
            shape)) + """ & next(cuts2[""" + half1_allowed + """][2]) = 1): next(shape[(abs(cuts1[""" + half1_allowed + """][2] + """ + str(
        len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) - next(cuts1[""" + half1_allowed + """][1]);

            next(state) = calc_cons | next(state) = correct: cuts2[""" + half1_allowed + """][1];
            TRUE: 0;
            esac;
    """
    s = 1
    for k in range(len(shape) / 2, len(shape) / 2 - 1 + num_allowed):
        text_assign += """next(inside1[""" + str(k) + """][0]):=""" + str(len(shape) + s) + """;
            next(inside1[""" + str(k) + """][1]):=case
            next(state) = guess: {90,270,180};
            TRUE: inside1[""" + str(k) + """][1];
            esac;

            next(inside1[""" + str(k) + """][2]):=""" + str(len(shape) + s + 1) + """;

            next(inside2[""" + str(k) + """][0]):=""" + str(len(shape) + s) + """;

            next(inside2[""" + str(k) + """][1]):=360 - next(inside1[""" + str(k) + """][1]);

            next(inside2[""" + str(k) + """][2]):=""" + str(len(shape) + s + 1) + """; 
            """
        s += 1

    text_assign += """next(legal):=cuts1[""" + half_1 + """][1] != 0 & cuts2[""" + half_1 + """][1] != 0 & cuts1[""" + half1_allowed + """][1] != 0 & cuts2[""" + half1_allowed + """][1] != 0;

            LTLSPEC
            G !(state = correct)"""
    os.chdir(r'C:\Users\liatw\OneDrive\Desktop\NuSMV-2.6.0-win64\bin')	# change to your NuSMV bin directory
									# writes to file
    code = '''j = ''' + str(j) + '''
text_var = """''' + text_var + '''"""
text_define = """''' + text_define + '''"""
text_assign = """''' + text_assign + '''"""
f = open('areasq' + str(j) + '.smv', 'w')
print >> f, text_var
print >> f, text_define
print >> f, text_assign
f.close()'''
    build_time = timeit.timeit(code, number=1)
    run_model('areasq' + str(j) + '.smv', j, len(shape) / 2 + num_allowed)
    return build_time


def write_model_tri(j, shape, num_allowed):
	"""
	This function gets a file index, the number of matchsticks for division and a shape (2D array)
	It creates a model file of the riddle
	Only basic area unit square is allowed here
	"""
	
    half = str(len(shape) / 2 - 2)				# last index for storing the new part's original junctions (from the shape). There are len(shape) / 2 - 1 original junction indices for each part to store.
    half_1 = str(len(shape) / 2 - 1)				# first index for storing the new part's cut junctions (one matchstick is new, one matchstick is from the original shape). There are 2 junctions represented as [match1_index, ang1, match2_index] for each part to store.
    half_2 = str(len(shape) / 2)				# first index for storing the new part's new inner junctions (both matchsticks are new). There are num_allowed - 1 junctions represented as [match1_index, ang1, match2_index] for each part to store.
    half1_allowed = str(len(shape) / 2 - 1 + num_allowed)	# last index for storing the new part's cut junctions (one matchstick is new, one matchstick is from the original shape). There are 2 junctions represented as [match1_index, ang1, match2_index] for each part to store.
    half2_allowed = str(len(shape) / 2 - 2 + num_allowed)	# last index for storing the new part's new inner junctions (both matchsticks are new). There are num_allowed - 1 junctions represented as [match1_index, ang1, match2_index] for each part to store.
    last = str(len(shape) - 1)					# last original matchstick's index 
    text_var = """MODULE main
        
        VAR
        
        state:{initial, guess, calc_cons, correct};
        arr_junct_1: array 0..""" + half + """ of 0..""" + last + """;
        arr_junct_2: array 0..""" + half + """ of 0..""" + last + """;
        num_it: 0..""" + str(3 + len(shape) / 2 + num_allowed) + """;
        cuts1: array """ + half_1 + """..""" + half1_allowed + """ of array 0..2 of {60,120,240,180,0"""
    str_num = """"""
    for i in range(1, num_allowed + 1 + len(shape)):
        if i != 120 and i != 60 and i != 300 and i != 240 and i != 180:
            str_num += """,""" + str(i)

    str_new = """"""
    for i in range(len(shape) + 1, len(shape) + num_allowed + 1):
        if i != 120 and i != 60 and i != 300 and i != 240 and i != 180:
            str_new += """,""" + str(i)

    text_var += str_num + """};
    cuts2: array """ + half_1 + """..""" + half1_allowed + """ of array 0..2 of {60,120,240,180,0""" + str_num + """};
    """
    if len(shape) / 2 <= len(shape) / 2 - 2 + num_allowed:
        text_var += """inside1: array """ + half_2 + """..""" + half2_allowed + """ of array 0..2 of {60,120,180,240,300""" + str_new + """};
    inside2: array """ + half_2 + """..""" + half2_allowed + """ of array 0..2 of {60,120,180,240,300""" + str_new + """};
    """
    text_var += """
    equal1: boolean;
    equal2: boolean;
    legal: boolean;
    ind1: 0..""" + half1_allowed + """;
    ind2: 0..""" + half1_allowed + """;
    ind3: 0..""" + half1_allowed + """;
    init_ind1: 0..""" + half1_allowed + """;
    init_ind2: 0..""" + half1_allowed + """;
    finished: boolean; """

    text_define = """DEFINE	
    shape:=""" + str(shape) + """;
    cut_in:=[""" + """[""" + str(len(shape) + 1) + """,180,1]""" + str(""",[""" + str(len(shape) + 1) + """,180,1]""") * (len(shape) / 2 + num_allowed) + """];
    junct_in:=""" + str([1] * (len(shape) / 2 - 1)) + """;
    """
    if len(shape) / 2 <= len(shape) / 2 - 2 + num_allowed:
        text_define += """ins_in:=[""" + """[""" + str(len(shape) + 1) + """,180,""" + str(len(shape) + 2) + """]""" + str(""",[""" + str(len(shape) + 1) + """,180,""" + str(len(shape) + 2) + """]""") * (len(shape) / 2 - 2 + num_allowed) + """];
    """

    list_match = """"""
    for i in range(1, len(shape)):
        list_match += """, """ + str(i)

    text_assign = """ASSIGN
        """
    if len(shape) / 2 <= len(shape) / 2 - 2 + num_allowed:
        text_assign += """
        init(inside1):=ins_in;
        init(inside2):=ins_in;
        """
    text_assign += """init(arr_junct_1):=junct_in;
        init(arr_junct_2):=junct_in;
        init(cuts1):=cut_in;
        init(cuts2):=cut_in;
        init(state):=initial;
        init(ind1):= 0; 
        init(ind2):= 0; 
        init(ind3):=0;
        init(init_ind1):=0;
        init(init_ind2):= 0; 
        init(legal):=TRUE;
        init(equal1):=TRUE;
        init(equal2):=TRUE;
         init(num_it):=1;
         
        next(state):=case
        state = initial: guess; 
        state = guess: calc_cons;
        state = calc_cons & finished & (equal1 | equal2) & legal: correct;
        TRUE: calc_cons;
        esac;
        
         next(num_it):=(num_it + 1) mod (""" + str(3 + len(shape) / 2 + num_allowed + 1) + """);
         
        next(arr_junct_1[0]):=case
        next(state) = guess: {0""" + list_match + """};
        TRUE: arr_junct_1[0];
        esac;
    """
    for k in range(1, len(shape) / 2 - 1):
        text_assign += """next(arr_junct_1[""" + str(k) + """]):=case
        next(state) = guess: (next(arr_junct_1[""" + str(k - 1) + """]) + 1)mod(""" + str(len(shape)) + """);
        TRUE: arr_junct_1[""" + str(k) + """];
        esac;
        """

    text_assign += """next(arr_junct_2[0]):=case
        next(state) = guess: (next(arr_junct_1[""" + str(len(shape) / 2 - 2) + """]) + 2)mod(""" + str(len(shape)) + """);
        TRUE: arr_junct_2[0];
        esac;
        """

    for k in range(1, len(shape) / 2 - 1):
        text_assign += """next(arr_junct_2[""" + str(k) + """]):=case
            next(state) = guess: (next(arr_junct_2[""" + str(k - 1) + """]) + 1)mod(""" + str(len(shape)) + """);
            TRUE: arr_junct_2[""" + str(k) + """];
            esac;
            """

    list_options = """"""
    for l in range(0, len(shape) / 2  + num_allowed):
        list_options += str(l) + ","
    list_options = list_options[:-1]

    text_assign += """next(ind1):=case
                state = initial: 0;
                                state = guess & next(state) = calc_cons: next(init_ind1);
                                state = calc_cons & !finished & ind1 < """ + half + """: (ind1 + 1)mod(""" + str(len(shape)/2 + num_allowed) + """);
								state = calc_cons & !finished & ind1 = """ + half + """ & cuts1[""" + half1_allowed + """][2] = (shape[(arr_junct_1[""" + half + """])mod(""" + str(len(shape)) + """)][2])mod(""" + str(len(shape) + 1) + """): """ + half1_allowed + """;
								state = calc_cons & !finished & cuts1[""" + half1_allowed + """][2] = (shape[(arr_junct_1[""" + half + """])mod(""" + str(len(shape)) + """)][2])mod(""" + str(len(shape) + 1) + """) & ind1 > """ + half_1 + """ : (ind1 + """ + half1_allowed + """)mod(""" + str(len(shape)/2 + num_allowed) + """);
								state = calc_cons & !finished & cuts1[""" + half1_allowed + """][2] = (shape[(arr_junct_1[""" + half + """])mod(""" + str(len(shape)) + """)][2])mod(""" + str(len(shape) + 1) + """) & ind1 = """ + half_1 + """ : 0;
								state = calc_cons & !finished & ind1 = """ + half + """ & cuts1[""" + half_1 + """][2] = (shape[(arr_junct_1[""" + half + """])mod(""" + str(len(shape)) + """)][2])mod(""" + str(len(shape) + 1) + """): """ + half_1 + """;
								state = calc_cons & !finished & ind1 > """ + half + """ & cuts1[""" + half_1 + """][2] = (shape[(arr_junct_1[""" + half + """])mod(""" + str(len(shape)) + """)][2])mod(""" + str(len(shape) + 1) + """): (ind1 + 1)mod(""" + str(len(shape)/2 + num_allowed) + """);
                                state = calc_cons & next(state) = guess: 0;
                                TRUE: ind1;
                                esac;
                
                next(ind3):=case
                state = guess & next(state) = calc_cons: next(init_ind1);
                                state = calc_cons & !finished & ind3 <= """ + half + """ & ind3 > 0: (ind3 + """ + half1_allowed + """)mod(""" + str(len(shape)/2 + num_allowed) + """);
								state = calc_cons & !finished & ind3 = 0 & cuts1[""" + half1_allowed + """][2] = (shape[(arr_junct_1[0])mod(""" + str(len(shape)) + """)][0])mod(""" + str(len(shape) + 1) + """): """ + half1_allowed + """;
								state = calc_cons & !finished & cuts1[""" + half1_allowed + """][2] = (shape[(arr_junct_1[0])mod(""" + str(len(shape)) + """)][0])mod(""" + str(len(shape) + 1) + """) & ind3 > """ + half_1 + """ & ind3 < """ + half1_allowed + """ : (ind3 + 1)mod(""" + str(len(shape)/2 + num_allowed) + """);
								state = calc_cons & !finished & cuts1[""" + half1_allowed + """][2] = (shape[(arr_junct_1[0])mod(""" + str(len(shape)) + """)][0])mod(""" + str(len(shape) + 1) + """) & ind3 = """ + half1_allowed + """ : """ + half + """;
								state = calc_cons & !finished & ind3 = 0 & cuts1[""" + half_1 + """][2] = (shape[(arr_junct_1[0])mod(""" + str(len(shape)) + """)][0])mod(""" + str(len(shape) + 1) + """): """ + half_1 + """;
								state = calc_cons & !finished & ind3 >= """ + half_1 + """ & ind3 < """ + half1_allowed + """ & cuts1[""" + half_1 + """][2] = (shape[(arr_junct_1[0])mod(""" + str(len(shape)) + """)][0])mod(""" + str(len(shape) + 1) + """): (ind3 + 1)mod(""" + str(len(shape)/2 + num_allowed) + """);
								state = calc_cons & !finished & ind3 = """ + half1_allowed + """ & cuts1[""" + half_1 + """][2] = (shape[(arr_junct_1[0])mod(""" + str(len(shape)) + """)][0])mod(""" + str(len(shape) + 1) + """): """ + half + """;
                                state = calc_cons & next(state) = guess: 0;
                                TRUE: ind3;
                                esac;
                
                next(ind2):=case
                                state = initial: 0;
                                state = guess & next(state) = calc_cons: next(init_ind2);
                                state = calc_cons & !finished & ind2 < """ + half + """: (ind2 + 1)mod(""" + str(len(shape)/2 + num_allowed) + """);
								state = calc_cons & !finished & ind2 = """ + half + """ & cuts2[""" + half1_allowed + """][2] = (shape[(arr_junct_2[""" + half + """])mod(""" + str(len(shape)) + """)][2])mod(""" + str(len(shape) + 1) + """): """ + half1_allowed + """;
								state = calc_cons & !finished & cuts2[""" + half1_allowed + """][2] = (shape[(arr_junct_2[""" + half + """])mod(""" + str(len(shape)) + """)][2])mod(""" + str(len(shape) + 1) + """) & ind2 > """ + half_1 + """ : (ind2 + """ + half1_allowed + """)mod(""" + str(len(shape)/2 + num_allowed) + """);
								state = calc_cons & !finished & cuts2[""" + half1_allowed + """][2] = (shape[(arr_junct_2[""" + half + """])mod(""" + str(len(shape)) + """)][2])mod(""" + str(len(shape) + 1) + """) & ind2 = """ + half_1 + """ : 0;
								state = calc_cons & !finished & ind2 = """ + half + """ & cuts2[""" + half_1 + """][2] = (shape[(arr_junct_2[""" + half + """])mod(""" + str(len(shape)) + """)][2])mod(""" + str(len(shape) + 1) + """): """ + half_1 + """;
								state = calc_cons & !finished & ind2 > """ + half + """ & cuts2[""" + half_1 + """][2] = (shape[(arr_junct_2[""" + half + """])mod(""" + str(len(shape)) + """)][2])mod(""" + str(len(shape) + 1) + """): (ind2 + 1)mod(""" + str(len(shape)/2 + num_allowed) + """);
                                state = calc_cons & next(state) = guess: 0;
                                TRUE: ind2;
                                esac;
        
        next(init_ind1):=case
        state = initial: 0;
        state = guess & next(state) = calc_cons: {""" + list_options + """};
        state = calc_cons & next(state) = guess: 0;
        TRUE: init_ind1;
        esac;
        
        next(init_ind2):=case
        state = initial: 0;
        state = guess & next(state) = calc_cons: {""" + list_options + """};
        state = calc_cons & next(state) = guess: 0;
        TRUE: init_ind2;
        esac;
        
        next(finished):= num_it = """ + str(3 + len(shape) / 2 + num_allowed - 1) + """;
        
        next(equal1):=case
        state = calc_cons & next(state) = calc_cons & ind1 <= """ + str(len(shape) / 2 - 2) + """ & ind2 <= """ + str(len(shape) / 2 - 2) + """: equal1 & shape[arr_junct_1[ind1]][1] = shape[arr_junct_2[ind2]][1];
        state = calc_cons & next(state) = calc_cons & ind1 <= """ + str(len(shape) / 2 - 2) + """ & ind2 = """ + str(len(shape) / 2 - 1) + """: equal1 & shape[arr_junct_1[ind1]][1] = cuts2[""" + half_1 + """][1];
        """
    if len(shape) / 2 <= len(shape) / 2 - 2 + num_allowed:
        text_assign += """state = calc_cons & next(state) = calc_cons & ind1 <= """ + half + """ & ind2 > """ + str(len(shape) / 2 - 1) + """ & ind2 < """ + half1_allowed + """ : equal1 & shape[arr_junct_1[ind1]][1] = inside2[ind2][1];
        """

    text_assign += """state = calc_cons & next(state) = calc_cons & ind1 <= """ + half + """ & ind2 = """ + half1_allowed + """: equal1 & shape[arr_junct_1[ind1]][1] = cuts2[""" + half1_allowed + """][1];
                
        state = calc_cons & next(state) = calc_cons & ind1 = """ + half_1 + """ & ind2 <= """ + half + """: equal1 & shape[arr_junct_2[ind2]][1] = cuts1[""" + half_1 + """][1];
        state = calc_cons & next(state) = calc_cons & ind1 = """ + half_1 + """ & ind2 = """ + half_1 + """: equal1 & cuts1[""" + half_1 + """][1] = cuts2[""" + half_1 + """][1];
    """
    if len(shape) / 2 <= len(shape) / 2 - 2 + num_allowed:
        text_assign += """state = calc_cons & next(state) = calc_cons & ind1 = """ + half_1 + """ & ind2 > """ + half_1 + """ & ind2 < """ + half1_allowed + """: equal1 & cuts1[""" + half_1 + """][1] = inside2[ind2][1];
        """
    text_assign += """state = calc_cons & next(state) = calc_cons & ind1 = """ + half_1 + """ & ind2 = """ + half1_allowed + """: equal1 & cuts1[""" + half_1 + """][1] = cuts2[""" + half1_allowed + """][1];
    """
    if len(shape) / 2 <= len(shape) / 2 - 2 + num_allowed:
        text_assign += """state = calc_cons & next(state) = calc_cons & ind1 > """ + half_1 + """ & ind1 < """ + half1_allowed + """ & ind2 <= """ + half + """: equal1 & shape[arr_junct_2[ind2]][1] = inside1[ind1][1];
        state = calc_cons & next(state) = calc_cons & ind1 > """ + half_1 + """ & ind1 < """ + half1_allowed + """ & ind2 = """ + half_1 + """: equal1 & cuts2[""" + half_1 + """][1] = inside1[ind1][1];
        state = calc_cons & next(state) = calc_cons & ind1 > """ + half_1 + """ & ind1 < """ + half1_allowed + """ & ind2 > """ + half_1 + """ & ind2 < """ + half1_allowed + """: equal1 & inside1[ind1][1] = inside2[ind2][1];
        state = calc_cons & next(state) = calc_cons & ind1 > """ + half_1 + """ & ind1 < """ + half1_allowed + """ & ind2 = """ + half1_allowed + """: equal1 & inside1[ind1][1] = cuts2[""" + half1_allowed + """][1];
        """
    text_assign += """
        state = calc_cons & next(state) = calc_cons & ind1 = """ + half1_allowed + """ & ind2 <= """ + half + """: equal1 & shape[arr_junct_2[ind2]][1] = cuts1[""" + half1_allowed + """][1];
        state = calc_cons & next(state) = calc_cons & ind1 = """ + half1_allowed + """ & ind2 = """ + half_1 + """: equal1 & cuts1[""" + half1_allowed + """][1] = cuts2[""" + half_1 + """][1];
        """
    if len(shape) / 2 <= len(shape) / 2 - 2 + num_allowed:
        text_assign += """state = calc_cons & next(state) = calc_cons & ind1 = """ + half1_allowed + """ & ind2 > """ + half_1 + """ & ind2 < """ + half1_allowed + """: equal1 & cuts1[""" + half1_allowed + """][1] = inside2[ind2][1];
        """
    text_assign += """state = calc_cons & next(state) = calc_cons & ind1 = """ + half1_allowed + """ & ind2 = """ + half1_allowed + """: equal1 & cuts1[""" + half1_allowed + """][1] = cuts2[""" + half1_allowed + """][1];
        next(state) = guess: TRUE;
        TRUE: equal1;
        esac;
        
        next(equal2):=case
        state = calc_cons & next(state) = calc_cons & ind3 <= """ + half + """ & ind2 <= """ + half + """: equal2 & shape[arr_junct_1[ind3]][1] = shape[arr_junct_2[ind2]][1];
        state = calc_cons & next(state) = calc_cons & ind3 <= """ + half + """ & ind2 = """ + half_1 + """: equal2 & shape[arr_junct_1[ind3]][1] = cuts2[""" + half_1 + """][1];
    """
    if len(shape) / 2 <= len(shape) / 2 - 2 + num_allowed:
        text_assign += """state = calc_cons & next(state) = calc_cons & ind3 <= """ + half + """ & ind2 > """ + half_1 + """ & ind2 < """ + half1_allowed + """: equal2 & shape[arr_junct_1[ind3]][1] = inside2[ind2][1];
        """
    text_assign += """state = calc_cons & next(state) = calc_cons & ind3 <= """ + half + """ & ind2 = """ + half1_allowed + """: equal2 & shape[arr_junct_1[ind3]][1] = cuts2[""" + half1_allowed + """][1];
        
        state = calc_cons & next(state) = calc_cons & ind3 = """ + half_1 + """ & ind2 <= """ + half + """: equal2 & shape[arr_junct_2[ind2]][1] = cuts1[""" + half_1 + """][1];
        state = calc_cons & next(state) = calc_cons & ind3 = """ + half_1 + """ & ind2 = """ + half_1 + """: equal2 & cuts1[""" + half_1 + """][1] = cuts2[""" + half_1 + """][1];
        """
    if len(shape) / 2 <= len(shape) / 2 - 2 + num_allowed:
        text_assign += """state = calc_cons & next(state) = calc_cons & ind3 = """ + half_1 + """ & ind2 > """ + half_1 + """ & ind2 < """ + half1_allowed + """: equal2 & cuts1[""" + half_1 + """][1] = inside2[ind2][1];
        """
    text_assign += """state = calc_cons & next(state) = calc_cons & ind3 = """ + half_1 + """ & ind2 = """ + half1_allowed + """: equal2 & cuts1[""" + half_1 + """][1] = cuts2[""" + half1_allowed + """][1];
        """
    if len(shape) / 2 <= len(shape) / 2 - 2 + num_allowed:
        text_assign += """state = calc_cons & next(state) = calc_cons & ind3 > """ + half_1 + """ & ind3 < """ + half1_allowed + """ & ind2 <= """ + half + """: equal2 & shape[arr_junct_2[ind2]][1] = inside1[ind3][1];
        state = calc_cons & next(state) = calc_cons & ind3 > """ + half_1 + """ & ind3 < """ + half1_allowed + """ & ind2 = """ + half_1 + """: equal2 & cuts2[""" + half_1 + """][1] = inside1[ind3][1];
        state = calc_cons & next(state) = calc_cons & ind3 > """ + half_1 + """ & ind3 < """ + half1_allowed + """ & ind2 > """ + half_1 + """ & ind2 < """ + half1_allowed + """: equal2 & inside1[ind3][1] = inside2[ind2][1];
        state = calc_cons & next(state) = calc_cons & ind3 > """ + half_1 + """ & ind3 < """ + half1_allowed + """ & ind2 = """ + half1_allowed + """: equal2 & inside1[ind3][1] = cuts2[""" + half1_allowed + """][1];
        """
    text_assign += """state = calc_cons & next(state) = calc_cons & ind3 = """ + half1_allowed + """ & ind2 <= """ + half + """: equal2 & shape[arr_junct_2[ind2]][1] = cuts1[""" + half1_allowed + """][1];
        state = calc_cons & next(state) = calc_cons & ind3 = """ + half1_allowed + """ & ind2 = """ + half_1 + """: equal2 & cuts1[""" + half1_allowed + """][1] = cuts2[""" + half_1 + """][1];
        """
    if len(shape) / 2 <= len(shape) / 2 - 2 + num_allowed:
        text_assign += """state = calc_cons & next(state) = calc_cons & ind3 = """ + half1_allowed + """ & ind2 > """ + half_1 + """ & ind2 < """ + half1_allowed + """: equal2 & cuts1[""" + half1_allowed + """][1] = inside2[ind2][1];
        """
    text_assign += """
        state = calc_cons & next(state) = calc_cons & ind3 = """ + half1_allowed + """ & ind2 = """ + half1_allowed + """: equal2 & cuts1[""" + half1_allowed + """][1] = cuts2[""" + half1_allowed + """][1];
        next(state) = guess: TRUE;
        TRUE: equal2;
        esac;
        
        next(cuts1[""" + half_1 + """][0]):=""" + str(len(shape) + 1)+ """;
        next(cuts1[""" + half1_allowed + """][0]):=""" + str(len(shape) + num_allowed)+ """;
        
        next(cuts2[""" + half_1 + """][0]):=""" + str(len(shape) + 1)+ """;
        next(cuts2[""" + half1_allowed + """][0]):=""" + str(len(shape) + num_allowed)+ """;
        
        
        next(cuts1[""" + half_1 + """][2]):=next(shape[arr_junct_1[0]][0]);
        next(cuts1[""" + half1_allowed + """][2]):=next(shape[arr_junct_1[""" + half + """]][2]);
        
        next(cuts2[""" + half_1 + """][2]):=next(shape[arr_junct_2[""" + half + """]][2]);
        next(cuts2[""" + half1_allowed + """][2]):=next(shape[arr_junct_2[0]][0]);

next(cuts1[""" + half_1 + """][1]) := case
        next(state) = guess & ((next(cuts1[""" + half_1 + """][2]))mod(""" + str(len(shape) + 1) + """) > (next(cuts2[""" + half_1 + """][2]))mod(""" + str(len(shape) + 1) + """) & !(next(cuts1[""" + half_1 + """][2]) = 1 & next(cuts2[""" + half_1 + """][2]) = """ + str(len(shape)) + """) | next(cuts1[""" + half_1 + """][2]) = 1 & next(cuts2[""" + half_1 + """][2]) = """ + str(len(shape)) + """) & next(shape[(abs(cuts2[""" + half_1 + """][2] + """ + str(len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) = 300: {60, 120, 180, 240};
        
        next(state) = guess & ((next(cuts1[""" + half_1 + """][2]))mod(""" + str(len(shape) + 1) + """) > (next(cuts2[""" + half_1 + """][2]))mod(""" + str(len(shape) + 1) + """) & !(next(cuts1[""" + half_1 + """][2]) = 1 & next(cuts2[""" + half_1 + """][2]) = """ + str(len(shape)) + """) | next(cuts1[""" + half_1 + """][2]) = 1 & next(cuts2[""" + half_1 + """][2]) = """ + str(len(shape)) + """) & next(shape[(abs(cuts2[""" + half_1 + """][2] + """ + str(len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) = 240: {60, 120, 180};
        
        next(state) = guess & ((next(cuts1[""" + half_1 + """][2]))mod(""" + str(len(shape) + 1) + """) > (next(cuts2[""" + half_1 + """][2]))mod(""" + str(len(shape) + 1) + """) & !(next(cuts1[""" + half_1 + """][2]) = 1 & next(cuts2[""" + half_1 + """][2]) = """ + str(len(shape)) + """) | next(cuts1[""" + half_1 + """][2]) = 1 & next(cuts2[""" + half_1 + """][2]) = """ + str(len(shape)) + """) & next(shape[(abs(cuts2[""" + half_1 + """][2] + """ + str(len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) = 180: {60, 120};
        
        next(state) = guess & ((next(cuts1[""" + half_1 + """][2]))mod(""" + str(len(shape) + 1) + """) > (next(cuts2[""" + half_1 + """][2]))mod(""" + str(len(shape) + 1) + """) & !(next(cuts1[""" + half_1 + """][2]) = 1 & next(cuts2[""" + half_1 + """][2]) = """ + str(len(shape)) + """) | next(cuts1[""" + half_1 + """][2]) = 1 & next(cuts2[""" + half_1 + """][2]) = """ + str(len(shape)) + """) & next(shape[(abs(cuts2[""" + half_1 + """][2] + """ + str(len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) = 120: 60;
        
        next(state) = guess & ((next(cuts1[""" + half_1 + """][2]))mod(""" + str(len(shape) + 1) + """) <= (next(cuts2[""" + half_1 + """][2]))mod(""" + str(len(shape) + 1) + """)  & !(next(cuts1[""" + half_1 + """][2]) = """ + str(len(shape)) + """ & next(cuts2[""" + half_1 + """][2]) = 1) | next(cuts1[""" + half_1 + """][2]) = """ + str(len(shape)) + """ & next(cuts2[""" + half_1 + """][2]) = 1) & next(shape[(abs(cuts1[""" + half_1 + """][2] + """ + str(len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) = 120: 60;
        
        next(state) = guess & ((next(cuts1[""" + half_1 + """][2]))mod(""" + str(len(shape) + 1) + """) <= (next(cuts2[""" + half_1 + """][2]))mod(""" + str(len(shape) + 1) + """)  & !(next(cuts1[""" + half_1 + """][2]) = """ + str(len(shape)) + """ & next(cuts2[""" + half_1 + """][2]) = 1) | next(cuts1[""" + half_1 + """][2]) = """ + str(len(shape)) + """ & next(cuts2[""" + half_1 + """][2]) = 1) & next(shape[(abs(cuts1[""" + half_1 + """][2] + """ + str(len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) = 180: {60, 120};
        
        next(state) = guess & ((next(cuts1[""" + half_1 + """][2]))mod(""" + str(len(shape) + 1) + """) <= (next(cuts2[""" + half_1 + """][2]))mod(""" + str(len(shape) + 1) + """)  & !(next(cuts1[""" + half_1 + """][2]) = """ + str(len(shape)) + """ & next(cuts2[""" + half_1 + """][2]) = 1) | next(cuts1[""" + half_1 + """][2]) = """ + str(len(shape)) + """ & next(cuts2[""" + half_1 + """][2]) = 1) & next(shape[(abs(cuts1[""" + half_1 + """][2] + """ + str(len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) = 240: {60, 120, 180};
        
        next(state) = guess & ((next(cuts1[""" + half_1 + """][2]))mod(""" + str(len(shape) + 1) + """) <= (next(cuts2[""" + half_1 + """][2]))mod(""" + str(len(shape) + 1) + """)  & !(next(cuts1[""" + half_1 + """][2]) = """ + str(len(shape)) + """ & next(cuts2[""" + half_1 + """][2]) = 1) | next(cuts1[""" + half_1 + """][2]) = """ + str(len(shape)) + """ & next(cuts2[""" + half_1 + """][2]) = 1) & next(shape[(abs(cuts1[""" + half_1 + """][2] + """ + str(len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) = 300: {60, 120, 180, 240};
        
        next(state) = calc_cons | next(state) = correct: cuts1[""" + half_1 + """][1];
        TRUE: 0;
        esac;
        
        next(cuts2[""" + half_1 + """][1]) := case
       
        next(state) = guess & ((next(cuts1[""" + half_1 + """][2]))mod(""" + str(len(shape) + 1) + """) > (next(cuts2[""" + half_1 + """][2]))mod(""" + str(len(shape) + 1) + """) & !(next(cuts1[""" + half_1 + """][2]) = 1 & next(cuts2[""" + half_1 + """][2]) = """ + str(len(shape)) + """)| next(cuts1[""" + half_1 + """][2]) = 1 & next(cuts2[""" + half_1 + """][2]) = """ + str(len(shape)) + """): next(shape[(abs(cuts2[""" + half_1 + """][2] + """ + str(len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) - next(cuts1[""" + half_1 + """][1]);
        
        next(state) = guess & ((next(cuts1[""" + half_1 + """][2]))mod(""" + str(len(shape) + 1) + """) <= (next(cuts2[""" + half_1 + """][2]))mod(""" + str(len(shape) + 1) + """) & !(next(cuts1[""" + half_1 + """][2]) = """ + str(len(shape)) + """ & next(cuts1[""" + half_1 + """][2]) = 1) | next(cuts1[""" + half_1 + """][2]) = """ + str(len(shape)) + """ & next(cuts2[""" + half_1 + """][2]) = 1): next(shape[(abs(cuts1[""" + half_1 + """][2] + """ + str(len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) - next(cuts1[""" + half_1 + """][1]);
        
        next(state) = calc_cons | next(state) = correct: cuts2[""" + half_1 + """][1];
        TRUE: 0;
        esac;
        
        next(cuts1[""" + half1_allowed + """][1]) := case
        next(state) = guess & ((next(cuts1[""" + half1_allowed + """][2]))mod(""" + str(len(shape) + 1) + """) > (next(cuts2[""" + half1_allowed + """][2]))mod(""" + str(len(shape) + 1) + """) & !(next(cuts1[""" + half1_allowed + """][2]) = 1 & next(cuts2[""" + half1_allowed + """][2]) = """ + str(len(shape)) + """)| next(cuts1[""" + half1_allowed + """][2]) = 1 & next(cuts2[""" + half1_allowed + """][2]) = """ + str(len(shape)) + """) & next(shape[(abs(cuts2[""" + half1_allowed + """][2] + """ + str(len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) = 300: {60, 120, 180, 240};
        
        next(state) = guess & ((next(cuts1[""" + half1_allowed + """][2]))mod(""" + str(len(shape) + 1) + """) > (next(cuts2[""" + half1_allowed + """][2]))mod(""" + str(len(shape) + 1) + """) & !(next(cuts1[""" + half1_allowed + """][2]) = 1 & next(cuts2[""" + half1_allowed + """][2]) = """ + str(len(shape)) + """)| next(cuts1[""" + half1_allowed + """][2]) = 1 & next(cuts2[""" + half1_allowed + """][2]) = """ + str(len(shape)) + """)& next(shape[(abs(cuts2[""" + half1_allowed + """][2] + """ + str(len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) = 240: {60, 120, 180};
        
        next(state) = guess & ((next(cuts1[""" + half1_allowed + """][2]))mod(""" + str(len(shape) + 1) + """) > (next(cuts2[""" + half1_allowed + """][2]))mod(""" + str(len(shape) + 1) + """) & !(next(cuts1[""" + half1_allowed + """][2]) = 1 & next(cuts2[""" + half1_allowed + """][2]) = """ + str(len(shape)) + """)| next(cuts1[""" + half1_allowed + """][2]) = 1 & next(cuts2[""" + half1_allowed + """][2]) = """ + str(len(shape)) + """)& next(shape[(abs(cuts2[""" + half1_allowed + """][2] + """ + str(len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) = 180: {60, 120};
        
        next(state) = guess & ((next(cuts1[""" + half1_allowed + """][2]))mod(""" + str(len(shape) + 1) + """) > (next(cuts2[""" + half1_allowed + """][2]))mod(""" + str(len(shape) + 1) + """) & !(next(cuts1[""" + half1_allowed + """][2]) = 1 & next(cuts2[""" + half1_allowed + """][2]) = """ + str(len(shape)) + """)| next(cuts1[""" + half1_allowed + """][2]) = 1 & next(cuts2[""" + half1_allowed + """][2]) = """ + str(len(shape)) + """)& next(shape[(abs(cuts2[""" + half1_allowed + """][2] + """ + str(len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) = 120: 60;
        
        next(state) = guess & ((next(cuts1[""" + half1_allowed + """][2]))mod(""" + str(len(shape) + 1) + """) <= (next(cuts2[""" + half1_allowed + """][2]))mod(""" + str(len(shape) + 1) + """) & !(next(cuts1[""" + half1_allowed + """][2]) = """ + str(len(shape)) + """ & next(cuts2[""" + half1_allowed + """][2]) = 1)| next(cuts1[""" + half1_allowed + """][2]) = """ + str(len(shape)) + """ & next(cuts2[""" + half1_allowed + """][2]) = 1)& next(shape[(abs(cuts1[""" + half1_allowed + """][2] + """ + str(len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) = 120: 60;
        
        next(state) = guess & ((next(cuts1[""" + half1_allowed + """][2]))mod(""" + str(len(shape) + 1) + """) <= (next(cuts2[""" + half1_allowed + """][2]))mod(""" + str(len(shape) + 1) + """) & !(next(cuts1[""" + half1_allowed + """][2]) = """ + str(len(shape)) + """ & next(cuts2[""" + half1_allowed + """][2]) = 1)| next(cuts1[""" + half1_allowed + """][2]) = """ + str(len(shape)) + """ & next(cuts2[""" + half1_allowed + """][2]) = 1)& next(shape[(abs(cuts1[""" + half1_allowed + """][2] + """ + str(len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) = 180: {60, 120};
        
        next(state) = guess & ((next(cuts1[""" + half1_allowed + """][2]))mod(""" + str(len(shape) + 1) + """) <= (next(cuts2[""" + half1_allowed + """][2]))mod(""" + str(len(shape) + 1) + """) & !(next(cuts1[""" + half1_allowed + """][2]) = """ + str(len(shape)) + """ & next(cuts2[""" + half1_allowed + """][2]) = 1)| next(cuts1[""" + half1_allowed + """][2]) = """ + str(len(shape)) + """ & next(cuts2[""" + half1_allowed + """][2]) = 1)& next(shape[(abs(cuts1[""" + half1_allowed + """][2] + """ + str(len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) = 240: {60, 120, 180};
        
        next(state) = guess & ((next(cuts1[""" + half1_allowed + """][2]))mod(""" + str(len(shape) + 1) + """) <= (next(cuts2[""" + half1_allowed + """][2]))mod(""" + str(len(shape) + 1) + """) & !(next(cuts1[""" + half1_allowed + """][2]) = """ + str(len(shape)) + """ & next(cuts2[""" + half1_allowed + """][2]) = 1)| next(cuts1[""" + half1_allowed + """][2]) = """ + str(len(shape)) + """ & next(cuts2[""" + half1_allowed + """][2]) = 1)& next(shape[(abs(cuts1[""" + half1_allowed + """][2] + """ + str(len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) = 300: {60, 120, 180, 240};
        
        next(state) = calc_cons | next(state) = correct: cuts1[""" + half1_allowed + """][1];
        TRUE: 0;
        esac;
        
        next(cuts2[""" + half1_allowed + """][1]) := case
        next(state) = guess & ((next(cuts1[""" + half1_allowed + """][2]))mod(""" + str(len(shape) + 1) + """) > (next(cuts2[""" + half1_allowed + """][2]))mod(""" + str(len(shape) + 1) + """) & !(next(cuts1[""" + half1_allowed + """][2]) = 1 & next(cuts2[""" + half1_allowed + """][2]) = """ + str(len(shape)) + """)| next(cuts1[""" + half1_allowed + """][2]) = 1 & next(cuts2[""" + half1_allowed + """][2]) = """ + str(len(shape)) + """): next(shape[(abs(cuts2[""" + half1_allowed + """][2] + """ + str(len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) - next(cuts1[""" + half1_allowed + """][1]);
        
        next(state) = guess & ((next(cuts1[""" + half1_allowed + """][2]))mod(""" + str(len(shape) + 1) + """) <= (next(cuts2[""" + half1_allowed + """][2]))mod(""" + str(len(shape) + 1) + """) & !(next(cuts1[""" + half1_allowed + """][2]) = """ + str(len(shape)) + """ & next(cuts2[""" + half1_allowed + """][2]) = 1)| next(cuts1[""" + half1_allowed + """][2]) = """ + str(len(shape)) + """ & next(cuts2[""" + half1_allowed + """][2]) = 1): next(shape[(abs(cuts1[""" + half1_allowed + """][2] + """ + str(len(shape) - 1) + """))mod(""" + str(len(shape)) + """)][1]) - next(cuts1[""" + half1_allowed + """][1]);
        
        next(state) = calc_cons | next(state) = correct: cuts2[""" + half1_allowed + """][1];
        TRUE: 0;
        esac;
"""
    s = 1
    for k in range(len(shape) / 2, len(shape) / 2 - 1 + num_allowed):
        text_assign += """next(inside1[""" + str(k) + """][0]):=""" + str(len(shape) + s) + """;
        next(inside1[""" + str(k) + """][1]):=case
        next(state) = guess: {60,120,240,180,300};
        TRUE: inside1[""" + str(k) + """][1];
        esac;
        
        next(inside1[""" + str(k) + """][2]):=""" + str(len(shape) + s + 1) + """;
        
        next(inside2[""" + str(k) + """][0]):=""" + str(len(shape) + s) + """;
        
        next(inside2[""" + str(k) + """][1]):=360 - next(inside1[""" + str(k) + """][1]);
        
        next(inside2[""" + str(k) + """][2]):=""" + str(len(shape) + s + 1) + """; 
        """
        s += 1

    text_assign += """next(legal):=cuts1[""" + half_1 + """][1] != 0 & cuts2[""" + half_1 + """][1] != 0 & cuts1[""" + half1_allowed + """][1] != 0 & cuts2[""" + half1_allowed + """][1] != 0;
        
        LTLSPEC
        G !(state = correct)"""
    os.chdir(r'C:\Users\liatw\OneDrive\Desktop\NuSMV-2.6.0-win64\bin')	# change it to your NuSMV bin directory
									# writes to file
    code = '''j = ''' + str(j) + '''
text_var = """''' + text_var + '''"""
text_define = """''' + text_define + '''"""
text_assign = """''' + text_assign + '''"""
f = open('areatri' + str(j) + '.smv', 'w')
print >> f, text_var
print >> f, text_define
print >> f, text_assign
f.close()'''
    build_time = timeit.timeit(code, number=1)	
    run_model('areatri' + str(j) + '.smv', j, len(shape) / 2 + num_allowed)	# runs the file, bmc bound: half shape's length (half of the number of original matchsticks) + num_allowed + 5
    return build_time


def run_model(file_model, j, len):
	"""
	This function gets a model file, its index and number of matchsticks in a new part (number of original matchsticks / 2 + num_allowed)
	Runs the file in bmc mode
	"""
    f = open(str(file_model), 'a')
    output_f = open('output_area' + str(j) + '.txt', 'w')
    subprocess.Popen("ptime.exe NuSMV -bmc -bmc_length " + str(len + 5) + " " + str(file_model), stdout=output_f, stderr=output_f)
    output_f.close()
    f.close()


def find_solution(j):
	"""
	This function returns the execution time of the riddle; flag - 2 if there is a solution for the riddle, else 1;
	"""
    run_time = 0

    f = open('output_area' + str(j) + '.txt', 'r')
    text = f.read()
    while "Execution time: " not in text:
        time.sleep(1)
        f = open('output_area' + str(j) + '.txt', 'r')
        text = f.read()
    run_str = (text.split("Execution time: "))[1].split(" s")[0]
    run_time = float(run_str)

    if 'is false' in text:
        f.close()
        return 2, run_time
    else:
        f.close()
        return 1, run_time


def build_dir(small):
	"""
	This function returns a directions array, given a shape. 
	The shape - represented by a 2-D array:
    	Every row represents a junction between 2 matchsticks
    	Each row includes 3 matchsticks: indices 0,2 represent the matchsticks and index 1 represents the angle between them.
    	Area units: the shape's area can be divided to 1-match-length squares or 1-match-length triangles.
    	The angles of the shape must be: 0,90,180,270 or: 0,60,120,180,240,300.
    	Every matchstick has an index - an integer between 1 - (# of matchsticks)
	
	"""
    dir1 = [1]
    m = 0   # m is negative (-1) positive (1) or zero (0)
    for i in range(0, len(small) - 1):
        if dir1[i] == 1 and m == 0:
            if small[i][1] == 60:
                dir1.append(2)
                m = -1
            elif small[i][1] == 90:
                dir1.append(2)
                m = -1
            elif small[i][1] == 120:
                dir1.append(1)
                m = 1
            elif small[i][1] == 180:
                dir1.append(1)
                m = 0
            elif small[i][1] == 240:
                dir1.append(1)
                m = -1
            elif small[i][1] == 270:
                dir1.append(1)
                m = 1
            elif small[i][1] == 300:
                dir1.append(2)
                m = 1

        elif dir1[i] == 1 and m == 1:
            if small[i][1] == 60:
                dir1.append(2)
                m = 0
            elif small[i][1] == 90:
                dir1.append(1)
                m = 0
            elif small[i][1] == 120:
                dir1.append(2)
                m = -1
            elif small[i][1] == 180:
                dir1.append(1)
                m = 1
            elif small[i][1] == 240:
                dir1.append(1)
                m = 0
            elif small[i][1] == 270:
                dir1.append(2)
                m = 0
            elif small[i][1] == 300:
                dir1.append(1)
                m = -1

        elif dir1[i] == 1 and m == -1:
            if small[i][1] == 60:
                dir1.append(1)
                m = 1
            elif small[i][1] == 120:
                dir1.append(1)
                m = 0
            elif small[i][1] == 180:
                dir1.append(1)
                m = -1
            elif small[i][1] == 240:
                dir1.append(2)
                m = 1
            elif small[i][1] == 300:
                dir1.append(2)
                m = 0

        elif dir1[i] == 2 and m == 0:
            if small[i][1] == 60:
                dir1.append(1)
                m = -1
            if small[i][1] == 90:
                dir1.append(1)
                m = 1
            elif small[i][1] == 120:
                dir1.append(2)
                m = 1
            elif small[i][1] == 180:
                dir1.append(2)
                m = 0
            elif small[i][1] == 240:
                dir1.append(2)
                m = -1
            elif small[i][1] == 270:
                dir1.append(2)
                m = -1
            elif small[i][1] == 300:
                dir1.append(1)
                m = 1

        elif dir1[i] == 2 and m == 1:
            if small[i][1] == 60:
                dir1.append(1)
                m = 0
            elif small[i][1] == 120:
                dir1.append(1)
                m = -1
            elif small[i][1] == 180:
                dir1.append(2)
                m = 1
            elif small[i][1] == 240:
                dir1.append(2)
                m = 0
            elif small[i][1] == 300:
                dir1.append(2)
                m = -1

        elif dir1[i] == 2 and m == -1:
            if small[i][1] == 60:
                dir1.append(2)
                m = 1
            elif small[i][1] == 90:
                dir1.append(2)
                m = 0
            elif small[i][1] == 120:
                dir1.append(2)
                m = 0
            elif small[i][1] == 180:
                dir1.append(2)
                m = -1
            elif small[i][1] == 240:
                dir1.append(1)
                m = 1
            elif small[i][1] == 270:
                dir1.append(1)
                m = 0
            elif small[i][1] == 300:
                dir1.append(1)
                m = 0
    return dir1


def get_shapes(j, original):
    os.chdir(r'C:\Users\liatw\OneDrive\Desktop\NuSMV-2.6.0-win64\bin')
    out = open('output_area' + str(j) + '.txt', 'r')
    text = out.read()
    if 'is false' in text:
        res, text2 = text.split('state = initial')
        rows = text2.split('\n')

        arr_junct_1 = []
        arr_junct_1_i = []
        arr_junct_2 = []
        arr_junct_2_i = []
        list_ind_1 = []
        list_ind_2 = []

        list_cuts1 = []
        list_cuts2 = []
        cuts1 = []
        cuts2 = []

        inside1 = []
        inside2 = []
        list_ins_1 = []
        list_ins_2 = []

        shape1 = []
        shape2 = []
        for row in rows:
            if 'arr_junct_1' in row:
                full_str_ind, val2 = row.split(' = ')
                ind1 = full_str_ind[:-1]
                str2, ind = ind1.split('[')
                if full_str_ind in list_ind_1:
                    arr_junct_1[int(ind)] = original[int(val2)]
                    arr_junct_1_i[int(ind)] = int(val2)
                else:
                    list_ind_1.append(full_str_ind)
                    arr_junct_1.append(original[int(val2)])
                    arr_junct_1_i.append(int(val2))

            elif 'arr_junct_2' in row:
                full_str_ind, val2 = row.split(' = ')
                ind1 = full_str_ind[:-1]
                str2, ind = ind1.split('[')
                if full_str_ind in list_ind_2:
                    arr_junct_2[int(ind)] = original[int(val2)]
                    arr_junct_2_i[int(ind)] = int(val2)
                else:
                    list_ind_2.append(full_str_ind)
                    arr_junct_2.append(original[int(val2)])
                    arr_junct_2_i.append(int(val2))

            elif 'cuts1' in row:
                full_str_ind, val2 = row.split(' = ')
                arr, in1, in2 = full_str_ind.split('[')
                in1 = in1[:-1]
                in2 = in2[:-1]
                if full_str_ind in list_cuts1:
                    cuts1[int(in1) - len(arr_junct_1)][int(in2)] = int(val2)
                elif str(arr + '[' + in1 + ']') in list_cuts1:
                    list_cuts1.append(full_str_ind)
                    cuts1[int(in1) - len(arr_junct_1)].append(int(val2))
                else:
                    list_cuts1.append(str(arr + '[' + in1 + ']'))
                    list_cuts1.append(full_str_ind)
                    cuts1.append([int(val2)])

            elif 'cuts2' in row:
                full_str_ind, val2 = row.split(' = ')
                arr, in1, in2 = full_str_ind.split('[')
                in1 = in1[:-1]
                in2 = in2[:-1]
                if full_str_ind in list_cuts2:
                    cuts2[int(in1) - len(arr_junct_1)][int(in2)] = int(val2)
                elif str(arr + '[' + in1 + ']') in list_cuts2:
                    list_cuts2.append(full_str_ind)
                    cuts2[int(in1) - len(arr_junct_1)].append(int(val2))
                else:
                    list_cuts2.append(str(arr + '[' + in1 + ']'))
                    list_cuts2.append(full_str_ind)
                    cuts2.append([int(val2)])

            elif 'inside1' in row:
                full_str_ind, val2 = row.split(' = ')
                arr, in1, in2 = full_str_ind.split('[')
                in1 = in1[:-1]
                in2 = in2[:-1]
                if full_str_ind in list_ins_1:
                    inside1[int(in1) - len(arr_junct_1) - 1][int(in2)] = int(val2)
                elif str(arr + '[' + in1 + ']') in list_ins_1:
                    list_ins_1.append(full_str_ind)
                    inside1[int(in1) - len(arr_junct_1) - 1].append(int(val2))
                else:
                    list_ins_1.append(str(arr + '[' + in1 + ']'))
                    list_ins_1.append(full_str_ind)
                    inside1.append([int(val2)])

            elif 'inside2' in row:
                full_str_ind, val2 = row.split(' = ')
                arr, in1, in2 = full_str_ind.split('[')
                in1 = in1[:-1]
                in2 = in2[:-1]
                if full_str_ind in list_ins_2:
                    inside2[int(in1) - len(arr_junct_1) - 1][int(in2)] = int(val2)
                elif str(arr + '[' + in1 + ']') in list_ins_2:
                    list_ins_2.append(full_str_ind)
                    inside2[int(in1) - len(arr_junct_1) - 1].append(int(val2))
                else:
                    list_ins_2.append(str(arr + '[' + in1 + ']'))
                    list_ins_2.append(full_str_ind)
                    inside2.append([int(val2)])

        for item in arr_junct_1:
            shape1.append(item)

        shape2.append(cuts2[len(cuts2) - 1])
        for item2 in arr_junct_2:
            shape2.append(item2)

        cut1 = copy.deepcopy(cuts1[len(cuts1) - 1])
        cut1.reverse()
        shape1.append(cut1)
        cut2 = copy.deepcopy(cuts2[0])
        cut2.reverse()
        shape2.append(cut2)
        inside1.reverse()

        for ang in inside1:
            ang2 = copy.deepcopy(ang)
            ang2.reverse()
            shape1.append(ang2)
        shape1.append(cuts1[0])

        for ang3 in inside2:
            shape2.append(ang3)

        cl1 = check_close.build_shape2(shape1, build_dir(shape1))
        cl2 = check_close.build_shape2(shape2, build_dir(shape2))

        if not cl1 or not cl2:
            str_another_sol = ""
            for i in range(0, len(arr_junct_1)):
                str_another_sol += "arr_junct_1[" + str(i) + "] = " + str(arr_junct_1_i[i]) + " & arr_junct_2[" + str(
                    i) + "] = " + str(arr_junct_2_i[i]) + " & "
            for k in range(0, len(inside1)):
                str_another_sol += "inside1[" + str(k + len(arr_junct_1) + 1) + "][0] = " + str(
                    inside1[k][0]) + " & inside1[" + str(k + len(arr_junct_1) + 1) + "][1] = " + str(
                    inside1[k][1]) + " & inside1[" + str(k + len(arr_junct_1) + 1) + "][2] = " + str(
                    inside1[k][2]) + " & inside2[" + str(
                    k + len(arr_junct_1) + 1) + "][0] = " + str(inside2[k][0]) + " & inside2[" + str(
                    k + len(arr_junct_1) + 1) + "][1] = " + str(inside2[k][1]) + " & inside2[" + str(
                    k + len(arr_junct_1) + 1) + "][2] = " + str(inside2[k][2]) + " & "
            str_another_sol += "cuts1[" + str(len(arr_junct_1)) + "][0] = " + str(cuts1[0][0]) + " & cuts1[" + str(len(
                arr_junct_1)) + "][1] = " + str(cuts1[0][1]) + " & cuts1[" + str(len(arr_junct_1)) + "][2] = " + str(
                cuts1[0][2]) + " & cuts1[" + str(len(arr_junct_1) + len(cuts1) - 1) + "][0] = " + str(
                cuts1[len(cuts1) - 1][0]) + " & cuts1[" + str(
                len(arr_junct_1) + len(cuts1) - 1) + "][1] = " + str(cuts1[len(cuts1) - 1][1]) + " & cuts1[" + str(
                len(arr_junct_1) + len(cuts1) - 1) + "][2] = " + str(cuts1[len(cuts1) - 1][2]) + " & " + "cuts2[" + str(
                len(arr_junct_1)) + "][0] = " + str(cuts2[0][0]) + " & cuts2[" + str(len(
                arr_junct_1)) + "][1] = " + str(cuts2[0][1]) + " & cuts2[" + str(len(arr_junct_1)) + "][2] = " + str(
                cuts2[0][2]) + " & cuts2[" + str(len(arr_junct_1) + len(cuts1) - 1) + "][0] = " + str(
                cuts2[len(cuts1) - 1][0]) + " & cuts2[" + str(
                len(arr_junct_1) + len(cuts1) - 1) + "][1] = " + str(cuts2[len(cuts1) - 1][1]) + " & cuts2[" + str(
                len(arr_junct_1) + len(cuts1) - 1) + "][2] = " + str(cuts2[len(cuts1) - 1][2])
            os.chdir(r'C:\Users\liatw\OneDrive\Desktop\NuSMV-2.6.0-win64\bin')
            m = open('areatri' + str(j) + '.smv', 'r')
            lines = m.readlines()
            model = open('areatri' + str(j) + '.smv', 'w')
            for line in lines:
                if 'G !(state = correct' not in line:
                    model.write(line)
                else:
                    if 'G !(state = correct)' in line:
                        model.write(line[:-2] + ' & !(' + str_another_sol + '))')
                    else:
                        imp, rest = line.split('))')
                        model.write(imp + ') & !(' + str_another_sol + '))')
            run_model('areatri' + str(j) + '.smv', j, len(shape1))
        return cl1 and cl2
    """
        for ang in inside2:
            shape2.append(ang)
        shape1.append(cuts1[0])
        shape2.append(cuts2[len(cuts1) - 1])
    """


def get_shapes2(j, original):
    os.chdir(r'C:\Users\liatw\OneDrive\Desktop\NuSMV-2.6.0-win64\bin')
    out = open('output_area' + str(j) + '.txt', 'r')
    text = out.read()
    if 'is false' in text:
        res, text2 = text.split('state = initial')
        rows = text2.split('\n')

        arr_junct_1 = []
        arr_junct_1_i = []
        arr_junct_2 = []
        arr_junct_2_i = []
        list_ind_1 = []
        list_ind_2 = []

        list_cuts1 = []
        list_cuts2 = []
        cuts1 = []
        cuts2 = []

        inside1 = []
        inside2 = []
        list_ins_1 = []
        list_ins_2 = []

        shape1 = []
        shape2 = []
        for row in rows:
            if 'arr_junct_1' in row:
                full_str_ind, val2 = row.split(' = ')
                ind1 = full_str_ind[:-1]
                str2, ind = ind1.split('[')
                if full_str_ind in list_ind_1:
                    arr_junct_1[int(ind)] = original[int(val2)]
                    arr_junct_1_i[int(ind)] = int(val2)
                else:
                    list_ind_1.append(full_str_ind)
                    arr_junct_1.append(original[int(val2)])
                    arr_junct_1_i.append(int(val2))

            elif 'arr_junct_2' in row:
                full_str_ind, val2 = row.split(' = ')
                ind1 = full_str_ind[:-1]
                str2, ind = ind1.split('[')
                if full_str_ind in list_ind_2:
                    arr_junct_2[int(ind)] = original[int(val2)]
                    arr_junct_2_i[int(ind)] = int(val2)
                else:
                    list_ind_2.append(full_str_ind)
                    arr_junct_2.append(original[int(val2)])
                    arr_junct_2_i.append(int(val2))

            elif 'cuts1' in row:
                full_str_ind, val2 = row.split(' = ')
                arr, in1, in2 = full_str_ind.split('[')
                in1 = in1[:-1]
                in2 = in2[:-1]
                if full_str_ind in list_cuts1:
                    cuts1[int(in1) - len(arr_junct_1)][int(in2)] = int(val2)
                elif str(arr + '[' + in1 + ']') in list_cuts1:
                    list_cuts1.append(full_str_ind)
                    cuts1[int(in1) - len(arr_junct_1)].append(int(val2))
                else:
                    list_cuts1.append(str(arr + '[' + in1 + ']'))
                    list_cuts1.append(full_str_ind)
                    cuts1.append([int(val2)])

            elif 'cuts2' in row:
                full_str_ind, val2 = row.split(' = ')
                arr, in1, in2 = full_str_ind.split('[')
                in1 = in1[:-1]
                in2 = in2[:-1]
                if full_str_ind in list_cuts2:
                    cuts2[int(in1) - len(arr_junct_1)][int(in2)] = int(val2)
                elif str(arr + '[' + in1 + ']') in list_cuts2:
                    list_cuts2.append(full_str_ind)
                    cuts2[int(in1) - len(arr_junct_1)].append(int(val2))
                else:
                    list_cuts2.append(str(arr + '[' + in1 + ']'))
                    list_cuts2.append(full_str_ind)
                    cuts2.append([int(val2)])

            elif 'inside1' in row:
                full_str_ind, val2 = row.split(' = ')
                arr, in1, in2 = full_str_ind.split('[')
                in1 = in1[:-1]
                in2 = in2[:-1]
                if full_str_ind in list_ins_1:
                    inside1[int(in1) - len(arr_junct_1) - 1][int(in2)] = int(val2)
                elif str(arr + '[' + in1 + ']') in list_ins_1:
                    list_ins_1.append(full_str_ind)
                    inside1[int(in1) - len(arr_junct_1) - 1].append(int(val2))
                else:
                    list_ins_1.append(str(arr + '[' + in1 + ']'))
                    list_ins_1.append(full_str_ind)
                    inside1.append([int(val2)])

            elif 'inside2' in row:
                full_str_ind, val2 = row.split(' = ')
                arr, in1, in2 = full_str_ind.split('[')
                in1 = in1[:-1]
                in2 = in2[:-1]
                if full_str_ind in list_ins_2:
                    inside2[int(in1) - len(arr_junct_1) - 1][int(in2)] = int(val2)
                elif str(arr + '[' + in1 + ']') in list_ins_2:
                    list_ins_2.append(full_str_ind)
                    inside2[int(in1) - len(arr_junct_1) - 1].append(int(val2))
                else:
                    list_ins_2.append(str(arr + '[' + in1 + ']'))
                    list_ins_2.append(full_str_ind)
                    inside2.append([int(val2)])

        for item in arr_junct_1:
            shape1.append(item)

        shape2.append(cuts2[len(cuts2) - 1])
        for item2 in arr_junct_2:
            shape2.append(item2)

        cut1 = copy.deepcopy(cuts1[len(cuts1) - 1])
        cut1.reverse()
        shape1.append(cut1)
        cut2 = copy.deepcopy(cuts2[0])
        cut2.reverse()
        shape2.append(cut2)
        inside1.reverse()

        for ang in inside1:
            ang2 = copy.deepcopy(ang)
            ang2.reverse()
            shape1.append(ang2)
        shape1.append(cuts1[0])

        for ang3 in inside2:
            shape2.append(ang3)

        cl1 = check_close.build_shape2(shape1, build_dir(shape1))
        cl2 = check_close.build_shape2(shape2, build_dir(shape2))

        if not cl1 or not cl2:
            str_another_sol = ""
            for i in range(0, len(arr_junct_1)):
                str_another_sol += "arr_junct_1[" + str(i) + "] = " + str(arr_junct_1_i[i]) + " & arr_junct_2[" + str(
                    i) + "] = " + str(arr_junct_2_i[i]) + " & "
            for k in range(0, len(inside1)):
                str_another_sol += "inside1[" + str(k + len(arr_junct_1) + 1) + "][0] = " + str(
                    inside1[k][0]) + " & inside1[" + str(k + len(arr_junct_1) + 1) + "][1] = " + str(
                    inside1[k][1]) + " & inside1[" + str(k + len(arr_junct_1) + 1) + "][2] = " + str(
                    inside1[k][2]) + " & inside2[" + str(
                    k + len(arr_junct_1) + 1) + "][0] = " + str(inside2[k][0]) + " & inside2[" + str(
                    k + len(arr_junct_1) + 1) + "][1] = " + str(inside2[k][1]) + " & inside2[" + str(
                    k + len(arr_junct_1) + 1) + "][2] = " + str(inside2[k][2]) + " & "
            str_another_sol += "cuts1[" + str(len(arr_junct_1)) + "][0] = " + str(cuts1[0][0]) + " & cuts1[" + str(len(
                arr_junct_1)) + "][1] = " + str(cuts1[0][1]) + " & cuts1[" + str(len(arr_junct_1)) + "][2] = " + str(
                cuts1[0][2]) + " & cuts1[" + str(len(arr_junct_1) + len(cuts1) - 1) + "][0] = " + str(
                cuts1[len(cuts1) - 1][0]) + " & cuts1[" + str(
                len(arr_junct_1) + len(cuts1) - 1) + "][1] = " + str(cuts1[len(cuts1) - 1][1]) + " & cuts1[" + str(
                len(arr_junct_1) + len(cuts1) - 1) + "][2] = " + str(cuts1[len(cuts1) - 1][2]) + " & " + "cuts2[" + str(
                len(arr_junct_1)) + "][0] = " + str(cuts2[0][0]) + " & cuts2[" + str(len(
                arr_junct_1)) + "][1] = " + str(cuts2[0][1]) + " & cuts2[" + str(len(arr_junct_1)) + "][2] = " + str(
                cuts2[0][2]) + " & cuts2[" + str(len(arr_junct_1) + len(cuts1) - 1) + "][0] = " + str(
                cuts2[len(cuts1) - 1][0]) + " & cuts2[" + str(
                len(arr_junct_1) + len(cuts1) - 1) + "][1] = " + str(cuts2[len(cuts1) - 1][1]) + " & cuts2[" + str(
                len(arr_junct_1) + len(cuts1) - 1) + "][2] = " + str(cuts2[len(cuts1) - 1][2])
            os.chdir(r'C:\Users\liatw\OneDrive\Desktop\NuSMV-2.6.0-win64\bin')
            m = open('areasq' + str(j) + '.smv', 'r')
            lines = m.readlines()
            model = open('areasq' + str(j) + '.smv', 'w')
            for line in lines:
                if 'G !(state = correct' not in line:
                    model.write(line)
                else:
                    if 'G !(state = correct)' in line:
                        model.write(line[:-2] + ' & !(' + str_another_sol + '))')
                    else:
                        imp, rest = line.split('))')
                        model.write(imp + ') & !(' + str_another_sol + '))')
            run_model('areasq' + str(j) + '.smv', j, len(shape1))
        return cl1 and cl2
    """
        for ang in inside2:
            shape2.append(ang)
        shape1.append(cuts1[0])
        shape2.append(cuts2[len(cuts1) - 1])
    """


def guess_shape(num_match):
    if num_match <= 3:
        return None
    shape = []
    for k in range(0, num_match):
        angles = [60, 120, 180, 300, 240]
        if k + 1 == num_match:
            ang = random.choice(angles)
            shape.append([k + 1, ang, 1])

        else:
            ang = random.choice(angles)
            shape.append([k + 1, ang, k + 2])

    while not check_close.build_shape2(shape, build_dir(shape)):
        shape = []
        for k in range(0, num_match):

            angles = [60, 120, 180, 300, 240]
            if k + 1 == num_match:
                shape.append([k + 1, random.choice(angles), 1])
            else:
                shape.append([k + 1, random.choice(angles), k + 2])
    return shape


def guess_shape2(num_match):
    if num_match <= 3:
        return None
    shape = []
    for k in range(0, num_match):
        angles = [90, 180, 270]
        if k + 1 == num_match:
            ang = random.choice(angles)
            shape.append([k + 1, ang, 1])

        else:
            ang = random.choice(angles)
            shape.append([k + 1, ang, k + 2])

    while not check_close.build_shape2(shape, build_dir(shape)):
        shape = []
        for k in range(0, num_match):

            angles = [90, 180, 270]
            if k + 1 == num_match:
                shape.append([k + 1, random.choice(angles), 1])
            else:
                shape.append([k + 1, random.choice(angles), k + 2])
    return shape


def create_shape(k):
    shape = [[1, 120, 2], [2, 240, 3], [3, 120, 4]]

    for i in range(4, k / 2 - 2):
        if i % 2 == 0:
            shape.append([i, 120, i + 1])
        else:
            shape.append([i, 240, i + 1])

    shape.append([k / 2 - 2, 120, k / 2 - 1])
    shape.append([k / 2 - 1, 240, k / 2])
    shape.append([k / 2, 120, k / 2 + 1])
    shape.append([k / 2 + 1, 120, k / 2 + 2])
    shape.append([k / 2 + 2, 240, k / 2 + 3])
    shape.append([k / 2 + 3, 120, k / 2 + 4])

    for i in range(k / 2 + 4, k - 2):
        if i % 2 == 1:
            shape.append([i, 120, i + 1])
        else:
            shape.append([i, 240, i + 1])

    shape.append([k - 2, 120, k - 1])
    shape.append([k - 1, 240, k])
    shape.append([k, 120, 1])
    return shape


def create_shape2(k):
    shape = [[1, 90, 2], [2, 270, 3], [3, 180, 4], [4, 90, 5]]

    for i in range(5, k / 2 - 3):
        shape.append([i, 180, i + 1])

    shape.append([k / 2 - 3, 90, k / 2 - 2])
    shape.append([k / 2 - 2, 180, k / 2 - 1])
    shape.append([k / 2 - 1, 270, k / 2])
    shape.append([k / 2, 90, k / 2 + 1])
    shape.append([k / 2 + 1, 90, k / 2 + 2])
    shape.append([k / 2 + 2, 270, k / 2 + 3])
    shape.append([k / 2 + 3, 180, k / 2 + 4])
    shape.append([k / 2 + 4, 90, k / 2 + 5])

    for i in range(k / 2 + 5, k - 3):
        shape.append([i, 180, i + 1])

    shape.append([k - 3, 90, k - 2])
    shape.append([k - 2, 180, k - 1])
    shape.append([k - 1, 270, k])
    shape.append([k, 90, 1])
    return shape


def main():
    # write_model_sq(1, [[1,180,2],[2,90,3],[3,180,4],[4,90,5],[5,180,6],[6,270,7],[7,90,8], [8,180,9], [9,270,10], [10,90,11], [11,180,12], [12,90,13],[13,180,14],[14,90,15],[15,180,16],[16,270,17],[17,90,18],[18,180,19],[19,270,20],[20,90,1]], 2)
    original = []
    avg_solved = 0
    avg_no = 0
    count_sol = 0
    count_no = 0

    for k in range(70, 78, 8):
        for j in range(5, 4, -1):
            original = create_shape(k)
            bool1 = check_close.build_shape2(original, build_dir(original))
            total = 0
            num_m = j
            write_model_tri(j, original, num_m)
            flag_solved, run_time = find_solution(j)
            total += run_time
            closed = True
            if flag_solved == 2:
                closed = get_shapes(j, original)
            while not closed and flag_solved == 2:
                flag_solved, run_time = find_solution(j)
                total += run_time
                closed = get_shapes(j, original)

            if flag_solved == 2:
                # avg_solved += total / 5.0
                count_sol += 1
                print 'solved'
            else:
                # avg_no += total / 5.0
                count_no += 1

            if count_sol >= 1:
                print total
                print num_m
                print k


if __name__ == '__main__':
    main()
