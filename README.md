```
The University of Melbourne
School of Computing and Information Systems
COMP30024 Artificial Intelligence
```

### Single-playerExpendibots

The single-player variant ofExpendibotswe will analyse works as follows. You will always play as White, and
you will be the only player that acts. The Black player is static and does not take any turns. As the White
player, you will start with at most 3 tokens in some configuration. You will repeatedly take turns until all of the
Black tokens have been eliminated, at which point you win. If on your last turn you eliminate all enemy tokens
but lose your last token, you still win.


### The tasks

Firstly, your team will design and implement a program that ‘plays’ a game of single-playerExpendibots— given
a board configuration, your program will find a sequence of actions for the White player to take to win (to
eliminate all enemy tokens). Your program’s performance will be judged based upon its ability to find winning
sequences of actions and handle cases involving multiple tokens (See the Assessment section for details). There
isnorequirement that your sequences be optimal.
Secondly, your team will write a brief report discussing and analysing the strategy your program uses to solve
this search problem. These tasks are described in detail in the following sections.

## The program

You must create a program to play this game in the form of a Python 3.6 module calledsearch(for example, a
folder namedsearchcontaining a Python file called main .pyas the program entry-point^1 would be sufficient
— see the provided skeleton code for a starting point).
When executed, your program must read a JSON-formatted board configuration from a file, calculate a
winning sequence of actions, and print out this sequence of actions. The input and output format are specified
below, along with the coordinate system we will use for both input and output.
