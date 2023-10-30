from __future__ import annotations
import random
from src.poker.cardecky import Deck, HandRanker
from enum import Enum


class Player:
    def __init__(self, player_ID: int, stack: int, hand: list, status: bool, chips_in_play: int) -> None:
        self.player_ID: int = player_ID
        self.stack: int = stack
        self.hand = hand
        self.status: bool = status
        self.chips_in_play: int = chips_in_play

    def __str__(self) -> str:
        """Representation of a player."""
        return str(self.player_ID)

    def can_bet(self, amount: int) -> bool:
        """Check if a player can bet a certain amount."""
        return amount <= self.stack

    def bet(self, amount: int, pot: Pot) -> None:
        """Make a bet or raise."""
        self.stack -= amount
        self.chips_in_play += amount
        pot.add_to_pot(amount=amount)

    def post_ante(self, ante: int, pot: Pot) -> None:
        """Post the ante."""
        self.bet(amount=ante, pot=pot)

    def call(self, amount: int, pot: Pot) -> None:
        """Make a call."""
        self.bet(amount=amount, pot=pot)

    def check(self) -> None:
        """Check."""
        pass

    def fold(self) -> None:
        """Fold the hand."""
        self.status = False
    
    def is_bust(self) -> bool:
        """Check if a player is bust."""
        return self.stack == 0

    def __hash__(self) -> int:
        """Hash a player."""
        return hash(self.player_ID)
    
class Pot:
    def __init__(self, total: int = 0) -> None:
        self.total: int = total

    def reset_pot(self) -> None:
        """Reset the pot."""
        self.total = 0

    def add_to_pot(self, amount: int) -> None:
        """Add to the pot."""
        self.total += amount

    def award_pot(self, winners: list[Player]):
        """Award the pot to the winner(s)."""
        if len(winners) > 1:
            split_amount = self.total // len(winners)
            for winner in winners:
                winner.stack += split_amount
            self.total = 0
        else:
            winner: Player = winners[0] 
            winner.stack += self.total
            self.total = 0


class Dealer:
    def __init__(self, pot: Pot, deck: Deck, button: int = 0, current_bet: int = 0):
        self.pot: Pot = pot
        self.deck: Deck = deck
        self.button: int = button
        self.current_bet: int = current_bet
        self.board: list = []  # To store the flop and turn cards

    def deal_hand(self, players: list[Player]) -> None:
        """Deal the hand to the players."""
        for player in players:
            if player is not None:
                player.hand = self.deck.deal_cards(1)

    def move_button(self, players: list[Player]) -> None:
        """Move the button to the next player."""
        if players[self.button] is None:
            self.button = 0
        else:
            self.button = (self.button + 1) % len(players)

    def deal_flop(self) -> list:
        """Deal the flop."""
        flop = self.deck.deal_cards(1)
        self.board.extend(flop)
        return flop

    def deal_turn(self) -> list:
        """Deal the turn."""
        turn = self.deck.deal_cards(1)
        self.board.extend(turn)
        return turn

    def active_players_count(self, players: list[Player]):
        """Count the number of active players."""
        return sum(1 for player in players if player.status)

    def determine_winner(self, players: list[Player]) -> list[Player]:
        """Determine the winner(s)."""
        best_rank = None
        winners = []
        for player in players:
            if player.status is True:
                combined_hand: list = player.hand + self.board
                ranked_hand = HandRanker.rank_hand(combined_hand)
                if best_rank is None or (ranked_hand and ranked_hand[0] < best_rank):
                    best_rank = ranked_hand[0]
                    winners = [(player, ranked_hand)]
                elif ranked_hand and ranked_hand[0] == best_rank:
                    winners.append((player, ranked_hand))


            return [winner for winner, _ in winners]

class Table:
    def __init__(self, seats) -> None:
        self.seats: list[None] = [None] * seats

    def __str__(self) -> str:
        """Representation of the table."""
        return str(object=self.seats)

    def seat_player(self, player, seat) -> None:
        """Seat a player at a seat."""
        self.seats[seat] = player

class PlayerAction(Enum):
    """Enum for player actions."""
    FOLD = 1
    CHECK = 2
    CALL = 3
    RAISE = 4

class Game:
    def __init__(self, players, dealer, betting_limit, current_bet=0) -> None:
        self.players = players
        self.dealer = dealer
        self.betting_limit = betting_limit
        self.current_bet = current_bet
        self.num_players = len(self.players)

    def betting_round(self, button, start_offset, round_limit) -> None:
        """Handle the logic for a round of betting."""
        current_bet = 0
        raise_occurred = True
        last_raiser = None
        players_acted = set()
        start_position = (button + start_offset) % self.num_players

        while raise_occurred:
            raise_occurred = False
            for i in range(self.num_players):
                current_player = (i + start_position) % self.num_players
                player = self.players[current_player]

                if player is None or not player.status:
                    continue

                if player in players_acted:
                    if player != last_raiser or not raise_occurred:
                        continue

                if current_bet == 0:
                    available_actions = [PlayerAction.CHECK, PlayerAction.RAISE]
                elif player == last_raiser:
                    continue
                else:
                    available_actions: list[PlayerAction] = [PlayerAction.FOLD, PlayerAction.CALL, PlayerAction.RAISE]

                action: PlayerAction = random.choice(available_actions)
                players_acted.add(player)

                if action == PlayerAction.FOLD:
                    player.fold()
                elif action == PlayerAction.CHECK:
                    player.check()
                elif action == PlayerAction.CALL:
                    player.call(amount=current_bet, pot=self.dealer.pot)
                elif action == PlayerAction.RAISE:
                    raise_amount = current_bet + round_limit
                    player.bet(amount=raise_amount, pot=self.dealer.pot)
                    current_bet = raise_amount
                    self.dealer.current_bet = raise_amount
                    raise_occurred = True
                    last_raiser = player
                    players_acted.clear()
            if not raise_occurred:
                break

    def preflop_betting(self, button, round_limit) -> None:
        """Preflop betting."""
        self.betting_round(button=button, start_offset=3, round_limit=round_limit)

    def flop_betting(self, button, round_limit) -> None:
        """Flop betting."""
        self.betting_round(button=button, start_offset=1, round_limit=round_limit)

    def turn_betting(self, button, round_limit) -> None:
        """Turn betting."""
        self.betting_round(button=button, start_offset=1, round_limit=round_limit)


