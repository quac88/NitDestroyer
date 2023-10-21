from deck import Deck
from game import Pot, Dealer, Player, Table


def main():
    # create a deck
    deck = Deck()
    # shuffle the deck
    deck.shuffle()
    # create a pot
    pot = Pot()
    # create a dealer
    dealer = Dealer(deck=deck, pot=pot)
    # create a table
    table = Table(seats=8)
    # create players
    player1 = Player(name="player1", stack=200, hand=[], status=True, chips_in_play=0)
    player2 = Player(name="player2", stack=200, hand=[], status=True, chips_in_play=0)
    players: list[Player] = [player1, player2]
    # seat players
    table.seat_player(player=player1, seat=0)
    table.seat_player(player=player2, seat=1)
    # move button
    dealer.move_button(players=table.seats)
    # print who the button is
    print("Button: " + str(table.seats[dealer.button]))
    # post antes
    for player in players:
        player.post_ante(ante=1)
    # update pot
    pot.add_to_pot(amount=2)
    # print pot
    print("Pot: " + str(pot.total))
    # print each players stack
    print("Player1 stack: " + str(player1.stack))
    print("Player2 stack: " + str(player2.stack))
    # deal 1 card to each player beggining to the seat left of the button
    dealer.deal_hand(players=table.seats)
    # print each players hand
    player1_hand = player1.hand[0]
    player2_hand = player2.hand[0]
    print("Player1 hand: " + str(player1_hand))
    print("Player2 hand: " + str(player2_hand))


if __name__ == "__main__":
    main()
