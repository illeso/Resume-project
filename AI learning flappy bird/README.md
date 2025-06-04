# AI Flappy Bird

This project implements an AI agent that learns to play Flappy Bird using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm.

## Requirements

- Python 3.7+
- Pygame
- NEAT-Python
- NumPy

Install the required packages using:
```bash
pip install -r requirements.txt
```

## How to Run

1. To train the AI:
```bash
python ai_agent.py
```

2. To play the game manually:
```bash
python flappy_bird.py
```

## Controls

- Space: Flap
- R: Restart (when game over)
- Close window to quit

## How it Works

The AI uses a neural network with the following inputs:
- Bird's current height
- Distance to the next pipe
- Height of the pipe gap
- Bird's current velocity

The neural network evolves using the NEAT algorithm, which:
1. Creates a population of neural networks
2. Evaluates their performance in the game
3. Selects the best performers
4. Creates new generations with mutations and crossovers
5. Repeats until the AI learns to play effectively

The fitness function rewards:
- Surviving longer (+0.1 per frame)
- Passing through pipes (+1.0 per pipe)

## Project Structure

- `flappy_bird.py`: The main game implementation
- `ai_agent.py`: The AI implementation using NEAT
- `config.txt`: NEAT configuration parameters
- `requirements.txt`: Project dependencies 