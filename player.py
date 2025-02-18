from dataclasses import dataclass
from typing import List
from card import Card

@dataclass
class Player:
    name: str
    hand: List[Card]
    chips: int
    is_ai: bool
    folded: bool = False
    current_bet: int = 0
    
    def __str__(self):
        return f"{self.name} ({self.chips} chips)"