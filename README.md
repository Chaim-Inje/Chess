# Chess Game Project

Welcome to our Chess Game Project! This game is a labor of love by [Jacob Wolman](https://www.linkedin.com/in/jacob-wolman-084277287/) and [Chaim Inje](https://www.linkedin.com/in/chaim-inje/). 



## About the Game

This is not just any chess game. We've designed it to be interactive, user-friendly, and challenging for all levels of chess enthusiasts. You can test your skills against a computer opponent, or challenge a friend to a match. 

## Features

- **Play against the computer**: Our game includes an AI opponent that you can play against. Don't underestimate it, it might surprise you!
- **Play against a friend**: Want to challenge a friend? Our game allows two players to play against each other. 
- **User-friendly interface**: We've made the game easy to navigate, so you can focus on your strategy and enjoy the game.

We hope you enjoy playing this game as much as we enjoyed creating it. Checkmate!



## Usage of Stockfish

This project uses the Stockfish chess engine for generating computer opponent moves. Please note that Stockfish is only used for move generation and does not influence other aspects of the game.

The source code of Stockfish can be found at their official GitHub repository: https://github.com/official-stockfish/Stockfish.

## Instructions to Run the Program

Note that this project is a Python-based chess game that works on Linux and Windows.

1. **Clone the Repository**
   ```
   git clone https://github.com/Chaim-Inje/Chess.git
   ```

2. **Navigate to the Directory**
   ```
   cd Chess
   ```

3. **Install Dependencies**
   ```
   pip install pygame typing stockfish
   ```

4. **Grant Execute Permissions (Linux Only)**
   If you're on a Linux system, you might need to grant execute permissions to the Stockfish binary:
   ```
   chmod +x stockfish-ubuntu-x86-64-avx2
   ```

5. **Run the Program**
   ```
   python3 main.py
   ```

If you encounter any issues, they might be related to permissions or your Python environment. In such cases, consider using a virtual environment or running the commands as an administrator.
```
Enjoy your game!

# License

This project is licensed under the MIT License - see the LICENSE.md file for details
