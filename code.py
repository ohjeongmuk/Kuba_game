# Author: Jeongmuk Oh
# Date: 30. May 2021
# Description: Create code to create objects for your Cuban game. Two players take turns playing and can move their marbles strictly according to the rules.
#              This is still unfinished code. Descriptions of each code and declarations of variables appear as comments under methods and classes.
#              The scenario file is submitted as an additional PDF.



class KubaGame:
    """
    Create Cuban games. Cuban games are strictly governed by the Cuban game rules.
    ...



    methods - Responsibilities
    --------------------------

    __init__: Contains board and player information. Each piece of information is updated by the method.
    get_current_turn: This method tells whose turn it is. This method helps to continue the game by giving and receiving one turn at a time.
    make_move: This is the make_move method that performs the overall action and communicates with all methods. The code to which the rules of the game are applied through this method is included.
                It also updates the movement of the board, letting you know how the game is progressing.
    get_winner: It tells who the winner is and serves as a reminder of the end of the game.
    get_captured: It tells you the number of red marbles that can determine the victory or defeat of the game. This could be code that could cause the game to quit.
    get_marble: Identifies the color of marbles placed at specific coordinates. This code serves to limit the movement of the player.
    get_marble_count: It serves to coordinate the game by indicating the current situation of the board. (W, B, R)
    """

    def __init__(self, player1, player2):
        """
        Set board and 2 players. Two players are accepted as a tuple, containing the player name and the color of the marble.
        It also creates a current_turn that tells you whose turn it is.
        ...

        board
        ...
        The board is set to 9x9.
        The end of the board is a border, and if a marble touches the border, the marble is removed from the board and counted.

        :param player1: tuple (player name1, color of mable)
        :param player2: tuple (player name2, color of mable)
        """
        self.board = [[' ' for col in range(9)] for row in range(9)]
        self.board_alignment()
        self.player_A = player1
        self.player_B = player2
        self.current_turn = None
        self.board_order = []
        self.winner = None
        self.temp_move_W = None
        self.temp_move_B = None
        self.captured_red_W = 0
        self.captured_red_B = 0
        self.captured_W = 0
        self.captured_B = 0
        #self.get_board_view()

    def board_alignment(self):
        # Create the board:
        for row in range(0, 9):
            for col in range(0, 9):
                if ((1 <= row <= 2) and (1 <= col <= 2)) or ((6 <= row <= 7) and (6 <= col <= 7)):
                    self.board[row][col] = 'W'
                if (6 <= row <= 7) and (1 <= col <= 2):
                    self.board[row][col] = 'B'
                    self.board[col][row] = 'B'
                if ((3 <= row <= 5) and (3 <= col <= 5)) or (row == 2 and col == 4) or (row == 4 and col == 6):
                    self.board[row][col] = "R"
                    self.board[col][row] = 'R'

    def get_board_view(self):
        """
        View the current Board
        ...

        :return: list (current_board view)
        """
        for col in self.board:
            print(col)
    
    def get_current_turn(self):
        """
        It tells which player's turn is the current turn. Returns None if the game has not been started.
        ...

        :return: player_name (Updated current_turn) or None
        """
        return self.current_turn

    def set_current_turn(self, player_name):
        """
        It will do update the current_player

        :param player_name: str (will be current_turn)
        """
        self.current_turn = player_name
        
    def get_player_from_color(self, color):
        """
        Gets the marble color chosen by the player by the player name.
        ...

        :param color: str ('B' or 'W')
        :return: str (player name)
        """
        if color == self.player_A[1]:
            return self.player_A[0]
        elif color == self.player_B[1]:
            return self.player_B[0]
        return None
    
    def get_opponent_from_current_player(self, player_name):
        """
        Gets the opponent using the current player's turn as a parameter.
        ...

        :param player_name: str
        :return: str (opponent's marble color)
        """
        if player_name == self.player_A[0]:
            return self.player_B[0]
        elif player_name == self.player_B[0]:
            return self.player_A[0]

    def get_opponent_color_from_current_player(self):
        """
        Get the color of the opponent using the current player's turn as a parameter
        ...

        :return: str (the opponent's marble color => 'B' or 'W')
        """
        if self.current_turn == self.player_A[0]:
            return self.player_B[1]
        elif self.current_turn == self.player_B[0]:
            return self.player_A[1]

    def get_current_color_from_current_turn(self):
        """
        Get the current  player's marble color as the current turn
        ...

        :return: str or None (if the game hasn't started, the value of return will be 'None')
        """
        if self.current_turn == self.player_A[0]:
            return self.player_A[1]
        elif self.current_turn == self.player_B[0]:
            return self.player_B[1]
        else:
            return None

    def make_move(self, player_name, coordinates, direction):
        """
        Create the code that moves the player's marbles. The player decides the coordinates and direction in which his marble will move.
        It also updates the status of the board taking into account the effect the moved marble had on the board.
        Returns True if the move is successful, otherwise False.
        ...

        Variable
        --------
        y : It represents the y-axis of Euclidean coordinates.
        x : It represents the x-axis of Euclidean coordinates.
        ...
        (Since the coordinate value received as a parameter represents (y,x) in the Euclidean coordinate value, the coordinates were artificially manipulated.)

        :param player_name: str
        :param coordinates: tuple (y, x)
        :param direction: str ('Forward', 'Backward', 'Right', 'Left')
        :return: True or False
        """
        # Convert to Euclidean coordinates
        y = coordinates[0] + 1
        x = coordinates[1] + 1

        # If the player moves the marble for the first time
        if self.board_order == []:
            # Update current turn
            self.set_current_turn(player_name)
            # It remembers the contents of the first board.
            self.board_order.append([item[:] for item in self.board])

        # Is it right a player's order & The marble color is right for the player? & Has the winner been decided yet? (OK)
        if self.get_current_turn() == player_name and self.get_current_color_from_current_turn() == self.board[y][x] and self.winner == None:

            # if you want to go forward?
            if direction == "F" and self.board[y+1][x] == ' ' and y >= 1:
                # Count the number of marbles in front of the selected marble.
                i = 0
                # Repeat until there is nothing in front of the selected marble.
                while self.board[y-i][x] != ' ':
                    i += 1
                # Draw the order one by one.
                for num in range(i, 0, -1):
                    self.board[y-num][x] = self.board[y-num+1][x]
                    self.board[y-num+1][x] = ' '
                    # The Marble Passed to the Boarder, Plus captured_marble to W,B,R Marbles
                    if y-num == 0:
                        if self.get_current_color_from_current_turn() == 'W' and self.board[y - num][x] == 'R':
                            self.captured_red_W += 1
                        elif self.get_current_color_from_current_turn() == 'B' and self.board[y - num][x] == 'R':
                            self.captured_red_B += 1
                        elif self.board[y-num][x] == 'B':
                            self.captured_B += 1
                        elif self.board[y-num][x] == 'W':
                            self.captured_W += 1
                        # Makes the marble's spot in the selected spot blank.
                        self.board[y-num][x] = ' '

            # if you want to go backward? As with 'Forward', comments are omitted.
            elif direction == "B" and self.board[y-1][x] == ' ' and y <= 7:
                i = 0
                while self.board[y+i][x] != ' ':
                    i += 1
                for num in range(i, 0, -1):
                    self.board[y+num][x] = self.board[y+num-1][x]
                    self.board[y+num-1][x] = ' '
                    if y+num == 8:
                        if self.get_current_color_from_current_turn() == 'W' and self.board[y + num][x] == 'R':
                            self.captured_red_W += 1
                        elif self.get_current_color_from_current_turn() == 'B' and self.board[y + num][x] == 'R':
                            self.captured_red_B += 1
                        elif self.board[y + num][x] == 'B':
                            self.captured_B += 1
                        elif self.board[y + num][x] == 'W':
                            self.captured_W += 1
                        self.board[y+num][x] = ' '

            # if you want to go Left? As with 'Forward', comments are omitted.
            elif direction == "L" and self.board[y][x+1] == ' ' and x >= 1:
                i = 0
                while self.board[y][x-i] != ' ':
                    i += 1
                for num in range(i, 0, -1):
                    self.board[y][x-num] = self.board[y][x-num+1]
                    self.board[y][x-num+1] = ' '
                    if x - num == 0:
                        if self.get_current_color_from_current_turn() == 'W' and self.board[y][x - num] == 'R':
                            self.captured_red_W += 1
                        elif self.get_current_color_from_current_turn() == 'B' and self.board[y][x - num] == 'R':
                            self.captured_red_B += 1
                        elif self.board[y][x - num] == 'B':
                            self.captured_B += 1
                        elif self.board[y][x - num] == 'W':
                            self.captured_W += 1
                        self.board[y][x-num] = ' '

            # if you want to go Right? As with 'Forward', comments are omitted.
            elif direction == "R" and self.board[y][x-1] == ' ' and x <= 7:
                i = 0
                while self.board[y][x+i] != ' ':
                    i += 1
                for num in range(i, 0, -1):
                    self.board[y][x+num] = self.board[y][x+num-1]
                    self.board[y][x+num-1] = ' '
                    if x+num == 8:
                        if self.get_current_color_from_current_turn() == 'W' and self.board[y][x + num] == 'R':
                            self.captured_red_W += 1
                        elif self.get_current_color_from_current_turn() == 'B' and self.board[y][x + num] == 'R':
                            self.captured_red_B += 1
                        elif self.board[y][x + num] == 'B':
                            self.captured_B += 1
                        elif self.board[y][x + num] == 'W':
                            self.captured_W += 1
                        self.board[y][x+num] = ' '

            # You Can Not Move Your Marble at the Direction
            else:
                return False

            # Previous board status equal with current?
            if len(self.board_order) >= 3 and self.board_order[len(self.board_order)-2] == self.board:
                # It immediately returns to the previous state of the board.
                self.board = [item[:] for item in self.board_order[len(self.board_order)-1]]
                return False

            # Make a Decision who is a winner : When you have captured all of the opponent's marbles or 7 red marbles
            if self.captured_red_W == 7 or self.captured_W == 8:
                self.winner = self.get_player_from_color('W')
            elif self.captured_red_B == 7 or self.captured_B == 8:
                self.winner = self.get_player_from_color('B')

            # if there is no a marble that can't move anywhere. Decide winner to 'W'
            count = 0
            for i in range(0, 9):
                for j in range(0, 9):
                    # The opposing marbles are surrounded by 4 directions.
                    if self.board[i][j] == self.get_opponent_color_from_current_player() and self.board[i-1][j] != ' ' and self.board[i+1][j] != ' ' and self.board[i][j-1] != ' ' and self.board[i][j+1] != ' ':
                        count += 1

            # Update the winner. The game is over.
            if self.get_current_color_from_current_turn() == 'W' and count == (8-self.captured_W):
                self.winner = self.get_player_from_color('W')
            elif self.get_current_color_from_current_turn() == 'B' and count == (8-self.captured_B):
                self.winner = self.get_player_from_color('B')
                
            # Pass your turn to your opponent.
            self.set_current_turn(self.get_opponent_from_current_player(player_name))
            # Now remembers the current state of the board.
            self.board_order.append([item[:] for item in self.board])
            
            # View the updated board
            #self.get_board_view()
            return True

        # It's not your turn and the marble you choose isn't your marble, it's a repeated move or a winner has already been decided.
        else:
            return False

    def get_winner(self):
        """
        Returns the name of the person who won the game. If there is no winner, it returns None.
        ...

        :return: player_name
        """
        return self.winner

    def get_captured(self, player_name):
        """
        This code tells how many red marbles a specific player has captured.
        It takes the player's name as a parameter.
        ...

        :return: int (the number of captured red marbles)
        """
        if player_name == self.player_A[0] and self.player_A[1] == 'W':
            return self.captured_red_W
        elif player_name == self.player_A[0] and self.player_A[1] == 'B':
            return self.captured_red_B
        elif player_name == self.player_B[0] and self.player_B[1] == 'W':
            return self.captured_red_W
        elif player_name == self.player_B[0] and self.player_B[1] == 'B':
            return self.captured_red_B

        # When a player has not yet been determined
        return None

    def get_marble(self, coordinates):
        """
        Get the cell's coordinates as a tuple and see what color marbles are at those coordinates. If the marble does not exist, it returns a specific character.
        ...

        :param coordinates: tuple
        :return: R, B, W or X (Color of marbles at specific coordinates)
        """
        x = coordinates[1] + 1
        y = coordinates[0] + 1

        if self.board[y][x] == 'R' or self.board[y][x] == 'B' or self.board[y][x] == 'W':
            return self.board[y][x]
        elif self.board[y][x] == ' ':
            return 'X'

    def get_marble_count(self):
        """
        Returns the number of marbles remaining in the current game. The order is white, then black, then red.
        ...

        :return: tuple (W,B,R)
        """
        return (8 - self.captured_W, 8 - self.captured_B, 13 - self.captured_red_W - self.captured_red_B)
