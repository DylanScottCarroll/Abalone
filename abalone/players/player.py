class Player():
    """A class that player types can inherit from"""

    def __init__(self):
        """Only called when the object is created in the beginning
        Not called in between games because objects persist between games"""

        pass

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