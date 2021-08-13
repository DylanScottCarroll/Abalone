import pygame

class Board(object):
    """Holds all of the data about the board and preforms all actions relating to the board"""

    def __init__(self, size, radius, colors):
        
        self.colors = colors
        
        self.size = size
        self.radius = radius

        self.spacing_x = size[0] / 10
        self.spacing_y = (size[1]* 0.866025403784) / 10 #hardcoded sqrt(3)/2 aka sin(pi/3)
        self.offset_y = size[1] *  ((1-0.866025403784)/2)

        #Initialize board
        self.spaces = {}
        for y in range(1, 10):
            start = y-4 if y-4 > 1 else 1
            end = y+4 if y+4 < 9 else 9
            for x in range(start, end+1):
                if y<=2 or (y,x) in [(3,3), (3,4), (3,5)]: #Player 1
                    self.spaces[y,x] = 0
                elif y>=8 or (y,x) in [(7,5), (7,6), (7,7)]: #Player 2
                    self.spaces[y,x] = 1
                else: #Empty
                    self.spaces[y,x] = 2

        self.remaining = [14, 14]   
        self.game_over = False
        self.winner = None 
        
    def draw_board(self, surface):
        """Draw the current board state to the given pygame surface"""
        surface.fill(self.colors[3])

        for y in range(1, 10):
            start = y-4 if y-4 > 1 else 1
            end = y+4 if y+4 < 9 else 9

            for x in range(start, end+1):
                self._draw_space((y, x), surface)

    def _draw_space(self, coord, surface):
        """only called by draw_board,
        draws a single space to the given pygame surface"""

        y, x = coord

        offset_x = (5-y) * (self.spacing_x/2)

        draw_y = int(self.size[1] - (self.spacing_y * y)) - self.offset_y #hardcoded sqrt(3)/2 aka sin(pi/3)
        draw_x = int(self.spacing_x * x) + offset_x

        color = self.colors[self.spaces[coord]]

        pygame.draw.circle(surface, color, (draw_x, draw_y), self.radius)
        
    def make_move(self, move, color):
        """Preforms the given move if it is valid and legal.
            Expects move to be a tuple containing two or three coordinates.
            Color is the color of the player that made the move

            Returns true if successful, otherwise returns false"""

        for coord in move:
            if not coord_in_board_or_edge(coord):
                return False

        if len(move) == 2:
            start, dest = move
            vector = _sub_tuples(dest, start)


            if vector != _normalize_tuple(vector) or vector==(0,0): return False
            if (vector[0]!=0 and vector[1]!=0) and (vector[0]!=vector[1]): return False
            if self.spaces[start] != color: return False

            
            is_self = True
            self_count = 0
            other_count = 0
            current = start
            chain = [2]

            #Put the marbles in chain until an empty space or the edge is reached
            while coord_in_board(current) and self.spaces[current]!=2:
                current_marble = self.spaces[current]
                
                if current_marble == color:
                    self_count+=1
                    
                    if not is_self: 
                        #This would mean that there is a player's marble on the other side of the opponents marbles
                        return False
                else:
                    other_count+=1
                    is_self=False #Marks that we're now counting opponent marbles
                
                chain.append(current_marble)
                current = _sum_tuples(current, vector)

            #Check that the player has the force to push the other marbles and doesn't try to push too many
            if self_count-other_count < 1 or self_count>3: return False


            #Lay down the chain
            current = start
            for marble in chain:
                
                if not coord_in_board(current):
                    self._marble_removed(marble)

                self.spaces[current] = marble

                current = _sum_tuples(current, vector)


        elif len(move) == 3:
            start, end, dest = move
            chain_vector = _normalize_tuple(_sub_tuples(end, start))
            vector = _sub_tuples(dest, start)
            end = _sum_tuples(end, chain_vector)

            #Check for nonsense moves
            if vector==(0,0) or chain_vector==(0, 0): return False
            if _normalize_tuple(vector) == chain_vector or _normalize_tuple(vector) != vector: return False
            if (vector[0]!=0 and vector[1]!=0) and (vector[0]!=vector[1]): return False

            current = start
            chain = []
            #Put the marbles in the selected row into the chain
            while current!=end and coord_in_board(current):
                current_marble = self.spaces[current]
                current_dest = _sum_tuples(current, vector)
                

                #Check that the marble being picked up is of the right color
                if current_marble != color:
                    return False

                #Check that the destination for each given marble is valid
                if not coord_in_board(current_dest) or self.spaces[current_dest]!=2:
                    return False


                chain.append(current_marble)
                current = _sum_tuples(current, chain_vector)

            if len(chain)>3: return False

            #Place down the chain
            current = start
            for marble in chain:
                
                self.spaces[current] = 2
                self.spaces[_sum_tuples(current, vector)] = marble

                if not coord_in_board(_sum_tuples(current, vector)):
                    self._marble_removed(marble)

                current = _sum_tuples(current, chain_vector)

        else:
            return False

        self._check_winner()

        return True
    
    def get_game_state(self):
        """Returns a copy of the game state stored in a dictionary"""

        game_state = {}

        for key in self.spaces.keys():
            game_state[key] = self.spaces[key]

        return game_state

    def _marble_removed(self, marble):
        """Marks that the given marble color has lost a marble
            Expects marble to be a marble color"""
        
        self.remaining[marble] -= 1

    def _check_winner(self):

        if self.remaining[0]<=8:
            self.game_over = True
            self.winner = 1
        elif self.remaining[1]<=8:
            self.game_over = True
            self.winner = 0

