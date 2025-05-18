# Shapeshift

<video src="media/demo.mp4" controls width="500"></video>


# 🕹️ Sketch-to-Game

Draw your own game levels using simple shapes — and watch them come to life as playable digital maps!

## ✏️ How It Works

Create your level by drawing basic shapes and lines on a 2D canvas. The game engine interprets your sketch and turns it into a functional platformer level.

## 🎮 Drawing Rules

Use these shapes to design your map:

| Shape         | Meaning         |
|---------------|-----------------|
| 🟦 Pentagon     | **Start point**  |
| 🟨 Hexagon      | **End point**    |
| 🔺 Triangle     | **Coin / Collectible** |
| ➖ Horizontal Line | **Platform**     |

> Only horizontal lines are considered platforms. Other lines are ignored.



## 🚀 Features

- Intuitive level creation by sketching
- Real-time conversion from drawing to gameplay
- Platformer-style player movement and collectibles
- Supports coins, platforms, start/end logic

## 🛠️ Tech Stack

- Godot Engine
- GDScript
- Custom shape parser

## 📂 Getting Started

1. Clone the repo
2. Open the project in Godot
3. Run the game
4. Start drawing and play!

```bash
git clone https://github.com/yourusername/sketch-to-game.git
