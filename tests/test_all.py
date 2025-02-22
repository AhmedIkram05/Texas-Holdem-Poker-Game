import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

import unittest
import random

from game import Game
from card import Card, Suit, Rank, HandRank
from hand_evaluator import evaluate_hand
from ai import make_betting_decision

# ----------------- Test Deck Management -----------------
class TestDeckManagement(unittest.TestCase):
    def test_deck_creation(self):
        game = Game()
        game.create_deck()
        self.assertEqual(len(game.deck), 52, "Deck should have 52 cards")
        cards_set = {(card.rank, card.suit) for card in game.deck}
        self.assertEqual(len(cards_set), 52, "All cards must be unique")

# ----------------- Test Hand Evaluator -----------------
class TestHandEvaluator(unittest.TestCase):
    def test_royal_flush(self):
        # Cards: 10, J, Q, K, A of the same suit + extras.
        cards = [
            Card(Rank.TEN, Suit.HEARTS), Card(Rank.JACK, Suit.HEARTS),
            Card(Rank.QUEEN, Suit.HEARTS), Card(Rank.KING, Suit.HEARTS),
            Card(Rank.ACE, Suit.HEARTS),
            Card(Rank.TWO, Suit.CLUBS), Card(Rank.THREE, Suit.DIAMONDS)
        ]
        result = evaluate_hand(cards)
        self.assertEqual(result[0], HandRank.ROYAL_FLUSH)
    
    def test_straight_flush(self):
        # 5-card straight flush (not royal)
        cards = [
            Card(Rank.NINE, Suit.SPADES),
            Card(Rank.EIGHT, Suit.SPADES),
            Card(Rank.SEVEN, Suit.SPADES),
            Card(Rank.SIX, Suit.SPADES),
            Card(Rank.FIVE, Suit.SPADES),
            Card(Rank.TWO, Suit.HEARTS),
            Card(Rank.THREE, Suit.CLUBS)
        ]
        result = evaluate_hand(cards)
        self.assertEqual(result[0], HandRank.STRAIGHT_FLUSH)
    
    def test_four_of_a_kind(self):
        cards = [
            Card(Rank.KING, Suit.HEARTS),
            Card(Rank.KING, Suit.SPADES),
            Card(Rank.KING, Suit.DIAMONDS),
            Card(Rank.KING, Suit.CLUBS),
            Card(Rank.THREE, Suit.HEARTS),
            Card(Rank.FIVE, Suit.DIAMONDS),
            Card(Rank.SEVEN, Suit.CLUBS)
        ]
        result = evaluate_hand(cards)
        self.assertEqual(result[0], HandRank.FOUR_OF_A_KIND)

    def test_full_house(self):
        cards = [
            Card(Rank.QUEEN, Suit.HEARTS),
            Card(Rank.QUEEN, Suit.SPADES),
            Card(Rank.QUEEN, Suit.DIAMONDS),
            Card(Rank.TEN, Suit.CLUBS),
            Card(Rank.TEN, Suit.HEARTS),
            Card(Rank.TWO, Suit.DIAMONDS),
            Card(Rank.FOUR, Suit.CLUBS)
        ]
        result = evaluate_hand(cards)
        self.assertEqual(result[0], HandRank.FULL_HOUSE)

    def test_flush(self):
        cards = [
            Card(Rank.TWO, Suit.CLUBS),
            Card(Rank.FIVE, Suit.CLUBS),
            Card(Rank.SEVEN, Suit.CLUBS),
            Card(Rank.JACK, Suit.CLUBS),
            Card(Rank.ACE, Suit.CLUBS),
            Card(Rank.THREE, Suit.HEARTS),
            Card(Rank.FOUR, Suit.DIAMONDS)
        ]
        result = evaluate_hand(cards)
        self.assertEqual(result[0], HandRank.FLUSH)

    def test_straight(self):
        cards = [
            Card(Rank.THREE, Suit.HEARTS),
            Card(Rank.FOUR, Suit.DIAMONDS),
            Card(Rank.FIVE, Suit.SPADES),
            Card(Rank.SIX, Suit.CLUBS),
            Card(Rank.SEVEN, Suit.HEARTS),
            Card(Rank.TWO, Suit.CLUBS),
            Card(Rank.NINE, Suit.DIAMONDS)
        ]
        result = evaluate_hand(cards)
        self.assertEqual(result[0], HandRank.STRAIGHT)

    def test_three_of_a_kind(self):
        cards = [
            Card(Rank.ACE, Suit.HEARTS),
            Card(Rank.ACE, Suit.SPADES),
            Card(Rank.ACE, Suit.DIAMONDS),
            Card(Rank.FOUR, Suit.CLUBS),
            Card(Rank.SEVEN, Suit.HEARTS),
            Card(Rank.THREE, Suit.CLUBS),
            Card(Rank.NINE, Suit.DIAMONDS)
        ]
        result = evaluate_hand(cards)
        self.assertEqual(result[0], HandRank.THREE_OF_A_KIND)

    def test_two_pair(self):
        cards = [
            Card(Rank.ACE, Suit.HEARTS),
            Card(Rank.ACE, Suit.SPADES),
            Card(Rank.KING, Suit.DIAMONDS),
            Card(Rank.KING, Suit.CLUBS),
            Card(Rank.NINE, Suit.HEARTS),
            Card(Rank.TWO, Suit.CLUBS),
            Card(Rank.THREE, Suit.DIAMONDS)
        ]
        result = evaluate_hand(cards)
        self.assertEqual(result[0], HandRank.TWO_PAIR)

    def test_pair(self):
        cards = [
            Card(Rank.JACK, Suit.HEARTS),
            Card(Rank.JACK, Suit.SPADES),
            Card(Rank.ACE, Suit.DIAMONDS),
            Card(Rank.SEVEN, Suit.CLUBS),
            Card(Rank.THREE, Suit.HEARTS),
            Card(Rank.FOUR, Suit.HEARTS),
            Card(Rank.TWO, Suit.DIAMONDS)
        ]
        result = evaluate_hand(cards)
        self.assertEqual(result[0], HandRank.PAIR)

    def test_high_card(self):
        cards = [
            Card(Rank.TWO, Suit.HEARTS),
            Card(Rank.FIVE, Suit.DIAMONDS),
            Card(Rank.SEVEN, Suit.SPADES),
            Card(Rank.NINE, Suit.CLUBS),
            Card(Rank.JACK, Suit.HEARTS),
            Card(Rank.THREE, Suit.HEARTS),
            Card(Rank.FOUR, Suit.DIAMONDS)
        ]
        result = evaluate_hand(cards)
        self.assertEqual(result[0], HandRank.HIGH_CARD)

