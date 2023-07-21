# Visual working memory game

## What is this repo?
The following video displays the output of this repository.

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
many variables can be adjusted

- It contains several pages such as <ins>welcome</ins>   ,<ins>sign up</ins>, <ins>guiding</ins>, <ins>guiding task</ins>, <ins>go to actual task</ins>, <ins>actual task</ins>. 
- The user signs up first, then receives guidance about how to do the memory task, then performs it.
- how to play the memory game?
    - At the beginning of the memory task, a 6*6 hexagonal grid is displayed for two seconds, with certain hexagons simultaneously highlighted in yellow (known as "targets") while the rest are white (this is the memorization phase). 
    - Once the time is up, all the hexagons turn white, and the player must recall and click on the exact locations of the targets (this is the recall phase). 
    - Correct clicks turn green and incorrect ones turn red. 
    - The player's score is calculated by dividing the number of correct clicks by the total number of targets in that task, which is a rational number between 0 and 1. 
    - A score of 1 represents a win, whereas other scores represent a loss.
- A rule-based difficulty adjustment is applied
- At the end, the user game play data is saved in csv and plk file.
- Lots of parameters can be adjusted.




https://user-images.githubusercontent.com/65596290/178737195-80565633-60ce-4d58-8590-a0c315346da4.mp4





