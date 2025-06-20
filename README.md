# Cat Runner Game 🐱

A Python-based endless runner game featuring a cat character that uses complex numbers for movement and physics calculations.

## 📋 Table of Contents
- [Description](#description)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Game Components](#game-components)
- [Controls](#controls)
- [Assets](#assets)
- [Technical Details](#technical-details)

## 🎮 Description
Cat Runner Game is a side-scrolling platformer built with Python and Pygame. The player controls a cat that automatically runs forward and must jump over obstacles like trees and mice to survive and score points.

## ✨ Features
- Smooth character animation
- Parallax scrolling background
- Dynamic obstacle generation
- Score tracking system
- High score system
- Sound effects and background music
- Game over screen with restart functionality

## 📦 Requirements
- Python 3.x
- Pygame library
- Required assets (images and sound files)

## 🚀 Installation
1. Clone the repository or download the game files
2. Install Python if not already installed
3. Install Pygame using pip:
```bash
pip install pygame
```
4. Run the game:
```bash
python app.py
```

## 🔧 Game Components

### Classes

#### Cat Class (`Cat`)
- Main player character class
- Inherits from `pygame.sprite.Sprite`
- Properties:
  - `frames`: List of animation frames
  - `velocity_y`: Vertical movement speed
  - `velocity_x`: Horizontal movement speed
  - `is_jumping`: Jump state
  - `gravity`: Gravity effect (0.5)
  - `jump_power`: Jump strength (-15)
- Methods:
  - `__init__()`: Initializes cat properties
  - `update()`: Handles animation and physics updates
  - `jump()`: Manages jump mechanics

#### Obstacle Class (`Obstacle`)
- Handles game obstacles (trees and mice)
- Inherits from `pygame.sprite.Sprite`
- Properties:
  - `image`: Obstacle sprite
  - `speed`: Movement speed
  - `passed`: Track if passed by player
- Methods:
  - `__init__()`: Sets up obstacle properties
  - `update()`: Handles obstacle movement

### Main Functions

#### `draw_button(text, x, y, width, height, color)`
- Creates interactive buttons
- Parameters:
  - `text`: Button text
  - `x, y`: Position coordinates
  - `width, height`: Button dimensions
  - `color`: Button color

#### `reset_game(cat, all_sprites, obstacles)`
- Resets game state
- Parameters:
  - `cat`: Player character
  - `all_sprites`: Sprite group
  - `obstacles`: Obstacle group
- Returns: Reset score (0)

#### `main()`
- Game's main loop
- Handles:
  - Game initialization
  - Event processing
  - Game state management
  - Score tracking
  - Obstacle spawning
  - Background scrolling

### Constants and Settings
- Screen dimensions: 800x600 pixels
- Ground level: 500 pixels from top
- Player position: 100 pixels from left
- Colors:
  - WHITE: (255, 255, 255)
  - BLACK: (0, 0, 0)
  - RED: (255, 0, 0)

## 🎯 Controls
- **Spacebar**: Jump
- **Mouse Click**: Restart game (when game over)

## 🎨 Assets
- `cat.png`: Player character sprite
- `mouse.png`: Mouse obstacle sprite
- `tree.png`: Tree obstacle sprite
- `dog.png`: Dog sprite (unused in current version)
- `background.png`: Scrolling background image
- `background_music.mp3`: Game background music
- `collision.wav`: Collision sound effect
- `jump.wav`: Jump sound effect

## 🔍 Technical Details

### Libraries Used
- **Pygame**: Main game engine
  - Handles graphics rendering
  - Sound management
  - Input processing
  - Sprite management
- **Random**: For obstacle generation
- **OS**: File path management
- **Sys**: System-specific parameters

### Game Mechanics
1. **Animation System**
   - Frame-based animation for cat
   - 4 animation frames for running
   - Animation speed: 100ms per frame

2. **Physics System**
   - Gravity-based jumping
   - Ground collision detection
   - Obstacle collision detection

3. **Scoring System**
   - Points awarded based on survival time
   - High score tracking
   - Score increment every 500ms

4. **Obstacle Generation**
   - Random obstacle type selection
   - Minimum spacing: 300 pixels
   - Spawn delay: 2000ms

5. **Background Scrolling**
   - Continuous parallax effect
   - Scroll speed: 5 pixels per frame

## Complex Number Implementation

The game extensively uses complex numbers for various game mechanics:

### 1. Movement and Physics
- **Position Representation**: 
  - Uses complex numbers to represent 2D positions (x + yi)
  - Real part (x) represents horizontal position
  - Imaginary part (y) represents vertical position

- **Velocity and Movement**:
  - `JUMP_COMPLEX = complex(0, -15)`: Represents jump velocity
  - `GRAVITY_COMPLEX = complex(0, 0.5)`: Represents gravity force
  - `MOVEMENT_COMPLEX = complex(5, 0)`: Represents horizontal movement

### 2. Obstacle Behavior
- **Tree Movement**:
  - Normal trees: `complex(-speed, 0)`
  - Fast trees: `complex(-speed * 1.5, 0)`
  - Bouncing trees: Complex position updates with vertical oscillation

- **Mouse Movement**:
  - Uses complex numbers for smooth movement
  - Position tracking with complex coordinates

### 3. Background Scrolling
- Uses complex numbers for parallax scrolling
- `bg_position = complex(0, 0)`
- `bg_scroll_speed = complex(-5, 0)`

## Game Features

### 1. Character Types
- **Cat**: Main player character with jumping mechanics
- **Mice**: Collectible items worth 5 points
- **Trees**: Three types of obstacles:
  - Normal trees
  - Fast trees (50% faster)
  - Bouncing trees (vertical movement)

### 2. Scoring System
- Base score: +1 point every second
- Mouse collection: +5 points per mouse
- High score tracking

### 3. Game Mechanics
- Space bar for jumping
- Collision detection with trees ends the game
- Mouse collection for bonus points
- Increasing difficulty with score

## Technical Implementation

### 1. Physics Engine
- Complex number-based velocity calculations
- Gravity simulation using imaginary components
- Collision detection using sprite rectangles

### 2. Animation System
- Frame-based animation for the cat
- Smooth movement using complex number interpolation
- Bouncing tree animation using complex oscillations

### 3. Spawn System
- Tree spawn rate: Every 2 seconds
- Mouse spawn rate: Every 8 seconds
- Maximum 2 mice on screen at once

## Performance Considerations

- Complex number calculations are optimized for real-time performance
- Sprite management for efficient rendering
- Collision detection optimization
- Background scrolling efficiency

## Future Improvements

1. Additional complex number-based features:
   - Spiral movement patterns
   - Wave-based obstacles
   - Complex number power-ups

2. Enhanced graphics:
   - Particle effects using complex numbers
   - More sophisticated animations

3. Gameplay features:
   - Multiple levels
   - Power-ups
   - Special abilities

## Contributing

Feel free to contribute to this project by:
1. Forking the repository
2. Creating a feature branch
3. Submitting a pull request

## License

This project is open source and available under the MIT License.

## Understanding Complex Numbers in Python

### What are Complex Numbers?
Complex numbers are numbers that consist of two parts:
- A real part (x)
- An imaginary part (y)
- Written in the form: x + yi, where i is the imaginary unit (√-1)

In Python, complex numbers are created using the `complex()` function or the `j` notation:
```python
# Creating complex numbers
z1 = complex(3, 4)    # 3 + 4i
z2 = 2 + 3j          # 2 + 3i
```

### Complex Number Operations in Python
```python
# Basic operations
z1 = complex(3, 4)
z2 = complex(1, 2)

# Addition
sum_z = z1 + z2      # (3+4i) + (1+2i) = (4+6i)

# Subtraction
diff_z = z1 - z2     # (3+4i) - (1+2i) = (2+2i)

# Multiplication
prod_z = z1 * z2     # (3+4i) * (1+2i) = (-5+10i)

# Accessing parts
real_part = z1.real  # Gets 3
imag_part = z1.imag  # Gets 4
```

### Complex Numbers in This Project

#### 1. Position Representation
```python
# Position as complex number
position = complex(x, y)

# Example from the game
cat_position = complex(100, GROUND_LEVEL)  # Cat's starting position
```

#### 2. Movement Calculations
```python
# Velocity as complex number
velocity = complex(horizontal_speed, vertical_speed)

# Example from the game
JUMP_COMPLEX = complex(0, -15)     # Upward jump
GRAVITY_COMPLEX = complex(0, 0.5)  # Downward gravity
```

#### 3. Physics Implementation
```python
# Updating position with velocity
def update_position(self):
    # Add velocity to position
    self.position += self.velocity
    
    # Apply gravity
    self.velocity += GRAVITY_COMPLEX
    
    # Update sprite position
    self.rect.x = int(self.position.real)
    self.rect.y = int(self.position.imag)
```

#### 4. Bouncing Tree Movement
```python
# Complex number-based bouncing
if self.tree_type == "bouncing":
    # Update bounce height
    self.bounce_height += self.bounce_speed * self.bounce_direction
    
    # Reverse direction at limits
    if self.bounce_height > 20 or self.bounce_height < 0:
        self.bounce_direction *= -1
    
    # Update position with bounce
    self.position = complex(
        self.position.real,
        GROUND_LEVEL - self.bounce_height
    )
```

### Benefits of Using Complex Numbers

1. **Simplified 2D Movement**:
   - Single number represents both x and y coordinates
   - Easier to perform calculations on both dimensions
   - Cleaner code structure

2. **Efficient Physics**:
   - Natural representation of forces and velocities
   - Easy to combine multiple movements
   - Simplified gravity and jump calculations

3. **Smooth Animations**:
   - Complex numbers enable smooth transitions
   - Easy to implement oscillating movements
   - Natural representation of circular motion

4. **Mathematical Operations**:
   - Built-in Python support for complex arithmetic
   - Efficient calculations for game physics
   - Easy to implement advanced movement patterns

### Example: Implementing a Spiral Movement
```python
# Spiral movement using complex numbers
def update_spiral_position(self):
    # Time-based angle
    angle = time.time() * 2
    
    # Spiral radius increases with time
    radius = 50 + time.time() * 10
    
    # Convert to complex number
    spiral_pos = complex(
        radius * math.cos(angle),
        radius * math.sin(angle)
    )
    
    # Update position
    self.position = spiral_pos
```

