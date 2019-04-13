#!/usr/bin/env python

# Written by Chris Conly based on C++
# code provided by Dr. Vassilis Athitsos
# Written to be Python 2.4 compatible for omega

# Logic Modified by Avinash Shanker
# AXS8570
# 1001668570
# Note Mix-Max(with Alpla-Beta) and Eval function logic is in MaxConnect4Game.py
# This is a driver program
# Usage:
# For one move mode: python maxconnect4.py one-move green.txt red.txt 5
# For interactive mode: python maxconnect4.py interactive input1.txt computer-next 5

import os.path
import sys
from MaxConnect4Game import *

def oneMoveGame(currentGame, depth):
    if currentGame.pieceCount == 42:    # Is the board full already?
        print 'BOARD FULL\n\nGame Over!\n'
        sys.exit(0)
    currentGame.aiPlay(depth) # Make a move (only random is implemented)

    print 'Game state after move:'
    currentGame.printGameBoard()

    currentGame.countScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

    currentGame.printGameBoardToFile()
    currentGame.gameFile.close()


def interactiveGame(currentGame, interactive_move, depth):
    output = interactive_move
    currentGame.CountPiece()
    while True:
	  currentGame.CountPiece()
	  if currentGame.pieceCount ==  42:
	     sys.exit('Board is Full')  	
	  output = currentGame.aiplay_interactive(output,depth)
          if output == 'Computer-next':
             currentGame.WriteToFile_Interactive('human.txt')
          else:
              if output == 'human.txt':
                 currentGame.WriteToFile_Interactive('computer.txt')
 
	  # Get the present state of the game board
	  print('Game state after move:')
	  currentGame.printGameBoard()
	  currentGame.countScore()
	  print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

def main(argv):
    # Make sure we have enough command-line arguments
    if len(argv) != 5:
        print 'Four command-line arguments are needed:'
        print('Usage: %s interactive [input_file] [computer-next/human-next] [depth]' % argv[0])
        print('or: %s one-move [input_file] [output_file] [depth]' % argv[0])
        sys.exit(2)

    game_mode, inFile = argv[1:3]

    if not game_mode == 'interactive' and not game_mode == 'one-move':
        print('%s is an unrecognized game mode' % game_mode)
        sys.exit(2)
	
    interactive_move = argv[3]
    depth = argv[4]
    currentGame = maxConnect4Game() # Create a game

    # Try to open the input file
    try:
        if os.path.isfile(inFile) and game_mode == 'interactive':
           currentGame.gameFile = open(inFile, 'r')
        else:
            if game_mode == 'one-move':
               currentGame.gameFile = open(inFile, 'r')
    except IOError:
           sys.exit("\nError opening input file.\nCheck file name.\n")
  
    # Read the initial game state from the file and save in a 2D list
    if os.path.isfile(inFile):
       file_lines = currentGame.gameFile.readlines()
       currentGame.gameBoard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]] #store in 2D array
       currentGame.currentTurn = int(file_lines[-1][0]) # last item in array
       currentGame.player = int(file_lines[-1][0])
       currentGame.gameFile.close()
    else:
       if game_mode == 'interactive':
          currentGame.currentTurn = 1
          currentGame.player = 1

    print '\nMaxConnect-4 game\n'
    print 'Game state before move:'
    currentGame.printGameBoard()

    # Update a few game variables based on initial state and print the score
    currentGame.CountPiece()
    currentGame.countScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

    if game_mode == 'interactive':
        interactiveGame(currentGame,interactive_move,depth) # Be sure to pass whatever else you need from the command line
    else: # game_mode == 'one-move'
        # Set up the output file
        outFile = argv[3]
        try:
            currentGame.gameFile = open(outFile, 'w')
        except:
            sys.exit('Error opening output file.')
        oneMoveGame(currentGame, depth) # Be sure to pass any other arguments from the command line you might need.


if __name__ == '__main__':
    main(sys.argv)


