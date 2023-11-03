import unittest
from unittest.mock import Mock, patch
import random
from src.poker.cardecky import Deck, HandRanker, Rank, Suit
from src.poker.game import Player, Pot, Dealer, Table, PlayerAction, Game

class TestPlayer(unittest.TestCase):
    def setUp(self) -> None:
        """Setup before each test"""
        self.player = Player(player_ID=0, stack=200, hand=[], status=True, chips_in_play=0)
        self.pot = Mock(Pot)

    def test_bet(self) -> None:
        """Test betting"""
        self.player.bet(amount=100, pot=self.pot)
        self.assertEqual(self.player.stack, 100)
        self.assertEqual(self.player.chips_in_play, 100)
        self.pot.add_to_pot.assert_called_once_with(amount=100)

    def test_can_bet(self) -> None:
        """Test if a player can bet a certain amount"""
        self.assertTrue(self.player.can_bet(amount=50))
        self.assertFalse(self.player.can_bet(amount=1500))

    def test_is_bust(self) -> None:
        """Test if a player is bust"""
        self.assertFalse(self.player.is_bust())
        self.player.stack = 0
        self.assertTrue(self.player.is_bust())

class TestPot(unittest.TestCase):
    def setUp(self) -> None:
        """Setup before each test"""
        self.pot = Pot()

    def test_add_to_pot(self) -> None:
        """Test adding to the pot"""
        self.pot.add_to_pot(amount=100)
        self.assertEqual(self.pot.total, 100)

    def test_reset_pot(self) -> None:
        """Test resetting the pot"""
        self.pot.add_to_pot(amount=100)
        self.pot.reset_pot()
        self.assertEqual(self.pot.total, 0)

class TestDealer(unittest.TestCase):
    def setUp(self) -> None:
        """Setup before each test"""
        self.pot = Mock(Pot)
        self.deck = Mock(Deck)
        self.dealer = Dealer(pot=self.pot, deck=self.deck)

    def test_deal_hand(self) -> None:
        player0 = Mock(Player)
        player1 = Mock(Player)
        self.deck.deal_cards.return_value = ['CardA']
        self.dealer.deal_hand(players=[player0, player1])
        player0.hand = ['CardA']
        player1.hand = ['CardA']

class TestTable(unittest.TestCase):
    def setUp(self) -> None:
        self.table = Table(seats=5)

    def test_seat_player(self) -> None:
        player = Mock(Player)
        self.table.seat_player(player=player, seat=2)
        self.assertEqual(self.table.seats[2], player)

class TestGame(unittest.TestCase):
    def setUp(self) -> None:
        """Setup before each test"""
        self.players: list[Player] = [
            Player(player_ID=0, stack=200, hand=[], status=True, chips_in_play=0),
            Player(player_ID=1, stack=200, hand=[], status=True, chips_in_play=0)
        ]
        self.dealer = Dealer(pot=Pot(), deck=Deck())
        self.game = Game(players=self.players, dealer=self.dealer, betting_limit=10)

    @patch("random.choice")
    def test_preflop_betting(self, mock_random_choice) -> None:
        """Test preflop betting"""
        mock_random_choice.side_effect = [PlayerAction.CHECK, PlayerAction.CHECK]
        self.game.preflop_betting(button=0, round_limit=10)

        for player in self.players:
            self.assertEqual(player.chips_in_play, 0)

    @patch("random.choice")
    def test_flop_betting(self, mock_random_choice) -> None:
        """Test flop betting"""
        mock_random_choice.side_effect = [PlayerAction.CALL, PlayerAction.RAISE, PlayerAction.CALL]
        self.game.flop_betting(button=0, round_limit=10)

        self.assertEqual(self.dealer.pot.total, 30)
        self.assertEqual(self.players[0].chips_in_play, 20)
        self.assertEqual(self.players[1].chips_in_play, 10)

    @patch("random.choice")
    def test_turn_betting(self, mock_random_choice) -> None:
        """Test turn betting"""
        mock_random_choice.side_effect = [PlayerAction.CALL, PlayerAction.RAISE, PlayerAction.FOLD]
        self.game.turn_betting(button=0, round_limit=10)

        self.assertEqual(self.dealer.pot.total, 20)
        self.assertEqual(self.players[0].chips_in_play, 10)
        self.assertFalse(self.players[1].status)

