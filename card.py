"""
This module defines the Card class and associated enums for suits, ranks, and hand rankings.
"""

from enum import Enum, auto
from dataclasses import dataclass

class Suit(Enum):
    """Enumeration for the four suits in a standard deck."""
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"

class Rank(Enum):
    """Enumeration for card ranks with associated integer values."""
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
    ACE = 14

@dataclass
class Card:
    """
    Represents a playing card.
    
    Attributes:
        rank (Rank): The rank of the card.
        suit (Suit): The suit of the card.
    """
    rank: Rank
    suit: Suit
    
    def __str__(self):
        """
        Return string representation such as "A♠" or "10♥".
        """
        rank_str = {
            11: "J",
            12: "Q",
            13: "K",
            14: "A"
        }.get(self.rank.value, str(self.rank.value))
        return f"{rank_str}{self.suit.value}"

class HandRank(Enum):
    """
    Enumerates hand rankings in increasing order of strength.
    auto() is used so that values are assigned automatically.
    """
    HIGH_CARD = auto()
    PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    STRAIGHT = auto()
    FLUSH = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    STRAIGHT_FLUSH = auto()
    ROYAL_FLUSH = auto()