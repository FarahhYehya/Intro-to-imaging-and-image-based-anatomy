# Skeleton Puzzle Game - Unity

Welcome to the **Skeleton Puzzle Game** repository! This project is a 3D puzzle game where players assemble a skeleton by correctly placing and rotating its pieces into their designated positions. The game features a variety of mechanics, including snapping, rotation, randomization, and a timer to challenge players. The skeleton model was created and cut into pieces using **Blender**, and the game was developed in **Unity**.

## Features

- **3D Puzzle Gameplay**: Players must assemble a skeleton by placing and rotating its pieces correctly.
- **Snapping Mechanism**: Pieces snap into place when positioned and rotated correctly.
- **Rotation Around 3 Axes**: Players can rotate pieces along the X, Y, and Z axes to fit them into the correct orientation.
- **Randomizer**: The skeleton pieces are randomized at the start of each game to provide a unique challenge every time.
- **Timer**: A timer adds an extra layer of difficulty, encouraging players to solve the puzzle as quickly as possible.
- **Blender-Made Skeleton Model**: The skeleton was modeled and cut into pieces using Blender, ensuring a clean and precise design.
- **Unity Implementation**: The game was developed in Unity, utilizing C# scripts for all game mechanics.

## How to Play

1. **Start the Game**: Launch the game in Unity or build and run the executable.
2. **Randomized Pieces**: The skeleton pieces will be randomly placed and rotated at the start.
3. **Assemble the Skeleton**: Drag and rotate the pieces to their correct positions. Pieces will snap into place when aligned correctly.
4. **Beat the Timer**: Complete the puzzle before the timer runs out for the best score!

## Repository Structure

```
Skeleton-Puzzle-Game/
├── Assets/
│   ├── Models/              # Contains the skeleton model and its pieces
│   ├── Scripts/             # All C# scripts for game mechanics
│   │   ├── Snapping.cs      # Handles snapping of pieces into place
│   │   ├── Rotation.cs      # Manages rotation around 3 axes
│   │   ├── Randomizer.cs    # Randomizes piece positions and rotations
│   │   ├── Timer.cs         # Implements the game timer
│   ├── Scenes/              # Unity scene files
│   ├── Materials/           # Textures and materials for the skeleton
├── Blender/                 # Contains the Blender project file for the skeleton model
├── README.md                # This file
└── LICENSE                  # License information for the project
```

## Requirements

- **Unity**: Version 2020.3 or later (LTS recommended).
- **Blender**: Optional, if you want to modify the skeleton model (version 2.8 or later).

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Skeleton-Puzzle-Game.git
   ```
2. Open the project in Unity.
3. Navigate to the `Scenes` folder and open the main game scene.
4. Press **Play** to start the game in the Unity Editor, or build the project to create an executable.

## Scripts Overview

- **Snapping.cs**: Handles the snapping of pieces into their correct positions when aligned properly.
- **Rotation.cs**: Allows players to rotate pieces around the X, Y, and Z axes.
- **Randomizer.cs**: Randomizes the position and rotation of skeleton pieces at the start of the game.
- **Timer.cs**: Implements a countdown timer to add challenge to the gameplay.

## Customization

- **Blender Model**: If you want to modify the skeleton model, open the `.blend` file in the `Blender` folder. Export the model as an FBX file and replace the existing model in the `Assets/Models` folder.
- **Game Mechanics**: Adjust the snapping sensitivity, rotation speed, or timer duration by modifying the corresponding scripts in the `Assets/Scripts` folder.

## Contributions

Contributions are welcome! If you have ideas for new features, improvements, or bug fixes, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Enjoy assembling the skeleton and have fun playing the game! If you have any questions or feedback, feel free to reach out. Happy coding! 🎮💀
