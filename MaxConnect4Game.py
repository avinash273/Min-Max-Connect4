#!/usr/bin/env python
# Written by Chris Conly based on C++
# code provided by Vassilis Athitsos
# Written to be Python 2.4 compatible for omega

# Logic Modified of the Sample code By Avinash Shanker
# AXS8570
# 1001668570s
# Code Contains MinMax and Alpla-Beta Pruning functions
# Eval functions

import sys
from copy import deepcopy
import random

class maxConnect4Game:
    def __init__(self):
        self.gameBoard = [[0 for i in range(7)] for j in range(6)]
        self.currentTurn = 1
        self.player1Score = 0
        self.player2Score = 0
        self.pieceCount = 0
        self.gameFile = None
	self.children = []
        self.name = 'root'
	self.player = 0
	self.alpha = -99
	self.beta = 99
	self.depth = 0
        
    # Count the number of pieces already played
    def CountPiece(self):
        self.pieceCount = sum(1 for row in self.gameBoard for piece in row if piece)

    # Output current game status to console
    def printGameBoard(self):
        print ' -----------------'
        for i in range(6):
            print ' |',
            for j in range(7):
                print('%d' % self.gameBoard[i][j]),
            print '| '
        print ' -----------------'

    # Output current game status to file
    def printGameBoardToFile(self):
        for row in self.gameBoard:
            self.gameFile.write(''.join(str(col) for col in row) + '\r\n')
        self.gameFile.write('%s\r\n' % str(self.currentTurn))

    # pen the output of interative to a file
    def WriteToFile_Interactive(self, outfile):
        self.gameFile = open(outfile, 'w')
        for row in self.gameBoard:
            self.gameFile.write(''.join(str(col) for col in row) + '\r\n')
        self.gameFile.write('%s\r\n' % str(self.currentTurn))

    # Place the current player's piece in the requested column
    def playPiece(self, column):
        if not self.gameBoard[0][column]:
            for i in range(5, -1, -1):
                if not self.gameBoard[i][column]:
                    self.gameBoard[i][column] = self.currentTurn
                    self.pieceCount += 1
                    return 1

    # The AI section modified now as per my logic explained in eval file
    def aiPlay(self, depth):
		if self.pieceCount == 42:
                   return
		selected_state = self.Min_Max_Logic(depth)
		self.gameBoard = deepcopy(selected_state.gameBoard)
		self.children = []
		self.changePlayerTurn()

    # AI section for interactive mode
    def aiplay_interactive(self, interactive_move, depth):
	# print "this is the turn of "+interactive_move
	if interactive_move == 'computer-next':
	   result = self.computer_turn(interactive_move,depth)
	else:
            if interactive_move == 'human-next':
               result = self.human_turn(interactive_move,depth)
	return result

    # computer's turn in interactive mode
    def computer_turn(self, interactive_move, depth):
	self.CountPiece()
	selected_state = self.Min_Max_Logic(depth)
	# copy the gameboard of selected move
	self.gameBoard = deepcopy(selected_state.gameBoard)
	self.children = []
	# self.printGameBoard()
	interactive_move = 'human-next'
	self.changePlayerTurn()
        outfile = 'computer.txt'
        self.WriteToFile_Interactive(outfile)
	return interactive_move

    # Human turn in interactive mode
    def human_turn(self, interactive_move, depth):
	self.CountPiece()
        # print "Human mode"
        outfile = 'human.txt'
        while True:
              human_move = input("Enter the column number you want to play: ")
              # print "Human Move: "+str(human_move)
              human_move = human_move - 1
	      result = self.playPiece(human_move)
              if result:
	         interactive_move = 'computer-next'
	         self.changePlayerTurn()
                 self.WriteToFile_Interactive(outfile)
	         return interactive_move
              else:
                 print "Invalid move..!!"
	
    # Function with MIN-MAX logic
    def Min_Max_Logic(self, depth):
	selected_move = maxConnect4Game()
	# generate states
        self.Base_States()
	utility = -99
	for row in self.children:
	    row.changePlayerTurn()
       	    this_state_utility = row.min_value(depth)
            # maximizing move
            if utility < this_state_utility:
	           utility = this_state_utility
		   self.alpha = max(utility,self.alpha)
	           selected_move = row
	    
        return selected_move
		
    # min-value function implementation
    def min_value(self, depth):
	turn = 'min'
	# first check the terminal state 
	utility = self.terminal_test(turn)
	# if it is a terminal state then return the utility value
	if utility < 99:
           return utility
	else:
	    if int(depth) == self.depth:
               return self.Evaluation_Function()	
            else:
	        utility = 99
	        # generate child states 
	        self.Base_States()
                for row in self.children:
		    row.beta = self.beta
		    row.changePlayerTurn()
	            utility = min(utility, row.max_value(depth))
		    if utility <= self.alpha:
		       return utility
		    self.beta = min(utility, self.beta)
	        return utility
	
    # max-value function implementation
    def max_value(self, depth):
	#first check the terminal state
	turn = 'max'
	utility = self.terminal_test(turn)
	# if it is terminalstate then return the utility value 
	if utility < 99:
	   return utility
	else:	
	    if int(depth) == self.depth:
               return self.Evaluation_Function()
            else:
	        utility = -99
	        # generate child states
	        self.Base_States()
	        for row in self.children:
		    row.alpha = self.alpha
		    row.changePlayerTurn()
                    utility = max(utility, row.min_value(depth))
	            if utility >= self.beta:
	               return utility
        	    self.alpha = max(utility, self.alpha)
	        return utility
	
    # function to check whether a state is terminal state 
    def terminal_test(self, turn):
	self.CountPiece()
	if self.pieceCount == 42:
	   self.countScore()
           if self.player1Score == self.player2Score:
              return 0
           if self.player1Score > self.player2Score and self.player == 1:
              return 1
           else:
	       if self.player1Score > self.player2Score:
		  return -1
	       else:
	           if self.player1Score < self.player2Score and self.player == 2:
	              return 1
		   else:
                       if self.player1Score < self.player2Score:
			  return -1
	      	       else:
	                  return 0
	else:
	    return 99		
		
    #Chnage turn of player from computer to human and vice versa	
    def changePlayerTurn(self):	
	if self.currentTurn == 1:
           self.currentTurn = 2
        elif self.currentTurn == 2:
	     self.currentTurn = 1
	
    #generates the further states
    def Base_States(self):
	for i in range(7):
            state = maxConnect4Game()
	    state.name = str(self.name) + str(i)
	    state.currentTurn = self.currentTurn
            state.depth = self.depth + 1
	    state.player = self.player
	    state.gameBoard = deepcopy(self.gameBoard)
	    state.pieceCount = self.pieceCount
	    result = state.playPiece(i)
	    if result:
	       self.children.append(state)
	
    # calculate the evaluation function
    def Evaluation_Function(self):
	
	if self.player == 1:
	   result =  self.EvalFun_P1()
	else:
	    if self.player == 2:
               result = self.EvalFun_P2()
	return result

    # evaluation function for player 1
    def EvalFun_P1(self):
        # Check horizontally
        four_cnt_1 = 0
        four_cnt_2 = 0
	for row in self.gameBoard:
            
            # Check player 1
            if row[0:4] == [1]*4:
                four_cnt_1 += 1
            if row[1:5] == [1]*4:
                four_cnt_1 += 1
            if row[2:6] == [1]*4:
                four_cnt_1 += 1
            if row[3:7] == [1]*4:
                four_cnt_1 += 1
	   
            # for 3 horizontally
            if row[0:3] == [1]*4:
                four_cnt_1 += 0.60
            if row[1:4] == [1]*4:
                four_cnt_1 += 0.60
            if row[2:5] == [1]*4:
                four_cnt_1 += 0.60
            if row[3:6] == [1]*4:
                four_cnt_1 += 0.60
            if row[4:7] == [1]*4:
                four_cnt_1 += 0.60

            # for 2 horizontally
            if row[0:2] == [1]*4:
                four_cnt_1 += 0.20
            if row[1:3] == [1]*4:
                four_cnt_1 += 0.20
            if row[2:4] == [1]*4:
                four_cnt_1 += 0.20
            if row[3:5] == [1]*4:
                four_cnt_1 += 0.20
            if row[4:6] == [1]*4:
                four_cnt_1 += 0.20
            if row[5:7] == [1]*4:
                four_cnt_1 += 0.20


            # Check player 2
            if row[0:4] == [2]*4:
                four_cnt_2 += -1
            if row[1:5] == [2]*4:
                four_cnt_2 += -1
            if row[2:6] == [2]*4:
                four_cnt_2 += -1
            if row[3:7] == [2]*4:
                four_cnt_2 += -1

            # for 3 horizontally
            if row[0:3] == [2]*4:
                four_cnt_2 += -0.60
            if row[1:4] == [2]*4:
                four_cnt_2 += -0.60
            if row[2:5] == [2]*4:
                four_cnt_2 += -0.60
            if row[3:6] == [2]*4:
                four_cnt_2 += -0.60
            if row[4:7] == [2]*4:
                four_cnt_2 += -0.60

            # for 2 horizontally
            if row[0:2] == [2]*4:
                four_cnt_2 += -0.20
            if row[1:3] == [2]*4:
                four_cnt_2 += -0.20
            if row[2:4] == [2]*4:
                four_cnt_2 += -0.20
            if row[3:5] == [2]*4:
                four_cnt_2 += -0.20
            if row[4:6] == [2]*4:
                four_cnt_2 += -0.20
            if row[5:7] == [2]*4:
                four_cnt_2 += -0.20

            # Check vertically for four
	    # player 1
            for j in range(7):
                # Check player 1
                if (self.gameBoard[0][j] == 1 and self.gameBoard[1][j] == 1 and
                    self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1):
                   four_cnt_1 += 1
                if (self.gameBoard[1][j] == 1 and self.gameBoard[2][j] == 1 and
                    self.gameBoard[3][j] == 1 and self.gameBoard[4][j] == 1):
                   four_cnt_1 += 1
                if (self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1 and
                    self.gameBoard[4][j] == 1 and self.gameBoard[5][j] == 1):
                   four_cnt_1 += 1

                # Check vertically for 3                
                if (self.gameBoard[0][j] == 1 and self.gameBoard[1][j] == 1 and
                    self.gameBoard[2][j] == 1):
                   four_cnt_1 += 0.60
                if (self.gameBoard[1][j] == 1 and self.gameBoard[2][j] == 1 and
                    self.gameBoard[3][j] == 1):
                   four_cnt_1 += 0.60
                if (self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1 and
                    self.gameBoard[4][j] == 1):
                   four_cnt_1 += 0.60
                if (self.gameBoard[3][j] == 1 and self.gameBoard[4][j] == 1 and
                    self.gameBoard[5][j] == 1):
                   four_cnt_1 += 0.60
		
		# Check vertically for 2
                if (self.gameBoard[0][j] == 1 and self.gameBoard[1][j] == 1):
                   four_cnt_1 += 0.20
                if (self.gameBoard[1][j] == 1 and self.gameBoard[2][j] == 1):
                   four_cnt_1 += 0.20
                if (self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1):
                   four_cnt_1 += 0.20
                if (self.gameBoard[3][j] == 1 and self.gameBoard[4][j] == 1):
                   four_cnt_1 += 0.20
                if (self.gameBoard[4][j] == 1 and self.gameBoard[5][j] == 1):
                   four_cnt_1 += 0.20

                # Check player 2
                if (self.gameBoard[0][j] == 2 and self.gameBoard[1][j] == 2 and
                    self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2):
                   four_cnt_2 += -1
                if (self.gameBoard[1][j] == 2 and self.gameBoard[2][j] == 2 and
                    self.gameBoard[3][j] == 2 and self.gameBoard[4][j] == 2):
                   four_cnt_2 += -1
                if (self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2 and
                    self.gameBoard[4][j] == 2 and self.gameBoard[5][j] == 2):
                   four_cnt_2 += -1

                # Check vertically for 3                
                if (self.gameBoard[0][j] == 2 and self.gameBoard[1][j] == 2 and
                    self.gameBoard[2][j] == 2):
                   four_cnt_2 += -0.60
                if (self.gameBoard[1][j] == 2 and self.gameBoard[2][j] == 2 and
                    self.gameBoard[3][j] == 2):
                   four_cnt_2 += -0.60
                if (self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2 and
                    self.gameBoard[4][j] == 2):
                   four_cnt_2 += -0.60
                if (self.gameBoard[3][j] == 2 and self.gameBoard[4][j] == 2 and
                    self.gameBoard[5][j] == 2):
                   four_cnt_2 += -0.60
		
		# Check vertically for 2
                if (self.gameBoard[0][j] == 2 and self.gameBoard[1][j] == 2):
                   four_cnt_2 += -0.20
                if (self.gameBoard[1][j] == 2 and self.gameBoard[2][j] == 2):
                   four_cnt_2 += -0.20
                if (self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2):
                   four_cnt_2 += -0.20
                if (self.gameBoard[3][j] == 2 and self.gameBoard[4][j] == 2):
                   four_cnt_2 += -0.20
                if (self.gameBoard[4][j] == 2 and self.gameBoard[5][j] == 2):
                   four_cnt_2 += -0.20
		
		
        # Check diagonally

        # Check player 1
        if (self.gameBoard[2][0] == 1 and self.gameBoard[3][1] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][3] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[1][0] == 1 and self.gameBoard[2][1] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][3] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[2][1] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][4] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[0][0] == 1 and self.gameBoard[1][1] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[1][1] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][4] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][5] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[0][1] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[1][2] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][5] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][5] == 1 and self.gameBoard[5][6] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[0][2] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][5] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][5] == 1 and self.gameBoard[4][6] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][5] == 1 and self.gameBoard[3][6] == 1):
            four_cnt_1 += 1

        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][1] == 1 and self.gameBoard[3][0] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[0][4] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][1] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][1] == 1 and self.gameBoard[4][0] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[0][5] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[1][4] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][1] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][1] == 1 and self.gameBoard[5][0] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[0][6] == 1 and self.gameBoard[1][5] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[1][5] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][2] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][1] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[1][6] == 1 and self.gameBoard[2][5] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][3] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[2][5] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][2] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[2][6] == 1 and self.gameBoard[3][5] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][3] == 1):
            four_cnt_1 += 1

        # check diagonally for 3 and blank
    
        if (self.gameBoard[5][3] == 1 and self.gameBoard[4][2] == 1 and
               self.gameBoard[3][1] == 1 and self.gameBoard[3][0] == 0):
            four_cnt_1 += 0.50
        if (self.gameBoard[3][4] == 1 and self.gameBoard[4][3] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[2][1] == 0):
            four_cnt_1 += 0.50
        if (self.gameBoard[4][3] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[2][1] == 1 and self.gameBoard[1][0] == 0):
            four_cnt_1 += 0.50
        if (self.gameBoard[5][5] == 1 and self.gameBoard[4][4] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[2][2] == 0):
            four_cnt_1 += 0.50
        if (self.gameBoard[4][4] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[1][1] == 0):
            four_cnt_1 += 0.50
        if (self.gameBoard[3][3] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[1][1] == 1 and self.gameBoard[0][0] == 0):
            four_cnt_1 += 0.50
        if (self.gameBoard[5][6] == 1 and self.gameBoard[4][5] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[2][3] == 0):
            four_cnt_1 += 0.50
        if (self.gameBoard[4][5] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[1][2] == 0):
            four_cnt_1 += 0.50
        if (self.gameBoard[3][4] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[1][2] == 1 and self.gameBoard[0][1] == 0):
            four_cnt_1 += 0.50
        if (self.gameBoard[4][6] == 1 and self.gameBoard[3][5] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[1][3] == 0):
            four_cnt_1 += 0.50
        if (self.gameBoard[3][5] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[1][3] == 1 and self.gameBoard[0][2] == 0):
            four_cnt_1 += 0.50
        if (self.gameBoard[5][3] == 1 and self.gameBoard[4][4] == 1 and
               self.gameBoard[3][5] == 1 and self.gameBoard[2][6] == 0):
            four_cnt_1 += 0.50
        if (self.gameBoard[5][2] == 1 and self.gameBoard[4][3] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[2][5] == 0):
            four_cnt_1 += 0.50
        if (self.gameBoard[4][3] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[2][5] == 1 and self.gameBoard[1][6] == 0):
            four_cnt_1 += 0.50
        if (self.gameBoard[5][1] == 1 and self.gameBoard[4][2] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[2][4] == 0):
            four_cnt_1 += 0.50
        if (self.gameBoard[4][2] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[1][5] == 1):
            four_cnt_1 += 0.50
        if (self.gameBoard[3][3] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[1][5] == 1 and self.gameBoard[0][6] == 0):
            four_cnt_1 += 0.50
        if (self.gameBoard[5][0] == 1 and self.gameBoard[4][1] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[2][3] == 0):
            four_cnt_1 += 0.50
        if (self.gameBoard[4][1] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[1][4] == 0):
            four_cnt_1 += 0.50
        if (self.gameBoard[3][2] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[1][4] == 1 and self.gameBoard[0][5] == 0):
            four_cnt_1 += 0.50
        if (self.gameBoard[4][0] == 1 and self.gameBoard[3][1] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[1][3] == 0):
            four_cnt_1 += 0.50
        if (self.gameBoard[3][1] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[1][3] == 1 and self.gameBoard[0][4] == 0):
            four_cnt_1 += 0.50
        if (self.gameBoard[3][0] == 1 and self.gameBoard[2][1] == 1 and
               self.gameBoard[1][2] == 1 and self.gameBoard[0][3] == 0):
            four_cnt_1 += 0.50
        

        # Check player 2
        if (self.gameBoard[2][0] == 2 and self.gameBoard[3][1] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][3] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[1][0] == 2 and self.gameBoard[2][1] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][3] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[2][1] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][4] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[0][0] == 2 and self.gameBoard[1][1] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[1][1] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][4] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][5] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[0][1] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[1][2] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][5] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][5] == 2 and self.gameBoard[5][6] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[0][2] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][5] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][5] == 2 and self.gameBoard[4][6] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][5] == 2 and self.gameBoard[3][6] == 2):
            four_cnt_2 += -1

        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][1] == 2 and self.gameBoard[3][0] == 2):
            four_cnt_2 +=-1
        if (self.gameBoard[0][4] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][1] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][1] == 2 and self.gameBoard[4][0] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[0][5] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[1][4] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][1] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][1] == 2 and self.gameBoard[5][0] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[0][6] == 2 and self.gameBoard[1][5] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[1][5] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][2] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][1] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[1][6] == 2 and self.gameBoard[2][5] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][3] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[2][5] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][2] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[2][6] == 2 and self.gameBoard[3][5] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][3] == 2):
            four_cnt_2 += -1
         
	# check player 2 diag 3
        if (self.gameBoard[5][3] == 2 and self.gameBoard[4][2] == 2 and
               self.gameBoard[3][1] == 2 and self.gameBoard[3][0] == 0):
            four_cnt_2 += -0.50
        if (self.gameBoard[3][4] == 2 and self.gameBoard[4][3] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[2][1] == 0):
            four_cnt_2 += -0.50
        if (self.gameBoard[4][3] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[2][1] == 2 and self.gameBoard[1][0] == 0):
            four_cnt_2 += -0.50
        if (self.gameBoard[5][5] == 2 and self.gameBoard[4][4] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[2][2] == 0):
            four_cnt_2 += -0.50
        if (self.gameBoard[4][4] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[1][1] == 0):
            four_cnt_2 += -0.50
        if (self.gameBoard[3][3] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[1][1] == 2 and self.gameBoard[0][0] == 0):
            four_cnt_2 +=  -0.50
        if (self.gameBoard[5][6] == 2 and self.gameBoard[4][5] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[2][3] == 0):
            four_cnt_2 += -0.50
        if (self.gameBoard[4][5] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[1][2] == 0):
            four_cnt_2 += -0.50
        if (self.gameBoard[3][4] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[1][2] == 2 and self.gameBoard[0][1] == 0):
            four_cnt_2 += -0.50
        if (self.gameBoard[4][6] == 2 and self.gameBoard[3][5] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[1][3] == 0):
            four_cnt_2 += -0.50
        if (self.gameBoard[3][5] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[1][3] == 2 and self.gameBoard[0][2] == 0):
            four_cnt_2 += -0.50
        if (self.gameBoard[5][3] == 2 and self.gameBoard[4][4] == 2 and
               self.gameBoard[3][5] == 2 and self.gameBoard[2][6] == 0):
            four_cnt_2 += -0.50
        if (self.gameBoard[5][2] == 2 and self.gameBoard[4][3] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[2][5] == 0):
            four_cnt_2 += -0.50
        if (self.gameBoard[4][3] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[2][5] == 2 and self.gameBoard[1][6] == 0):
            four_cnt_2 += -0.50
        if (self.gameBoard[5][1] == 2 and self.gameBoard[4][2] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[2][4] == 0):
            four_cnt_2 += -0.50
        if (self.gameBoard[4][2] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[1][5] == 0):
            four_cnt_2 += -0.50
        if (self.gameBoard[3][3] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[1][5] == 2 and self.gameBoard[0][6] == 0):
            four_cnt_2 += -0.50
        if (self.gameBoard[5][0] == 2 and self.gameBoard[4][1] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[2][3] == 0):
            four_cnt_2 += -0.50
        if (self.gameBoard[4][1] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[1][4] == 0):
            four_cnt_2 += -0.50
        if (self.gameBoard[3][2] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[1][4] == 2 and self.gameBoard[0][5] == 0):
            four_cnt_2 += -0.50
        if (self.gameBoard[4][0] == 2 and self.gameBoard[3][1] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[1][3] == 0):
            four_cnt_2 += -0.50
        if (self.gameBoard[3][1] == 2 and self.gameBoard[2][2] == 2and
               self.gameBoard[1][3] == 2 and self.gameBoard[0][4] == 0):
            four_cnt_2 += -0.50
        if (self.gameBoard[3][0] == 2 and self.gameBoard[2][1] == 2 and
               self.gameBoard[1][2] == 2 and self.gameBoard[0][3] == 0):
            four_cnt_2 += -0.50
        
	sum = four_cnt_2 + four_cnt_1
        return sum

    # evaluation function for player 2
    def EvalFun_P2(self):
        four_cnt_1 = 0
        four_cnt_2 = 0
        # Check horizontally
	for row in self.gameBoard:
            
            # Check player 1
            if row[0:4] == [1]*4:
                four_cnt_1 += -1
            if row[1:5] == [1]*4:
                four_cnt_1 += -1
            if row[2:6] == [1]*4:
                four_cnt_1 += -1
            if row[3:7] == [1]*4:
                four_cnt_1 += -1
	   
            # for 3 horizontally
            if row[0:3] == [1]*4:
                four_cnt_1 += -0.60
            if row[1:4] == [1]*4:
                four_cnt_1 += -0.60
            if row[2:5] == [1]*4:
                four_cnt_1 += -0.60
            if row[3:6] == [1]*4:
                four_cnt_1 += -0.60
            if row[4:7] == [1]*4:
                four_cnt_1 += -0.60

            # for 2 horizontally
            if row[0:2] == [1]*4:
                four_cnt_1 += -0.20
            if row[1:3] == [1]*4:
                four_cnt_1 += -0.20
            if row[2:4] == [1]*4:
                four_cnt_1 += -0.20
            if row[3:5] == [1]*4:
                four_cnt_1 += -0.20
            if row[4:6] == [1]*4:
                four_cnt_1 += -0.20
            if row[5:7] == [1]*4:
                four_cnt_1 += -0.20


            # Check player 2
            if row[0:4] == [2]*4:
                four_cnt_2 += 1
            if row[1:5] == [2]*4:
                four_cnt_2 += 1
            if row[2:6] == [2]*4:
                four_cnt_2 += 1
            if row[3:7] == [2]*4:
                four_cnt_2 += 1

            # for 3 horizontally
            if row[0:3] == [2]*4:
                four_cnt_2 += 0.60
            if row[1:4] == [2]*4:
                four_cnt_2 += 0.60
            if row[2:5] == [2]*4:
                four_cnt_2 += 0.60
            if row[3:6] == [2]*4:
                four_cnt_2 += 0.60
            if row[4:7] == [2]*4:
                four_cnt_2 += 0.60

            # for 2 horizontally
            if row[0:2] == [2]*4:
                four_cnt_2 += 0.20
            if row[1:3] == [2]*4:
                four_cnt_2 += 0.20
            if row[2:4] == [2]*4:
                four_cnt_2 += 0.20
            if row[3:5] == [2]*4:
                four_cnt_2 += 0.20
            if row[4:6] == [2]*4:
                four_cnt_2 += 0.20
            if row[5:7] == [2]*4:
                four_cnt_2 += 0.20

            # Check vertically for four
	    # player 1
            for j in range(7):
                # Check player 1
                if (self.gameBoard[0][j] == 1 and self.gameBoard[1][j] == 1 and
                    self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1):
                   four_cnt_1 += -1
                if (self.gameBoard[1][j] == 1 and self.gameBoard[2][j] == 1 and
                    self.gameBoard[3][j] == 1 and self.gameBoard[4][j] == 1):
                   four_cnt_1 += -1
                if (self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1 and
                    self.gameBoard[4][j] == 1 and self.gameBoard[5][j] == 1):
                   four_cnt_1 += -1

                # Check vertically for 3                
                if (self.gameBoard[0][j] == 1 and self.gameBoard[1][j] == 1 and
                    self.gameBoard[2][j] == 1):
                   four_cnt_1 += -0.60
                if (self.gameBoard[1][j] == 1 and self.gameBoard[2][j] == 1 and
                    self.gameBoard[3][j] == 1):
                   four_cnt_1 += -0.60
                if (self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1 and
                    self.gameBoard[4][j] == 1):
                   four_cnt_1 += -0.60
                if (self.gameBoard[3][j] == 1 and self.gameBoard[4][j] == 1 and
                    self.gameBoard[5][j] == 1):
                   four_cnt_1 += -0.60
		
		# Check vertically for 2
                if (self.gameBoard[0][j] == 1 and self.gameBoard[1][j] == 1):
                   four_cnt_1 += -0.20
                if (self.gameBoard[1][j] == 1 and self.gameBoard[2][j] == 1):
                   four_cnt_1 += -0.20
                if (self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1):
                   four_cnt_1 += -0.20
                if (self.gameBoard[3][j] == 1 and self.gameBoard[4][j] == 1):
                   four_cnt_1 += -0.20
                if (self.gameBoard[4][j] == 1 and self.gameBoard[5][j] == 1):
                   four_cnt_1 += -0.20

                # Check player 2
                if (self.gameBoard[0][j] == 2 and self.gameBoard[1][j] == 2 and
                    self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2):
                   four_cnt_2 += 1
                if (self.gameBoard[1][j] == 2 and self.gameBoard[2][j] == 2 and
                    self.gameBoard[3][j] == 2 and self.gameBoard[4][j] == 2):
                   four_cnt_2 += 1
                if (self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2 and
                    self.gameBoard[4][j] == 2 and self.gameBoard[5][j] == 2):
                   four_cnt_2 += 1

                # Check vertically for 3                
                if (self.gameBoard[0][j] == 2 and self.gameBoard[1][j] == 2 and
                    self.gameBoard[2][j] == 2):
                   four_cnt_2 += 0.60
                if (self.gameBoard[1][j] == 2 and self.gameBoard[2][j] == 2 and
                    self.gameBoard[3][j] == 2):
                   four_cnt_2 += 0.60
                if (self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2 and
                    self.gameBoard[4][j] == 2):
                   four_cnt_2 += 0.60
                if (self.gameBoard[3][j] == 2 and self.gameBoard[4][j] == 2 and
                    self.gameBoard[5][j] == 2):
                   four_cnt_2 += 0.60
		
		# Check vertically for 2
                if (self.gameBoard[0][j] == 2 and self.gameBoard[1][j] == 2):
                   four_cnt_2 += 0.20
                if (self.gameBoard[1][j] == 2 and self.gameBoard[2][j] == 2):
                   four_cnt_2 += 0.20
                if (self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2):
                   four_cnt_2 += 0.20
                if (self.gameBoard[3][j] == 2 and self.gameBoard[4][j] == 2):
                   four_cnt_2 += 0.20
                if (self.gameBoard[4][j] == 2 and self.gameBoard[5][j] == 2):
                   four_cnt_2 += 0.20
		
		
        # Check diagonally

        # Check player 1
        if (self.gameBoard[2][0] == 1 and self.gameBoard[3][1] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][3] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[1][0] == 1 and self.gameBoard[2][1] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][3] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[2][1] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][4] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[0][0] == 1 and self.gameBoard[1][1] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[1][1] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][4] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][5] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[0][1] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[1][2] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][5] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][5] == 1 and self.gameBoard[5][6] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[0][2] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][5] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][5] == 1 and self.gameBoard[4][6] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][5] == 1 and self.gameBoard[3][6] == 1):
            four_cnt_1 += -1

        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][1] == 1 and self.gameBoard[3][0] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[0][4] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][1] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][1] == 1 and self.gameBoard[4][0] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[0][5] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[1][4] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][1] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][1] == 1 and self.gameBoard[5][0] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[0][6] == 1 and self.gameBoard[1][5] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[1][5] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][2] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][1] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[1][6] == 1 and self.gameBoard[2][5] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][3] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[2][5] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][2] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[2][6] == 1 and self.gameBoard[3][5] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][3] == 1):
            four_cnt_1 += -1

	# check player 1 diagonally for 3
        if (self.gameBoard[5][3] == 1 and self.gameBoard[4][2] == 1 and
               self.gameBoard[3][1] == 1 and self.gameBoard[3][0] == 0):
            four_cnt_1 += -0.50
        if (self.gameBoard[3][4] == 1 and self.gameBoard[4][3] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[2][1] == 0):
            four_cnt_1 += -0.50
        if (self.gameBoard[4][3] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[2][1] == 1 and self.gameBoard[1][0] == 0):
            four_cnt_1 += -0.50
        if (self.gameBoard[5][5] == 1 and self.gameBoard[4][4] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[2][2] == 0):
            four_cnt_1 += -0.50
        if (self.gameBoard[4][4] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[1][1] == 0):
            four_cnt_1 += -0.50
        if (self.gameBoard[3][3] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[1][1] == 1 and self.gameBoard[0][0] == 0):
            four_cnt_1 +=  -0.50
        if (self.gameBoard[5][6] == 1 and self.gameBoard[4][5] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[2][3] == 0):
            four_cnt_1 += -0.50
        if (self.gameBoard[4][5] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[1][2] == 0):
            four_cnt_1 += -0.50
        if (self.gameBoard[3][4] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[1][2] == 1 and self.gameBoard[0][1] == 0):
            four_cnt_1 += -0.50
        if (self.gameBoard[4][6] == 1 and self.gameBoard[3][5] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[1][3] == 0):
            four_cnt_1 += -0.50
        if (self.gameBoard[3][5] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[1][3] == 1 and self.gameBoard[0][2] == 0):
            four_cnt_1 += -0.50
        if (self.gameBoard[5][3] == 1 and self.gameBoard[4][4] == 1 and
               self.gameBoard[3][5] == 1 and self.gameBoard[2][6] == 0):
            four_cnt_1 += -0.50
        if (self.gameBoard[5][2] == 1 and self.gameBoard[4][3] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[2][5] == 0):
            four_cnt_1 += -0.50
        if (self.gameBoard[4][3] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[2][5] == 1 and self.gameBoard[1][6] == 0):
            four_cnt_1 += -0.50
        if (self.gameBoard[5][1] == 1 and self.gameBoard[4][2] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[2][4] == 0):
            four_cnt_1 += -0.50
        if (self.gameBoard[4][2] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[1][5] == 1):
            four_cnt_1 += -0.50
        if (self.gameBoard[3][3] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[1][5] == 1 and self.gameBoard[0][6] == 0):
            four_cnt_1 += -0.50
        if (self.gameBoard[5][0] == 1 and self.gameBoard[4][1] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[2][3] == 0):
            four_cnt_1 += -0.50
        if (self.gameBoard[4][1] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[1][4] == 0):
            four_cnt_1 += -0.50
        if (self.gameBoard[3][2] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[1][4] == 1 and self.gameBoard[0][5] == 0):
            four_cnt_1 += -0.50
        if (self.gameBoard[4][0] == 1 and self.gameBoard[3][1] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[1][3] == 0):
            four_cnt_1 += -0.50
        if (self.gameBoard[3][1] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[1][3] == 1 and self.gameBoard[0][4] == 0):
            four_cnt_1 += -0.50
        if (self.gameBoard[3][0] == 1 and self.gameBoard[2][1] == 1 and
               self.gameBoard[1][2] == 1 and self.gameBoard[0][3] == 0):
            four_cnt_1 += -0.50
        


        # Check player 2
        if (self.gameBoard[2][0] == 2 and self.gameBoard[3][1] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][3] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[1][0] == 2 and self.gameBoard[2][1] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][3] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[2][1] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][4] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[0][0] == 2 and self.gameBoard[1][1] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[1][1] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][4] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][5] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[0][1] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[1][2] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][5] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][5] == 2 and self.gameBoard[5][6] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[0][2] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][5] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][5] == 2 and self.gameBoard[4][6] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][5] == 2 and self.gameBoard[3][6] == 2):
            four_cnt_2 += 1

        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][1] == 2 and self.gameBoard[3][0] == 2):
            four_cnt_2 +=1
        if (self.gameBoard[0][4] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][1] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][1] == 2 and self.gameBoard[4][0] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[0][5] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[1][4] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][1] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][1] == 2 and self.gameBoard[5][0] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[0][6] == 2 and self.gameBoard[1][5] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[1][5] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][2] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][1] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[1][6] == 2 and self.gameBoard[2][5] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][3] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[2][5] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][2] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[2][6] == 2 and self.gameBoard[3][5] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][3] == 2):
            four_cnt_2 += 1
      
        # player 2 diagonal for 3
        if (self.gameBoard[5][3] == 2 and self.gameBoard[4][2] == 2 and
               self.gameBoard[3][1] == 2 and self.gameBoard[3][0] == 0):
            four_cnt_2 += 0.50
        if (self.gameBoard[3][4] == 2 and self.gameBoard[4][3] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[2][1] == 0):
            four_cnt_2 += 0.50
        if (self.gameBoard[4][3] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[2][1] == 2 and self.gameBoard[1][0] == 0):
            four_cnt_2 += 0.50
        if (self.gameBoard[5][5] == 2 and self.gameBoard[4][4] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[2][2] == 0):
            four_cnt_2 += 0.50
        if (self.gameBoard[4][4] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[1][1] == 0):
            four_cnt_2 += 0.50
        if (self.gameBoard[3][3] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[1][1] == 2 and self.gameBoard[0][0] == 0):
            four_cnt_2 +=  0.50
        if (self.gameBoard[5][6] == 2 and self.gameBoard[4][5] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[2][3] == 0):
            four_cnt_2 += 0.50
        if (self.gameBoard[4][5] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[1][2] == 0):
            four_cnt_2 += 0.50
        if (self.gameBoard[3][4] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[1][2] == 2 and self.gameBoard[0][1] == 0):
            four_cnt_2 += 0.50
        if (self.gameBoard[4][6] == 2 and self.gameBoard[3][5] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[1][3] == 0):
            four_cnt_2 += 0.50
        if (self.gameBoard[3][5] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[1][3] == 2 and self.gameBoard[0][2] == 0):
            four_cnt_2 += 0.50
        if (self.gameBoard[5][3] == 2 and self.gameBoard[4][4] == 2 and
               self.gameBoard[3][5] == 2 and self.gameBoard[2][6] == 0):
            four_cnt_2 += 0.50
        if (self.gameBoard[5][2] == 2 and self.gameBoard[4][3] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[2][5] == 0):
            four_cnt_2 += 0.50
        if (self.gameBoard[4][3] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[2][5] == 2 and self.gameBoard[1][6] == 0):
            four_cnt_2 += 0.50
        if (self.gameBoard[5][1] == 2 and self.gameBoard[4][2] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[2][4] == 0):
            four_cnt_2 += 0.50
        if (self.gameBoard[4][2] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[1][5] == 0):
            four_cnt_2 += 0.50
        if (self.gameBoard[3][3] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[1][5] == 2 and self.gameBoard[0][6] == 0):
            four_cnt_2 += 0.50
        if (self.gameBoard[5][0] == 2 and self.gameBoard[4][1] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[2][3] == 0):
            four_cnt_2 += 0.50
        if (self.gameBoard[4][1] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[1][4] == 0):
            four_cnt_2 += 0.50
        if (self.gameBoard[3][2] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[1][4] == 2 and self.gameBoard[0][5] == 0):
            four_cnt_2 += 0.50
        if (self.gameBoard[4][0] == 2 and self.gameBoard[3][1] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[1][3] == 0):
            four_cnt_2 += 0.50
        if (self.gameBoard[3][1] == 2 and self.gameBoard[2][2] == 2and
               self.gameBoard[1][3] == 2 and self.gameBoard[0][4] == 0):
            four_cnt_2 += 0.50
        if (self.gameBoard[3][0] == 2 and self.gameBoard[2][1] == 2 and
               self.gameBoard[1][2] == 2 and self.gameBoard[0][3] == 0):
            four_cnt_2 += 0.50
        


        sum = four_cnt_2 + four_cnt_1
        return sum 

    # Calculate the number of 4-in-a-row each player has
    def countScore(self):
        self.player1Score = 0;
        self.player2Score = 0;

        # Check horizontally
        for row in self.gameBoard:
            # Check player 1
            if row[0:4] == [1]*4:
                self.player1Score += 1
            if row[1:5] == [1]*4:
                self.player1Score += 1
            if row[2:6] == [1]*4:
                self.player1Score += 1
            if row[3:7] == [1]*4:
                self.player1Score += 1
            # Check player 2
            if row[0:4] == [2]*4:
                self.player2Score += 1
            if row[1:5] == [2]*4:
                self.player2Score += 1
            if row[2:6] == [2]*4:
                self.player2Score += 1
            if row[3:7] == [2]*4:
                self.player2Score += 1

        # Check vertically
        for j in range(7):
            # Check player 1
            if (self.gameBoard[0][j] == 1 and self.gameBoard[1][j] == 1 and
                   self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1):
                self.player1Score += 1
            if (self.gameBoard[1][j] == 1 and self.gameBoard[2][j] == 1 and
                   self.gameBoard[3][j] == 1 and self.gameBoard[4][j] == 1):
                self.player1Score += 1
            if (self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1 and
                   self.gameBoard[4][j] == 1 and self.gameBoard[5][j] == 1):
                self.player1Score += 1
            # Check player 2
            if (self.gameBoard[0][j] == 2 and self.gameBoard[1][j] == 2 and
                   self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2):
                self.player2Score += 1
            if (self.gameBoard[1][j] == 2 and self.gameBoard[2][j] == 2 and
                   self.gameBoard[3][j] == 2 and self.gameBoard[4][j] == 2):
                self.player2Score += 1
            if (self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2 and
                   self.gameBoard[4][j] == 2 and self.gameBoard[5][j] == 2):
                self.player2Score += 1

        # Check diagonally

        # Check player 1
        if (self.gameBoard[2][0] == 1 and self.gameBoard[3][1] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][0] == 1 and self.gameBoard[2][1] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][1] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][0] == 1 and self.gameBoard[1][1] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][1] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][1] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][2] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][5] == 1 and self.gameBoard[5][6] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][2] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][5] == 1 and self.gameBoard[4][6] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][5] == 1 and self.gameBoard[3][6] == 1):
            self.player1Score += 1

        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][1] == 1 and self.gameBoard[3][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][4] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][1] == 1 and self.gameBoard[4][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][5] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][4] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][1] == 1 and self.gameBoard[5][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][6] == 1 and self.gameBoard[1][5] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][5] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][6] == 1 and self.gameBoard[2][5] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][5] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][6] == 1 and self.gameBoard[3][5] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][3] == 1):
            self.player1Score += 1

        # Check player 2
        if (self.gameBoard[2][0] == 2 and self.gameBoard[3][1] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][0] == 2 and self.gameBoard[2][1] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][1] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][0] == 2 and self.gameBoard[1][1] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][1] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][1] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][2] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][5] == 2 and self.gameBoard[5][6] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][2] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][5] == 2 and self.gameBoard[4][6] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][5] == 2 and self.gameBoard[3][6] == 2):
            self.player2Score += 1

        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][1] == 2 and self.gameBoard[3][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][4] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][1] == 2 and self.gameBoard[4][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][5] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][4] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][1] == 2 and self.gameBoard[5][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][6] == 2 and self.gameBoard[1][5] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][5] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][6] == 2 and self.gameBoard[2][5] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][5] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][6] == 2 and self.gameBoard[3][5] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][3] == 2):
            self.player2Score += 1
