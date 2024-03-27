import pygame, time, abalone

from math import sqrt
from abalone.players import Player
from timeit import default_timer as timer


class DylanAI(Player):
    """Dylan's Abalone AI"""

    def __init__(self, name, depth):
        self.name = name
        self.depth = depth
        self.timer = MultiTimer()

    def setup(self):
        
        self.selection = 0

        self.remaining_w = 200
        self.e_remaining_w = -100

        self.avg_center_dist_w = -10
        self.e_avg_center_dist_w = 5

        self.on_rim_w = -1
        self.e_on_rim_w = 2

        pass

    def game_over(self, game_state, winner, moves):
        print(winner, " won")

    def get_move(self, game_state, screen, events, viewscreen_size, space_radius):
        self.moves = 0

        rating, line, vector = self.propagate(game_state, True, None, 0, self.depth)

        print(line, vector)
        print("copy", self.timer["copy"])
        return self.reformat_move(line, vector)

    def propagate(self, game_state, maximizing, max_hitherto, depth, max_depth):    
        """ game_state - The current game state.
            line/vector - The line and vector that was applied to get to the given game state.
            max - True if maximizing score, False if minimizing score.
            depth - The current recursion depth.
            max_depth - the maximum recursion depth.
            
            Return:
            (best_score, line, vector) """
        
        self.moves += 1

        if depth >= max_depth:
            rating = self.rate_game_state(game_state)

            return (rating, None, None)
        
        else:
            
            color = self.color if maximizing else (1 if self.color==0 else 0)
            choices = []

            all_lines = self.get_all_lines(game_state, color)

            for line in all_lines:
                for vector in abalone.LEGAL_VECTORS:
                    new_game_state = self.get_new_game_state(game_state, line, vector, color)

                    if new_game_state is not None:
                        rating = self.rate_game_state(new_game_state)

                        choices.append( (new_game_state, rating, line, vector) )

            choices = sorted(choices, key=lambda x: x[1], reverse=maximizing)
            
            
            final_choice = choices[0][1:]
            del choices[0]

            for choice in choices:

                new_game_state, estimated_rating, line, vector = choice
                actual_rating, _, _ = self.propagate(new_game_state, not maximizing, final_choice[0], depth+1, max_depth)
                
                
                if maximizing:
                    if final_choice[0] < actual_rating:
                        final_choice = (actual_rating, line, vector)

                else: #minimizing
                    if (max_hitherto is not None) and (actual_rating < max_hitherto): 
                        
                        return (actual_rating, line, vector)

                    if actual_rating < final_choice[0]:
                        final_choice = (actual_rating, line, vector)
                
               

            return final_choice

    def get_all_lines(self, game_state, current_color):
        """Collect a list of all unique lines of one two and three marbles made from the specified color. 
        
        Returns a list of tuples of board coordinates.
        Coordinates in each line are in a consistent order based on the direction. 
        """

        singles = []
        doubles = []
        triples = []

        #Collect single 
        for coord in abalone.all_coords():
            if game_state[coord] == current_color:
                singles.append([coord])

        #Add all positive-direction movements to form the doubles
        for single in singles:
            for vector in [(1, 0), (0, 1), (1, 1)]:

                coord = abalone.sum_tuples(single[0], vector)
                if abalone.coord_in_board(coord) and game_state[ coord ] == current_color:
                    doubles.append(single + [coord])

        #Add the the third marble in the row after the two unless it doesn't exist
        for double in doubles:
            vector = abalone.sub_tuples(double[1], double[0])
            coord = abalone.sum_tuples(double[1], vector)

            if abalone.coord_in_board(coord) and game_state[ coord ] == current_color:
                triples.append(double + [coord])

        return singles + doubles + triples

    def get_new_game_state(self, game_state, line, vector, current_color):
        """Given a game state a line, a movement vector, and a color to move,
            get a new board state from making that move
        Returns None if the move is illegal""" 

        #Determine if the move is parallel to the line
        parallel = False
        
        if len(line) > 1:
            if (line[0][0]+vector[0], line[0][1]+vector[1]) == line[1]:
                parallel = True
            if (line[-1][0]+vector[0], line[-1][1]+vector[1])  == line[-2]:
                parallel = True


        if parallel:            
            #Find the rear marble in the motion
            start = line[0] if abalone.sum_tuples(line[0], vector) == line[1] else line[-1]
            end = line[-1] if start==line[0] else  line[0]

            off_end = abalone.sum_tuples(end, vector)
            if abalone.coord_in_board(off_end) and  game_state[off_end] == current_color: return None

            counting_others = False
            self_count = 0
            other_count = 0
            current = start
            chain = [2]
            #Put the marbles in chain until an empty space or the edge is reached
            while abalone.coord_in_board(current) and game_state[current]!=2:

                current_marble = game_state[current]
                if current_marble == current_color:
                    if counting_others: 
                        return None
                    else:
                        self_count+=1
                else:
                    other_count+=1
                    counting_others=True
                
                if self_count>3 or other_count > 3 or other_count>=self_count: return None

                chain.append(current_marble)
                current = (current[0] + vector[0], current[1]+vector[1])

            #Check if ball is being pushed off
            if not counting_others and not abalone.coord_in_board(current): 
                return None
            
            #Lay down the chain onto the new game state
            new_game_state = game_state.copy()

            current = start
            for marble in chain:
                x,y = current
                if ((1<=x<=9) and (1<=y<=9) and (y-4 <= x <= y+4)):
                    new_game_state[current] = marble
                current = current[0]+vector[0], current[1]+vector[1]

            return new_game_state

        else: #Perpendicular moves
            for coord in line:
                move_coord = coord[0]+vector[0], coord[1]+vector[1]
                
                x,y = move_coord
                in_board = ((1<=x<=9) and (1<=y<=9) and (y-4 <= x <= y+4))
                if in_board and game_state[move_coord] != 2:
                    return None
                elif not in_board:
                    return None

            new_game_state = game_state.copy()
            for coord in line:
                new_game_state[coord] = 2
                move_coord = coord[0]+vector[0], coord[1]+vector[1]
                x,y = coord
                if (1<=x<=9) and (1<=y<=9) and (y-4 <= x <= y+4):
                    new_game_state[move_coord] = current_color

            return new_game_state 

    def rate_game_state(self, game_state):

        avg_center_dist = 0
        e_avg_center_dist = 0

        remaining = 0
        e_remaining = 0

        on_rim = 0
        e_on_rim = 0 

        enemy_color = 1 if self.color == 0 else 0
        
        for coord in abalone.all_coords():
            
            x, y = coord
            #Calculate distance
            #Count for remaining
            if game_state[coord] == self.color: 
                remaining += 1

                if abalone.coord_on_rim(coord):on_rim += 1

                current_dist = sqrt((0.866*y-4.33)**2 + (x-0.5*y-2.5)**2)
                avg_center_dist += current_dist

            elif game_state[coord] == enemy_color:
                e_remaining += 1

                if abalone.coord_on_rim(coord): e_on_rim += 1

                current_dist = sqrt((0.866*y-4.33)**2 + (x-0.5*y-2.5)**2)
                e_avg_center_dist += current_dist

        avg_center_dist /= remaining
        e_avg_center_dist /= e_remaining

        #Weight and sum the values
        return (avg_center_dist*self.avg_center_dist_w + 
                e_avg_center_dist * self.e_avg_center_dist_w +
                remaining * self.remaining_w +
                e_remaining * self.e_remaining_w +
                on_rim * self.on_rim_w + 
                e_on_rim * self.e_on_rim_w )  
                    
    def reformat_move(self, line, vector):
        parallel = False
        for coord in line:
            if abalone.sum_tuples(coord, vector) in line:
                parallel = True
                break

        if len(line) == 1: parallel = True

        if parallel:
            #Find the rear marble in the motion
            start = line[0] if len(line)==1 or abalone.sum_tuples(line[0], vector) == line[1] else line[-1]

            return (start, abalone.sum_tuples(start, vector))

        else:
            return (line[0], line[-1], abalone.sum_tuples(line[0], vector))

    def _display_lines(self, lines, screen, viewscreen_size):
        if self.selection >= len(lines): self.selection = 0


        for coord in lines[self.selection]:
            print(coord)
            pygame.draw.circle(screen, (255, 0, 0), abalone.board_to_pixel_coords(coord, viewscreen_size), 5 )


        
        self.selection += 1

    def _draw_state(self, game_states, surface, viewscreen_size, space_radius):
        """Draw the given board state to the given pygame surface"""
        
        self.selection += 1
        if self.selection >= len(game_states): 
            self.selection = 0
            input()

        print(self.selection)

        game_state = game_states[self.selection]

        colors = [(0, 0, 0), (255, 255, 255), (100, 100, 100)]

        spacing_x = viewscreen_size[0] / 10
        spacing_y = (viewscreen_size[1]* 0.866025403784) / 10 #hardcoded sqrt(3)/2 aka sin(pi/3)
        offset_y = viewscreen_size[1] *  ((1-0.866025403784)/2)

        for coord in abalone.all_coords():
            x, y = coord

            offset_x = (5-y) * (spacing_x/2)

            draw_y = int(viewscreen_size[1] - (spacing_y * y)) - offset_y
            draw_x = int(spacing_x * x) + offset_x

            color = colors[game_state[(x, y)]]

            pygame.draw.circle(surface, color, (draw_x, draw_y), space_radius)
   
