from enum import Enum, auto
from dataclasses import dataclass

class Suit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"

class Rank(Enum):
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
    rank: Rank
    suit: Suit
    
    def __str__(self):
        rank_str = {
            11: "J",
            12: "Q",
            13: "K",
            14: "A"
        }.get(self.rank.value, str(self.rank.value))
        return f"{rank_str}{self.suit.value}"

class HandRank(Enum):
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