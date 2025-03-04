"""
This module provides functions to evaluate Texas Hold'em poker hands.
It determines combinations (e.g. flush, straight, full house) and returns
tuples that include hand type and tie-breaking information.
"""

from collections import Counter
from card import HandRank

def is_straight(ranks):
    """
    Check if the provided list of rank values contains a straight.
    
    Args:
        ranks (List[int]): A list of card rank values.
        
    Returns:
        (bool, int or None): A tuple where the first element is True if a 
        straight exists, and the second element is the highest rank in the 
        straight. Special case for A-2-3-4-5 is handled.
    """
    unique_ranks = sorted(set(ranks))
    if len(unique_ranks) < 5:
        return False, None
    for i in range(len(unique_ranks) - 4):
        window = unique_ranks[i:i+5]
        if window == list(range(window[0], window[0] + 5)):
            return True, window[-1]
    # Handle special A-2-3-4-5 straight.
    if set([14, 2, 3, 4, 5]).issubset(ranks):
        return True, 5
    return False, None

def is_flush(cards):
    """
    Determine if the given cards contain a flush.
    
    Args:
        cards (List[Card]): List of Card objects.
    
    Returns:
        (bool, Suit or None, List[int]): A tuple indicating if flush exists,
        the flush suit, and a sorted list of rank values (high-to-low) forming the flush.
    """
    suit_groups = {}
    for card in cards:
        suit_groups.setdefault(card.suit, []).append(card.rank.value)
    for suit, values in suit_groups.items():
        if len(values) >= 5:
            return True, suit, sorted(values, reverse=True)
    return False, None, []

def evaluate_hand(cards):
    """
    Evaluate the best hand from a list of cards.
    
    Returns a tuple with a structure specific to the hand type for tie-breaking.
    For example:
      - Straight Flush / Royal Flush: (HandRank, highest_card)
      - Four of a Kind: (HandRank, quad_rank, kicker)
      - Full House: (HandRank, triple_rank, pair_rank)
      - Flush: (HandRank, sorted_flush_cards)
      - Straight: (HandRank, highest_card)
      - Three of a Kind: (HandRank, triple_rank, [kicker1, kicker2])
      - Two Pair: (HandRank, (high_pair, low_pair), kicker)
      - One Pair: (HandRank, pair_rank, [kicker1, kicker2, kicker3])
      - High Card: (HandRank, [five_highest_cards])
      
    Args:
        cards (List[Card]): List containing community and hole cards.
    
    Returns:
        tuple: A tuple representing the evaluated hand.
    """
    rank_list = [card.rank.value for card in cards]
    rank_counts = Counter(rank_list)
    counts = list(rank_counts.items())
    counts.sort(key=lambda x: (x[1], x[0]), reverse=True)
    
    # Check for flush in the entire list of cards.
    flush_found, flush_suit, flush_values = is_flush(cards)
    
    # Check for straight using all available card rank values.
    has_straight, highest_straight = is_straight(rank_list)
    
    # Check for straight flush.
    if flush_found:
        flush_cards = [card for card in cards if card.suit == flush_suit]
        flush_ranks = [card.rank.value for card in flush_cards]
        has_sf, highest_sf = is_straight(flush_ranks)
        if has_sf:
            # Royal flush: Straight flush ending with Ace.
            if highest_sf == 14:
                return (HandRank.ROYAL_FLUSH, highest_sf)
            return (HandRank.STRAIGHT_FLUSH, highest_sf)
    
    # Four of a Kind.
    if counts[0][1] == 4:
        quad = counts[0][0]
        kicker = max([r for r in rank_list if r != quad])
        return (HandRank.FOUR_OF_A_KIND, quad, kicker)
    
    # Full House: three-of-a-kind combined with a pair.
    if counts[0][1] == 3:
        triple = counts[0][0]
        pair = None
        for rank, cnt in counts[1:]:
            if cnt >= 2:
                pair = rank
                break
        if pair is not None:
            return (HandRank.FULL_HOUSE, triple, pair)
    
    # Flush.
    if flush_found:
        return (HandRank.FLUSH, flush_values)
    
    # Straight.
    if has_straight:
        return (HandRank.STRAIGHT, highest_straight)
    
    # Three of a Kind.
    if counts[0][1] == 3:
        triple = counts[0][0]
        kickers = sorted([r for r in rank_list if r != triple], reverse=True)[:2]
        return (HandRank.THREE_OF_A_KIND, triple, kickers)
    
    # Two Pair.
    if counts[0][1] == 2 and len(counts) > 1 and counts[1][1] == 2:
        high_pair, low_pair = counts[0][0], counts[1][0]
        kicker = max([r for r in rank_list if r not in (high_pair, low_pair)])
        return (HandRank.TWO_PAIR, (high_pair, low_pair), kicker)
    
    # One Pair.
    if counts[0][1] == 2:
        pair = counts[0][0]
        kickers = sorted([r for r in rank_list if r != pair], reverse=True)[:3]
        return (HandRank.PAIR, pair, kickers)
    
    # High Card.
    high_cards = sorted(rank_list, reverse=True)[:5]
    return (HandRank.HIGH_CARD, high_cards)
