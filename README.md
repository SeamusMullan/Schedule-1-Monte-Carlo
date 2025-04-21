# Schedule-1-Monte-Carlo

A Python package for running Monte Carlo simulations on the casino games in Schedule 1.

## Features

- **Modular Design**: Separate packages for cards, games, and Monte Carlo simulation framework
- **Multiple Games**: Implementation of Blackjack, Slot Machines, and Ride the Bus
- **Statistical Analysis**: Comprehensive statistics from simulation runs
- **Basic Strategy**: Includes optimal basic strategy for blackjack

## Installation (for local use)

```bash
uv sync
uv run main.py
```

The usage guidelines will show up and you can choose how to run it from there.

## Usage

### Monte Carlo Simulation Framework

```python
from monte_carlo import MonteCarlo

# Create a simulation with optional random seed
monte_carlo = MonteCarlo(random_seed=42)

# Define simple simulation function
def simulate_coin_flip():
    return {"result": "heads" if random.random() > 0.5 else "tails"}

# Run 10,000 simulations
results = monte_carlo.run_simulation(simulate_coin_flip, num_iterations=10000)
print(f"Heads percentage: {results['result_percentages']['heads']}%")
```

### Blackjack

```python
from games.blackjack import BlackjackGame, BasicStrategy

# Create a game with 6 decks
game = BlackjackGame(num_decks=6)

# Deal initial hand
game.deal_initial_hands(bet=1.0)

# Get dealer up card and recommended action
dealer_up_card = game.get_dealer_up_card()
action = BasicStrategy.get_action(game.player_hands[0], dealer_up_card)
print(f"Recommended action: {action.value}")
```

### Slot Machine

```python
from games.slots import SlotMachine

# Create a slot machine with default settings
slot_machine = SlotMachine() 

# Simulate a single spin with $1 bet
result = slot_machine.simulate_game(bet=1)
print(f"Result: {result['result']}, Payout: ${result['payout']}")
```

### Ride the Bus

```python
from games.rtb import RideTheBus, ColorChoice

# Create a new game with $1 bet
game = RideTheBus(bet=1.0)

# Play the first round (guess color)
card, correct = game.round_color(ColorChoice.RED)
print(f"Card: {card}, Correct: {correct}")

# Continue if correct
if correct:
    print(f"Current winnings: ${game.current_winnings}")
```

## Components

### Cards Package

- `Card`: Represents a playing card with suit and value
- `Deck`: Represents a deck of playing cards

### Games Package

- `BlackjackGame`: Implementation of blackjack with standard rules
- `BasicStrategy`: Implements basic strategy for blackjack
- `SlotMachine`: Implementation of a slot machine with configurable reels and paytable
- `RideTheBus`: Implementation of the Ride the Bus card game with multiple rounds

### Monte Carlo Package

- `MonteCarlo`: Framework for running Monte Carlo simulations and gathering statistics

## Running Simulations

Use the main.py script to run different simulations:

```bash
# Run blackjack simulations
uv run main.py blackjack

# Run Ride the Bus simulations
uv run main.py rtb

# Run all simulations
uv run main.py all
```

## Requirements

- Python 3.13 or higher

## License

This project is licensed under the MIT License - see the LICENSE file for details.
