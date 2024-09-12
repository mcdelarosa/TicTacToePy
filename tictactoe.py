import re

class Player:
    def __init__(self, name, symbol, value):
        self.name = name
        self.wins = 0
        self.symbol = symbol #input(f'{name} put your symbol (only one): ')
        self.value = value


class Game:
    def __init__(self):
        
        self.winner = None
        self.x_map = {'A':0, 'B':1, 'C':2}
        self.y_map = {'1':0, '2':1, '3':2}
        self.names =[]
        self.wins_list =[]
        self.default = True
        self.start()


    def reset(self):
        self.table = [0, 0, 0],[0, 0, 0], [0, 0, 0]     # y and x are inverted!
        self.rounds = len(self.table)**2
        self.drawer()
    def ask_name_symbol(self):
        value = input('Do you want the default settings [y/n]? ')
        if value.upper() == 'N':
            self.default = False

    def set_name_symbol(self):
        if self.default == True:
            name1 = 'P1'
            symbol1 ='X'
            name2 = 'P2'
            symbol2 ='O'
        else:
            name1 = input('Name of Player 1: ')
            symbol1 = input('P1 put your symbol (only one): ')

            name2 = input('Name of Player 2: ')
            symbol2 = input('P2 put your symbol (only one): ')
        self.read_and_write_names_file('names.txt')
        self.p1 = Player(name1, symbol1, 1)
        self.p2 = Player(name2, symbol2, 4) # the value is 4 because then there is no problem by checking who the winner is



    def ask(self, value, player):
        if self.winner is None:

            coordinates =  None
            pattern = "^\w{1}\d+|^\d+\w{1}"     # from re library. This filters the input.
            while ((coordinates is None or len(coordinates) == 0) or
                  (coordinates is not None and not re.match(pattern, coordinates))):

                coordinates = input(f'{value} :: Enter your coordinates [1-Letter+Number] {player}:').upper()
            coor_x, coor_y = self.validate(coordinates)
            if coor_x is not None and coor_y is not None:
                if not self.table[coor_y][coor_x] == 0:
                    print('this coordinates have been already picked...')
                    self.ask(value, player)
                else:
                    self.assign(coor_x, coor_y, value)
                    self.drawer()
                    self.check_win()


    def validate(self, coordinates):
        x, y = None, None
        try:
            for c in coordinates:
                c = str(c)
                if c in self.x_map:
                    x = self.x_map[c]

                elif c in self.y_map:
                    y = self.y_map[c]
        except:
            print('out of range...')
            return [ None, None ]

        return [ x, y ]

    def assign(self,x,y,value):
        self.table[y][x] = value

            
    def start(self):
        self.winner = None
        self.ask_name_symbol()
        self.set_name_symbol()
        self.reset()

        while self.winner is None:
            self.ask(self.p1.value, self.p1.name)
            self.ask(self.p2.value, self.p2.name)
        print(f'The winner is {self.winner}!')

    # read and write names.txt file to find and put new players and their winrates
    def read_and_write_names_file(self, file_name, wins = None, player = None):
        if self.default == False:
            try:
                with open(file_name, 'r+') as file:
                    for line in file:
                        values = line.strip().split(':')
                        self.names.append(values[0].upper())
                        self.wins_list.append(values[1])
                        self.write_names_file(wins,player, file)    #only when the game is over
                    file.close()
                print(self.names)
                print(self.wins_list)
            except FileNotFoundError:
                print(f"The file '{file_name}' was not found.")

    def write_names_file(self, wins, player, file_name):
        if wins != None and player != None:
            try:
                i = self.names.index(player)
                self.wins_list[i] = wins + self.wins_list[i]
            except ValueError:  # More specific exception
                self.names.append(player)
                self.wins_list.append(wins)

            # Move to the start of the file and clear it
            file_name.seek(0)
            file_name.truncate()

            # Write each name and their respective wins on a new line
            for i in range(len(self.names)):
                file_name.write(f"{self.names[i]}:{self.wins_list[i]}\n")


    #functions to check for the winner
    def check_win(self):
        p1_win = 1 * len(self.table)    #value the players need to reach to win
        p2_win = 4 * len(self.table)    #value the players need to reach to win
        if self.calculate_row() == p1_win or self.calculate_column() == p1_win or self.calculate_to_l() == p1_win or self.calculate_to_r() == p1_win:
            self.winner = 'P1'
            self.read_and_write_names_file('names.txt', self.p1.wins+1, self.p1.name)
            self.read_and_write_names_file('names.txt', self.p2.wins, self.p2.name)
        elif self.calculate_row() == p2_win or self.calculate_column() == p2_win or self.calculate_to_l() == p2_win or self.calculate_to_r() == p2_win:
            self.winner = 'P2'
            self.read_and_write_names_file('names.txt', self.p1.wins, self.p1.name)
            self.read_and_write_names_file('names.txt', self.p2.wins+1, self.p2.name)

    def calculate_column(self):
        for x in range(len(self.table[0])):
            result = 0
            for y in range(len(self.table)):
                result = result + self.table[y][x]
            if result == 3 or result == 12:
                return result

    def calculate_row(self):
        for y in range(len(self.table)):
            result = 0
            for x in range(len(self.table[0])):
                result = result + self.table[y][x]
            if result == 3 or result == 12:
                return result

    # calculate in diagonal:
    #Starting from right and going to the left
    def calculate_to_l(self):
        result = 0
        for i in range(len(self.table)):
            result = result + self.table[i][i]
        return result
    #Starting from left and going to the right
    def calculate_to_r(self):
        result = 0
        for i in range(len(self.table)):
            result = result + self.table[i][2-i]
        return result
    
    def drawer(self):
        print(' A|B|C')
        for y in range(len(self.table)):
            print(f"{(y + 1)}|", end='')
            for x in range(len(self.table[0])):
                if self.table[y][x] == 1:
                    print(self.p1.symbol, end='|')
                elif self.table[y][x] == 4:
                    print(self.p2.symbol,end='|')
                else:
                    print(' ', end='|')
            print('')
tictactoe = Game()
