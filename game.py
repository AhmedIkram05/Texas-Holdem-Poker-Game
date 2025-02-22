"""
This module implements the main game logic for Texas Hold'em.
It manages deck creation, dealing cards, betting rounds, and determining winners.
"""

import random
from typing import List
from card import Card, Suit, Rank, HandRank
from player import Player
from ui import GameUI  # New import
from hand_evaluator import evaluate_hand  # New import
from ai import make_betting_decision  # New import

class Game:
    # Define game states.
    PRE_FLOP = "PRE_FLOP"
    FLOP = "FLOP"
    TURN = "TURN"
    RIVER = "RIVER"
    SHOWDOWN = "SHOWDOWN"
    
    def __init__(self, player_name="Player", starting_chips=1000):
        """
        Initialize game state including deck, players, blinds, and pot.
        
        Args:
            player_name (str): Name of the human player.
            starting_chips (int): Initial chip count for each player.
        """
        self.deck = []  # List of Card objects.
        self.community_cards = []  # Cards shared among players.
        self.players = [
            Player(player_name, [], starting_chips, False),
            Player("AI 1", [], starting_chips, True),
            Player("AI 2", [], starting_chips, True),
            Player("AI 3", [], starting_chips, True)
        ]
        self.pot = 0
        self.current_bet = 0
        self.small_blind = 5
        self.big_blind = 10
        self.dealer_idx = 0
        
    def create_deck(self):
        """Generate a standard deck and shuffle it."""
        self.deck = []
        for suit in Suit:
            for rank in Rank:
                self.deck.append(Card(rank, suit))
        random.shuffle(self.deck)
    
    def deal_cards(self):
        """
        Deal two cards to each active player and clear community cards.
        """
        for player in self.players:
            player.hand = []  # Reset hands.
        self.community_cards = []
        for _ in range(2):
            for player in self.players:
                if not player.folded:
                    player.hand.append(self.deck.pop())
    
    def deal_flop(self):
        """
        Deal the flop (three community cards) after discarding one card.
        """
        self.deck.pop()  # Burn card.
        for _ in range(3):
            self.community_cards.append(self.deck.pop())
            
    def deal_turn_or_river(self):
        """
        Deal one more community card (turn or river) after discarding one card.
        """
        self.deck.pop()  # Burn card.
        self.community_cards.append(self.deck.pop())
    
    def get_active_players(self):
        """Return a list of players who have not folded."""
        return [p for p in self.players if not p.folded]
    
    def betting_round(self):
        """
        Execute a betting round until all active players match the current bet.
        """
        # Only proceed if more than one active player.
        if len(self.get_active_players()) <= 1:
            return
        
        while True:
            for player in self.get_active_players():
                if not player.folded:
                    if player.is_ai:
                        make_betting_decision(self, player)  # Use AI helper
                    else:
                        self.human_betting_decision(player)
            # After a full cycle, check if bets are equal.
            active_players = self.get_active_players()
            if all(p.current_bet == self.current_bet for p in active_players):
                break
    
    def human_betting_decision(self, player):
        """
        Prompt the human player for their betting choice using the UI.
        
        Args:
            player (Player): The human player.
        """
        to_call = self.current_bet - player.current_bet
        info = f"Your hand: {' '.join(str(card) for card in player.hand)}\n"
        if self.community_cards:
            info += f"Community cards: {' '.join(str(card) for card in self.community_cards)}\n"
        info += f"Pot: {self.pot} | Your chips: {player.chips}"
        if to_call > 0:
            info += f" | To call: {to_call}"
        
        if to_call == 0:
            action = self.ui.prompt_action(info+"\nChoose action:", ["check", "bet", "fold"])
            if action == "check":
                return
            elif action == "bet":
                amount = self.ui.prompt_amount("Bet amount:", 1, player.chips)
                if amount:
                    self.place_bet(player, amount)
                    return
                else:
                    player.folded = True
                    return
            elif action == "fold":
                player.folded = True
                return
        else:
            action = self.ui.prompt_action(info+"\nChoose action:", ["call", "raise", "fold"])
            if action == "call":
                self.place_bet(player, to_call)
                return
            elif action == "raise":
                raise_amount = self.ui.prompt_amount("Raise by:", 1, player.chips - to_call)
                if raise_amount and (to_call + raise_amount) <= player.chips:
                    self.place_bet(player, to_call + raise_amount)
                    return
                else:
                    player.folded = True
                    return
            elif action == "fold":
                player.folded = True
                return
    
    def place_bet(self, player, amount):
        """
        Process a bet for a player including adjusting chip counts and updating pot.
        
        Args:
            player (Player): The player placing a bet.
            amount (int): Amount to bet.
        """
        amount = min(amount, player.chips)
        player.chips -= amount
        player.current_bet += amount
        self.pot += amount
        if player.current_bet > self.current_bet:
            self.current_bet = player.current_bet
        if amount > 0:
            if player.current_bet == self.current_bet:
                print(f"{player.name} calls {amount}.")
            else:
                print(f"{player.name} raises to {player.current_bet}.")
    
    def compare_hands(self, hand1, hand2):
        """
        Compare two hand evaluation tuples element-by-element.
        Returns:
            1 if hand1 is stronger, -1 if hand2 is stronger, 0 if tied.
        """
        max_len = max(len(hand1), len(hand2))
        h1 = list(hand1) + [0] * (max_len - len(hand1))
        h2 = list(hand2) + [0] * (max_len - len(hand2))
        for a, b in zip(h1, h2):
            # If elements are HandRank, compare their .value.
            if hasattr(a, 'value') and hasattr(b, 'value'):
                if a.value > b.value:
                    return 1
                elif a.value < b.value:
                    return -1
            else:
                if a > b:
                    return 1
                elif a < b:
                    return -1
        return 0

    def find_winners(self):
        """
        Evaluate hands of active players to determine the winner(s).
        
        Returns:
            List[Player]: The winning player(s).
        """
        active_players = self.get_active_players()
        if len(active_players) == 1:
            return active_players
        
        board_eval = evaluate_hand(self.community_cards)
        player_hands = []
        for player in active_players:
            hand_eval = evaluate_hand(player.hand + self.community_cards)
            # If a player hasn't improved on the board, use the board's evaluation.
            if self.compare_hands(hand_eval, board_eval) < 0:
                hand_eval = board_eval
            player_hands.append((player, hand_eval))
        
        # Determine best hand using component-wise comparison.
        best_hand = player_hands[0][1]
        for _, hand_eval in player_hands[1:]:
            if self.compare_hands(hand_eval, best_hand) == 1:
                best_hand = hand_eval
        
        # Collect all players whose hand compares as tied with best_hand.
        winners = [p for p, hand_eval in player_hands if self.compare_hands(hand_eval, best_hand) == 0]
        return winners

    def show_all_hands(self):
        """
        Display all active players' hands along with their evaluated hand rank.
        """
        print("\nFinal hands:")
        for player in self.get_active_players():
            hand_str = ' '.join(str(card) for card in player.hand)
            hand_rank = evaluate_hand(player.hand + self.community_cards)
            print(f"{player.name}: {hand_str} - {hand_rank[0].name}")
    
    def distribute_pot(self, winners):
        """
        Distribute the pot among winners, handling any remainders.
        
        Args:
            winners (List[Player]): List of winning players.
        """
        split_amount = self.pot // len(winners)
        remainder = self.pot % len(winners)
        for player in winners:
            player.chips += split_amount
            print(f"{player.name} wins {split_amount} chips!")
        if remainder > 0:
            winners[0].chips += remainder
    
    def post_blinds(self):
        """
        Post the small and big blinds for the round.
        """
        small_blind_idx = (self.dealer_idx + 1) % len(self.players)
        big_blind_idx = (self.dealer_idx + 2) % len(self.players)
        self.place_bet(self.players[small_blind_idx], self.small_blind)
        self.place_bet(self.players[big_blind_idx], self.big_blind)
        self.current_bet = self.big_blind
    
    def reset_round(self):
        """
        Reset player bets and state for a new round and update the dealer index.
        """
        for player in self.players:
            player.current_bet = 0
            player.folded = False
        self.current_bet = 0
        self.pot = 0
        self.dealer_idx = (self.dealer_idx + 1) % len(self.players)
    
    def play_round(self):
        """
        Execute a full round using a state machine for phases:
        PRE_FLOP, FLOP, TURN, RIVER, and SHOWDOWN.
        """
        print("\n" + "=" * 50)
        print(f"ROUND START - Dealer: {self.players[self.dealer_idx].name}")
        print("=" * 50)
        self.create_deck()
        self.reset_round()
        self.post_blinds()
        self.deal_cards()
        
        # Update UI: display player's hand and AI hands after dealing hole cards.
        human = next((p for p in self.players if not p.is_ai), None)
        if human:
            self.ui.display_player_hand(human.hand)
        ai_hands = [(p.name, p.hand, p.folded) for p in self.players if p.is_ai]
        self.ui.display_ai_hands(ai_hands)
        
        state = self.PRE_FLOP
        
        while state != "END":
            if state == self.PRE_FLOP:
                print("\nPre-flop betting:")
                self.betting_round()
                state = self.FLOP if len(self.get_active_players()) > 1 else self.SHOWDOWN
            
            elif state == self.FLOP:
                self.deal_flop()
                print(f"\nFlop: {' '.join(str(card) for card in self.community_cards)}")
                # Update community cards display.
                self.ui.display_community_cards(self.community_cards)
                self.current_bet = 0
                for player in self.players:
                    player.current_bet = 0
                print("\nFlop betting:")
                self.betting_round()
                state = self.TURN if len(self.get_active_players()) > 1 else self.SHOWDOWN
            
            elif state == self.TURN:
                self.deal_turn_or_river()
                print(f"\nTurn: {' '.join(str(card) for card in self.community_cards)}")
                # Update community cards display.
                self.ui.display_community_cards(self.community_cards)
                self.current_bet = 0
                for player in self.players:
                    player.current_bet = 0
                print("\nTurn betting:")
                self.betting_round()
                state = self.RIVER if len(self.get_active_players()) > 1 else self.SHOWDOWN
            
            elif state == self.RIVER:
                self.deal_turn_or_river()
                print(f"\nRiver: {' '.join(str(card) for card in self.community_cards)}")
                # Update community cards display.
                self.ui.display_community_cards(self.community_cards)
                self.current_bet = 0
                for player in self.players:
                    player.current_bet = 0
                print("\nRiver betting:")
                self.betting_round()
                state = self.SHOWDOWN
            
            elif state == self.SHOWDOWN:
                # Reveal all AI cards at showdown.
                ai_hands = [(p.name, p.hand, p.folded) for p in self.players if p.is_ai]
                self.ui.display_ai_hands(ai_hands, reveal_all=True)
                active_players = self.get_active_players()
                if len(active_players) > 1:
                    self.show_all_hands()
                    winners = self.find_winners()
                    self.distribute_pot(winners)
                else:
                    self.distribute_pot(active_players)
                state = "END"
        
        print("\nCurrent chip counts:")
        for player in self.players:
            print(f"{player.name}: {player.chips}")
    
    def play_game(self):
        """
        Main game loop that continues rounds until a termination condition is met.
        Uses a UI for user prompts and displays results via message boxes.
        """
        from tkinter import messagebox
        if not hasattr(self, "ui"):
            import tkinter as tk
            self.ui = GameUI(tk._default_root)
        print("Welcome to Simple Texas Hold'em!")
        while True:
            self.players = [p for p in self.players if p.chips > 0]
            if len(self.players) == 1:
                messagebox.showinfo("Game Over", f"{self.players[0].name} wins the game!")
                break
            elif not any(not p.is_ai for p in self.players):
                messagebox.showinfo("Game Over", "Game over! All human players are out.")
                break
            self.play_round()
            cont = self.ui.prompt_action("Continue to next round?", ["yes", "no"])
            if cont != "yes":
                break
        messagebox.showinfo("Thanks", "Thanks for playing!")