import random
from enum import Enum
from typing import List

class Rank(Enum):
    """Rank of a card."""
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

class Suit(Enum):
    """Suit of a card."""
    CLUBS = 'C'
    DIAMONDS = 'D'
    HEARTS = 'H'
    SPADES = 'S'

class Card:
    def __init__(self, rank: Rank, suit: Suit) -> None:
        self.rank: Rank = rank
        self.suit: Suit = suit

    def __repr__(self) -> str:
        """Representation of a card."""
        return f"{self.rank.value}{self.suit.value}"
class Deck:
    def __init__(self) -> None:
        self.deck = [Card(rank, suit) for rank in Rank for suit in Suit]
        self.cards_used = 0

    def shuffle(self) -> None:
        """Shuffle the deck."""
        random.shuffle(self.deck)
        self.cards_used = 0

    def cardsLeft(self) -> int:
        """Return the number of cards left in the deck."""
        return len(self.deck) - self.cards_used

    def deal_card(self) -> Card:
        """Deal a card from the deck."""
        if self.cards_used >= len(self.deck):
            print("Error: There are no cards left in the deck.")
            return None
        else:
            self.cards_used += 1
            return self.deck[self.cards_used - 1]

    def deal_cards(self, num):
        """Deal a number of cards from the deck."""
        if (self.cards_used + num) > len(self.deck):
            print("Error: There are not enough cards left in the deck.")
            return []
        else:
            deal = []
            for i in range(num):
                card = self.deal_card()
                if card:
                    deal.append(card)
            return deal

    def __str__(self) -> str:
        """Representation of the deck."""
        tmp_deck = "Deck: "
        for c in self.deck:
            tmp_deck += str(c) + " "
        return tmp_deck

class HandRanker:
    @staticmethod
    def rank_value(card):
        """Return the value of a card."""
        return card.rank.value
    
    @staticmethod
    def rank_counts(cards):
        """Return a dictionary of the rank counts."""
        ranks = [card.rank for card in cards]
        return {rank: ranks.count(rank) for rank in set(ranks)}
    
    @staticmethod
    def is_straight(cards: List['Card']) -> bool:
        """Return True if the cards are a straight, False otherwise."""
        ranks = [card.rank.value for card in cards]
        sorted_ranks = sorted(ranks)
        # Check for regular straight
        if sorted_ranks[-1] - sorted_ranks[0] == len(cards) - 1 and len(set(ranks)) == len(cards):
            return True
        # Check for A2345 straight (the wheel)
        if set(sorted_ranks) == {14, 2, 3, 4, 5}:
            return True
        return False

    @staticmethod
    def is_flush(cards) -> bool:
        """Return True if the cards are a flush, False otherwise."""
        return len(set(card.suit for card in cards)) == 1
    
    @staticmethod
    def is_straight_flush(cards) -> bool:
        return HandRanker.is_straight(cards=cards) and HandRanker.is_flush(cards=cards)
    
    @staticmethod
    def is_three_of_a_kind(cards) -> bool:
        counts = HandRanker.rank_counts(cards=cards)
        return any(count == 3 for count in counts.values())
    
    @staticmethod
    def is_pair(cards) -> bool:
        counts = HandRanker.rank_counts(cards=cards)
        return any(count == 2 for count in counts.values())

    @staticmethod
    def rank_hand(cards):
        if HandRanker.is_straight_flush(cards=cards):
            return (1, max(cards, key=HandRanker.rank_value).rank)
        
        if HandRanker.is_three_of_a_kind(cards=cards):
            three_card = next(card for card, count in HandRanker.rank_counts(cards).items() if count == 3)
            return (2, three_card)
        
        if HandRanker.is_straight(cards=cards):
            return (3, max(cards, key=HandRanker.rank_value).rank)
        
        if HandRanker.is_flush(cards=cards):
            sorted_flush_cards = tuple(sorted(cards, key=HandRanker.rank_value, reverse=True))
            return (4, *sorted_flush_cards)
        
        if HandRanker.is_pair(cards=cards):
            pair_card = next(card for card, count in HandRanker.rank_counts(cards=cards).items() if count == 2)
            non_pair_cards = sorted([card for card in cards if card.rank != pair_card], key=HandRanker.rank_value, reverse=True)
            return (5, pair_card, non_pair_cards[0].rank)
        
        high_cards = tuple(sorted(cards, key=HandRanker.rank_value, reverse=True))
        return (6, *high_cards)
    

