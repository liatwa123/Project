# Interactive Matchstick Riddles Solver

Matchstick riddles are popular puzzles that typically require adding, removing or moving around matchsticks from an initial setup to make an equation true, or to create a given number of identical shapes.
This is an automatic method and tool to efficiently solve several classes of matchstick puzzles by using formal verification methods. 
The mathstick puzzle is encoded as a transition system and model checking is used to search for a counter example that serves as a solution to the underlying puzzle, or to prove that no solution exists. Our tool
can also find multiple solutions if more than one solution exists and automatically generate new puzzles. This tool uses different
algorithms including Linear Temporal Logic (LTL) based on Binary Decision Diagrams and SAT and demonstrate efficient solutions for some challenging mathctick puzzles.
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

### Running the GUI

After following the steps in Prerequisites and Getting Started:

In order to run the project, click 'Run solver':

![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/run.jpg?raw=true)



If this option does not appear, click 'Run' and then press 'solver':

![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/run2.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/run3.jpg?raw=true)


Then, you will see a new screen:


![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/main_menu.jpg?raw=true)


This is the main menu of the riddles solver. There, you need to enter the number of the riddle that you want to solve. If you do not want to continue solving a specific riddle type, you will return automatically to this menu. If you want to exit from the solver, it is possible only from this menu (option 0).

#### Mathematical Riddles
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/nav_math.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_add_nor.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_add_opt.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_add_nor.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_add_opt.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_remove_nor.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_remove_opt.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_remove_nor.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_remove_opt.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_move_nor.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_move_opt.jpg?raw=true)

#### Square Riddles 
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/nav_square.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/nor_sqr_in1.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/nor_sqr_in2.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/nor_sqr_in3.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/nor_sqr_in4.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_sqr_opt_move1.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_sqr_opt_move2.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_sqr_opt_move3.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_sqr_opt_move4.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_sqr_opt_sq1.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_sqr_opt_sq2.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_sqr_opt_sq3.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_sqr_opt_sq4.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_sqr_nor1.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_sqr_nor2.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_sqr_nor3.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_sqr_opt_sq1.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_sqr_opt_sq2.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_sqr_opt_sq3.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_sqr_opt_move1.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_sqr_opt_move2.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_sqr_opt_move3.jpg?raw=true)

#### Sum of Matchstick Heads Riddles
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/nav_sum.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_sum1.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_sum2.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_sum3.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_sum1.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/gen_sum2.jpg?raw=true)

#### Shape Division Riddles
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/nav_area.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_area_sq1.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_area_sq2.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_area_sq3.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/man_area_tri1.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/series_area_sq1.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/series_area_sq2.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/series_area_tri1.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/series_area_tri2.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/series_area_tri3.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/all_sol_move_in.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/all_sol_move_out1.jpg?raw=true)
![Alt text](https://github.com/liatwa123/Project-Matchstick-Puzzles/blob/master/Screenshots/all_sol_move_out2.jpg?raw=true)



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
