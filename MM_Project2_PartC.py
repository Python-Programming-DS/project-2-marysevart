"""
Tic-Tac-Toe

This program implements a machine learning algorithm (Random Forest Classifier) as player 'O' to play against a human player 'X' in a Tic-Tac-Toe game.

The chosen dataset is "tictac_single.txt" for the intermediate boards optimal play (multi-class classification).    
    
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# define Board class to building the Game Board:

class Board:
     # this constructor initiates the board with empty cells
    def __init__(self):
        self.c = [[" "," "," "],
                  [" "," "," "],
                  [" "," "," "]]
      
    # this method prints the board. Recall that class methods are functions
    def printBoard(self):
        # it first prints the BOARD_HEADER constant
        # BOARD_HEADER constant
        BOARD_HEADER = "-----------------\n|R\\C| 0 | 1 | 2 |\n-----------------"
        print(BOARD_HEADER)

        # using a for-loop, it increments through the rows
        for i in range(3):
            print(f"| {i:3} | {self.c[i][0]:1} | {self.c[i][1]:1} | {self.c[i][2]:1} |")
            print("-----------------")

    
# define Game class to implement the Game Logic:

class Game:

    # the constructor
    def __init__(self):
        self.board = Board()
        self.turn = 'X'

    # this method switches players 
    def switchPlayer(self):
        if self.turn == 'X':
            self.turn = 'O'
        else:
            self.turn = 'X'
    
    # this method validates the user's entry
    def validateEntry(self, row, col):
        if row > 2 or col > 2:
            print("Invalid entry: try again.")
            print("Row & column numbers must be either 0, 1, or 2.")
            output = False
        elif self.board.c[row][col] == ' ':
            output = True
        else:
            print("That cell is already taken.")
            print("Please make another selection.")
            output = False
        return output


    # this method checks if the board is full
    def checkFull(self):
        while True:
            for i in range(len(self.board.c)):
                for k in range(len(self.board.c)):
                    if self.board.c[i][k] == ' ':
                        return False
                    elif i == 2 and k ==2:
                        return True

    
    # this method checks for a winner
    def checkWin(self):
        for i in range(len(self.board.c[0])):       #checking rows and columns for a win
            if self.board.c[i][0] ==  self.board.c[i][1] == self.board.c[i][2] and self.board.c[i][0] != ' ':
                return True
            elif self.board.c[0][i] == self.board.c[1][i] == self.board.c[2][i] and self.board.c[0][i] != ' ':
                return True
        if self.board.c[0][0] == self.board.c[1][1] == self.board.c[2][2] and self.board.c[0][0] != ' ': #checking diagonals for a win
            return True
        elif self.board.c[2][0] == self.board.c[1][1] == self.board.c[0][2] and self.board.c[2][0] != ' ': #checking diagonals for a win
            return True
        else:
            return False

    # returns the player who won (X or O), or None if no winner
    def get_winner(self):
        # rows and columns
        for i in range(3):
            if self.board.c[i][0] == self.board.c[i][1] == self.board.c[i][2] and self.board.c[i][0] != ' ':
                return self.board.c[i][0]
            if self.board.c[0][i] == self.board.c[1][i] == self.board.c[2][i] and self.board.c[0][i] != ' ':
                return self.board.c[0][i]
        # diagonals
        if self.board.c[0][0] == self.board.c[1][1] == self.board.c[2][2] and self.board.c[0][0] != ' ':
            return self.board.c[0][0]
        if self.board.c[2][0] == self.board.c[1][1] == self.board.c[0][2] and self.board.c[2][0] != ' ':
            return self.board.c[2][0]
        return None

    # checks if game is over by calling checkFull() and checkWin()
    # hint: you can call a class method using self.method_name() within another class method, e.g., self.checkFull()
    def checkEnd(self):
        full = self.checkFull()
        win = self.checkWin()

    def read_dataset(self):
        # in dataset, player X (human) is +1 and player O (ML) is -1 and empty squares are 0
        # outputs from dataset indicate the optimal move for the state of tic-tac-toe squares (e.g. 6 is row 3 col 0)
        data = pd.read_csv("tictac_single.txt", sep=' ', header=None)
        y = data[9]
        x = data.drop(columns = [9])
        return x, y
    
    def pred_move(self):
        x, y = self.read_dataset()
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size =0.2, random_state = 42)
        rf = RandomForestClassifier(n_estimators=200, max_depth=1000, criterion='entropy')
        rf.fit(X_train, y_train)
        # make sure model is predicting the current board state rather than just off the training data
        # X = 1; O = -1; empty = 0
        mapping = {'X': 1, 'O': -1, ' ': 0}
        current_state = []
        for i in range(3):
            for j in range(3):
                current_state.append(mapping.get(self.board.c[i][j], 0))
        # predict a single move for the current board state
        y_pred = rf.predict([current_state])
        accuracy = rf.score(X_test, y_test)
        print(f"Model accuracy: {accuracy*100:.2f}%")
        return y_pred

    # this method runs the tic-tac-toe game
     # hint: you can call a class method using self.method_name() within another class method
    def playGame(self):
        self.board.printBoard()
        while True:
            if self.turn == 'X':
                print(f"Player {self.turn}'s turn.")
                coordinates = input("Please enter row number and column number separated by a comma. ")
                clean_coord = coordinates.replace(',', '')      #will split coordinates and clean them and return the row and col entered by the user
                split_coord = [coord for coord in clean_coord]
                int_coord = [int(value) for value in split_coord]
                row = int_coord[0]
                col = int_coord[1]
                print(f"You have entered row #{row}\n\t and column #{col}")
                print("Thank you for your selection.")
                # will validate entry, place X or O, print board, check for win or draw, and switch players
                if self.validateEntry(row, col) == True:
                    self.board.c[row][col] = self.turn
                    self.board.printBoard()
                    if self.checkWin() == True:
                        print(f"Player {self.turn} wins!")
                        break
                    elif self.checkFull() == True:
                        print("DRAW! NOBODY WINS!")
                        break
                    else:
                        self.switchPlayer()
                else:
                    continue
            elif self.turn == 'O':
                print(f"Player {self.turn}'s turn.")
                best_move = self.pred_move()
                move = best_move[0]
                row = move // 3
                col = move % 3
                print(f"Computer chooses row #{row} and column #{col}")
                if self.validateEntry(row, col) == True:
                    self.board.c[row][col] = self.turn
                    self.board.printBoard()
                    if self.checkWin() == True:
                        print(f"Player {self.turn} wins!")
                        break
                    elif self.checkFull() == True:
                        print("DRAW! NOBODY WINS!")
                        break
                    else:
                        self.switchPlayer()
                else:
                    continue



# main function
def main():
    # first initializes a variable to repeat the game
    print("New Game: X goes first.")
    print()
    while True:     # while loop for repeating the game until the user says no
        play = Game()
        play.playGame()
        cont = input("Another game? Enter Y or y for yes. ")
        if cont.lower() == 'y':
            print("New Game: X goes first.")
            print()
            continue
        else:
            break

    # goodbye message 
    print("Thank you for playing!")
    
# call to main() function
if __name__ == "__main__":
    main()
