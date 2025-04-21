import random
from typing import Dict, Any

from monte_carlo.MonteCarlo import MonteCarlo
from games.rtb import (
    RideTheBus, 
    ColorChoice, 
    HighLowChoice, 
    InOutChoice,
    Suit
)
from cards.card import Suit, Value, Card


def get_optimal_high_low_choice(card: Card) -> HighLowChoice:
    """
    Determine the optimal high/low choice based on the card value.
    
    Args:
        card: The card to base the decision on
        
    Returns:
        The optimal high/low choice
    """
    # Get numerical value (using actual face card values 11, 12, 13 and Ace as 14)
    value = card.value.value
    if card.value == Value.ACE:
        value = 14  # Ace high
    
    # High cards - almost always go lower
    if value >= 10:
        # 95% chance of guessing LOWER for high cards
        return HighLowChoice.LOWER if random.random() < 0.95 else HighLowChoice.HIGHER
    
    # Low cards - almost always go higher
    elif value <= 5:
        # 95% chance of guessing HIGHER for low cards
        return HighLowChoice.HIGHER if random.random() < 0.95 else HighLowChoice.LOWER
    
    # Middle cards - weighted probability
    else:
        # For 6: 80% HIGHER, 20% LOWER
        # For 7: 65% HIGHER, 35% LOWER
        # For 8: 35% HIGHER, 65% LOWER
        # For 9: 20% HIGHER, 80% LOWER
        higher_prob = max(0, 1.15 - (value / 10))  # Linear function that decreases as value increases
        return HighLowChoice.HIGHER if random.random() < higher_prob else HighLowChoice.LOWER


def get_optimal_in_out_choice(card1: Card, card2: Card) -> InOutChoice:
    """
    Determine the optimal inside/outside choice based on the two cards.
    
    Args:
        card1: The first card
        card2: The second card
        
    Returns:
        The optimal inside/outside choice
    """
    # Get numerical values (using actual face card values)
    value1 = card1.value.value
    if card1.value == Value.ACE:
        value1 = 14  # Ace high
        
    value2 = card2.value.value
    if card2.value == Value.ACE:
        value2 = 14  # Ace high
    
    # Calculate the range between cards
    low = min(value1, value2)
    high = max(value1, value2)
    range_size = high - low - 1  # -1 because endpoints aren't counted
    
    # Calculate outside range (1-low and high-14)
    outside_range = (low - 1) + (14 - high)
    
    # If inside range is larger, choose INSIDE with high probability
    if range_size > outside_range:
        return InOutChoice.INSIDE if random.random() < 0.9 else InOutChoice.OUTSIDE
    # If outside range is larger, choose OUTSIDE with high probability
    elif outside_range > range_size:
        return InOutChoice.OUTSIDE if random.random() < 0.9 else InOutChoice.INSIDE
    # If equal, slightly favor OUTSIDE (more ways to get outside with duplicates)
    else:
        return InOutChoice.OUTSIDE if random.random() < 0.55 else InOutChoice.INSIDE


def simulate_strategy_cashout_after_color() -> Dict[str, Any]:
    """
    Strategy 1: Cash out after the first round (color) if successful.
    
    Returns:
        Dict[str, Any]: Results of the simulation.
    """
    game = RideTheBus(bet=1.0)
    
    # Choose a random color
    color_choice = random.choice(list(ColorChoice))
    
    # Play the first round
    card1, correct1 = game.round_color(color_choice)
    
    # If correct, we cash out immediately with a 2x multiplier
    if correct1:
        return {
            "bet": game.bet,
            "rounds_played": 1,
            "cards": [str(card1)],
            "choices": [color_choice.value],
            "results": [correct1],
            "strategy": "cashout_after_color",
            "winnings": game.bet * 2,  # 2x multiplier for color round
            "net_win": game.bet  # Bet is $1, so net win is $1
        }
    else:
        # If incorrect, we lose our bet
        return {
            "bet": game.bet,
            "rounds_played": 1,
            "cards": [str(card1)],
            "choices": [color_choice.value],
            "results": [correct1],
            "strategy": "cashout_after_color",
            "winnings": 0,
            "net_win": -game.bet
        }


