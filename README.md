# visual working memory game in pygame

## how to run
just run `main_game.py`
##### dependencies
    python='3.8'
    pygame='2.1.2'

------   
## About visual working memory task
### The following video displays the output of this repository.

- It contains several pages such as <ins>welcome</ins>   ,<ins>sign up</ins>, <ins>guiding</ins>, <ins>guiding task</ins>, <ins>go to actual task</ins>, <ins>actual task</ins>. 
- The user signs up first, then receives guidance about how to do the memory task, then performs it.
- how to play the memory game?
    - At the beginning of the memory task, a 6*6 hexagonal grid is displayed for two seconds, with certain hexagons simultaneously highlighted in yellow (known as "targets") while the rest are white (this is the memorization phase). 
    - Once the time is up, all the hexagons turn white, and the player must recall and click on the exact locations of the targets (this is the recall phase). 
    - Correct clicks turn green and incorrect ones turn red. 
    - The player's score is calculated by dividing the number of correct clicks by the total number of targets in that task, which is a rational number between 0 and 1. 
    - A score of 1 represents a win, whereas other scores represent a loss.
- A rule-based difficulty adjustment is applied
- At the end, the user game play data is saved in .csv and .plk file.
- Lots of parameters can be adjusted.




https://user-images.githubusercontent.com/65596290/178737195-80565633-60ce-4d58-8590-a0c315346da4.mp4





