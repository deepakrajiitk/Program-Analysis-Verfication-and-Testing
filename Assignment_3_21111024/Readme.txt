1. data fact - <move command, index of move command>
2. direction - backward
3. each basic block in cfg consists of only one statement, this helps in better optimization
4. Initialization:
	- IN  --> empty set
	- OUT --> emtpy set
5. meet function:
	forward + forward = union
	backward + forward = empty set
	backward + backward = union
	left + forward = empty set
	left + left = union
	right + right = union
	left + right = empty set

6. OUT[n] = ((IN[n] U GEN[n]) - KILL[n]
7. At any program point, our algo find move statements which are available on all the path from that program point and are used before getting
   killed by any other statement, if more than on move command are available at IN of any program point, it means we can remove the move command
   at that point and add its value to the corresponding upcoming move commands in paths

Limitations:
-- in program, i am always considering there is a pendown(going by the worst case optimization scenario) that is why forward command will be killed
   by the backward command, left command will be kill by right move command, etc