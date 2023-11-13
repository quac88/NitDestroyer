from rich.progress import track
from loguru import logger
import argparse
import time
from cardecky import Deck
from game import Pot, Dealer, Player, Table, Game
from game_tree import build_game_state_tree, print_game_state_tree
from data_logger import Data_Logger, Node

# constants for betting - these are the max bets for each betting round
ANTE = 1
PRE_FLOP_LIMIT = 2
FLOP_LIMIT = 4
TURN_LIMIT = 4
START_STACK = 200
NUM_ROUNDS: int = 1

# Set up command line argument parsing
parser = argparse.ArgumentParser(description="Run the poker game.")
parser.add_argument("--log", action="store_true", help="Enable logging to a file.")
args = parser.parse_args()

# Configure the logger based on the command line flag
if args.log:
    logger.add("game_log.log", rotation="10 MB", retention="10 days", format="{time} {level} {message}")
else:
    # Disable all logging if --log is not provided
    logger.remove()


def log_game_state(game, data_logger):
    game_state = game.get_game_state()
    data_logger.add_game_state(game_state)
    logger.info("Game state logged")

def play_round(players, dealer, pot, game, button, data_logger) -> None:         
    # Increment the hand number at the start of each round
    data_logger.next_hand()
    
    for player in players:
        player.hand = []
        player.status = True
        player.chips_in_play = 0
    dealer.board = []

    # shuffle the deck
    dealer.deck.shuffle()

    ## ANTE #################################################
    for player in players:
        player.post_ante(ante=ANTE, pot=pot)

    # Log initial game state
    logger.info(f"Players posted antes. Pot: {pot.total}")
    log_game_state(game, data_logger)
    #########################################################

    # DEAL HANDS #############################################
    dealer.deal_hand(players=players)
    logger.info("Hands dealt")

    # Log the players' hands
    for player in players:
        logger.info(f"Player {player.player_ID} hand: {player.hand}")
    ##########################################################

    ## PRE-FLOP ##############################################
    logger.info("Pre-flop betting")
    game.preflop_betting(button=button, round_limit=PRE_FLOP_LIMIT)
    logger.info(f"End of pre-flop betting. Pot: {pot.total}")
    log_game_state(game, data_logger)
    

    # If there is only one player left, award the pot and move on to the next round
    if dealer.active_players_count(players=players) <= 1:
        winners = [player for player in players if player.status]
        for winner in winners:
            logger.info(f"Player {winner.player_ID} won {pot.total} chips")
        pot.award_pot(winners)
        # print the winner and their stack
        for winner in winners:
            logger.info(f"Player {winner.player_ID} stack: {winner.stack}")
        # print the losers stack
        for player in players:
            if player not in winners:
                logger.info(f"Player {player.player_ID} stack: {player.stack}")
        pot.reset_pot()
        return
    ##########################################################

    ## DEAL FLOP #############################################
    flop = dealer.deal_flop()
    # Log the flop
    logger.info(f"Flop: {flop}")
    logger.info(f"Flop betting")

    ## FLOP ##################################################
    game.flop_betting(button=button, round_limit=FLOP_LIMIT)
    logger.info(f"End of flop betting. Pot: {pot.total}")
    log_game_state(game, data_logger)

    # If there is only one player left, award the pot and move on to the next round
    if dealer.active_players_count(players=players) <= 1:
        winners = [player for player in players if player.status]
        for winner in winners:
            logger.info(f"Player {winner.player_ID} won {pot.total} chips")
        pot.award_pot(winners)
        # print the winner and their stack
        for winner in winners:
            logger.info(f"Player {winner.player_ID} stack: {winner.stack}")
        # print the losers stack
        for player in players:
            if player not in winners:
                logger.info(f"Player {player.player_ID} stack: {player.stack}")
        pot.reset_pot()
        return
    ##########################################################

    ## DEAL TURN #############################################
    turn = dealer.deal_turn()
    logger.info(f"Turn: {turn}")
    logger.info(f"Turn betting")
    ##########################################################

    ## TURN ##################################################
    game.turn_betting(button=button, round_limit=TURN_LIMIT)
    logger.info(f"End of turn betting. Pot: {pot.total}")
    log_game_state(game, data_logger)

    if dealer.active_players_count(players=players) <= 1:
        winners = [player for player in players if player.status]
        # print how much the winner won
        for winner in winners:
            logger.info(f"Player {winner.player_ID} won {pot.total} chips")
        pot.award_pot([player for player in players if player.status])
        # print the winner and their stack
        for winner in winners:
            logger.info(f"Player {winner.player_ID} stack: {winner.stack}")
        # print the losers stack
        for player in players:
            if player not in winners:
                logger.info(f"Player {player.player_ID} stack: {player.stack}")
        pot.reset_pot()
    # if there is more than one player left, determine the winner
    else:
        winners = dealer.determine_winner(players=players)
        if winners:
            for winner in winners:
                logger.info(f"Player {winner.player_ID} won {pot.total} chips")
            pot.award_pot(winners)
            # print the winner and their stack
            for winner in winners:
                logger.info(f"Player {winner.player_ID} stack: {winner.stack}")
            # print the losers stack
            for player in players:
                if player not in winners:
                    logger.info(f"Player {player.player_ID} stack: {player.stack}")
        pot.reset_pot()
    ##########################################################

    # Log the game state
    game_state = game.get_game_state()
    data_logger.add_game_state(game_state)

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

    data_logger = Data_Logger()  # Initialize Data_Logger

    hand_counter = 0  # Initialize the hand counter

    
    args = [(players, dealer, pot, game, button, data_logger) for _ in range(NUM_ROUNDS)]
    for arg in track(args, total=NUM_ROUNDS, description="Rounds"):
        play_round(*arg)

        # Increment and log the hand counter
        hand_counter += 1
        logger.info(f"Completed hand number: {hand_counter}")

        if not enough_players_to_continue(players):
            logger.info("Not enough players to continue the round.")
            break

    data_logger.store_tree()  # Store the game state tree

# Helper function to check if enough players are left
def enough_players_to_continue(players) -> bool:
    return sum(player.stack > 0 for player in players) >= 2
    
if __name__ == "__main__":
    # check the time it takes to run
    start_time = time.time()
    main()
    execution_time = time.time() - start_time
    logger.info(f"Execution time for {NUM_ROUNDS} rounds: {execution_time:.9f} seconds")
