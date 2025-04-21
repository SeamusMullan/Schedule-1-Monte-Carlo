from enum import Enum
from typing import Optional


class Suit(Enum):
    """Enum representing card suits."""

    HEARTS = "Hearts"
    DIAMONDS = "Diamonds"
    CLUBS = "Clubs"
    SPADES = "Spades"


class Value(Enum):
    """Enum representing card values."""

    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE_HIGH = 14  # For games where Ace is high


class Card:
    """
    Represents a playing card with a suit and value.

    Attributes:
        suit (Suit): The suit of the card.
        value (Value): The value of the card.
    """

    def __init__(self, suit: Suit, value: Value):
        """
        Initialize a new card.

        Args:
            suit (Suit): The suit of the card.
            value (Value): The value of the card.
        """
        self.suit = suit
        self.value = value

    def __str__(self) -> str:
        """Return a string representation of the card."""
        value_names = {
            Value.ACE: "Ace",
            Value.JACK: "Jack",
            Value.QUEEN: "Queen",
            Value.KING: "King",
        }
        value_name = value_names.get(self.value, str(self.value.value))
        return f"{value_name} of {self.suit.value}"

    def __repr__(self) -> str:
        """Return a string representation for debugging."""
        return f"Card({self.suit}, {self.value})"

    def __eq__(self, other: object) -> bool:
        """Check if two cards are equal."""
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.value == other.value
