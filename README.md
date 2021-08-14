# Abalone

A python program for playing the game abalone. Made specifically to be easily extended with custom AI players. This program handles all of the graphics, move-checking, scoring, and player handling. 

---

# Documentation


## Game

The main class that represents the game and facilitates communication between the players and the game state.

<br/>


> #### \_\_init\_\_(player1, player2, [viewscreen_size], [space_radius], [board_colors]) : Game
>
>Set all of the parameters of the game and returns the game object.

| Argument        | Type         | Default Value| Purpose              
|-----------------|--------------|-------------------|---------------------- 
| player1         | Player       | N/A               | An object inherited from Player that can make moves given a board state.
| player2         | Player       | N/A               | "
| viewscreen_size | (int, int)   | (500, 500)        | The size of the window that the game is played in.
| space_radius    | int          | 15                | The size in pixels of each space on the board.
| board_colors    | list[tuple]  | <nobr> (0, 0, 0) <br/> (255, 255, 255) <br/> (100, 100, 100)  <br/> (128, 128, 128) </nobr>|  <nobr>The color of player 1 <br/> The color of player 2 <br/> The color of empty spaces <br/> The background color </nobr>


<br/>

>
> #### **play()** : None
>
> Plays an entire game of abalone until one player wins

<br/>

> #### **set_player(slot, new_player)** : None
>
> Replace the **player** in the given slot with the specified new player.

|  Argument  |  Type  |                                  Purpose                                                  |
|------------|--------|-------------------------------------------------------------------------------------------|
| slot       | int    | The integer value 1 or 2, representing whether player1 or player2 is meant to be replaced |
| new_player | Player | The new player that is being placed at the index of **slot**    |

---

## Board

This is a class that handles the board state, the positions of the marbles, the current game score, and preforming and checking moves.

<br/>

| Public Fields |   Type      |                 Purpose                    |
|---------------|-------------|--------------------------------------------------|
| remaining     | list[int]   | Stores how many marble each player has remaining.
| game_over     | boolean     | True if the game has ended, False if it has not.
| winner        | None / int  | Holds the value of the color of the winner (0 : Player1, 1: Player2)

<br/>

> #### **\_\_init\_\_(size, radius, colors)** : Board
>
>Initializes the board given the specified parameters.

|  Argument  |  Type       |   Purpose     |
|------------|-------------|---------------|
| size       | (int, int)  | The size of the window in which the game is played in pixels  |
| radius     | int         | The radius of the circles that make up the slots              |
| colors     | list[tuple] | The colors of the game board. [player1, player2, empty, background]             |

<br/>
<br/>

> #### **draw_board(surface)** : None
>
> Draw the board to the screen
>
>**surface** Represents the pygame surface that the board is being drawn to.

<br/>
<br/>

> #### **make_move(move, color)** : bool
>
> Given the **move** as a list of tuples, preform that move. This method also checks if the move is legal or not. If the move is legal, it preforms it and returns True. Otherwise, the move is not preformed and False is returned.

| Argument | Type        | Purpose   |
|----------|-------------|-----------| 
| move     | list[tuple] | A list with either two or three tuples representing the move. Each tuple represents a coordinate. |        
| color    | int         | The color of the player making the move. (0 : Player1, 1 : Player2)


<br/>
<br/>

> #### **Moves:**
> There are two types of moves. **Perpendicular** and **parallel**. 
> **Parallel** moves are represented by a list of two coordinates. One coordinate represents the starting position, and the second coordinate represents the position that the marble at the starting position moves to. Any other marbles in the direction of the move are pushed.
> **Perpendicular** moves are represented by a list of three coordinates. The first represents the start, the second represents the end, and the third represents the destination. All marbles in between and including the start and the end are moved so that the start marble lines up with the end marble

<br/>
<br/>

> #### **get_game_state(self)** : dict[tuple : int ]
>
> Returns a copy of the game state as a dictionary where the keys are coordinate tuples, and the values are integers representing what is at that position. (0:player1, 1:player2, 2:empty) 

---

## Player

This is a class that is supposed to be inherited from and the main functions overwritten

