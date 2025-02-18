"""
This module defines the Player class which holds player-related information,
including name, hand, chip count, and status flags.
"""

from dataclasses import dataclass
from typing import List
from card import Card

@dataclass
class Player:
    """
    Represents a player in the poker game.
    
    Attributes:
        name (str): Player's name.
        hand (List[Card]): List of cards in player's hand.
        chips (int): Current chip count.
        is_ai (bool): Flag indicating if player is an AI.
        folded (bool): Flag indicating if player has folded.
        current_bet (int): Amount currently bet in the round.
    """
    name: str
    hand: List[Card]
    chips: int
    is_ai: bool
    folded: bool = False
    current_bet: int = 0
    
    def __str__(self):
        return f"{self.name} ({self.chips} chips)"