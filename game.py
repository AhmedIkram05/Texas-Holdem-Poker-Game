import random
from typing import List
from card import Card, Suit, Rank, HandRank
from player import Player
from ui import GameUI  # New import
from hand_evaluator import evaluate_hand  # New import

class Game:
    def __init__(self, player_name="Player", starting_chips=1000):
        self.deck = []
        self.community_cards = []
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
        self.deck = []
        for suit in Suit:
            for rank in Rank:
                self.deck.append(Card(rank, suit))
        random.shuffle(self.deck)
    
    def deal_cards(self):
        for player in self.players:
            player.hand = []
        self.community_cards = []
        
        for _ in range(2):
            for player in self.players:
                if not player.folded:
                    player.hand.append(self.deck.pop())
    
    def deal_flop(self):
        self.deck.pop()
        for _ in range(3):
            self.community_cards.append(self.deck.pop())
            
    def deal_turn_or_river(self):
        self.deck.pop()
        self.community_cards.append(self.deck.pop())
    
    def get_active_players(self):
        return [p for p in self.players if not p.folded]
    
    def betting_round(self):
        active_players = self.get_active_players()
        if len(active_players) <= 1:
            return
        
        start_idx = (self.dealer_idx + 1) % len(self.players)
        current_idx = start_idx
        
        all_matched = False
        while not all_matched:
            player = self.players[current_idx]
            
            if not player.folded:
                if player.is_ai:
                    self.ai_betting_decision(player)
                else:
                    self.human_betting_decision(player)
            
            current_idx = (current_idx + 1) % len(self.players)
            
            active_players = self.get_active_players()
            all_matched = all(p.current_bet == self.current_bet for p in active_players)
            
            if current_idx == start_idx and all_matched:
                break
    
    def ai_betting_decision(self, player):
        to_call = self.current_bet - player.current_bet
        
        if to_call == 0:
            if random.random() < 0.7:
                print(f"{player.name} checks.")
                return
            else:
                bet_amount = random.randint(1, max(1, int(player.chips * 0.2)))
                self.place_bet(player, bet_amount)
                return
                
        hand_strength = random.random()
        
        if hand_strength < 0.3:
            if to_call > player.chips // 10:
                player.folded = True
                print(f"{player.name} folds.")
            else:
                self.place_bet(player, to_call)
        elif hand_strength < 0.7:
            if to_call > player.chips // 5:
                player.folded = True
                print(f"{player.name} folds.")
            else:
                self.place_bet(player, to_call)
        else:
            if random.random() < 0.5:
                raise_amount = random.randint(1, max(1, int(player.chips * 0.3)))
                self.place_bet(player, to_call + raise_amount)
            else:
                self.place_bet(player, to_call)
    
    def human_betting_decision(self, player):
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
    
    def find_winners(self):
        active_players = self.get_active_players()
        if len(active_players) == 1:
            return active_players
        
        player_hands = []
        for player in active_players:
            hand_rank = evaluate_hand(player.hand + self.community_cards)
            player_hands.append((player, hand_rank))
        
        player_hands.sort(key=lambda x: (x[1][0].value, x[1][1]), reverse=True)
        
        best_hand = player_hands[0][1]
        winners = [p for p, h in player_hands if h == best_hand]
        
        return winners
    
    def show_all_hands(self):
        print("\nFinal hands:")
        for player in self.get_active_players():
            hand_str = ' '.join(str(card) for card in player.hand)
            hand_rank = evaluate_hand(player.hand + self.community_cards)
            print(f"{player.name}: {hand_str} - {hand_rank[0].name}")
    
    def distribute_pot(self, winners):
        split_amount = self.pot // len(winners)
        remainder = self.pot % len(winners)
        
        for player in winners:
            player.chips += split_amount
            print(f"{player.name} wins {split_amount} chips!")
        
        if remainder > 0:
            winners[0].chips += remainder
    
    def post_blinds(self):
        small_blind_idx = (self.dealer_idx + 1) % len(self.players)
        big_blind_idx = (self.dealer_idx + 2) % len(self.players)
        
        self.place_bet(self.players[small_blind_idx], self.small_blind)
        self.place_bet(self.players[big_blind_idx], self.big_blind)
        
        self.current_bet = self.big_blind
    
    def reset_round(self):
        for player in self.players:
            player.current_bet = 0
            player.folded = False
        
        self.current_bet = 0
        self.pot = 0
        
        self.dealer_idx = (self.dealer_idx + 1) % len(self.players)
    
    def play_round(self):
        print("\n" + "=" * 50)
        print(f"ROUND START - Dealer: {self.players[self.dealer_idx].name}")
        print("=" * 50)
        
        self.create_deck()
        self.reset_round()
        
        self.post_blinds()
        
        self.deal_cards()
        
        print("\nPre-flop betting:")
        self.betting_round()
        
        if len(self.get_active_players()) > 1:
            self.deal_flop()
            print(f"\nFlop: {' '.join(str(card) for card in self.community_cards)}")
            
            self.current_bet = 0
            for player in self.players:
                player.current_bet = 0
            print("\nFlop betting:")
            self.betting_round()
        
        if len(self.get_active_players()) > 1:
            self.deal_turn_or_river()
            print(f"\nTurn: {' '.join(str(card) for card in self.community_cards)}")
            
            self.current_bet = 0
            for player in self.players:
                player.current_bet = 0
            print("\nTurn betting:")
            self.betting_round()
        
        if len(self.get_active_players()) > 1:
            self.deal_turn_or_river()
            print(f"\nRiver: {' '.join(str(card) for card in self.community_cards)}")
            
            self.current_bet = 0
            for player in self.players:
                player.current_bet = 0
            print("\nRiver betting:")
            self.betting_round()
        
        active_players = self.get_active_players()
        if len(active_players) > 1:
            self.show_all_hands()
            winners = self.find_winners()
            self.distribute_pot(winners)
        else:
            self.distribute_pot(active_players)
        
        print("\nCurrent chip counts:")
        for player in self.players:
            print(f"{player.name}: {player.chips}")
    
    def play_game(self):
        from tkinter import messagebox
        # Initialize UI once (assume root exists)
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