# ----------------- Test Betting Logic -----------------
class TestBettingLogic(unittest.TestCase):
    def test_place_bet(self):
        game = Game()
        player = game.players[0]
        player.chips = 100
        player.current_bet = 0
        initial_pot = game.pot
        game.current_bet = 10
        game.place_bet(player, 10)
        self.assertEqual(player.chips, 90)
        self.assertEqual(player.current_bet, 10)
        self.assertEqual(game.pot, initial_pot + 10)

    def test_multiple_bets(self):
        game = Game()
        # Simulate two bets on the same round.
        player = game.players[0]
        player.chips = 150
        game.current_bet = 0
        game.place_bet(player, 20)
        self.assertEqual(player.chips, 130)
        self.assertEqual(game.current_bet, 20)
        # Second bet raising the current bet.
        game.place_bet(player, 10)
        self.assertEqual(player.current_bet, 30)
        self.assertEqual(game.pot, 20 + 10)

# ----------------- Test Game State Machine -----------------
class TestStateMachine(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        # Override human decision to auto-call to simplify round flow.
        self.game.human_betting_decision = lambda p: self.game.place_bet(p, self.game.current_bet - p.current_bet)
        # Force both AI and human to have a fixed behavior.
        for p in self.game.players:
            p.chips = 1000

    def test_play_round_transitions(self):
        # Monkey-patch betting_round to automatically match bet.
        original_betting = self.game.betting_round
        self.game.betting_round = lambda: None  # skip actual bets for testing state transitions

        # Force active players count for transition.
        for p in self.game.players:
            p.folded = False
            p.current_bet = 0

        self.game.community_cards = []
        # Run play_round and check that dealer index advanced.
        prev_dealer = self.game.dealer_idx
        self.game.play_round()
        self.assertEqual(self.game.dealer_idx, (prev_dealer + 1) % len(self.game.players))
        # Restore betting_round if needed.
        self.game.betting_round = original_betting

# ----------------- Test AI Decision Logic -----------------
class TestAIDecision(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.player = self.game.players[1]  # AI player.
        self.player.chips = 1000
        self.game.current_bet = 50
        # Provide a strong hand
        self.player.hand = [Card(Rank.ACE, Suit.SPADES), Card(Rank.ACE, Suit.HEARTS)]

    def test_ai_aggressive(self):
        # Monkey-patch random.random to simulate strong confidence.
        orig_random = random.random
        random.random = lambda: 0.1  # Very low value triggers raise condition.
        make_betting_decision(self.game, self.player)
        self.assertGreater(self.player.current_bet, 50)
        random.random = orig_random

    def test_ai_fold(self):
        # Force a scenario where AI should fold.
        self.player.hand = [Card(Rank.TWO, Suit.SPADES), Card(Rank.THREE, Suit.HEARTS)]
        orig_random = random.random
        random.random = lambda: 0.9  # High value may trigger fold under high call risk.
        prev_chips = self.player.chips
        make_betting_decision(self.game, self.player)
        # If folded, chips remain unchanged.
        if self.player.folded:
            self.assertEqual(self.player.chips, prev_chips)
        random.random = orig_random

if __name__ == '__main__':
    unittest.main()
