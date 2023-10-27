from qqdm import qqdm
from multiprocessing import Pool
import timeit
from data_logger import Data_Logger
from cardecky import Deck
from game import Pot, Dealer, Player, Table, Game


# constants for betting - these are the max bets for each betting round
ANTE = 1
PRE_FLOP_LIMIT = 2
FLOP_LIMIT = 4
TURN_LIMIT = 4

START_STACK = 200


def play_round(players: list[Player], dealer, pot, game, button, logger) -> None:

    # initialize logger

    # reset each player's hand and status
    for player in players:
        player.hand = []
        player.status = True
        player.chips_in_play = 0

    # shuffle the deck
    dealer.deck.shuffle()

    logger.add_game_state(game.get_game_state())
    # post the antes
    for player in players:
        player.post_ante(ante=ANTE, pot=pot)
    logger.add_game_state(game.get_game_state())

    # Deal the hands to players
    dealer.deal_hand(players=players)
    logger.add_game_state(game.get_game_state())

    # Betting for pre-flop
    game.preflop_betting(button=button, round_limit=PRE_FLOP_LIMIT)
    logger.add_game_state(game.get_game_state())

    # If there is only one player left, award the pot and move on to the next round
    if dealer.active_players_count(players=players) <= 1:
        winners = [player for player in players if player.status]
        pot.award_pot(winners)
        pot.reset_pot()
        logger.add_game_state(game.get_game_state())
        logger.store_tree()
        logger.reset()

    # Deal the flop and begin betting round for the flop
    flop = dealer.deal_flop()
    game.flop_betting(button=button, round_limit=FLOP_LIMIT)
    logger.add_game_state(game.get_game_state())

    # Deal the turn and begin betting round for the turn
    turn = dealer.deal_turn()
    game.turn_betting(button=button, round_limit=TURN_LIMIT)
    logger.add_game_state(game.get_game_state())

    if dealer.active_players_count(players=players) <= 1:
        pot.award_pot([player for player in players if player.status])
        logger.add_game_state(game.get_game_state())
        logger.store_tree()
        logger.reset()
        pot.reset_pot()

    # if there is more than one player left, determine the winner
    else:
        winners = dealer.determine_winner(players=players)
        if winners:
            pot.award_pot(winners)
            logger.add_game_state(game.get_game_state())
            logger.store_tree()
            logger.reset()
            pot.reset_pot()


# Passing a tuple to the wrapper function allows us to use the imap_unordered function from the multiprocessing module


def play_round_wrapper(args) -> None:
    players, dealer, pot, game, button, round_number = args
    play_round(players=players, dealer=dealer,
               pot=pot, game=game, button=button, logger=Data_Logger())
    button = (button + 1) % len(players)  # Move the button


NUM_ROUNDS: int = 1000


def main() -> None:
    ##### Initial setup #####
    deck = Deck()
    pot = Pot()
    dealer = Dealer(pot=pot, deck=deck)
    table = Table(seats=9)
    player0 = Player(player_ID=0, stack=START_STACK,
                     hand=[], status=True, chips_in_play=0)
    player1 = Player(player_ID=1, stack=START_STACK,
                     hand=[], status=True, chips_in_play=0)
    players: list[Player] = [player0, player1]
    table.seat_player(player=player0, seat=0)
    table.seat_player(player=player1, seat=1)
    dealer.move_button(players=players)
    button = dealer.button
    game = Game(players=players, dealer=dealer, betting_limit=PRE_FLOP_LIMIT)
    #####  End initial setup #####

    # Create a list of arguments to pass to the play_round function
    args: list[tuple[list[Player], Dealer, Pot, Game, int, int]] = [
        (players, dealer, pot, game, button, i + 1) for i in range(NUM_ROUNDS)]

    # Create a pool of processes
    with Pool(processes=20) as pool:  # Adjust the number of processes as needed for the CPU
        # Use qqdm to track progress and dispalay a very pretty progress bar
        for _ in qqdm(pool.imap_unordered(func=play_round_wrapper, iterable=args), total=NUM_ROUNDS, desc="Rounds"):
            pass  # qqdm will handle the progress automatically


if __name__ == "__main__":
    # main()
    # check the time it takes to run
    execution_time: float = timeit.timeit(stmt=main, number=1)
    print(
        f"Execution time for {NUM_ROUNDS} rounds: {execution_time:.9f} seconds")
