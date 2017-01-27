# Campfire
### An esoteric programming language where every instruction is a branch
##### and you'll want to set them on fire
<hr/>
We all know that the standard flow of execution is so dull and boring, that's why every code anyone writes after "Hello world" has at least a conditional branch or a loop in it. With this in mind, I present you the most interesting language ever produced! In campfire every instruction doubles up as a (possibly conditional) branch, and since instructions are composed by a single byte this gives us an incredible 100% score on the branches per byte executed category!

###How it works

The instruction pointer starts from the first byte moving forward, but after every instruction:

 - If the instruction just executed occurs only once in the code, terminate.
 - If the top of the main stack is not 0, invert the direction
 - Jump to just after the next occurrence of the just executed instruction

The code is considered to be cyclic (the first and last characters are next to each other). Whats the _next_ occurrence of an instruction and what's the instruction _after_ that depend on the current direction.

The memory is composed by two stacks (main and auxiliary) which can contain an unlimited amount of arbitrary integers: most commands operate on the main stack, but every time a value is popped from a stack it is automatically pushed on the other one. Every stack has an infinite amount of implicit 0s on the bottom.

###Instructions

Lines starting with `#` are considered comments. Any newline is ignored.

Character|Instruction|Notes
--------------------|-----------------|----------------
0-9|Push the corresponding int on the main stack
\- + \* / % |b=pop(),a=pop(),push(a op b)| / is integer division
> < = |b=pop(),a=pop(),push(a compare b)| 1 for True, 0 for False
!|push(not(pop()))| Pushes 1 if popped value was 0, pushes 0 otherwise
\_|pop()| Pushes on auxiliary stack
^|pop() from auxiliary stack| Pushes on main stack
;|clear auxiliary stack| The only way to erase data
$|swap top two values on main stack| Doesn't use pop-push
&|push(integer from input)|
~|push(char from input)|
.|print((pop() as int)+space)|
,|print(pop() as char)|
"|start/end string mode| Any other char encountered while in string mode pushes its value instead of executing normally.
Anything else|noop|

Instruction pointer jumps on noops as it does on any other command. Even during string mode branches are performed after every character pushed.

###Example of program flow:

    ab1dabc1ca
    1 36 24  5
(First line is the code, second line the order of execution)

In this code, all letters are noops, while the `1` pushes a 1 on the stack. After executing the first `a`, the top of stack is still 0 (an empty stack is considered as full of 0s), so the direction doesn't change and the next instruction to be executed is the one after the next `a`. We reach `b`, and then jump again in the same way (while wrapping from the end to the start of the code). The `1` then puts a 1 to the top of the stack, so now we need to switch direction and execute the instruction before the previous `1` (wrapping again). In the same way, we execute `c` and `a`, changing direction every time (there's still a 1 on top of the stack). We finally execute `d` then, since it's the only `d` in the whole code, the program terminates.
