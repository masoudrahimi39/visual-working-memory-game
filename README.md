# Visual working memory game

### Demo
https://user-images.githubusercontent.com/65596290/178737195-80565633-60ce-4d58-8590-a0c315346da4.mp4

## Installation
1. Clone the repository by running
```php
git clone https://github.com/masoudrahimi39/visual-working-memory-game.git
   ```

2. Install dependencies: `python='3.8', pygame='2.1.2', Pandas, NumPy, Matplotlib` by running below:
   ```php
   pip install pygame='2.1.2', Pandas, NumPy, Matplotlib
   ```
4. Run `main_game.py`

## Usage
This project serves multiple purposes:
1. **Entertainment**: Play the game for fun and test your visual working memory abilities.
3. **Gameplay and Eye Tracker Data Collection**: The game collects and saves the player's gameplay data, along with eye tracker data when enabled, providing valuable insights for research and analysis.

## Features
- **Adjustable Parameters**: All Python functions and classes have clear and concise docstrings, making it easy to modify and extend the game's functionalities.
- - **Rule-Based Difficulty Adjustment**: The game incorporates a rule-based difficulty adjustment system, ensuring that players are appropriately challenged as they progress through the tasks.
- **Data Storage**: The player's gameplay data is saved in CSV and plk (Pandas DataFrames) files, facilitating data analysis and post-game insights.
- **Structured User Journey**: The task follows a well-structured user journey, guiding players through different pages, including "Welcome," "Sign Up," "Guiding," "Guiding trials," and "Actual Trials."

## About the memory game?
- At the beginning, a 6*6 hexagonal grid is displayed for two seconds, with certain hexagons simultaneously highlighted in yellow (known as "targets") while the rest are white. 
- After two seconds, all the hexagons become white, and the player must recall and click on the exact locations of the targets. 
- Correct and incorrect clicks instantly become green and red, respectively. 
- The player's score is the number of correct clicks divided by the total number of targets in the task.
- A score 1 represents a win, whereas other scores represent a loss.
