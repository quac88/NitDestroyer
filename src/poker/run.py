from cardecky import Deck
from game import Pot, Dealer, Player, Table, Game

# constants for betting - these are the max bets for each betting round
ANTE = 1
PRE_FLOP_LIMIT = 2
FLOP_LIMIT = 4
TURN_LIMIT = 4

START_STACK = 200

def main():
    # create a deck
    deck = Deck()

    # create a pot
    pot = Pot()

    # create a dealer
    dealer = Dealer(pot=pot, deck=deck)

    # create a table
    table = Table(seats=9)

    # create two players
    player0 = Player(player_ID=0, stack=START_STACK, hand=[], status=True, chips_in_play=0)
    player1 = Player(player_ID=1, stack=START_STACK, hand=[], status=True, chips_in_play=0)
    # create a list of players
    players: list[Player] = [player0, player1]

    # seat the players
    table.seat_player(player=player0, seat=0)
    table.seat_player(player=player1, seat=1)

    # shuffle the deck
    deck.shuffle()

    # set the button
    dealer.move_button(players=players)

    # set the button to default
    button = 0

    # create a game
    game = Game(players=players, dealer=dealer, betting_limit=PRE_FLOP_LIMIT)

    # post the antes
    player0.post_ante(ante=ANTE, pot=pot) # player 0 puts in 1 chip to be eligable to play
    player1.post_ante(ante=ANTE, pot=pot) # player 1 puts in 1 chip to be eligable to play

    # deal the hand
    dealer.deal_hand(players=players)
    print(f"Player0 has hand: {player0.hand}")
    print(f"Player1 has hand: {player1.hand}")

    print("PRE-FLOP")
    game.preflop_betting(button=button, round_limit=PRE_FLOP_LIMIT)
    print(pot.total)
    if dealer.active_players_count(players=players) > 1:
        print("FLOP")
        flop = dealer.deal_flop()
        print(flop)
        game.flop_betting(button=button, round_limit=FLOP_LIMIT)
        print(pot.total)
        if dealer.active_players_count(players=players) > 1:
            print("TURN")
            turn = dealer.deal_turn()
            print(turn)
            game.turn_betting(button=button, round_limit=TURN_LIMIT)
            print(pot.total)
        else:
            print("Only one player remains. The hand is over.")
    else:
        print("Only one player remains. The hand is over.")
    
if __name__ == "__main__":
    main()