def simulate_strategy_cashout_after_inout() -> Dict[str, Any]:
    """
    Strategy 2: Cash out after the third round (in/out) if all rounds are successful.
    Uses intelligent choices for high/low and in/out based on card values.
    
    Returns:
        Dict[str, Any]: Results of the simulation.
    """
    game = RideTheBus(bet=1.0)
    cards = []
    choices = []
    results = []
    
    # Random choice for color
    color_choice = random.choice(list(ColorChoice))
    
    # Round 1: Color
    card1, correct1 = game.round_color(color_choice)
    cards.append(str(card1))
    choices.append(color_choice.value)
    results.append(correct1)
    
    if not correct1:
        return {
            "bet": game.bet,
            "rounds_played": 1,
            "cards": cards,
            "choices": choices,
            "results": results,
            "strategy": "cashout_after_inout",
            "winnings": 0,
            "net_win": -game.bet
        }
    
    # Round 2: High/Low - Make informed choice based on card1
    high_low_choice = get_optimal_high_low_choice(card1)
    
    card2, correct2 = game.round_high_low(high_low_choice)
    cards.append(str(card2))
    choices.append(high_low_choice.value)
    results.append(correct2)
    
    if not correct2:
        return {
            "bet": game.bet,
            "rounds_played": 2,
            "cards": cards,
            "choices": choices,
            "results": results,
            "strategy": "cashout_after_inout",
            "winnings": 0,
            "net_win": -game.bet
        }
    
    # Round 3: In/Out - Make informed choice based on card1 and card2
    in_out_choice = get_optimal_in_out_choice(card1, card2)
    
    card3, correct3 = game.round_in_out(in_out_choice)
    cards.append(str(card3))
    choices.append(in_out_choice.value)
    results.append(correct3)
    
    if correct3:
        # Cash out after successful in/out round
        # Color (2x) * High/Low (3x) * In/Out (4x) = 24x multiplier
        winnings = game.bet * 24
        return {
            "bet": game.bet,
            "rounds_played": 3,
            "cards": cards,
            "choices": choices,
            "results": results,
            "strategy": "cashout_after_inout",
            "winnings": winnings,
            "net_win": winnings - game.bet
        }
    else:
        return {
            "bet": game.bet,
            "rounds_played": 3,
            "cards": cards,
            "choices": choices,
            "results": results,
            "strategy": "cashout_after_inout",
            "winnings": 0,
            "net_win": -game.bet
        }


def simulate_strategy_always_go_for_suit() -> Dict[str, Any]:
    """
    Strategy 3: Always go for the suit (final round) without cashing out.
    Uses intelligent choices for high/low and in/out based on card values.
    
    Returns:
        Dict[str, Any]: Results of the simulation.
    """
    # Use the full game simulation
    game = RideTheBus(bet=1.0)
    
    # Process one round at a time to make informed decisions
    
    # Round 1: Color (random choice)
    color_choice = random.choice(list(ColorChoice))
    card1, correct1 = game.round_color(color_choice)
    
    if not correct1:
        return {
            "bet": game.bet,
            "rounds_played": 1,
            "cards": [str(card1)],
            "choices": [color_choice.value],
            "results": [correct1],
            "strategy": "always_go_for_suit",
            "winnings": 0,
            "net_win": -game.bet
        }
    
    # Round 2: High/Low (informed choice)
    high_low_choice = get_optimal_high_low_choice(card1)
    card2, correct2 = game.round_high_low(high_low_choice)
    
    if not correct2:
        return {
            "bet": game.bet,
            "rounds_played": 2,
            "cards": [str(card1), str(card2)],
            "choices": [color_choice.value, high_low_choice.value],
            "results": [correct1, correct2],
            "strategy": "always_go_for_suit",
            "winnings": 0,
            "net_win": -game.bet
        }
    
    # Round 3: In/Out (informed choice)
    in_out_choice = get_optimal_in_out_choice(card1, card2)
    card3, correct3 = game.round_in_out(in_out_choice)
    
    if not correct3:
        return {
            "bet": game.bet,
            "rounds_played": 3,
            "cards": [str(card1), str(card2), str(card3)],
            "choices": [color_choice.value, high_low_choice.value, in_out_choice.value],
            "results": [correct1, correct2, correct3],
            "strategy": "always_go_for_suit",
            "winnings": 0,
            "net_win": -game.bet
        }
    
    # Round 4: Suit (random choice - all suits have equal probability)
    suit_choice = random.choice(list(Suit))
    card4, correct4 = game.round_suit(suit_choice)
    
    winnings = game.bet * 24 * 20 if correct4 else 0  # 24x for first 3 rounds * 20x for suit
    
    return {
        "bet": game.bet,
        "rounds_played": 4,
        "cards": [str(card1), str(card2), str(card3), str(card4)],
        "choices": [color_choice.value, high_low_choice.value, in_out_choice.value, suit_choice.value],
        "results": [correct1, correct2, correct3, correct4],
        "strategy": "always_go_for_suit",
        "winnings": winnings,
        "net_win": winnings - game.bet
    }


