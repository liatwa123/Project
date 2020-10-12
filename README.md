# Interactive Matchstick Riddles Solver

Matchstick riddles are popular puzzles that typically require adding, removing or moving around matchsticks from an initial setup to make an equation true, or to create a given number of identical shapes.
This is an automatic method and tool to efficiently solve several classes of matchstick puzzles by using formal verification methods. 
The mathstick puzzle is encoded as a transition system and model checking is used to search for a counter example that serves as a solution to the underlying puzzle, or to prove that no solution exists. Our tool
can also find multiple solutions if more than one solution exists and automatically generate new puzzles. This tool uses different
algorithms including Linear Temporal Logic (LTL) based on Binary Decision Diagrams and SAT and demonstrate efficient solutions for some challenging matchstick puzzles.
This tool can serve as an illustrative example in teaching formal verification.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

#### NuSMV

Install NuSMV 2.6 on your computer.

Go to the bin folder in this github project and copy the files to your NuSMV bin folder.

#### Python

Install PyCharm and Python 2.7 on your computer.

In this github project, go to the Python_Interactive_Solver folder.

#### PyCharm

Open a new PyCharm project including all the files in the Python_Interactive_Solver folder.

For each file in the Interactive Python Solver: if chdir method is found, change the directory to your NuSMV bin folder path. If there are import errors (Python packages/libraries missing), move the mouse to the red errors and click 'install package_name.py'. 

### Prerequisites

#### Python + PyCharm Installation

Install Python 2.7 here: https://www.python.org/download/releases/2.7/

Install PyCharm here: https://www.jetbrains.com/pycharm/

Instructions for Python interpreter configuration in PyCharm (connecting Python 2.7 with PyCharm): https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html#add-existing-interpreter

#### NuSMV Installation

Go to this link (you do not have to register, just enter the words you see in the box): http://nusmv.fbk.eu/NuSMV/download/getting_bin-v2.html

Then, click on the zip file with the correct NuSMV 2.6 version (win64 / win32)

Extract the zip file.

## Running the GUI

After following the steps in Prerequisites and Getting Started:

In order to run the project, click 'Run solver':

![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/run.jpg?raw=true)



If this option does not appear, click 'Run' and then press 'solver':

![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/run2.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/run3.jpg?raw=true)


Then, you will see a new screen:


![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/main_menu.jpg?raw=true)


This is the main menu of the riddles solver. There, you need to enter the number of the riddle that you want to solve. If you do not want to continue solving a specific riddle type, you will return automatically to this menu. If you want to exit from the solver, it is possible only from this menu (option 0).

### Mathematical Equations Riddles

#### Features:
Solving normal riddles (the user enters all the input)

Solving normal riddles (the computer chooses a random equation)

Finding all possible solutions (for normal riddles, both normal and random input, with move operations only)

Solving optimization riddles (the user enters all the input except for the number of matchsticks to add/remove/move)

Solving optimization riddles (the computer chooses a random equation, the number of matchsticks to add/remove/move should be optimized)

Generating normal riddles and solving them

Generating optimization riddles and solving them

#### The Navigation Menu

![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/nav_math.jpg?raw=true)

When the user chooses to solve mathematical equations riddles, the input variables that must be entered are: the operation (add / remove / move), the riddle’s type (normal / optimization), the input type (manual / random / generated), the number of digits per operand and the operator (+ / -). The rest of the input depends on the options chosen. For example: a user that wants to solve a normal riddle and enter the input manually – will enter all the operands next; A user that wants to generate a normal riddle – does not need to enter any input next.
In the end of the process, the input will be printed on the screen. (Note: in the generated riddles, the generated input will be printed on the screen too.)

#### Manual input, normal riddles, add matchsticks
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_add_nor.jpg?raw=true)

#### Manual input, optimization riddles, add matchsticks
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_add_opt.jpg?raw=true)

#### Generated input, normal riddles, add matchsticks
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_add_nor.jpg?raw=true)

#### Generated input, optimization riddles, add matchsticks
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_add_opt.jpg?raw=true)

#### Manual input, normal riddles, remove matchsticks
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_remove_nor.jpg?raw=true)

#### Manual input, optimization riddles, remove matchsticks
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_remove_opt.jpg?raw=true)

#### Generated input, normal riddles, remove matchsticks
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_remove_nor.jpg?raw=true)

#### Generated input, optimization riddles, remove matchsticks
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_remove_opt.jpg?raw=true)

