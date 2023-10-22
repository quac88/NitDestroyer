from cardecky import Deck
from dataclasses import dataclass


@dataclass
class Player:
    player_ID: int # unique identifier
    stack: int # chips in stack
    hand: list # list of cards
    status: bool # True = active, False = folded
    chips_in_play: int # chips in play for current hand

    # for printing and debugging
    def __str__(self) -> int:
        return self.player_ID 

    # post the ante
    def post_ante(self, ante: int, pot) -> None:
        self.stack -= ante
        self.chips_in_play += ante
        pot.total += ante

    # place a raise - we can't use the word raise as it is a keyword of python  
    def raise_pot(self, amount: int, pot) -> None:
        self.stack -= amount
        self.chips_in_play += amount
        pot.total += amount


    # make a call
    def call(self, amount: int, pot) -> None:
        self.stack -= amount
        self.chips_in_play += amount
        pot.total += amount

    # check
    def check(self) -> None:
        pass

    # fold
    def fold(self) -> None:
        self.status = False

@dataclass
class Pot:
    total: int = 0

    def reset_pot(self) -> None:
        self.total = 0

    def add_to_pot(self, amount: int) -> None:
        self.total += amount

    def award_pot(self, player: Player) -> None:
        player.stack += self.total

    # split the pot between all active players (last standing players)
    def split_pot(self, players: list[Player]) -> None:
        active_players = [player for player in players if player.status]
        for player in active_players:
            player.stack += self.total / len(active_players)



@dataclass
class Dealer:
    pot: Pot
    deck: Deck
    current_bet: int = 0
    button: int = 0

    # Rhode Island Hold'em
    def deal_hand(self, players: list[Player]) -> None:
        for player in players:
            if player is not None:  # Only deal to non-empty seats
                player.hand = self.deck.deal_cards(1)
                # this error can be ignored as we will never not have enough cards

    # move the button (dealer seat) to the next player
    def move_button(self, players: list[Player]) -> None:
        if players[self.button] is None:
            self.button = 0
        else:
            self.button = (self.button + 1) % len(players)

    # we don't need blind setting functions for now

    # deal the flop
    def deal_flop(self) -> list:
        return self.deck.deal_cards(1)
    
    def deal_turn(self) -> list:
        return self.deck.deal_cards(1)


class Table:
    def __init__(self, seats) -> None:
        self.seats = seats
        self.seats: list[None] = [None] * seats

    def __str__(self) -> str:
        return str(self.seats)

    def seat_player(self, player, seat) -> None:
        self.seats[seat] = player
