from deck import Deck


class Pot:
    def __init__(self) -> None:
        self.total: float = 0

    def reset_pot(self) -> None:
        self.total = 0

class Dealer:
    def __init__(self, deck, pot) -> None:
        self.pot: float = pot
        self.deck = deck
        self.current_bet = 0
        self.button = 0

    # Rhode Island Hold'em
    def deal_hand(self, players) -> None:
        for player in players:
            player.hand = self.deck.dealCards(1)

    def move_button(self, players) -> None:
        self.button = (self.button + 1) % len(players)

    # we don't need blind setting functions for now

class Player:
    def __init__(self, name, stack, hand, status, chips_in_play) -> None:
        self.name: str = name
        self.stack: float = stack # change to integer later
        self.hand = hand
        self.status: bool = status
        self.bet: float = chips_in_play

    def __str__(self) -> str:
        return self.name

class Table:
    def __init__(self, seats) -> None:
        self.seats = seats
        self.seats: list[None] = [None] * seats


    





    










