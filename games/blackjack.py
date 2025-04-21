from typing import List, Dict, Any, Tuple, Optional
from enum import Enum

from cards.deck import Deck
from cards.card import Card, Value


class BlackjackAction(Enum):
    """Possible actions in a blackjack game."""

    HIT = "hit"
    STAND = "stand"
    DOUBLE = "double"
    SPLIT = "split"


class BlackjackResult(Enum):
    """Possible outcomes of a blackjack game."""

    WIN = "win"
    LOSE = "lose"
    PUSH = "push"
    BLACKJACK = "blackjack"


class BlackjackHand:
    """
    Represents a hand in blackjack.

    Attributes:
        cards (List[Card]): The cards in the hand.
        bet (float): The bet placed on this hand.
        doubled (bool): Whether the hand has been doubled.
        is_split (bool): Whether this hand was created from a split.
    """

    def __init__(self, cards: List[Card], bet: float = 1.0, is_split: bool = False):
        """
        Initialize a new blackjack hand.

        Args:
            cards (List[Card]): Initial cards in the hand.
            bet (float, optional): Initial bet. Defaults to 1.0.
            is_split (bool, optional): Whether this hand was created from a split. Defaults to False.
        """
        self.cards = cards.copy()
        self.bet = bet
        self.doubled = False
        self.is_split = is_split

    def add_card(self, card: Card) -> None:
        """Add a card to the hand."""
        self.cards.append(card)

    def get_values(self) -> List[int]:
        """
        Calculate all possible values of the hand.

        Returns:
            List[int]: List of possible values accounting for Aces being 1 or 11.
        """
        # Count aces
        ace_count = sum(1 for card in self.cards if card.value == Value.ACE)

        # Calculate minimum value (all aces = 1)
        min_value = 0
        for card in self.cards:
            if card.value == Value.ACE:
                min_value += 1
            elif card.value in (Value.JACK, Value.QUEEN, Value.KING):
                min_value += 10
            else:
                min_value += card.value.value

        # Generate all possible values with aces
        values = [min_value]
        for i in range(ace_count):
            new_values = []
            # For each existing value, add 10 (convert one Ace from 1 to 11)
            for val in values:
                if val + 10 <= 21:
                    new_values.append(val + 10)
            values.extend(new_values)

        return sorted(set(values))

    def get_best_value(self) -> int:
        """
        Get the best value of the hand.

        Returns:
            int: The highest value that doesn't bust, or the lowest value if all bust.
        """
        values = self.get_values()
        # Get highest value that doesn't bust
        non_bust_values = [v for v in values if v <= 21]
        if non_bust_values:
            return max(non_bust_values)
        # All values bust, return lowest
        return min(values)

    def is_bust(self) -> bool:
        """Check if the hand is bust (over 21)."""
        return min(self.get_values()) > 21

    def is_blackjack(self) -> bool:
        """Check if the hand is a blackjack (21 with 2 cards)."""
        return len(self.cards) == 2 and 21 in self.get_values()

    def can_split(self) -> bool:
        """Check if the hand can be split."""
        if len(self.cards) != 2:
            return False

        # Check if both cards have the same value
        card1, card2 = self.cards

        # Convert face cards to 10 for comparison
        def card_value(card: Card) -> int:
            if card.value in (Value.JACK, Value.QUEEN, Value.KING):
                return 10
            return card.value.value

        return card_value(card1) == card_value(card2)

    def double_down(self, card: Card) -> None:
        """
        Double the bet and add one more card.

        Args:
            card (Card): The card to add.
        """
        self.bet *= 2
        self.doubled = True
        self.add_card(card)

    def split(
        self, card1: Card, card2: Card
    ) -> Tuple["BlackjackHand", "BlackjackHand"]:
        """
        Split the hand into two new hands.

        Args:
            card1 (Card): Card to add to the first hand.
            card2 (Card): Card to add to the second hand.

        Returns:
            Tuple[BlackjackHand, BlackjackHand]: The two new hands.
        """
        first_hand = BlackjackHand([self.cards[0]], self.bet, is_split=True)
        first_hand.add_card(card1)

        second_hand = BlackjackHand([self.cards[1]], self.bet, is_split=True)
        second_hand.add_card(card2)

        return first_hand, second_hand


