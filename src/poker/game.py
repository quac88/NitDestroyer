from __future__ import annotations
from loguru import logger
import random
from cardecky import Deck, HandRanker
from data_logger import DataLogger
from enum import Enum

# Configure Loguru Logger
logger.add("game_log.log", rotation="10 MB", retention="10 days", format="{time} {level} {message}")

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

    def is_busted(self) -> bool:
        """Check if a player is busted."""
        return self.stack == 0

    def can_bet(self, amount: int) -> bool:
        """Check if a player can bet a certain amount."""
        return amount <= self.stack

    def bet(self, amount: int, pot: Pot) -> None:
        """Make a bet or raise."""
        if amount < 0:
            raise ValueError("Bet amount cannot be negative")
        if amount > self.stack:
            # All in
            amount = self.stack
            logger.info(f"Player {self} is all in")
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
    
    def reset_for_new_round(self):
        """Reset the player's state for a new round."""
        self.hand = []
        self.status = True
        self.chips_in_play = 0

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
        num_players: int = len(players)
        next_button: int = (self.button + 1) % num_players
        # Keep moving the button until a non-None player is found
        while players[next_button] is None:
            next_button = (next_button + 1) % num_players
        self.button = next_button

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
        if seat < 0 or seat >= len(self.seats) or not isinstance(seat, int):
            raise IndexError("Invalid seat index")
        self.seats[seat] = player

class PlayerAction(Enum):
    """Enum for player actions."""
    FOLD = 1
    CHECK = 2
    CALL = 3
    RAISE = 4

