# Schedule-1-Monte-Carlo

A Python package for running Monte Carlo simulations on the casino games in Schedule 1.

## Features

- **Modular Design**: Separate packages for cards, games, and Monte Carlo simulation framework
- **Multiple Games**: Implementation of Blackjack, Slot Machines, and Real-Time Bidding
- **Statistical Analysis**: Comprehensive statistics from simulation runs
- **Basic Strategy**: Includes optimal basic strategy for blackjack

## Installation (for local use)

```bash
uv sync
uv run main.py
```

## Usage

### Blackjack Simulation

```python
from monte_carlo import MonteCarlo
from games.blackjack import BlackjackGame, BasicStrategy

# Create Monte Carlo simulation
monte_carlo = MonteCarlo()

# Define simulation function
def simulate_blackjack():
    game = BlackjackGame()
    # Simulate a game of blackjack
    # ...
    return {"result": "win", "payout": 2.0}

# Run simulation
results = monte_carlo.run_simulation(simulate_blackjack, num_iterations=10000)
print(results)
```

### Slot Machine Simulation

```python
from games.slots import SlotMachine
from monte_carlo import MonteCarlo

# Create slot machine
slot_machine = SlotMachine()

# Define simulation function
def simulate_slot():
    return slot_machine.simulate_game(bet=1)

# Run simulation 
monte_carlo = MonteCarlo()
results = monte_carlo.run_simulation(simulate_slot, num_iterations=10000)
print(f"House edge: {-results['net_win_mean'] * 100:.2f}%")
```

## Components

### Cards Package

- `Card`: Represents a playing card with suit and value
- `Deck`: Represents a deck of playing cards

### Games Package

- `BlackjackGame`: Implementation of blackjack with standard rules
- `BasicStrategy`: Implements basic strategy for blackjack
- `SlotMachine`: Implementation of a slot machine with configurable reels
- `RTBAuction`: Implementation of a real-time bidding auction

### Monte Carlo Package

- `MonteCarlo`: Framework for running Monte Carlo simulations and gathering statistics

## Requirements

- Python 3.13 or higher

## License

This project is licensed under the MIT License - see the LICENSE file for details.
