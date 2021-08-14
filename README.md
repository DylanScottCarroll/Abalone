# Abalone

A python program for playing the game abalone. Made specifically to be easily extended with custom AI players. This program handles all of the graphics, move-checking, scoring, and player handling. 

---

# Documentation


## Game

The main class that represents the game and facilitates communication between the players and the game state.

<br/>


> **\_\_init\_\_(player1, player2, [viewscreen_size], [space_radius], [board_colors])** : Game
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
> **play()** : None
>
> Plays an entire game of abalone until one player wins

<br/>

> **set_player(slot, new_player)** : None
>
> Replace the player in the given slot with the specified new player.

|  Argument  |  Type  |                                  Purpose                                                  |
|------------|--------|-------------------------------------------------------------------------------------------|
| slot       | int    | The integer value 1 or 2, representing whether player1 or player2 is meant to be replaced |
| new_player | Player | The player that is taking the place of the player currently in the specified position.    |

---

## Board

| Public Fields |   Type      |                 Purpose                    |
|---------------|-------------|--------------------------------------------------|
| remaining     | list[int]   | Stores how many marble each player has remaining.
| game_over     | boolean     | True if the game has ended, False if it has not.
| winner        | None / int  | Holds the value of 

<br/>

>**\_\_init\_\_(self, size, radius, colors)** : Board

|  Argument  |  Type       |   Purpose     |
|------------|-------------|---------------|
| size       | (int, int)  | The size of the window in which the game is played in pixels  |
| radius     | int         | The radius of the circles that make up the slots              |
| colors     | list[tuple] | The colors of the game board. [player1, player2, empty, background]             |

<br/>

> **draw_board(self, surface)** : None
>
> Draw the board to the screen


>**surface** Represents the pygame surface that the board is being drawn to.

<br/>
<br/>

> **make_move(self, move, color)** : bool
>
> Given the move represented as a list of tuples, preform that move. This method also checks if the move is legal or not. If the move is legal, it preforms it and returns true. Otherwise, the move is not preformed and false is returned.

| Argument | Type        | Purpose   |
|----------|-------------|-----------| 
| move     | list[tuple] | A list with either two or three tuples representing the move. Each tuple represents a coordinate. |        
| color    | sqrt(10)    | 

> **Moves**
> There are two types of moves. **Perpendicular** and **parallel**. 
> **Parallel** moves are represented by a list of two coordinates. One coordinate represents the starting position, and the second coordinate represents the position that the marble at the starting position moves to. Any other marbles in the direction of the move are pushed.
> **Perpendicular** moves are represented by a list of three coordinates. The first represents the start, the second represents the end, and the third represents the destination. All marbles in between and including the start and the end are moved so that the start marble lines up with the end marble

<br/>

>**get_game_state(self)** : dict[tuple : int ]
>
> Returns a dictionary where the keys are coordinate tuples, and the values are integers representing what is at that position. (0:player1, 1:player2, 2:empty) 

---

## Player

> **color**
>
> Holds the color of the player. Not to be modified by the player itself. Only modified by the Game object.

> **get_move(self, game_state, screen, events, viewscreen_size, space_radius)** : list[tuple]
>
>


---

## Human_Player

---

## Public Functions

---

## Public Values