class BlackjackGame:
    """
    Represents a game of blackjack.

    This class handles the game logic, including dealing cards, player decisions,
    and determining outcomes.
    """

    def __init__(self, num_decks: int = 6):
        """
        Initialize a new blackjack game.

        Args:
            num_decks (int, optional): Number of decks to use. Defaults to 6.
        """
        self.deck = self._create_shoe(num_decks)
        self.player_hands: List[BlackjackHand] = []
        self.dealer_hand: Optional[BlackjackHand] = None

    def _create_shoe(self, num_decks: int) -> Deck:
        """Create a shoe with multiple decks."""
        shoe = Deck(shuffle=False)
        shoe.cards = []

        # Add multiple decks
        for _ in range(num_decks):
            temp_deck = Deck(shuffle=False)
            shoe.cards.extend(temp_deck.cards)

        # Shuffle the shoe
        shoe.shuffle()
        return shoe

    def deal_initial_hands(self, num_hands: int = 1, bet: float = 1.0) -> None:
        """
        Deal the initial hands to the player and dealer.

        Args:
            num_hands (int, optional): Number of player hands. Defaults to 1.
            bet (float, optional): Bet amount for each hand. Defaults to 1.0.
        """
        # Reset hands
        self.player_hands = []
        self.dealer_hand = None

        # Deal cards
        for _ in range(num_hands):
            player_cards = self.deck.draw_multiple(2)
            self.player_hands.append(BlackjackHand(player_cards, bet))

        dealer_cards = self.deck.draw_multiple(2)
        self.dealer_hand = BlackjackHand(dealer_cards)

    def get_dealer_up_card(self) -> Optional[Card]:
        """Get the dealer's face-up card."""
        if self.dealer_hand and len(self.dealer_hand.cards) > 0:
            return self.dealer_hand.cards[0]
        return None

    def play_hand(
        self, hand_index: int, action: BlackjackAction
    ) -> Optional[BlackjackHand]:
        """
        Play a player hand based on the given action.

        Args:
            hand_index (int): Index of the hand to play.
            action (BlackjackAction): The action to take.

        Returns:
            Optional[BlackjackHand]: The new hand if the action was split, None otherwise.
        """
        if hand_index >= len(self.player_hands):
            return None

        hand = self.player_hands[hand_index]

        # Process the action
        if action == BlackjackAction.HIT:
            card = self.deck.draw()
            if card:
                hand.add_card(card)
            return None

        elif action == BlackjackAction.DOUBLE:
            card = self.deck.draw()
            if card:
                hand.double_down(card)
            return None

        elif action == BlackjackAction.SPLIT and hand.can_split():
            card1 = self.deck.draw()
            card2 = self.deck.draw()
            if card1 and card2:
                hand1, hand2 = hand.split(card1, card2)
                self.player_hands[hand_index] = hand1
                self.player_hands.insert(hand_index + 1, hand2)
                return hand2

        return None

    def play_dealer_hand(self) -> None:
        """Play the dealer's hand according to standard rules."""
        if not self.dealer_hand:
            return

        # Dealer hits on 16 or less, stands on 17 or more
        while self.dealer_hand.get_best_value() < 17:
            card = self.deck.draw()
            if card:
                self.dealer_hand.add_card(card)
            else:
                break

    def get_hand_result(self, hand: BlackjackHand) -> Tuple[BlackjackResult, float]:
        """
        Determine the result of a player hand.

        Args:
            hand (BlackjackHand): The player hand to evaluate.

        Returns:
            Tuple[BlackjackResult, float]: The result and the payout amount.
        """
        if not self.dealer_hand:
            return BlackjackResult.PUSH, 0.0

        # Check for player blackjack
        if hand.is_blackjack():
            if self.dealer_hand.is_blackjack():
                return BlackjackResult.PUSH, hand.bet
            return BlackjackResult.BLACKJACK, hand.bet * 2.5

        # Check if player busts
        if hand.is_bust():
            return BlackjackResult.LOSE, 0.0

        # Check if dealer busts
        if self.dealer_hand.is_bust():
            return BlackjackResult.WIN, hand.bet * 2

        # Compare values
        player_value = hand.get_best_value()
        dealer_value = self.dealer_hand.get_best_value()

        if player_value > dealer_value:
            return BlackjackResult.WIN, hand.bet * 2
        elif player_value < dealer_value:
            return BlackjackResult.LOSE, 0.0
        else:
            return BlackjackResult.PUSH, hand.bet

    def get_all_results(self) -> List[Tuple[BlackjackHand, BlackjackResult, float]]:
        """
        Get results for all player hands.

        Returns:
            List[Tuple[BlackjackHand, BlackjackResult, float]]: List of (hand, result, payout) tuples.
        """
        results = []
        for hand in self.player_hands:
            result, payout = self.get_hand_result(hand)
            results.append((hand, result, payout))
        return results


