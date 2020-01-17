# 2048 Text

A text-based version of the video game '2048'.

## Download

In order to play the game, you need to download the ```2048_text.py``` file in this repository. Then, to run the program, simply open a shell, navigate to the folder in which the file is located, and run ```python 2048_text.py```.

## How to play

'2048' is a game in which you manoeuvre tiles around a 4x4 board, merging tiles of the same value in an attempt to reach 2048. You can play it online at https://play2048.co/.

'2048 Text' follows the same rules as the original game. Use the WASD keys to move tiles up, left, down, and right (respectively). If adjacent tiles with the same number are moved into one another, they will form one tile with double the value. As an example, take the following board state:

```
- - - -
- - - -
- 2 - -
4 2 - 8
```

If the player presses the S key (for down), then the two tiles of value 2 will merge with one another, forming a single '4' tile:

```
2 - - -
- - - -
- - - -
4 4 - 8
```

You will probably have noticed that a 2 has appeared in the top-left corner – after each move, a single new tile (either a '2' or a '4') spawns in a random empty position.

Assuming the player presses the D key (for right), the board will change once more, as can be seen below:

```
- - - 2
4 - - -
- - - -
- - 8 8
```

All of the tiles (excluding the newly spawned '4' tile) have moved over to the right, with the two '4' tiles in the bottom row merging into an '8'. It is important to note that tiles do not continuously merge in a cascading manner. If this was the case, the two '8' tiles in the bottom-right would have merged into a '16' from a single move.

You lose the game if you have filled the board such that you cannot make any move to shift or merge tiles. You win if you can create a tile with the value of 2048.
