---

# Tetris with Pygame

A classic Tetris game built from scratch using Python and Pygame. This implementation features falling tetrominoes, line clearing with scoring, and a restart option when the game ends.

## Table of Contents
- [Overview](#overview)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Features](#features)
- [Contributing](#contributing)
- [Future Improvements](#future-improvements)
- [License](#license)

## Overview

This project is a simple yet functional Tetris game developed as a learning exercise in Python and Pygame. It includes the core mechanics of Tetris such as piece movement, rotation, and line clearing, with a wider playfield (15 blocks) and a game-over screen with a restart button.

## Screenshots

*Gameplay:*
![Gameplay Screenshot](screenshots/gameplay.png)

*Game Over Screen:*
![Game Over Screenshot](screenshots/gameover.png)


## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/YerraRahul23/Tetris.git
   cd Tetris-pygame
   ```

2. **Install Dependencies:**
   Ensure you have Python 3.x installed. Then install Pygame:
   ```bash
   pip install pygame
   ```

3. **Run the Game:**
   ```bash
   python Tetris.py
   ```

## How to Play

- **Controls:**
  - **Left Arrow**: Move piece left
  - **Right Arrow**: Move piece right
  - **Down Arrow**: Move piece down faster
  - **Up Arrow**: Rotate piece
  - **Mouse Click**: Click the "Restart" button on the game-over screen to start a new game
  - **Close Window**: Exit the game

- **Objective:**
  Stack the falling tetrominoes to fill rows completely. Each cleared row adds 10 points to your score. The game ends when pieces stack to the top of the playfield.

## Features

- Wider playfield (15 blocks wide x 20 blocks tall)
- Five classic tetromino shapes (O, I, T, S, Z) with rotation
- Line clearing with score tracking
- Stable red border around the playfield
- Game-over screen with final score and restart button
- Real-time score display during gameplay

## Contributing

Contributions are welcome! If you'd like to improve this project:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m "Add feature"`).
4. Push to your branch (`git push origin feature-branch`).
5. Open a pull request.

Feel free to suggest bug fixes, new features, or optimizations!

## Future Improvements

Here are some ideas to enhance the game:
- Add a preview window for the next tetromino
- Implement increasing difficulty (faster fall speed over time)
- Include sound effects and background music
- Add a high-score system with persistent storage
- Create a start/pause menu

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
