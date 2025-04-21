import random
from typing import List, Optional

from .card import Card, Suit, Value


class Deck:
    """
    Represents a deck of playing cards.

    Attributes:
        cards (List[Card]): The list of cards in the deck.
    """

    def __init__(self, shuffle: bool = True):
        """
        Initialize a new standard deck of 52 cards.

        Args:
            shuffle (bool, optional): Whether to shuffle the deck. Defaults to True.
        """
        self.cards: List[Card] = []
        self._initialize_deck()

        if shuffle:
            self.shuffle()

    def _initialize_deck(self) -> None:
        """Initialize the deck with all 52 cards."""
        self.cards = []
        for suit in Suit:
            for value in Value:
                self.cards.append(Card(suit, value))

    def shuffle(self) -> None:
        """Shuffle the deck."""
        random.shuffle(self.cards)

    def draw(self) -> Optional[Card]:
        """
        Draw a card from the top of the deck.

        Returns:
            Optional[Card]: The drawn card, or None if the deck is empty.
        """
        if not self.cards:
            return None
        return self.cards.pop()

    def draw_multiple(self, count: int) -> List[Card]:
        """
        Draw multiple cards from the deck.

        Args:
            count (int): The number of cards to draw.

        Returns:
            List[Card]: The list of drawn cards. May be shorter than count if deck runs out.
        """
        result = []
        for _ in range(count):
            card = self.draw()
            if card is None:
                break
            result.append(card)
        return result

    def cards_remaining(self) -> int:
        """
        Get the number of cards remaining in the deck.

        Returns:
            int: The number of cards remaining.
        """
        return len(self.cards)

    def is_empty(self) -> bool:
        """
        Check if the deck is empty.

        Returns:
            bool: True if the deck is empty, False otherwise.
        """
        return len(self.cards) == 0

    def reset(self, shuffle: bool = True) -> None:
        """
        Reset the deck to a full 52-card deck.

        Args:
            shuffle (bool, optional): Whether to shuffle the deck. Defaults to True.
        """
        self._initialize_deck()
        if shuffle:
            self.shuffle()