class Game_State(object):

    @staticmethod
    def index(self, coord):
        #Values are hard-coded to make this a smidgeon faster because this method will get called a lot
        return ([0, 5, 11, 18, 26, 35, 43, 50, 56][coord[1]-1] + coord[0] - 1 - (coord[1]-5 if coord[1]-5 > 0 else 0))
        

    def __init__(self, game_state = None):
        if game_state != None:
            self.slots = []
            for coord in abalone.all_coords():
                self.slots.append( game_state[coord] )

    def __getitem__(self, coord):
        #Values are hard-coded to make this a smidgeon faster because this method will get called a lot
        return self.slots[ 
            [0, 5, 11, 18, 26, 35, 43, 50, 56][
                coord[1]-1
            ] + 
            coord[0] - 1 - 
            (coord[1]-5 if coord[1]-5 > 0 else 0)
        ]


    def __setitem__(self, coord, value):
        #Values are hard-coded to make this a smidgeon faster because this method will get called a lot
        self.slots[ 
            [0, 5, 11, 18, 26, 35, 43, 50, 56][
                coord[1]-1
            ] + 
            coord[0] - 1 - 
            (coord[1]-5 if coord[1]-5 > 0 else 0)
        ] = value

    def copy(self):
        newGameState = Game_State()
        newGameState.slots = self.slots.copy()
        return newGameState

class MultiTimer():
    def __init__(self):
        self.last_starts = {}
        self.total_times = {}

    def start(self, name: str):
        self.last_starts[name] = timer()


    def end(self, name: str):
        if not name in self.total_times.keys():
            self.total_times[name] = 0
        self.total_times[name] += timer() - self.last_starts[name]

    def __getitem__(self, name):
        return self.total_times[name]

    def __str__(self):
        string = ""
        for key in self.total_times.keys():
            string += key + " : " + str(self.total_times[key]) + "\n"

        return string

        