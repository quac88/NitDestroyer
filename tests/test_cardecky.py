import unittest
from unittest.mock import patch
from src.poker.cardecky import Card, Deck, Rank, Suit, HandRanker

class TestCard(unittest.TestCase):
    def test_card_representation(self) -> None:
        card = Card(Rank.ACE, Suit.SPADES)
        self.assertEqual(repr(card), "ACES")

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