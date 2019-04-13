------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Name and UTA ID of the student:
Name - Avinash Shanker
UTA ID - 1001668570

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

What programming language is used:
Python 2
Omega Compatible

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

How the code is structured:
1) maxconnect4.py is the code which has to be run on command line which imports MaxConnect4Game.py
2) MinMax and Alpla-Beta Pruning functions, Eval function logic are written in MaxConnect4Game.py
3) There are two modes in which the code operates, first in one-move game and second is interative game with human player.
4) Input is given in text file and in interactive mode input is provided in from screen
5) Values are processed in the form of a tree
6) Function interactivegame will make a function call to aiplay_interactive with the input provided of the game state and based on human-next or computer-next next move will be decided
7) During one move game aiplay will invoked which will perform depth limited minmax.
8) For both modes Logic for MinMax with 'Alpha Beta' Pruning is implemented function Min_Max_Logic in MaxConnect4Game.py
9) Eval function logic is written in Evaluation_Function inside MaxConnect4Game.py
10) Utility values are calculated from the terminal_test function and the evaluation function Evaluation_Function, terminal_test validates if board is full.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

How to run the code with specific instructions:
The code is programmed to run in Python 2, Run compatible in Omega

1) For one_move game:
   python maxconnect4.py one-move input1.txt output.txt 3

2) For Interrative mode:
   When Computer as the next player:
   python maxconnect4.py interactive input1.txt computer-next 3

   When Human as the next player:
   python maxconnect4.py interactive input1.txt human-next 3

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

