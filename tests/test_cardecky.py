import unittest
from unittest.mock import patch
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
            Rank.JACK: "J",
            Rank.QUEEN: "Q",
            Rank.KING: "K",
            Rank.ACE: "A"
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

class TestDeck(unittest.TestCase):
    def test_initial_deck_size(self) -> None:
        deck = Deck()
        self.assertEqual(deck.cardsLeft(), 52)

    def test_shuffle_resets_cards_used(self) -> None:
        deck = Deck()
        deck.cards_used = 5
        deck.shuffle()
        self.assertEqual(deck.cardsLeft(), 52)

    def test_deal_card(self):
        deck = Deck()
        card = deck.deal_card()
        self.assertIsInstance(card, Card)
        self.assertEqual(deck.cardsLeft(), 51)

    def test_deal_card_empty_deck(self):
        deck = Deck()
        deck.cards_used = 52
        card = deck.deal_card()
        self.assertIsNone(card)

class TestHandRanker(unittest.TestCase):
    def test_rank_value(self):
        card = Card(Rank.FOUR, Suit.CLUBS)
        self.assertEqual(HandRanker.rank_value(card), 4)

    def test_is_straight_true(self):
        cards = [Card(Rank.FIVE, Suit.CLUBS), Card(Rank.SIX, Suit.DIAMONDS), Card(Rank.SEVEN, Suit.HEARTS)]
        self.assertTrue(HandRanker.is_straight(cards))

    def test_is_flush_true(self):
        cards = [Card(Rank.TWO, Suit.CLUBS), Card(Rank.SIX, Suit.CLUBS), Card(Rank.SEVEN, Suit.CLUBS)]
        self.assertTrue(HandRanker.is_flush(cards))

if __name__ == '__main__':
    unittest.main()