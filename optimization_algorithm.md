# Optimizing the Solutions
### The limits updating algorithm

This algorithm returns new limits for the optimization model: lower, upper. It also returns a status flag –
‘mid’: the upper/lower bound was chosen to be: the median of the previous range; ‘last’: the upper bound was chosen to be: (the current minimal number of matchsticks for the operation that leads to a correct solution) - 1.


#### First iteration (no previous limits):

If the riddle is solved and the parameter == 0: return the construction, return 0 as the minimum. Otherwise: calculate the maximal value of this parameter (max), if max == 0: stop. Else: change the limits to 1, max



#### The following iterations:

If the current minimal value that leads to a correct solution is 1: stop

If a solution was found in the previous range:

----> If prev. lower bound == prev. upper bound: stop

----> If the previous range’s median >  the current minimal value of the parameter leads to a correct solution: status = ‘last’. Else: status = ‘mid’

----> Return prev. lower, min(the previous range’s median, the current minimal value that leads to a correct solution - 1), status

If no solution was found in the previous range:

----> If the current minimal value that leads to a correct solution == prev. upper + 1: stop

----> If status == ‘last’: stop

----> If it is the first time searching for solutions (no status value): stop

----> If status == ‘mid’: return prev.upper + 1, current minimal value that leads to a correct solution - 1, ‘mid’


### The optimization algorithm

#### First iteration: the same as the first iteration in the limits updating, if max == 0 return No Solution


#### The following iterations: (stop iterating if no new limits are returned)

Find a solution in the range (lower, upper). If there is a solution: save the solution and the current parameter's value: current\_min. Update the limits (lower and upper), save the status (middle of range / last solution – 1).

After the iterations are finished: return the last solution found and the minimal value.