#### Manual input, normal riddles, move matchsticks
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_move_nor.jpg?raw=true)

#### Manual input, optimization riddles, move matchsticks
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_move_opt.jpg?raw=true)

#### Generated input, normal riddles, move matchsticks
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_move_nor.jpg?raw=true)

#### Generated input, optimization riddles, move matchsticks
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_move_opt.jpg?raw=true)

#### Move operation - finding all possible solutions:

For finding all the possible solutions (Move operation), the solutions will be printed one after another:

![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/all_sol_move_in.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/all_sol_move_out1.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/all_sol_move_out2.jpg?raw=true)


### Square Riddles

#### Features:

Solving normal riddles (the user enters all the input)

Solving optimization riddles (the user enters all the input except for the number of matchsticks to move)

Solving optimization riddles (the user enters all the input except for the number of final squares)

Generating normal riddles and solving them

Generating optimization riddles and solving them (the user chooses which parameter to optimize)

#### The Navigation Menu
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/nav_square.jpg?raw=true)

When the user chooses to solve squares riddles, the input variables that must be entered are: the riddle’s type (normal / optimization), the input type (manual / generated). The rest of the input depends on the options chosen. For example: a user that wants to solve a normal riddle and enter the input manually – will enter the initial construction, the final number of squares and the number of matchsticks to move next; A user that wants to generate a normal riddle – does not need to enter any input next.
In the end of the process, the input will be printed on the screen. (Note: in the generated riddles, the generated input will be printed on the screen too.)
In order to enter the initial construction, the user needs to enter ‘T’ if a square appears, ‘F’ otherwise. 

The output format is the same for all the squares riddles. The green matchsticks represent the new matchsticks’ locations, the grey ones represent the old locations. 

##### IMPORTANT - CLOSE THE WINDOWS TITLED 'THE INPUT' AND 'THE OUTPUT' IN ORDER TO CONTINUE THE EXECUTION OF THE PROGRAM! THE EXECUTION OF THE SOLVER STOPS UNTIL THE USER CLOSES THESE WINDOWS!!!

#### Manual input, normal riddles
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/nor_sqr_in1.jpg?raw=true)

![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/nor_sqr_in2.jpg?raw=true)

#### Manual input, normal riddles, input VS output
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/nor_sqr_in3.jpg?raw=true)

![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/nor_sqr_in4.jpg?raw=true)

#### Manual input, optimization riddles, the optimized parameter - the number of final squares
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_sqr_opt_move1.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_sqr_opt_move2.jpg?raw=true)

#### Manual input, optimization riddles, the optimized parameter - the number of final squares, input VS output
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_sqr_opt_move3.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_sqr_opt_move4.jpg?raw=true)


#### Manual input, optimization riddles, the optimized parameter - the number of matchsticks to move
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_sqr_opt_sq1.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_sqr_opt_sq2.jpg?raw=true)

#### Manual input, optimization riddles, the optimized parameter - the number of matchsticks to move, input VS output
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_sqr_opt_sq3.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_sqr_opt_sq4.jpg?raw=true)

#### Generated input, normal riddles
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_sqr_nor1.jpg?raw=true)

#### Generated input, normal riddles, input VS output
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_sqr_nor2.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_sqr_nor3.jpg?raw=true)

#### Generated input, optimization riddles, the optimized parameter - the number of final squares
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_sqr_opt_sq1.jpg?raw=true)

#### Generated input, optimization riddles, the optimized parameter - the number of final squares, input VS output
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_sqr_opt_sq2.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_sqr_opt_sq3.jpg?raw=true)

#### Generated input, optimization riddles, the optimized parameter - the number of matchsticks to move
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_sqr_opt_move1.jpg?raw=true)

#### Generated input, optimization riddles, the optimized parameter - the number of final squares, input VS output
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_sqr_opt_move2.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_sqr_opt_move3.jpg?raw=true)

### Sum of Matchstick Heads Riddles

#### Features:

Solving normal riddles (the user enters all the input)

Generating normal riddles and solving them

#### The Navigation Menu
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/nav_sum.jpg?raw=true)

When the user chooses to solve sum of matchstick heads riddles, the only input that must be entered is the input type (manual / generated). The rest of the input depends on the option chosen (a user that wants to generate a riddle automatically will not need to enter any input next). 
In the end of the process, the input will be printed on the screen. (Note: in the generated riddles, the generated input will be printed on the screen too.)
In order to enter the initial construction, the user needs to enter the pointing direction for each matchstick. The possible directions are: ‘R’ – right, ‘L’ – left, ‘U’ – up, ‘D’ – down.

