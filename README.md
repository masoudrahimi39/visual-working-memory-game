# Visual working memory game

## What is this repo?
The following video displays the output of this repo.

https://user-images.githubusercontent.com/65596290/178737195-80565633-60ce-4d58-8590-a0c315346da4.mp4

## Installation
1. Clone the repository by running `git clone https://github.com/masoudrahimi39/visual-working-memory-game.git`
2. Install dependencies
`   python='3.8'
    pygame='2.1.2'
    Pandas
   NumPy
   Matplotlib`
4. Run `main_game.py`

## Usage
1. Playing the game for fun.
2. Syncing with an eye tracker device.
3. Collecting player's gameplay and eye tracker data when playing the visual working memory game.

## Features
- Lots of parameters can be adjusted. All Python functions and Classes have neat doc strings.
- It contains several pages such as <ins>welcome</ins>   ,<ins>sign up</ins>, <ins>guiding</ins>, <ins>guiding task</ins>, <ins>go to actual task</ins>, <ins>actual task</ins>. 
- The user signs up first, receives guidance about playing the game, then the task starts.
- A rule-based difficulty adjustment is applied
- Finally, the user gameplay data is saved in CSV and plk files.

## About the memory game?
- At the beginning, a 6*6 hexagonal grid is displayed for two seconds, with certain hexagons simultaneously highlighted in yellow (known as "targets") while the rest are white. 
- After two seconds, all the hexagons become white, and the player must recall and click on the exact locations of the targets. 
- Correct and incorrect clicks instantly become green and red, respectively. 
- The player's score is the number of correct clicks divided by the total number of targets in the task.
- A score of 1 represents a win, whereas other scores represent a lose.
    







