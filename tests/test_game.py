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
        self.pot.total = 0  # Set the 'total' attribute on the mock


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

    def test_bet_large(self) -> None:
        """Test attempting to post an ante larger than the stack"""
        with self.assertRaises(ValueError, msg="Should raise error for ante larger than stack"):
            self.player.post_ante(ante=201, pot=self.pot)

    def test_bet_negative(self) -> None:
        """Test attempting to post a negative ante"""
        with self.assertRaises(ValueError, msg="Should raise error for negative ante"):
            self.player.post_ante(ante=-1, pot=self.pot)

    def test_bet_zero(self) -> None:
        """Test posting an ante of zero"""
        self.player.post_ante(ante=0, pot=self.pot)
        self.assertEqual(self.player.stack, 200)
        self.assertEqual(self.player.chips_in_play, 0)
        self.pot.add_to_pot.assert_called_once_with(amount=0)

    
    def test_post_ante(self) -> None:
        """Test posting a valid ante"""
        self.player.post_ante(ante=1, pot=self.pot)
        self.assertEqual(self.player.stack, 199)
        self.assertEqual(self.player.chips_in_play, 1)
        self.pot.add_to_pot.assert_called_once_with(amount=1)

    def test_call(self) -> None:
        """Test making a call"""
        call_amount = 50
        # Mock the 'add_to_pot' method
        def add_to_pot(amount) -> None:
            self.pot.total += amount
        self.pot.add_to_pot = add_to_pot
        self.player.call(amount=call_amount, pot=self.pot)
        # Check that the player's stack has decreased and chips in play increased
        self.assertEqual(self.player.stack, 200 - call_amount)
        self.assertEqual(self.player.chips_in_play, call_amount)
        self.assertEqual(self.pot.total, call_amount)

    def test_is_bust(self) -> None:
        """Test if a player is bust"""
        self.assertFalse(self.player.is_bust())
        self.player.stack = 0
        self.assertTrue(self.player.is_bust())

    def test_check(self) -> None:
        """Test checking"""
        initial_stack = self.player.stack
        self.player.check()
        # Check that the player's stack remains unchanged
        self.assertEqual(self.player.stack, initial_stack)
        self.assertTrue(self.player.status)  # The player should still be active

    def test_fold(self) -> None:
        """Test folding"""
        self.player.fold()
        # Check that the player's status is set to False
        self.assertFalse(self.player.status)

    def test_player_hash(self) -> None:
        """Test that the hash of a player is consistent with its player_ID."""
        # Create some players with different player_IDs
        player0 = Player(player_ID=0, stack=200, hand=[], status=True, chips_in_play=0)
        player1 = Player(player_ID=1, stack=200, hand=[], status=True, chips_in_play=0)
        player2 = Player(player_ID=2, stack=200, hand=[], status=True, chips_in_play=0)

        # Check that the hash of a player is the hash of its player_ID
        self.assertEqual(hash(player0), hash(player0.player_ID))
        self.assertEqual(hash(player1), hash(player1.player_ID))
        self.assertEqual(hash(player2), hash(player2.player_ID))

        # Check that players with different IDs have different hashes
        self.assertNotEqual(hash(player0), hash(player1))
        self.assertNotEqual(hash(player0), hash(player2))
        self.assertNotEqual(hash(player1), hash(player2))

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
        """Test dealing hands to players"""
        player0 = Mock(Player)
        player1 = Mock(Player)
        # Mock the return value of deal_cards to simulate dealing different cards to different players
        self.deck.deal_cards.side_effect = [['CardA'], ['CardB']]
        # Call the method to deal hands
        self.dealer.deal_hand(players=[player0, player1])
        # Assert that each player's hand is set correctly with different cards
        self.assertEqual(player0.hand, ['CardA'])
        self.assertEqual(player1.hand, ['CardB'])

    def test_move_button(self) -> None:
        """Test moving the button to the next player"""
        # Mock the players
        player0 = Mock(Player)
        player1 = Mock(Player)
        player2 = Mock(Player)
        players: list[Mock] = [player0, player1, player2]
        # Initial button position
        self.assertEqual(self.dealer.button, 0)
        # Move button once
        self.dealer.move_button(players=players)
        self.assertEqual(self.dealer.button, 1)
        # Move button again
        self.dealer.move_button(players=players)
        self.assertEqual(self.dealer.button, 2)
        # Move button again, should wrap around to first player
        self.dealer.move_button(players=players)
        self.assertEqual(self.dealer.button, 0)

    def test_move_button_with_none_player(self) -> None:
        """Test moving the button with a None player"""
        # Mock the players
        player0 = Mock(Player)
        players = [player0, None, None]
        # Initial button position
        self.assertEqual(self.dealer.button, 0)
        # Move button, should wrap around to first player since other players are None
        self.dealer.move_button(players)
        self.assertEqual(self.dealer.button, 0)

class TestTable(unittest.TestCase):
    def setUp(self) -> None:
        self.table = Table(seats=5)

    def test_seat_player(self) -> None:
        player = Mock(Player)
        self.table.seat_player(player=player, seat=2)
        self.assertEqual(self.table.seats[2], player)
    
    def test_seat_player_invalid_seat(self) -> None:
        """Test attempting to seat a player at an invalid seat"""
        player = Mock(Player)
        
        # Test negative seat index
        with self.assertRaises(IndexError, msg="Should raise error for negative seat index"):
            self.table.seat_player(player=player, seat=-1)
        
        # Test seat index larger than available seats
        with self.assertRaises(IndexError, msg="Should raise error for seat index larger than available seats"):
            self.table.seat_player(player=player, seat=6)
        
        # Test floating-point seat index
        with self.assertRaises(IndexError, msg="Should raise error for floating-point seat index"):
            self.table.seat_player(player=player, seat=2.5)

if __name__ == '__main__':
    unittest.main()