> #### **color**
>
> Holds the color of the player. Not to be modified by the player itself. Only modified by the **Game** object.

<br/>

> #### **get_move(self, game_state, screen, events, viewscreen_size, space_radius)** : list[tuple]
>
> This is the main function that needs to be implemented for a player. Given information about.
> The expected return type is a list of tuples specified in the **make_move()** section of the Board documentation.
>
> Returning None, will not make any move, so you can return None if you want to wait another frame to decide a move. This is mostly for the human player being able to detect key-events in-between frames.

|     Argument     |     Type          | Purpose |
|------------------|-------------------|---------|
| game_state       | <nobr> dict[tuple : int] </nobr> | Passes the entire state of the game as a dictionary where the keys are coordinate tuples, and the values are integers representing what is at that position. (0:player1, 1:player2, 2:empty) |
| screen           | pygame Surface                   | The pygame screen surface for drawing on if the player needs to draw a GUI. Mostly for human players. |
| events           | pygame Events                    | The pygame events from the last frame if the player needs mouse and key events for a GUI. Mostly for human players.
| viewscreen_size  | (int, int)                       | The size of the game window in pixels. Mostly for human player GUI.
| space_radius     | int                              | The radius of the marbles and slots in pixels. Mostly for human player GUI.

<br/>

> #### **game_over(self, game_state, winner, moves)** : None
>
> Preform any game-over tasks.
> Not required. Use this to do logging, tallying, or maching learning or whatever.
>
>  **game_state** and **winner** are described elsewhere in the documentation.
>
>  **moves** is a list of all of the moves that were taken throughout the game.


<br/>

> #### **setup(self)** : None
>
> Preform any pre-game setup. Called before first the game after the player is first initialized. Also called in-between back-to-back games, so this method should totally reset all state. So the player can play a game fresh from start immediately.

---

## Human_Player

Inherits from Player and implements the functions needed for the game to be operated by a mouse and keyboard.
Click on the positions to select, starts, ends, and/or destinations for the move. Click off the board somewhere to clear all selections or click on a selection to delete it. 
Hit enter to send a move.

> See **Player** for all of the method signatures and expectations.

---

## Public Functions

> #### **coord_in_board(coord)** : bool
>
> Returns True if the given coordinate represents a space **on** the board. Otherwise returns False.
>
> **coord** is expected to be a two-tuple of integers.

<br/>

> #### **coord_in_board_or_edge(coord)** : bool
>
> Returns true if the given coordinate represents a space on the board **or** a space one step immediately off the board.
>
> #### **coord** is expected to be a two-tuple of integers.


<br/>

> #### **get_adjacent_spaces(coord)** : (int, int)
>
> Returns a list of int two-tuple coordinates representing every position that is a single legal move away from the given coordinate.
>
> **coord** is expected to be a two-tuple of integers.

<br/>

> #### **sum_tuples(a, b)** : tuple
>
> Add every corresponding element of **a** and **b** and returns the result.
> **a** and **b** are expected to be number n-tuples of the same length.
>
> This is intended to be useful in preforming operations on board coordinates.

<br/>

> #### **sub_tuples(a, b)** : tuple
>
> **a** and **b** are expected to be number n-tuples of the same length.
>
> This is intended to be useful in preforming operations on board coordinates.

<br/>

> #### **normalize_tuple(a)** : tuple
>
> Scales each value in the given tuple *a*, such that each value is either -1, 0, or 1. All negative values become -1, all positive values become 1, and zeroes stay zero.
> Expects integers, but floats might work. I'm not sure why you'd want to do that though.
>
> This is intended to be useful in preforming operations on board coordinates.

---

## Public Values

Please don't change these, okay?

>  **LEGAL_VECTORS** = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1,), (-1, -1)]
>
> A list of all legal moves that can be made

<br/>

> **START_MARBLE_COUNT** = 14
>
> The number of marbles that each player starts with

<br/>

> **TOTAL_SPACE_COUNT** = 61
>
> The total number of spaces on the board.

<br/>

> **LOSE_THRESHOLD** = 6
>
> The number of marbles that need to ne pushed off in order to lose


