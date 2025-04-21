import random
from typing import Dict, Any

from monte_carlo.MonteCarlo import MonteCarlo
from games.blackjack import BlackjackGame, BlackjackAction, BlackjackResult, BasicStrategy, BlackjackHand
from cards.card import Card, Value


def simulate_basic_strategy_hand() -> Dict[str, Any]:
    """
    Simulate a single hand of blackjack played using basic strategy.
    
    Returns:
        Dict[str, Any]: Results of the simulation.
    """
    # Initialize game with 6 decks
    game = BlackjackGame(num_decks=6)
    
    # Deal initial hand
    game.deal_initial_hands(num_hands=1, bet=1.0)
    
    # Get dealer up card
    dealer_up_card = game.get_dealer_up_card()
    if not dealer_up_card:
        return {"result": BlackjackResult.PUSH.value, "net_win": 0.0}
    
    # Play each player hand according to basic strategy
    for i, hand in enumerate(game.player_hands):
        # If we get blackjack, no need to play the hand
        if hand.is_blackjack():
            continue
        
        # Play hand according to basic strategy until we stand or bust
        while not hand.is_bust():
            # Get recommended action from basic strategy
            action = BasicStrategy.get_action(hand, dealer_up_card)
            
            # Apply action
            if action == BlackjackAction.STAND:
                break
            
            game.play_hand(i, action)
            
            # Double down and split actions are terminal
            if action in (BlackjackAction.DOUBLE, BlackjackAction.SPLIT):
                break
    
    # Play dealer hand
    game.play_dealer_hand()
    
    # Get results
    results = game.get_all_results()
    total_bet = sum(hand.bet for hand in game.player_hands)
    total_payout = sum(payout for _, _, payout in results)
    net_win = total_payout - total_bet
    
    # Determine overall result
    if len(results) == 1:
        result = results[0][1].value
    else:
        # Multiple hands, determine overall result based on net win
        if net_win > 0:
            result = BlackjackResult.WIN.value
        elif net_win < 0:
            result = BlackjackResult.LOSE.value
        else:
            result = BlackjackResult.PUSH.value
    
    return {
        "result": result,
        "net_win": net_win,
        "total_bet": total_bet,
        "total_payout": total_payout,
        "num_hands": len(game.player_hands)
    }


def simulate_dealer_bust_probability() -> Dict[str, Any]:
    """
    Simulate to find probability of dealer busting for different up cards.
    
    Returns:
        Dict[str, Any]: Results of the simulation.
    """
    # Define dealer up cards to test
    up_card_values = list(range(2, 11)) + [1]  # 2-10 and Ace
    
    # Initialize results
    results = {}
    
    # For each dealer up card
    for up_value in up_card_values:
        # Create a game with a fixed dealer up card
        game = BlackjackGame()
        
        # Handle Ace and face cards
        if up_value == 1:
            card_value = Value.ACE
            value_name = "Ace"
        elif up_value == 10:
            # Randomly choose 10, J, Q, K
            card_value = random.choice([Value.TEN, Value.JACK, Value.QUEEN, Value.KING])
            value_name = "10"
        else:
            card_value = list(Value)[up_value - 1]  # -1 because ACE is 0
            value_name = str(up_value)
        
        # Set up dealer hand with the specific up card
        up_card = Card(game.deck.cards[0].suit, card_value)
        second_card = game.deck.draw()
        if second_card:
            game.dealer_hand = BlackjackHand([up_card, second_card])
            
            # Play dealer hand
            game.play_dealer_hand()
            
            # Record result
            results[f"dealer_bust_{value_name}"] = 1 if game.dealer_hand.is_bust() else 0
    
    return results


def main():
    """Run various blackjack simulations using Monte Carlo methods."""
    print("Schedule 1 Monte Carlo Simulations - Blackjack")
    print("=============================================")
    
    # Create Monte Carlo simulation
    monte_carlo = MonteCarlo(random_seed=42)
    
    # Simulate basic strategy
    print("\nSimulating Basic Strategy Blackjack...")
    basic_strategy_results = monte_carlo.run_simulation(
        simulate_basic_strategy_hand,
        num_iterations=10000,
        progress_interval=1000
    )
    
    # Print results
    print("\nBasic Strategy Results:")
    print(f"Win Percentage: {basic_strategy_results['result_percentages'].get(BlackjackResult.WIN.value, 0):.2f}%")
    print(f"Blackjack Percentage: {basic_strategy_results['result_percentages'].get(BlackjackResult.BLACKJACK.value, 0):.2f}%")
    print(f"Push Percentage: {basic_strategy_results['result_percentages'].get(BlackjackResult.PUSH.value, 0):.2f}%")
    print(f"Loss Percentage: {basic_strategy_results['result_percentages'].get(BlackjackResult.LOSE.value, 0):.2f}%")
    print(f"Average Net Win per Hand: ${basic_strategy_results['net_win_mean']:.4f}")
    print(f"House Edge: {-basic_strategy_results['net_win_mean'] * 100:.2f}%")
    
    # Simulate dealer bust probabilities
    print("\nSimulating Dealer Bust Probabilities...")
    dealer_bust_results = monte_carlo.run_simulation(
        simulate_dealer_bust_probability, 
        num_iterations=10000,
        progress_interval=1000
    )
    
    # Print dealer bust probabilities
    print("\nDealer Bust Probabilities by Up Card:")
    for up_card in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Ace"]:
        bust_percentage = dealer_bust_results[f"dealer_bust_{up_card}_percentages"].get(1, 0)
        print(f"  {up_card}: {bust_percentage:.2f}%")
    
    print("\nSimulation complete!")


if __name__ == "__main__":
    main()