The output format is the same for all the sum of matchstick heads riddles. The pointing directions are printed.

##### IMPORTANT - CLOSE THE WINDOWS TITLED 'THE INPUT' AND 'THE OUTPUT' IN ORDER TO CONTINUE THE EXECUTION OF THE PROGRAM! THE EXECUTION OF THE SOLVER STOPS UNTIL THE USER CLOSES THESE WINDOWS!!!

#### Manual input
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_sum1.jpg?raw=true)

#### Manual input, input VS output
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_sum2.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_sum3.jpg?raw=true)

#### Generated input, input VS output
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_sum1.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_sum2.jpg?raw=true)

### Shape Division Riddles

#### Features:

Solving normal riddles: the user enters all the input
Solving normal riddles: the computer chooses a random shape
Solving normal riddles: the user enters the basic area unit, the number of matchsticks for division and the number of angles, the polygon is randomly created 
Solving normal riddles: the user enters the basic area unit, the number of matchsticks for division and the number of angles, the polygon is a part of a series of polygons. 

##### The Navigation Menu

![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/nav_area.jpg?raw=true)

When the user chooses to solve shape division riddles, the input variables that must be entered are the basic area unit (triangle / square), the number of angles and the input type (manual input / random shape / a constant shape which is a part of an input series). The rest of the input depends on the option chosen (a user that wants get an input shape automatically will only need to enter the number of matchsticks for division next). 
In the end of the process, the input will be printed on the screen. (Note: if the shape is automatically calculated, the input will be printed on the screen too.)
In order to enter the initial shape, the user needs to enter the angles:
Basic area unit – square: the angles must be: 90, 180, 270.
Basic area unit – triangle: the angles must be 60, 120, 180, 240, 300.

#### The input series (3rd input type)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/shapes_series.jpg?raw=true)

##### IMPORTANT - CLOSE THE WINDOWS TITLED 'THE INPUT' AND 'THE OUTPUT' IN ORDER TO CONTINUE THE EXECUTION OF THE PROGRAM! THE EXECUTION OF THE SOLVER STOPS UNTIL THE USER CLOSES THESE WINDOWS!!!

#### Shape Division Riddles – manual input – basic area unit: square

![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_area_sq1.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_area_sq2.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_area_sq3.jpg?raw=true)

#### Shape Division Riddles – manual input – basic area unit: triangle

![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_area_tri1.jpg?raw=true)

#### Shape Division Riddles – input series – basic area unit: square

![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/series_area_sq1.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/series_area_sq2.jpg?raw=true)

#### Shape Division Riddles – input series – basic area unit: triangle

![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/series_area_tri1.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/series_area_tri2.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/series_area_tri3.jpg?raw=true)

## Calculating the time complexity graphs

In the Interactive_Solver_Python folder, there are six relevant files: 

general2.py - this file includes methods controlling the mathematical equations riddles - operations: add/remove

general_move.py - this file includes methods controlling the mathematical equations riddles - 'move' operation

sqr_code_proj.py - this file includes methods controlling the square riddles

mathead_code_proj.py - this file includes methods controlling the sum of matchstick heads riddles

areanew_proj.py - this file includes methods controlling the shape division riddles

check_close.py - this file includes methods checking that a given shape is a polygon

#### Mathematical Equations riddles - operations: add/remove

The basic method used here is calculate_avg:

![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/avg_method.jpg?raw=true)

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

The output file contains the riddle's solution and the execution time. For each riddle, the status is returned (solved / not solved, valid / invalid) with its execution time,  after reading its output file.

The method counts the cases for the solved riddles and for the no - solution riddles and stops adding new cases to the average if a certain number of measurements (solved riddles / no-solution riddles) has been reached.

In order to calculate an average execution time, just change this method's rows as documented. 

In order to generate results for a full graph (execution time as a function of the number of matchsticks to add/remove): use this code template in the general2.py main() method:

    for i in range(0, 14):
        print str(calculate_avg('minus', i, 'remove', 1, i * 10 ** 7))  # you may change the operator, the number of digits per operand and the operation (1 is the number of                                                                             
                                                                        # digits per operand)
Finally, run general2.py.
                                           
#### Mathematical Equations riddles - operations: move

The basic method used here is calculate_avg:

