import unittest
from unittest.mock import patch
from itertools import product
from src.poker.cardecky import Card, Deck, Rank, Suit, HandRanker

class TestCard(unittest.TestCase):
    def test_card_representation(self) -> None:
        'Dictionary to map each Rank to its expected string representation'
        rank_to_string = {
            Rank.TWO: "2",
            Rank.THREE: "3",
            Rank.FOUR: "4",
            Rank.FIVE: "5",
            Rank.SIX: "6",
            Rank.SEVEN: "7",
            Rank.EIGHT: "8",
            Rank.NINE: "9",
            Rank.TEN: "10",
            Rank.JACK: "11",
            Rank.QUEEN: "12",
            Rank.KING: "13",
            Rank.ACE: "14"
        }
        'Dictionary to map each Suit to its expected string representation'
        suit_to_string = {
            Suit.HEARTS: "H",
            Suit.DIAMONDS: "D",
            Suit.CLUBS: "C",
            Suit.SPADES: "S"
        }
        
        'Loop through each rank and suit to test the representation of each card'
        for rank, rank_str in rank_to_string.items():
            for suit, suit_str in suit_to_string.items():
                # Create a Card object
                card = Card(rank=rank, suit=suit)
                # Construct the expected representation of the card
                expected_repr = f"{rank_str}{suit_str}"
                # Check if the actual representation matches the expected representation
                self.assertEqual(repr(card), expected_repr)

"""Test the Deck class."""
class TestDeck(unittest.TestCase):
    """Test the initial size of the deck."""
    def test_initial_deck_size(self) -> None:
        deck = Deck()
        self.assertEqual(deck.cardsLeft(), 52)

    """Test the size of the deck after shuffling."""
    def test_shuffle_resets_cards_used(self) -> None:
        deck = Deck()
        deck.cards_used = 5
        deck.shuffle()
        self.assertEqual(deck.cardsLeft(), 52)

    """Test the size of the deck after dealing a card."""
    def test_deal_card(self) -> None:
        deck = Deck()
        card: Card = deck.deal_card()
        self.assertIsInstance(card, Card)
        self.assertEqual(deck.cardsLeft(), 51)

    """Test that None is returned after all the cards have been dealt."""
    def test_deal_card_empty_deck(self) -> None:
        deck = Deck()
        deck.cards_used = 52
        card = deck.deal_card()
        self.assertIsNone(card)

"""Test the HandRanker class."""
class TestHandRanker(unittest.TestCase):
    """Test the rank_value method."""
    def test_rank_value_for_all_cards(self) -> None:
        # Iterate through all ranks in the Rank enum
        for rank in Rank:
            # For each rank, create a card with a fixed suit (e.g., CLUBS)
            card = Card(rank=rank, suit=Suit.CLUBS)
            # Call the rank_value method and check if it returns the correct value
            self.assertEqual(HandRanker.rank_value(card), rank.value,
                             f"Failed for card: {repr(card)}")

    def test_is_straight_true(self) -> None:
        all_ranks: list[Rank] = [Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE, Rank.SIX, 
                     Rank.SEVEN, Rank.EIGHT, Rank.NINE, Rank.TEN, Rank.JACK, 
                     Rank.QUEEN, Rank.KING, Rank.ACE]

        # Test all consecutive 5-card straights
        for i in range(len(all_ranks) - 4):
            cards: list[Card] = [Card(rank=all_ranks[j], suit=Suit.CLUBS) for j in range(i, i + 5)]
            self.assertTrue(HandRanker.is_straight(cards))

        # Test A2345 straight
        cards = [Card(rank=Rank.ACE, suit=Suit.CLUBS), Card(rank=Rank.TWO, suit=Suit.DIAMONDS), 
                 Card(rank=Rank.THREE, suit=Suit.HEARTS), Card(rank=Rank.FOUR, suit=Suit.SPADES), 
                 Card(rank=Rank.FIVE, suit=Suit.CLUBS)]
        self.assertTrue(HandRanker.is_straight(cards))

    def test_is_flush_true(self) -> None:
        all_ranks: list[Rank] = [Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE, Rank.SIX, 
                     Rank.SEVEN, Rank.EIGHT, Rank.NINE, Rank.TEN, Rank.JACK, 
                     Rank.QUEEN, Rank.KING, Rank.ACE]

        all_suits: list[Suit] = [Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]

        # Test all possible flushes
        for suit in all_suits:
            for ranks_combination in product(all_ranks, repeat=5):
                cards = [Card(rank, suit) for rank in ranks_combination]
                self.assertTrue(HandRanker.is_flush(cards))

    def test_is_three_of_a_kind_true(self):
        # Iterate over all ranks for the three similar cards
        for rank in Rank:
            # Generate two cards of different ranks
            other_cards = [Card(other_rank, suit) for other_rank, suit in product(Rank, Suit) if other_rank != rank][:2]
            # Generate the three cards of the same rank
            three_of_a_kind_cards = [Card(rank, suit) for suit in Suit][:3]
            # Combine and test
            cards = three_of_a_kind_cards + other_cards
            self.assertTrue(HandRanker.is_three_of_a_kind(cards))


if __name__ == '__main__':
    unittest.main()