def main():
    """Run various Ride the Bus simulations using Monte Carlo methods."""
    print("Schedule 1 Monte Carlo Simulations - Ride the Bus")
    print("===============================================")
    
    # Create Monte Carlo simulation
    monte_carlo = MonteCarlo(random_seed=42)
    
    # Simulate Strategy 1: Cash out after color
    print("\nSimulating Strategy 1: Cash out after color round...")
    strategy1_results = monte_carlo.run_simulation(
        simulate_strategy_cashout_after_color,
        num_iterations=10000,
        progress_interval=2000
    )
    
    # Simulate Strategy 2: Cash out after in/out
    print("\nSimulating Strategy 2: Cash out after in/out round (with optimal choices)...")
    strategy2_results = monte_carlo.run_simulation(
        simulate_strategy_cashout_after_inout,
        num_iterations=10000,
        progress_interval=2000
    )
    
    # Simulate Strategy 3: Always go for suit
    print("\nSimulating Strategy 3: Always go for suit round (with optimal choices)...")
    strategy3_results = monte_carlo.run_simulation(
        simulate_strategy_always_go_for_suit,
        num_iterations=10000,
        progress_interval=2000
    )
    
    # Print results summary
    print("\nResults Summary:")
    print("===============")
    
    # Strategy 1 results
    print("\nStrategy 1: Cash out after color round")
    # Fix: Corrected key names for percentages
    print(f"Win Rate: {strategy1_results.get('results_counts', {}).get(True, 0) / 100:.2f}%")
    print(f"Average Net Win: ${strategy1_results['net_win_mean']:.4f}")
    print(f"Expected Value: {strategy1_results['net_win_mean'] * 100:.2f}%")
    
    # Strategy 2 results
    print("\nStrategy 2: Cash out after in/out round (with optimal choices)")
    # Fix: Calculate success rate correctly
    success_rate = sum(
        count for value, count in strategy2_results.get('rounds_played_counts', {}).items() 
        if value >= 3
    ) / 100
    print(f"Win Rate: {strategy2_results.get('results_counts', {}).get(True, 0) / 100:.2f}%")
    print(f"Average Net Win: ${strategy2_results['net_win_mean']:.4f}")
    print(f"Expected Value: {strategy2_results['net_win_mean'] * 100:.2f}%")
    
    # Strategy 3 results
    print("\nStrategy 3: Always go for suit round (with optimal choices)")
    print(f"Win Rate: {strategy3_results.get('results_counts', {}).get(True, 0) / 100:.2f}%")
    print(f"Average Net Win: ${strategy3_results['net_win_mean']:.4f}")
    print(f"Expected Value: {strategy3_results['net_win_mean'] * 100:.2f}%")
    
    # Compare strategies
    print("\nStrategy Comparison:")
    strategies = [
        {"name": "Cash out after color", "ev": strategy1_results['net_win_mean']},
        {"name": "Cash out after in/out (optimal choices)", "ev": strategy2_results['net_win_mean']},
        {"name": "Always go for suit (optimal choices)", "ev": strategy3_results['net_win_mean']}
    ]
    
    # Sort by expected value
    strategies.sort(key=lambda x: x["ev"], reverse=True)
    
    print("\nRanking by Expected Value:")
    for i, strategy in enumerate(strategies, 1):
        print(f"{i}. {strategy['name']}: {strategy['ev'] * 100:.2f}%")
    
    print("\nSimulation complete!")


if __name__ == "__main__":
    main()