class Game:
    def __init__(self, num_players, start_stack, betting_limit):
        self.num_players = num_players
        self.deck = Deck()
        self.pot = Pot()
        self.table = Table(seats=num_players)
        self.players = [Player(player_ID=i, stack=start_stack, hand=[], status=True, chips_in_play=0) for i in range(num_players)]
        self.dealer = Dealer(self.pot, self.deck)
        self.betting_limit = betting_limit
        self.current_bet = 0

    def setup_game(self):
        for i, player in enumerate(self.players):
            self.table.seat_player(player, i)
        self.dealer.move_button(self.players)
        self.deck.shuffle()

    def post_antes(self, ante_amount):
        """Post the antes for each player."""
        for player in self.players:
            if player.status:  # Post ante only if the player is active
                player.post_ante(ante=ante_amount, pot=self.pot)
                logger.info(f"Player {player.player_ID} posted ante of {ante_amount}")

    def deal_hands(self):
        self.dealer.deal_hand(self.players)

    def deal_flop(self):
        flop = self.dealer.deal_flop()
        logger.info(f"Flop: {flop}")

    def deal_turn(self):
        turn = self.dealer.deal_turn()
        logger.info(f"Turn: {turn}")

    def betting_round(self, button, start_offset, round_limit) -> None:
        """Handle the logic for a round of betting."""
        current_bet = 0
        raise_occurred = True
        last_raiser = None
        players_acted = set()
        start_position = (button + start_offset) % self.num_players
        raise_count = 0

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
                    available_actions = [PlayerAction.FOLD, PlayerAction.CALL]
                    # Allow raise only if the raise count is less than 3
                    if raise_count < 3:
                        available_actions.append(PlayerAction.RAISE)

                action: PlayerAction = random.choice(available_actions)
                players_acted.add(player)

                # Replace print statements with loguru logging
                if action == PlayerAction.FOLD:
                    player.fold()
                    logger.info(f"Player {player} folded")
                elif action == PlayerAction.CHECK:
                    player.check()
                    logger.info(f"Player {player} checked")
                elif action == PlayerAction.CALL:
                    player.call(amount=current_bet, pot=self.dealer.pot)
                    logger.info(f"Player {player} called {current_bet}")
                    logger.info(f"Pot: {self.dealer.pot.total}")
                elif action == PlayerAction.RAISE:
                    raise_amount = current_bet + round_limit
                    player.bet(amount=raise_amount, pot=self.dealer.pot)
                    logger.info(f"Player {player} raised to {raise_amount}")
                    logger.info(f"raise_count: {raise_count}")
                    logger.info(f"Pot: {self.dealer.pot.total}")
                    current_bet = raise_amount
                    self.dealer.current_bet = raise_amount
                    raise_occurred = True
                    last_raiser = player
                    players_acted.clear()
                    raise_count += 1
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

    def reset_round(self):
        self.pot.reset_pot()
        self.current_bet = 0
        for player in self.players:
            player.reset_for_new_round()
        self.dealer.board.clear()
        
    def check_round_completion(self):
        """Check if the round is complete."""
        active_players = [player for player in self.players if player.status]
        if len(active_players) <= 1:
            # Only one player is active, they win the pot
            winner = active_players[0] if active_players else None
            if winner:
                self.pot.award_pot([winner])
                logger.info(f"Player {winner.player_ID} won the pot as the last active player.")
            else:
                logger.info("No active players remaining to award the pot.")
            return True  # Round is complete
        return False  # Round continues

    def determine_winner(self):
        # Determine the winner(s) among active players
        winners = self.dealer.determine_winner(players=self.players)

        if winners:
            # Award pot to the identified winners
            pot = self.dealer.pot.total
            logger.info(f"Pot: {pot}")
            self.pot.award_pot(winners)
            logger.info(f"Player(s) {winners} won the pot.")
        else:
            # Handle the case where no winners are identified
            # This might occur if all players folded except one
            remaining_player = next((p for p in self.players if p.status), None)
            if remaining_player:
                logger.info(f"Player {remaining_player.player_ID} wins the pot by default.")
                pot = self.dealer.pot.total
                logger.info(f"Pot: {pot}")
                self.pot.award_pot([remaining_player])
            else:
                logger.info("No active players remaining to award the pot.")


    def log_game_state(self, data_logger):
        game_state = self.get_game_state()
        data_logger.add_game_state(game_state)
        logger.info("Game state logged")

    def play_round(self, data_logger, ante_amount, pre_flop_limit, flop_limit, turn_limit):
        self.setup_game()
        self.post_antes(ante_amount=ante_amount)
        self.deal_hands()
        self.preflop_betting(button=self.dealer.button, round_limit=pre_flop_limit)
        self.log_game_state(data_logger)

        if self.check_round_completion():
            return

        self.deal_flop()
        self.flop_betting(button=self.dealer.button, round_limit=flop_limit)
        self.log_game_state(data_logger=data_logger)

        if self.check_round_completion():
            return

        self.deal_turn()
        self.turn_betting(button=self.dealer.button, round_limit=turn_limit)
        self.log_game_state(data_logger=data_logger)

        if self.check_round_completion():
            return

        self.determine_winner()
        self.reset_round()


    # return game state data
    def get_game_state(self):
        # define game state as a fixed length array of 52 cards with 0 or 1 for each card and 16 additional positions with 1,2,3,4 as options that coorespond to whether we folded, checked, called, or raised
        # 0-51: 0 or 1 for each card
        # 52-60: 1,2,3,4 for call, raise, check, fold, each position in the array is a player and their action, only one round of raising is allowed, maximum length of 2 turns around table to call
        # this is preflop_betting
        # 61-68, 1,2,3,4 for call, raise, check, fold, each position in the array is a player and their action, only one round of raising is allowed, maximum length of 2 turns around table to call
        # flop_betting
        # 69-77, 1,2,3,4 for call, raise, check, fold, each position in the array is a player and their action, only one round of raising is allowed, maximum length of 2 turns around table to call
        # turn_betting
        # 78-86, 1,2,3,4 for call, raise, check, fold, each position in the array is a player and their action, only one round of raising is allowed, maximum length of 2 turns around table to call
        # river_betting

        game_data = {
            'current_bet': self.dealer.current_bet,
            'board': self.dealer.board}
        for player in self.players:
            game_data[str(player.player_ID)] = {
                'stack': player.stack,
                'hand': player.hand,
                'status': player.status,
                'chips_in_play': player.chips_in_play
            }
        return game_data