class BasicStrategy:
    """
    Implements basic blackjack strategy.

    This class provides methods to determine the best action for a hand
    based on standard basic strategy rules.
    """

    @staticmethod
    def get_action(player_hand: BlackjackHand, dealer_up_card: Card) -> BlackjackAction:
        """
        Get the recommended action based on basic strategy.

        Args:
            player_hand (BlackjackHand): The player's hand.
            dealer_up_card (Card): The dealer's up card.

        Returns:
            BlackjackAction: The recommended action.
        """
        # Convert dealer card to value
        dealer_value = dealer_up_card.value.value
        if dealer_up_card.value in (Value.JACK, Value.QUEEN, Value.KING):
            dealer_value = 10

        # Check for pair
        if player_hand.can_split():
            return BasicStrategy._handle_pair(player_hand, dealer_value)

        # Check for soft hand (hand with an Ace counted as 11)
        values = player_hand.get_values()
        if len(values) > 1:  # Multiple values means we have an Ace
            for val in values:
                if val <= 21 and any(
                    card.value == Value.ACE for card in player_hand.cards
                ):
                    return BasicStrategy._handle_soft_hand(val, dealer_value)

        # Hard hand
        return BasicStrategy._handle_hard_hand(
            player_hand.get_best_value(), dealer_value
        )

    @staticmethod
    def _handle_pair(hand: BlackjackHand, dealer_value: int) -> BlackjackAction:
        """Handle strategy for pairs."""
        card_value = hand.cards[0].value.value
        if card_value in (10, 11, 12, 13):  # 10, J, Q, K
            card_value = 10

        # Always split Aces and 8s
        if card_value == 1:  # Ace
            return BlackjackAction.SPLIT
        if card_value == 8:
            return BlackjackAction.SPLIT

        # Never split 10s, 5s
        if card_value == 10:
            return BlackjackAction.STAND
        if card_value == 5:
            return BlackjackAction.HIT

        # Split 2s, 3s, 7s against dealer 2-7
        if card_value in (2, 3, 7) and dealer_value <= 7:
            return BlackjackAction.SPLIT

        # Split 4s against dealer 5-6
        if card_value == 4 and 5 <= dealer_value <= 6:
            return BlackjackAction.SPLIT

        # Split 6s against dealer 2-6
        if card_value == 6 and 2 <= dealer_value <= 6:
            return BlackjackAction.SPLIT

        # Split 9s against dealer 2-6, 8-9
        if card_value == 9 and (2 <= dealer_value <= 6 or 8 <= dealer_value <= 9):
            return BlackjackAction.SPLIT

        # Otherwise, treat as a normal hand
        return BasicStrategy._handle_hard_hand(card_value * 2, dealer_value)

    @staticmethod
    def _handle_soft_hand(value: int, dealer_value: int) -> BlackjackAction:
        """Handle strategy for soft hands."""
        # Always stand on soft 20 (A,9)
        if value >= 20:
            return BlackjackAction.STAND

        # Always hit soft 17 or less
        if value <= 17:
            return BlackjackAction.HIT

        # Soft 18
        if value == 18:
            # Double on dealer 3-6
            if 3 <= dealer_value <= 6:
                return BlackjackAction.DOUBLE
            # Stand against 2, 7, 8
            if dealer_value in (2, 7, 8):
                return BlackjackAction.STAND
            # Hit against 9, 10, A
            return BlackjackAction.HIT

        # Soft 19
        if value == 19:
            # Double on dealer 6
            if dealer_value == 6:
                return BlackjackAction.DOUBLE
            return BlackjackAction.STAND

        return BlackjackAction.STAND  # Default case

    @staticmethod
    def _handle_hard_hand(value: int, dealer_value: int) -> BlackjackAction:
        """Handle strategy for hard hands."""
        # Always stand on 17+
        if value >= 17:
            return BlackjackAction.STAND

        # Always hit on 8 or less
        if value <= 8:
            return BlackjackAction.HIT

        # 9
        if value == 9:
            # Double on dealer 3-6
            if 3 <= dealer_value <= 6:
                return BlackjackAction.DOUBLE
            return BlackjackAction.HIT

        # 10 or 11
        if value in (10, 11):
            # Double on lower dealer cards
            if dealer_value <= 9:
                return BlackjackAction.DOUBLE
            return BlackjackAction.HIT

        # 12
        if value == 12:
            # Stand against dealer 4-6
            if 4 <= dealer_value <= 6:
                return BlackjackAction.STAND
            return BlackjackAction.HIT

        # 13-16
        if 13 <= value <= 16:
            # Stand against dealer 2-6
            if 2 <= dealer_value <= 6:
                return BlackjackAction.STAND
            return BlackjackAction.HIT

        return BlackjackAction.HIT  # Default case
