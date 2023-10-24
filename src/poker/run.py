from cardecky import Deck
from game import Pot, Dealer, Player, Table, Game

# constants for betting - these are the max bets for each betting round
ANTE = 1
PRE_FLOP_LIMIT = 2
FLOP_LIMIT = 4
TURN_LIMIT = 4

START_STACK = 200

def play_round(players, dealer, pot, game, button):
    # shuffle the deck
    dealer.deck.shuffle()

    # post the antes
    for player in players:
        player.post_ante(ante=ANTE, pot=pot)

    # Deal the hands to players
    dealer.deal_hand(players=players)
    for player in players:
        print(f"Player{player.player_ID}'s hand: {player.hand}")

    # Betting for pre-flop
    print("PRE-FLOP")
    game.preflop_betting(button=button, round_limit=PRE_FLOP_LIMIT)
    print(f"Pot total after PRE-FLOP: {pot.total}")

    if dealer.active_players_count(players=players) <= 1:
        print("Only one player remains. The hand is over.")
        return

    # Deal the flop and betting for flop
    print("\nFLOP")
    flop = dealer.deal_flop()
    print(f"Flop cards: {flop}")
    game.flop_betting(button=button, round_limit=FLOP_LIMIT)
    print(f"Pot total after FLOP: {pot.total}")

    if dealer.active_players_count(players=players) <= 1:
        print("Only one player remains. The hand is over.")
        return

    # Deal the turn and betting for turn
    print("\nTURN")
    turn = dealer.deal_turn()
    print(f"Turn card: {turn}")
    game.turn_betting(button=button, round_limit=TURN_LIMIT)
    print(f"Pot total after TURN: {pot.total}")

    winner = dealer.determine_winner(players=players)
    if winner:
        pot.award_pot([winner])  # assuming there's always a single winner
        print(f"\nPlayer {winner.player_ID} wins with hand: {winner.hand} and is awarded the pot of {pot.total} chips!")
    pot.reset_pot()

NUM_ROUNDS = 10
def main():
    # Initial setup
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

    # Play 10 rounds
    for i in range(NUM_ROUNDS):
        print(f"\n========== ROUND {i + 1} ==========")
        play_round(players=players, dealer=dealer, pot=pot, game=game, button=button)
        button = (button + 1) % len(players)  # Move the button
        for player in players:
            print(f"Player{player.player_ID} chip count: {player.stack}")  # Update chip stacks


if __name__ == "__main__":
    main()