import random
from typing import Dict, Any, List, Tuple, Optional
from enum import Enum

from cards.deck import Deck
from cards.card import Card, Suit, Value


class ColorChoice(Enum):
    """Player's choice for the color round."""
    RED = "red"
    BLACK = "black"


class HighLowChoice(Enum):
    """Player's choice for the high/low round."""
    HIGHER = "higher"
    LOWER = "lower"


class InOutChoice(Enum):
    """Player's choice for the inside/outside round."""
    INSIDE = "inside"
    OUTSIDE = "outside"


class RideTheBus:
    """
    Represents a game of Ride the Bus.
    
    Attributes:
        deck (Deck): The deck of cards.
        drawn_cards (List[Card]): Cards drawn during the game.
        bet (float): Player's bet amount.
        current_winnings (float): Player's current winnings.
    """
    
    # Multipliers for each round
    MULTIPLIERS = {
        "color": 2,
        "high_low": 3,
        "in_out": 4,
        "suit": 20
    }
    
    def __init__(self, bet: float = 1.0):
        """
        Initialize a new Ride the Bus game.
        
        Args:
            bet (float, optional): Initial bet amount. Defaults to 1.0.
        """
        self.deck = Deck()
        self.drawn_cards: List[Card] = []
        self.bet = bet
        self.current_winnings = 0.0
    
    def _is_red(self, card: Card) -> bool:
        """Check if a card is red."""
        return card.suit in [Suit.HEARTS, Suit.DIAMONDS]
    
    def _card_value(self, card: Card) -> int:
        """Get the numerical value of a card."""
        if card.value == Value.ACE:
            return 14  # Treat Ace as high
        return card.value.value
    
    def round_color(self, choice: ColorChoice) -> Tuple[Card, bool]:
        """
        Play the color round.
        
        Args:
            choice (ColorChoice): Player's color choice.
            
        Returns:
            Tuple[Card, bool]: The drawn card and whether the guess was correct.
        """
        card = self.deck.draw()
        if not card:
            self.deck = Deck()
            card = self.deck.draw()
        
        self.drawn_cards.append(card)
        
        is_red = self._is_red(card)
        is_correct = (choice == ColorChoice.RED and is_red) or (choice == ColorChoice.BLACK and not is_red)
        
        if is_correct:
            self.current_winnings = self.bet * self.MULTIPLIERS["color"]
        else:
            self.current_winnings = 0
            
        return card, is_correct
    
    def round_high_low(self, choice: HighLowChoice) -> Tuple[Card, bool]:
        """
        Play the higher/lower round.
        
        Args:
            choice (HighLowChoice): Player's higher/lower choice.
            
        Returns:
            Tuple[Card, bool]: The drawn card and whether the guess was correct.
        """
        if not self.drawn_cards:
            return None, False
        
        prev_card = self.drawn_cards[-1]
        card = self.deck.draw()
        if not card:
            self.deck = Deck()
            card = self.deck.draw()
            
        self.drawn_cards.append(card)
        
        prev_value = self._card_value(prev_card)
        current_value = self._card_value(card)
        
        is_higher = current_value >= prev_value
        is_correct = (choice == HighLowChoice.HIGHER and is_higher) or (choice == HighLowChoice.LOWER and not is_higher)
        
        if is_correct:
            self.current_winnings *= self.MULTIPLIERS["high_low"]
        else:
            self.current_winnings = 0
            
        return card, is_correct
    
    def round_in_out(self, choice: InOutChoice) -> Tuple[Card, bool]:
        """
        Play the inside/outside round.
        
        Args:
            choice (InOutChoice): Player's inside/outside choice.
            
        Returns:
            Tuple[Card, bool]: The drawn card and whether the guess was correct.
        """
        if len(self.drawn_cards) < 2:
            return None, False
        
        card1 = self.drawn_cards[-2]
        card2 = self.drawn_cards[-1]
        
        card = self.deck.draw()
        if not card:
            self.deck = Deck()
            card = self.deck.draw()
            
        self.drawn_cards.append(card)
        
        value1 = self._card_value(card1)
        value2 = self._card_value(card2)
        current_value = self._card_value(card)
        
        # Sort the boundary values
        low_bound = min(value1, value2)
        high_bound = max(value1, value2)
        
        is_inside = low_bound <= current_value <= high_bound
        is_correct = (choice == InOutChoice.INSIDE and is_inside) or (choice == InOutChoice.OUTSIDE and not is_inside)
        
        if is_correct:
            self.current_winnings *= self.MULTIPLIERS["in_out"]
        else:
            self.current_winnings = 0
            
        return card, is_correct
    
    def round_suit(self, suit_choice: Suit) -> Tuple[Card, bool]:
        """
        Play the suit round.
        
        Args:
            suit_choice (Suit): Player's suit choice.
            
        Returns:
            Tuple[Card, bool]: The drawn card and whether the guess was correct.
        """
        card = self.deck.draw()
        if not card:
            self.deck = Deck()
            card = self.deck.draw()
            
        self.drawn_cards.append(card)
        
        is_correct = card.suit == suit_choice
        
        if is_correct:
            self.current_winnings *= self.MULTIPLIERS["suit"]
        else:
            self.current_winnings = 0
            
        return card, is_correct
    
    def simulate_game(self, 
                     color_choice: ColorChoice = None, 
                     high_low_choice: HighLowChoice = None,
                     in_out_choice: InOutChoice = None,
                     suit_choice: Suit = None) -> Dict[str, Any]:
        """
        Simulate a complete game of Ride the Bus.
        
        Args:
            color_choice (ColorChoice, optional): Player's color choice. 
                Defaults to random.
            high_low_choice (HighLowChoice, optional): Player's high/low choice. 
                Defaults to random.
            in_out_choice (InOutChoice, optional): Player's inside/outside choice. 
                Defaults to random.
            suit_choice (Suit, optional): Player's suit choice. 
                Defaults to random.
            
        Returns:
            Dict[str, Any]: Results of the simulation.
        """
        self.drawn_cards = []
        self.current_winnings = 0.0
        
        # Use random choices if not provided
        if color_choice is None:
            color_choice = random.choice(list(ColorChoice))
        if high_low_choice is None:
            high_low_choice = random.choice(list(HighLowChoice))
        if in_out_choice is None:
            in_out_choice = random.choice(list(InOutChoice))
        if suit_choice is None:
            suit_choice = random.choice(list(Suit))
        
        # Round 1: Color
        card1, correct1 = self.round_color(color_choice)
        
        # If first round fails, the game is over
        if not correct1:
            return {
                "bet": self.bet,
                "cards": [str(card1)],
                "winnings": 0.0,
                "choices": [color_choice.value],
                "results": [correct1],
                "rounds_completed": 1,
                "net_win": -self.bet
            }
        
        # Round 2: High/Low
        card2, correct2 = self.round_high_low(high_low_choice)
        
        # If second round fails, the game is over
        if not correct2:
            return {
                "bet": self.bet,
                "cards": [str(card1), str(card2)],
                "winnings": 0.0,
                "choices": [color_choice.value, high_low_choice.value],
                "results": [correct1, correct2],
                "rounds_completed": 2,
                "net_win": -self.bet
            }
        
        # Round 3: Inside/Outside
        card3, correct3 = self.round_in_out(in_out_choice)
        
        # If third round fails, the game is over
        if not correct3:
            return {
                "bet": self.bet,
                "cards": [str(card1), str(card2), str(card3)],
                "winnings": 0.0,
                "choices": [color_choice.value, high_low_choice.value, in_out_choice.value],
                "results": [correct1, correct2, correct3],
                "rounds_completed": 3,
                "net_win": -self.bet
            }
        
        # Round 4: Suit
        card4, correct4 = self.round_suit(suit_choice)
        
        # Game complete
        return {
            "bet": self.bet,
            "cards": [str(card1), str(card2), str(card3), str(card4)],
            "winnings": self.current_winnings if correct4 else 0.0,
            "choices": [color_choice.value, high_low_choice.value, in_out_choice.value, suit_choice.value],
            "results": [correct1, correct2, correct3, correct4],
            "rounds_completed": 4,
            "net_win": self.current_winnings - self.bet if correct4 else -self.bet
        }


def simulate_rtb_game() -> Dict[str, Any]:
    """
    Simulate a game of Ride the Bus with random choices.
    
    Returns:
        Dict[str, Any]: Results of the RTB simulation.
    """
    game = RideTheBus(bet=1.0)
    return game.simulate_game()
