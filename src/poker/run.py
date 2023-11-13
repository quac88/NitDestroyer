from rich.progress import track
from loguru import logger
import argparse
import time
from game import Game
from data_logger import DataLogger

# Constants
NUM_PLAYERS = 2
START_STACK = 200
ANTE= 1
PRE_FLOP_LIMIT = 2
FLOP_LIMIT = 4
TURN_LIMIT = 4
NUM_ROUNDS = 1

# Set up command line argument parsing
parser = argparse.ArgumentParser(description="Run the poker game.")
parser.add_argument("--log", action="store_true", help="Enable logging to a file.")
args = parser.parse_args()

# Configure the logger based on the command line flag
if args.log:
    logger.add("game_log.log", rotation="10 MB", retention="10 days", format="{time} {level} {message}")
else:
    logger.remove()

def main() -> None:
    # Initialize game and logger
    game = Game(num_players=NUM_PLAYERS, start_stack=START_STACK, betting_limit=PRE_FLOP_LIMIT)
    data_logger = DataLogger()

    # Prepare the game
    game.setup_game()

    # Play rounds
    for round_number in track(range(NUM_ROUNDS), description="Rounds"):
        logger.info(f"Starting round {round_number + 1}")
        game.play_round(data_logger=data_logger, ante_amount=ANTE, pre_flop_limit=PRE_FLOP_LIMIT, flop_limit=FLOP_LIMIT, turn_limit=TURN_LIMIT)
        if not enough_players_to_continue(game.players):
            logger.info("Not enough players to continue the round.")
            break
        logger.info(f"Completed round {round_number + 1}")

    # Store the game state tree
    data_logger.store_tree()

def enough_players_to_continue(players) -> bool:
    """Check if there are enough players with a non-zero stack."""
    return sum(player.stack > 0 for player in players) >= 2
    
if __name__ == "__main__":
    # Measure execution time
    start_time = time.time()
    main()
    execution_time = time.time() - start_time
    logger.info(f"Execution time for {NUM_ROUNDS} rounds: {execution_time:.9f} seconds")
