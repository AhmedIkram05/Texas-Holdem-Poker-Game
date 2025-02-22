import random

def make_betting_decision(game, player):
    """
    Enhanced AI decision making using simple rule-based logic.
    
    Evaluates AI hole cards by summing rank values and adding a bonus if paired,
    then uses thresholds to decide to fold, call, check, or raise.
    
    Args:
        game: Instance providing game state and place_bet method.
        player: The AI player making a decision.
    """
    # Basic evaluation of hole cards.
    if len(player.hand) < 2:
        # fallback: call if not enough info
        to_call = game.current_bet - player.current_bet
        game.ui.append_log(f"{player.name} calls {to_call} (insufficient hole cards).")
        game.place_bet(player, to_call)
        return

    card1, card2 = player.hand[0], player.hand[1]
    strength = card1.rank.value + card2.rank.value
    if card1.rank == card2.rank:
        strength += 10  # Bonus for a pair.

    to_call = game.current_bet - player.current_bet

    # When no call is needed.
    if to_call <= 0:
        if strength >= 24 and player.chips > 10:
            bet_amount = min(player.chips, int(player.chips * 0.25))
            game.ui.append_log(f"{player.name} bets {bet_amount} (strong hand).")
            game.place_bet(player, bet_amount)
        else:
            game.ui.append_log(f"{player.name} checks.")
        return

    # If the call amount is risky for a weak hand.
    if to_call > player.chips * 0.3 and strength < 20:
        player.folded = True
        game.ui.append_log(f"{player.name} folds (weak hand, high call: strength {strength}).")
    elif strength >= 24 and player.chips > to_call + 10:
        raise_amount = 10  # Fixed raise amount.
        total_bet = to_call + raise_amount
        game.ui.append_log(f"{player.name} raises from {player.current_bet} to {player.current_bet + total_bet} (strength {strength}).")
        game.place_bet(player, total_bet)
    else:
        game.ui.append_log(f"{player.name} calls {to_call} (moderate hand: strength {strength}).")
        game.place_bet(player, to_call)