def coord_in_board(coord):
        """Returns true or false whether or not the given tuple is a valid board coordanite"""
        
        if type(coord)==tuple and len(coord)==2:
            y, x = coord

            if type(y)!=int or type(x)!=int: return False

            return (1<=x<=9) and (1<=y<=9) and (y-4 <= x <= y+4)

        else: return False

def coord_in_board_or_edge(coord):
    """Returns true or false whether or not the given tuple is a valid board coordanite
    or if it is only one step away from a valid board coordinate"""
            
    if type(coord)==tuple and len(coord)==2:
        y, x = coord

        if type(y)!=int or type(x)!=int: return False

        return (0<=x<=10) and (0<=y<=10) and (y-5 <= x <= y+5)

    else: return False


    
def _sum_tuples(a, b):
        """Sums all the entries in the given tuples"""
        return tuple(map(lambda x, y: x+y, a, b))

def _sub_tuples(a, b):
    """Subtracts the entries in the given tuples"""
    return tuple(map(lambda x, y: x-y, a, b))

def _normalize_tuple(a):
    """Scales the each value in the tuple independently to either 1, -1, or 0"""
    return tuple(map(lambda x: 0 if x==0 else x//abs(x), a))

class Player(object):
    """A class that player types can inherit from"""

    def get_move(self, game_state, screen, events, viewscreen_size, space_radius):
        """Ask the player class to give the move it would play on the given game_state
            
            game_state is a dictionary {(x, y), space}, where space is an integer representing the color, (0:player1, 1:player2, 2:empty)
            screen is the pygame display surface
            events are the pygame events that happened in the last frame
            viewscreen_size is the size of the pygame surface that the board is being drawn to
            space_radius is the radius of the spaces
            
            Either:
                Returns a tuple in the valid move format.
                Returns None if another render frame is needed to make a decision. Mostly for human players"""
        
        raise NotImplementedError("Please implement the get_move method.")
        return None

    def game_over(self, game_state, winner, moves):
        """Preform any game-over tasks. 
        Not required. Use this to do logging, tallying, or maching learning or whatever.
        
        game_state is a dictionary {(x, y), space}, where space is an integer representing the color, (0:player1, 1:player2, 2:empty)
        winner is the color of the winner (0:player1, 1:player2)"""


        pass

    def reset(self, color):
        """Don't overwrite this please.
        This is just for the game object to reset the player fields it needs to read.
        Calls setup()"""
        
        self.color = color
        self.setup()


    def setup(self):
        """Reset the state of the player back to default
            This method called before anything else, so use it to preform initialization"""
        
        raise NotImplementedError("Please implement the setup method.")
              
class Human_Player(Player):
    def setup(self):
        self.selected = []
    
    def get_move(self, game_state, screen, events, viewscreen_size, space_radius):
        
        #Detect player input
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #Modify the selected list based on where the key press was
                    coord = self._find_nearest_space(event.pos[0], event.pos[1], viewscreen_size, space_radius)
                    if coord is None:
                        self.selected = []
                    elif coord in self.selected:
                        self.selected.remove(coord)
                    else:
                        self.selected.append(coord)
                        if len(self.selected) > 3:
                            del self.selected[0]

            elif event.type == pygame.KEYDOWN:
                #If enter is pressed, return the selected as a tuple to make the move.
                if event.key == pygame.K_RETURN:
                    move = tuple(self.selected)
                    self.selected = []
                    return move
        
        #Draw the current state of the selection onto the board

        spacing_x = viewscreen_size[0] / 10
        spacing_y = (viewscreen_size[1]* 0.866025403784) / 10 #hardcoded sqrt(3)/2 aka sin(pi/3)
        offset_y = viewscreen_size[1] *  ((1-0.866025403784)/2)

        for i, selection in enumerate(self.selected):
            if selection is not None:
                y, x = selection
                offset_x = (5-y) * (spacing_x/2)
                draw_y = int(viewscreen_size[1] - (spacing_y * y)) - offset_y #hardcoded sqrt(3)/2 aka sin(pi/3)
                draw_x = int(spacing_x * x) + offset_x

                color = (0, 0, 255) if i==len(self.selected)-1>0 else (255, 0, 0)

                pygame.draw.circle(screen, color, (draw_x, draw_y), space_radius, int(space_radius*0.2))


        #No move was made. Wait until next frame
        return None

    def _find_nearest_space(self, m_x, m_y, viewscreen_size, space_radius):
        """Finds the nearest space to the given mouse coordinates"""
        #I know this isn't optimized, but it runs so infrequently that it would be a waste of time to optimize it at all.

        spacing_x = viewscreen_size[0] / 10
        spacing_y = (viewscreen_size[1]* 0.866025403784) / 10 #hardcoded sqrt(3)/2 aka sin(pi/3)
        offset_y = viewscreen_size[1] *  ((1-0.866025403784)/2)
        
        space = None
        for y in range(1, 10):
            for x in range(1, 10):
                
                if coord_in_board_or_edge((x, y)):
                
                    offset_x = (5-y) * (spacing_x/2)
                    draw_y = int(viewscreen_size[1] - (spacing_y * y)) - offset_y
                    draw_x = int(spacing_x * x) + offset_x

                    if (((draw_x - m_x)**2 + (draw_y - m_y)**2)**0.5) <= space_radius:
                        return (y, x)

        return None
  
class Game(object):
    """Controls the entire game.
        Acts as a mediator between the board, the graphics, and the players"""
    def __init__(self, player1, player2, viewscreen_size=(500, 500), space_radius=15, board_colors=[(0, 0, 0), (255, 255, 255), (100, 100, 100), (128, 128, 128)] ):
        self._players = [player1, player2]
        self._turn = 0

        self._viewscreen_size = viewscreen_size
        self._space_radius = space_radius
        self._board_colors = board_colors

        self._board = Board(viewscreen_size, space_radius, board_colors)

        self._moves = 0

        pygame.init()
        self._screen = pygame.display.set_mode(viewscreen_size)

    def play(self):
        """Play an entire game of abalone until game over"""


        self._players[0].reset(0)
        self._players[1].reset(1)
        
        
        while True:
                
            events = pygame.event.get()
            for event in events:
                if event.type==pygame.QUIT: pygame.display.quit()

            self._board.draw_board(self._screen)

            pygame.draw.circle(self._screen, self._board_colors[self._turn] ,(int(self._space_radius*1.5), int(self._space_radius*1.5)), self._space_radius)

            game_state = self._board.get_game_state()
            move = self._players[self._turn].get_move(game_state, self._screen, events, self._viewscreen_size, self._space_radius)
            pygame.display.flip()

            if (move is not None) and ( self._board.make_move(move, self._players[self._turn].color) ):
                self._turn = int(not self._turn)
                self._moves += 1

                if self._board.game_over:
                    game_state = self._board.get_game_state()
                    for player in self._players:
                        player.game_over(game_state, self._board.winner, self._moves)

                    break

    def set_player(self, slot, new_player):
        """Slot is a 1 or a 2 depending on which player you want to replace"""
        if slot not in (1, 2):
            raise ValueError("Slot must be either 1 or 2.") 
        
        if not isinstance(new_player, Player):
            raise TypeError("new_player must inherit from Player.") 

        self._players[slot-1]
    