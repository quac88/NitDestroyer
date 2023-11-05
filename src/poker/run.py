from qqdm import qqdm
import time
from cardecky import Deck
from game import Pot, Dealer, Player, Table, Game

# constants for betting - these are the max bets for each betting round
ANTE = 1
PRE_FLOP_LIMIT = 2
FLOP_LIMIT = 4
TURN_LIMIT = 4
START_STACK = 200
NUM_ROUNDS: int = 1

def play_round(players, dealer, pot, game, button) -> None:
    # reset each player's hand and status
    for player in players:
        player.hand = []
        player.status = True
        player.chips_in_play = 0

    # shuffle the deck
    dealer.deck.shuffle()

    # post the antes
    for player in players:
        player.post_ante(ante=ANTE, pot=pot)
    print(f"Pot: {pot.total}")

    # Deal the hands to players
    dealer.deal_hand(players=players)

    # Betting for pre-flop
    game.preflop_betting(button=button, round_limit=PRE_FLOP_LIMIT)

    # If there is only one player left, award the pot and move on to the next round
    if dealer.active_players_count(players=players) <= 1:
        winners = [player for player in players if player.status]
        pot.award_pot(winners)
        pot.reset_pot()
        return

    # Deal the flop and begin betting round for the flop
    flop = dealer.deal_flop()
    game.flop_betting(button=button, round_limit=FLOP_LIMIT)

    # If there is only one player left, award the pot and move on to the next round
    if dealer.active_players_count(players=players) <= 1:
        winners = [player for player in players if player.status]
        pot.award_pot(winners)
        pot.reset_pot()
        return

    # Deal the turn and begin betting round for the turn
    turn = dealer.deal_turn()
    game.turn_betting(button=button, round_limit=TURN_LIMIT)
    if dealer.active_players_count(players=players) <= 1:
        pot.award_pot([player for player in players if player.status])
        pot.reset_pot()
    # if there is more than one player left, determine the winner
    else:
        winners = dealer.determine_winner(players=players)
        if winners:
            pot.award_pot(winners)
        pot.reset_pot()

def main() -> None:
    ##### Initial setup #####
    deck = Deck()
    pot = Pot()
    dealer = Dealer(pot=pot, deck=deck)
    table = Table(seats=9)
    player0 = Player(player_ID=0, stack=START_STACK, hand=[], status=True, chips_in_play=0)
    player1 = Player(player_ID=1, stack=START_STACK, hand=[], status=True, chips_in_play=0)
    players: list[Player] = [player0, player1]
    table.seat_player(player=player0, seat=0)
    table.seat_player(player=player1, seat=1)
    dealer.move_button(players=players)
    button = dealer.button
    game = Game(players=players, dealer=dealer, betting_limit=PRE_FLOP_LIMIT)
    #####  End initial setup #####
    
    # Create a list of arguments to pass to the play_round function
    args: list[tuple[list[Player], Dealer, Pot, Game, int, int]] = [(players, dealer, pot, game, button, i + 1) for i in range(NUM_ROUNDS)]
    
    # Use qqdm to track progress and display a very pretty progress bar
    for arg in qqdm(args, total=NUM_ROUNDS, desc="Rounds"):
        play_round(*arg)
    
if __name__ == "__main__":
    # check the time it takes to run
    start_time = time.time()
    main()
    execution_time = time.time() - start_time
    print(f"Execution time for {NUM_ROUNDS} rounds: {execution_time:.9f} seconds")
