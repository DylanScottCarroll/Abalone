import abalone
from abalone import players

if __name__ == "__main__":

    game = abalone.Game(players.HumanPlayer(), players.DylanAI("P2", 5))

    game.play(10000)


# rate_game_state    39.52
# get_new_game_state 10.92
#     paralell      2.60
#     perpendicular 5.92
    
