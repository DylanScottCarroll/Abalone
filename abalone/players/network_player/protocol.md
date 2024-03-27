# Abalone Network Specifications






## Message Format


|     (Field)     | *Message Length* |  *Message Type* |    *Flags*      |          *Data*       |
|-----------------|------------------|-----------------|-----------------|-----------------------|
|  Size (Bytes)   |        1         |        1        |        1        |         1 - 61        |
|    Value        |      3 - 63      |      0 - 2      |  See "Flags"    |  Control/Move/Board   |
 

**Message Length**
Holds the total length of the message excluding this field.
Minimum of 2 and maximum of 63

**Message Type**

0 - Control
1 - Move Request (Board State)
2 - Move

**Flags** 
Information stored bitwise about the meaning of control messages in the lowest 6 bytes.

0x1 -  Message from server
0x2 -  Message from client
0x4 -  Handshake
0x8 -  Game over
0x10 - Invalid move received from player
0x20 - Player resigns


**Data**
Either a control code, a move, or a board state.

A **control code** is used to inform the client of their color during the handshake and for the server to inform the player who has won at the end.


A **move** is either two or three integer byes representing either a parallel or perpendicular move respectively. All indices are 0-60 corresponding to the order in the conveyed board state.
* *Parallel move*: One index representing the rear ball of a push and a second index representing the new position that that rear ball after the move.
* *Perpendicular Move*: Three indices. The first two represent a rear and front ball respectively, and the third representing the new position of thr rear ball after the push. Perpendicular moves may not push the balls in a direction parallel to the row of balls. 



A **board state** is an array of 61 bytes representing board positions. The bytes are arranged in row-major order starting from the bottom right (black on bottom).
Each byte can hold one of three values:
* 0 - White
* 1 - Black
* 2 - Empty


## Handshaking

When the client first connects to the server, the server sends the client a control message with the handshake flag. This message contains the color that that player is going to be during the game in the data field.

The client then responds with the same message as an acknowledgement.

Now the client waits to receive a message from the server requesting a move containing a board state.

## Sending Move Requests
The server requests a move from the client by sending the client a board state. Messages of this type are specified by a message type field of value 1. 
The message from server flag should be set in the flags field. 


If the server receives an illegal move from the client, the server will send a board move request and board state with the Invalid Move Received flag set.

Once the move request is sent, the server will wait for a response from the client containing a move.

## Sending Moves

Once the client receives a move request, it interprets the attached board state and generates a move.

It sends that move back to the server with the Message type field set to 2 and the Message From Player flag set.

If the client cannot find a move or has otherwise decided to resign, the client may resign by sending a control message with the Player Resigns flag set.

## Ending the  Game

Once one player has lost or resigned, the server will immediately send a game over message to the player.
This message is a control message and has the Game Over flag set. The data field of this message contains the color of the player that won: 
* 0 - White
* 1 - Black
* 2 - Draw
* 3 - Error