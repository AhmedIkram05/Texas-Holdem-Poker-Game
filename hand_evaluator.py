from collections import Counter
from card import HandRank

def is_straight(ranks):
    """Check if ranks form a straight."""
    ranks = sorted(set(ranks))
    if len(ranks) < 5:
        return False, None
    for i in range(len(ranks) - 4):
        window = ranks[i:i+5]
        if window == list(range(window[0], window[0] + 5)):
            return True, window[-1]
    # Special case: A-2-3-4-5 straight
    if set([14, 2, 3, 4, 5]).issubset(ranks):
        return True, 5
    return False, None

def is_flush(suits):
    """Check if suits form a flush."""
    cnt = Counter(suits)
    for suit, count in cnt.items():
        if count >= 5:
            return True, suit
    return False, None

def evaluate_hand(cards):
    """Evaluate and return a tuple (hand_rank, score) for comparison."""
    ranks = [card.rank.value for card in cards]
    suits = [card.suit for card in cards]
    
    rank_counts = Counter(ranks)
    counts = rank_counts.most_common()

    straight, high_straight = is_straight(ranks)
    flush, flush_suit = is_flush(suits)
    
    # Check for flush straight
    if flush:
        flush_cards = [card.rank.value for card in cards if card.suit == flush_suit]
        st_flush, high_st_flush = is_straight(flush_cards)
        if st_flush:
            # Distinguish royal flush from straight flush
            if high_st_flush == 14:
                return (HandRank.ROYAL_FLUSH, high_st_flush)
            else:
                return (HandRank.STRAIGHT_FLUSH, high_st_flush)
    
    if counts[0][1] == 4:
        return (HandRank.FOUR_OF_A_KIND, counts[0][0])
    if counts[0][1] == 3 and counts[1][1] >= 2:
        return (HandRank.FULL_HOUSE, counts[0][0])
    if flush:
        return (HandRank.FLUSH, max([card.rank.value for card in cards if card.suit == flush_suit]))
    if straight:
        return (HandRank.STRAIGHT, high_straight)
    if counts[0][1] == 3:
        return (HandRank.THREE_OF_A_KIND, counts[0][0])
    if counts[0][1] == 2 and counts[1][1] == 2:
        return (HandRank.TWO_PAIR, max(counts[0][0], counts[1][0]))
    if counts[0][1] == 2:
        return (HandRank.PAIR, counts[0][0])
    return (HandRank.HIGH_CARD, max(ranks))
