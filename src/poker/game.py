from __future__ import annotations
import random
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
    def post_ante(self, ante: int, pot: Pot) -> None:
        self.stack -= ante
        self.chips_in_play += ante
        pot.total += ante

    # place a raise - we can't use the word raise as it is a keyword of python
    def raise_pot(self, amount: int, pot: Pot) -> None:
        self.stack -= amount
        self.chips_in_play += amount
        pot.total += amount


    # make a call
    def call(self, amount: int, pot: Pot) -> None:
        self.stack -= amount
        self.chips_in_play += amount
        pot.total += amount

    # check
    def check(self) -> None:
        pass

    # fold
    def fold(self) -> None:
        self.status = False

    def __hash__(self) -> int:
        return hash(self.player_ID)
    
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
    button: int = 0
    current_bet: int = 0

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

    def active_players_count(self, players: list[Player]):
        return sum(1 for player in players if player.status)


class Table:
    def __init__(self, seats) -> None:
        self.seats = seats
        self.seats: list[None] = [None] * seats

    def __str__(self) -> str:
        return str(self.seats)

    def seat_player(self, player, seat) -> None:
        self.seats[seat] = player

@dataclass
class Game:
    players: list
    dealer: Dealer
    betting_limit: int
    current_bet: int = 0

    def betting_round(self, button, start_offset, round_limit) -> None:
        num_players = len(self.players)
        current_bet = 0 # Track the current bet
        raise_occurred = True # Track if a raise occurred
        last_raiser = None # Track the last raiser
        players_acted = set()  # Track players who have acted

        start_position = (button + start_offset) % num_players # start at three players left of the button preflop and one player left postflop

        while raise_occurred:
            raise_occurred = False
            for i in range(start_position, start_position + num_players):
                player_position = i % num_players
                player = self.players[player_position]

                if player is None or not player.status: # Skip empty seats and folded players
                    continue

                if player in players_acted: 
                    if player != last_raiser or not raise_occurred:
                        continue

                if current_bet == 0:
                    available_actions = [1, 3]  # check or raise
                elif player == last_raiser:
                    continue  # Skip the last raiser's turn if there's no re-raise after their action
                else:
                    available_actions = [0, 2, 3]  # fold, call, or raise

                action = random.choice(available_actions)
                players_acted.add(player)

                if action == 0:
                    player.fold()
                    print(f"Player {player.player_ID} folded")
                    if last_raiser:  # if there was a raise before, end the round.
                        return
                elif action == 1:
                    player.check()
                    print(f"Player {player.player_ID} checked")
                elif action == 2:
                    player.call(amount=current_bet, pot=self.dealer.pot)
                    print(f"Player {player.player_ID} called {current_bet}")
                elif action == 3:
                    raise_amount = current_bet + round_limit
                    player.raise_pot(amount=raise_amount, pot=self.dealer.pot)
                    current_bet = raise_amount
                    self.dealer.current_bet = raise_amount
                    raise_occurred = True
                    last_raiser = player
                    players_acted.clear()
                    print(f"Player {player.player_ID} raised to {raise_amount}")

            if not raise_occurred:
                break

    def preflop_betting(self, button, round_limit) -> None:
        self.betting_round(button=button, start_offset=3, round_limit=round_limit)

    def flop_betting(self, button, round_limit) -> None:
        self.betting_round(button=button, start_offset=1, round_limit=round_limit)

    def turn_betting(self, button, round_limit) -> None:
        self.betting_round(button=button, start_offset=1, round_limit=round_limit)
