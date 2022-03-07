import sys
import curses
# Add curses
# Add any size board
# Add story mode


class Game:
    def __init__(self,x='x',o='o',isplaying=True, size=3, iscurses=False):
        # Set the main variable
        self.isplaying = isplaying # To debug things
        self.playerturn = 0 # Whose turn is this
        self.x, self.o = self.players = x, o # Set players 

        self.size = size
        self.board = [] # Make a board 1 to 9

        self.boardsize = self.size*2 + 3
        self.set_board(self.size)
        # Curses
        self.realscreen = curses.initscr() # Screen for curses
        curses.start_color()
        self.iscurses = iscurses # Is display gonna be curses 
        self.init_curses()
        # Message box properties
        self.messagebox = -1 # curses.boxorsomething 
        self.messagex, self.messagey = self.messagecoord = o, self.size*2 + 3
        self.messagecount = 0
        # OUTER GAME LOOP
        while self.isplaying: # Create the outer game loop to play again if asked
            self.start_game() # Start the game
            curses.endwin()
            startagain = input('Do you want to start again: (Y/N)') # If game ends ask if player wants to play
            if not startagain or startagain.strip()[0].lower() == 'n':
                break
            self.set_board(self.size) # Reset the board to replay
            self.playerturn = 0 # Reset the player turn to replay
        if self.iscurses: curses.endwin() # End the curses
        print('GoodBye') # ==> Goodbye
    def init_curses(self):
        self.screen = curses.initscr() # Init curses screen
        self.screensize = self.screenwidth, self.screenheight = self.screen.getmaxyx() # Get screen size
        # Set up message box window
        self.messagebox = curses.newwin(self.screenwidth, self.boardsize, 0, self.screenheight - self.boardsize)
        # Set colors
        curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_RED)
        # Color pick
        self.colors = {
                'error':curses.color_pair(1)
                }
    def set_board(self, size=3):
        self.board = [[str(i+(j*size)) for i in range(1,size+1)] for j in range(size)]
    def message(self, message,mtype=None):
        if self.iscurses:
            if not mtype:
                self.screen.addstr(self.messagecount,0,'>'+str(message))
            else:
                if mtype == 'alert':
                    self.screen.addstr(self.messagecount,0,'X>'+str(message), self.colors['error'])
        """Gets a message and prints as a game message"""
        if not mtype:
            print('>'+message)
        else:
            if mtype == 'alert':
                print('XXX> ' + str(message)+'!!!')
            else:
                print(message)
    def start_game(self):
        while True:
            self.print_board() # Print the board
            handled_input = self.handle_input() # Get the input
            self.process_input(*handled_input) # Process the input
            if self.doeswin(): # Check if any of the players win
                self.message(self.doeswin() + ' WON THE GAME')
                break
    def isavaible(self,answer):
        """
            Will get the answer and will check if it is avaible
        """
        isit = False
        for i in self.board:
            for y in i:
                if y == answer:
                    isit = True
        return isit
    def get_input(self, player_rep):
        player_input = -1
        if self.iscurses:
            self.message('It\' turn of'+str(player_rep))
            self.screen.addstr(self.size*2 + 3,0,'INPUT for '+str(player_rep)+': ')
            self.screen.refresh()
            player_input = self.screen.getstr()
            player_input = player_input.decode('utf-8')
        else:
            player_input = input('Choose a box'+player_rep+': ')
        return player_input
    def handle_input(self):
        """
            Will get the input,
            and return answer(str), player_rep(str)
        """
        player = (self.playerturn % 2) + 1 # Get player 
        player_rep = str(self.players[player-1]) # Get player representation
        answer = -1
        self.playerturn += 1 # End turn
        while True:
            answer = self.get_input(player_rep)
            if answer == 'exit': # exit if answer is exit
                sys.exit()
            if self.isavaible(answer):
                break
            else:
                self.message('Please choose a real box')
        return answer, player_rep
    def process_input(self,answer,player):
        """
            Will get answer and player and puts player in board
        """
        print('This is outer proocess input')
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                print(self.board[i][j])
                if self.board[i][j] == answer:
                    print('This is process input')
                    self.board[i][j] = player

    def print_board(self):
        '''
            Gets board as a two dimensional list and returns a string
            thats the board
        '''
        if self.iscurses:
            line = '-'*(self.size*2 +1)+'\n'
            self.screen.clear()
            self.screen.addstr(line)
            for x in self.board:
                oses = map(str,x)
                self.screen.addstr('|'+'|'.join(oses)+'|\n')
                self.screen.addstr(line)
            self.screen.refresh()
        else:
            line = '-'*20 # Line that will separate board
            print(line) # Print top line
            for x in self.board: # print X and O's and a separator
                oses = map(str,x)
                print('|'+'|'.join(oses)+'|')
                print(line)
    def doeswin(self):
        """ ADD:--> Implement for every board """
        coordinats = self.tocheck()
        b = self.board
        for coord in coordinats:
            f, s, t = coord
            if b[f[0]][f[1]] == b[s[0]][s[1]] == b[t[0]][t[1]]:
                return b[f[0]][f[1]]
        return False
    def tocheck(self):
        """
            Will return list of triple coordinats to check
        """
        def cross2(a):
            toret = []
            l = len(a)
            for i in range(l):
                for j in range(l):
                    f, s, t = (i,j),(i+1,j+1),(i+2,j+2)
                    if i+2<l and j+2<l:
                        toret.append((f,s,t))
                        toret.append(((f[0],f[1]+2),s,(t[0],t[1]-2)))
            return toret
        def pos(a):
            hor = []
            ver = []
            for i in range(len(a)):
                l = len(a)
                for j in range(len(a)):
                    f,s,t = j,j+1,j+2
                    if f<l and s<l and t<l:
                        hor.append(((i,f),(i,s),(i,t)))
                        ver.append(((f,i),(s,i),(t,i)))
            return hor+ver
        ret = cross2(self.board)+pos(self.board)
        # print(ret) # DEBUG
        return ret

game = Game(iscurses=True)
'''
a = Game(isplaying=False)
a.print_board()
print(a.board)
a.message('You have been violated the law','alert')
toprint = a.tocheck()
print(*toprint,sep='\n')
game = Game(x='❌',o='⭕',size=5)
'''