![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/avg_method2.jpg?raw=true)

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

It calculates the average execution time for solved riddles         

The output file contains the riddle's solution and the execution time. For each riddle, the status is returned (solved / not solved, valid / invalid) with its execution time,  after reading its output file.

The method counts the cases for the solved riddles and for the no - solution riddles and stops adding new cases to the average if a certain number of measurements (solved riddles / no-solution riddles) has been reached.

In order to calculate an average execution time, just change this method's rows as documented. 

In order to generate results for a full graph (execution time as a function of the number of matchsticks to add/remove): use this code template in the general_move.py main() method:

    for i in range(0, 15):
        print str(calculate_avg('minus', i, 1, i * 10 ** 7))  # you may change the operator and the number of digits per operand (1 is the number of                                                                             
                                                                        # digits per operand)
                                                                        
Finally, run general_move.py. 

#### Square riddles

The basic method used here is calculate_avg:

![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/avg_method3.jpg?raw=true)

This function gets:

index - starting index for the input/output files

num_allowed - number of matchsticks required for solving the riddle

This function chooses randomly:

The initial number of 1-match-length squares

The initial number of 2-match-length squares

The initial number of 3-match-length squares

The squares locations 

It checks if the construction input is valid.

If yes - it writes a model file and runs it

It calculates the average execution time for solved riddles         

The output file contains the riddle's solution and the execution time. For each riddle, the status is returned (solved / not solved, valid / invalid) with its execution time,  after reading its output file.

The method counts the cases for the solved riddles and for the no - solution riddles and stops adding new cases to the average if a certain number of measurements (solved riddles / no-solution riddles) has been reached.

In order to calculate an average execution time, just change this method's rows as documented. 

In order to generate results for a full graph (execution time as a function of the number of matchsticks to move): use this code template in the sqr_code_proj.py main() method:

    for i in range(0, 11):
        print str(calculate_avg(i * 10 ** 7, i))  
                                                                        
Finally, run sqr_code_proj.py. 

#### Sum of Matchstick Heads riddles

The basic method used here is calculate_avg:

![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/avg_method4.jpg?raw=true)

This function gets:

index - starting index for the input/output files

This function chooses randomly:

match_rows: integers input array - the rows that the matchsticks point to (must be 1 - 4)

match_cols: integers input array - the columns that the matchsticks point to (must be 1 - 4)

match_dis: integers input array - the diagonals that the matchsticks point to (must be 1 - 2, 0:
     no diagonal was pointed by this match). This parameter is synchronized with the rows and columns guess.

It checks if the input equation is valid.

If yes - it writes a model file and runs it

It calculates the average execution time for solved riddles         

The output file contains the riddle's solution and the execution time. For each riddle, the status is returned (solved / not solved, valid / invalid) with its execution time,  after reading its output file.

The method counts the cases for the solved riddles and for the no - solution riddles and stops adding new cases to the average if a certain number of measurements (solved riddles / no-solution riddles) has been reached.

In order to calculate an average execution time, just change this method's rows as documented. 

In order to generate results for a full graph (execution time as a function of the number of matchsticks to add/remove): use this code template in the mathead_code_proj.py main() method:

    for i in range(0, 1):
        print str(calculate_avg(i))  # you may change the operator and the number of digits per operand (1 is the number of                                                                             
                                                                        # digits per operand)
                                                                        
Finally, run mathead_code_proj.py. 

#### Shape Division riddles

In order to get measurements for the shapes input series:
in areanew_proj.py, in main(), run the following code:

    times, flag_solved, run_time, shape1, shape2 = (-1, -1, -1, [], [])
    for k in range(14, 86, 8):  # for squares input series: change to (18, 4, 62)
        for j in range(5, 4, -1):
            original = create_shape(k)  # for squares input series: change to create_shape2(k)

            # for squares input series: change from 'T' to 'S'
            times, flag_solved, run_time, shape1, shape2 = solve_rid_input(k, original, j, 'T')
            if flag_solved == 2:
                print k
                print run_time
                
Repeat this code several times. 

## Built With

* [NuSMV](http://nusmv.fbk.eu/) - The model checker used
* [PyCharm](https://www.jetbrains.com/pycharm/) - The Python development environment (used for GUI and automation tests)

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.


## Authors

* **Liat Walter** - [Liatwa123](https://github.com/Liatwa123)

* **Hillel Kugler** - [kuglerh](https://github.com/kuglerh)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
