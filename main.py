from abalone import *    
from dylanai import Dylanai

if __name__ == "__main__":

    game = Game(Human_Player(), Dylanai("P2", 2))

    game.play(10000)