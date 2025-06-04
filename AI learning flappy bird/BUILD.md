# Building the AI Flappy Bird Project

This document explains the step-by-step process of building the AI Flappy Bird project.

## 1. Project Setup

First, we set up the project structure and dependencies:

```bash
# Created requirements.txt with:
pygame==2.5.2    # For game graphics and input handling
numpy==1.24.3    # For numerical operations
neat-python==0.92 # For neural network evolution
```

## 2. Game Implementation (flappy_bird.py)

The game was built in layers:

### 2.1 Constants and Initialization
```python
# Game window and physics constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.25
FLAP_STRENGTH = -7
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_FREQUENCY = 1500
```

### 2.2 Bird Class
- Implemented basic physics (gravity, velocity)
- Added flap mechanics
- Created collision detection rectangle
- Added drawing functionality

### 2.3 Pipe Class
- Random gap generation
- Movement mechanics
- Collision rectangles for top and bottom pipes
- Score tracking (passed flag)

### 2.4 Game Class
- Game loop implementation
- Event handling (keyboard input)
- Score tracking
- Game state management
- Rendering system

## 3. AI Implementation (ai_agent.py)

The AI was implemented using the NEAT algorithm:

### 3.1 Neural Network Inputs
```python
inputs = [
    bird.y / 600,                    # Normalized bird height
    closest_pipe.gap_y / 600,        # Normalized gap center
    (closest_pipe.x - bird.x) / 400, # Normalized distance to pipe
    bird.velocity / 10               # Normalized velocity
]
```

### 3.2 Fitness Function
```python
# Rewards:
genome.fitness += 0.1  # For surviving each frame
genome.fitness += 1.0  # For passing each pipe
```

### 3.3 NEAT Configuration (config.txt)
- Population size: 50 birds
- Mutation rates for nodes and connections
- Species compatibility threshold
- Stagnation parameters
- Reproduction settings

## 4. Key Design Decisions

### 4.1 Game Mechanics
- Used simple rectangle-based collision detection for performance
- Implemented smooth physics with gravity and velocity
- Added score tracking for both manual and AI play

### 4.2 AI Design
- Chose NEAT algorithm for its ability to evolve both topology and weights
- Normalized all inputs to [0,1] range for better neural network performance
- Used tanh activation function for smooth decision making
- Implemented population-based learning for better exploration

### 4.3 Performance Optimizations
- Limited pipe generation frequency
- Removed off-screen pipes
- Used efficient collision detection
- Implemented frame rate limiting

## 5. Testing and Refinement

The project went through several iterations:

1. Basic game mechanics
2. AI integration
3. Parameter tuning
4. Performance optimization
5. Documentation

## 6. Future Improvements

Potential enhancements:
- Add graphics and animations
- Implement sound effects
- Add difficulty levels
- Save/load best AI models
- Add visualization of neural networks
- Implement parallel training
- Add more sophisticated fitness functions

## 7. Lessons Learned

1. Start with simple mechanics and build up
2. Normalize inputs for better AI performance
3. Balance fitness function rewards
4. Use appropriate data structures for performance
5. Document code thoroughly
6. Test extensively before adding complexity 