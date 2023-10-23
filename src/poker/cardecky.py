import random

# Card and Deck classes combined into one file
# Uses dataclass and field for simplicity

class Card:
    def __init__(self, suit: str, rank: str) -> None:
        self.suit: str = suit
        self.rank: str = rank
        self.card: str = self.rank + self.suit

    def __repr__(self) -> str:
        return self.card


class Deck:
    def __init__(self) -> None:
        self.deck: list = []
        self.cards_used = 0
        self.suits: list[str] = ['C', 'H', 'D', 'S']
        self.ranks: list[str] = ['2', '3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K', 'A']
        self._initialize_deck()

    def _initialize_deck(self) -> None:
        for suit in self.suits:
            for rank in self.ranks:
                self.deck.append(Card(suit=suit, rank=rank))

    def shuffle(self) -> None:
        random.shuffle(self.deck)
        self.cards_used = 0

    def cardsLeft(self):
        return len(self.deck) - self.cards_used

    def deal_card(self):
        if self.cards_used >= len(self.deck):
            print("Error: There are no cards left in the deck.")
            return None
        else:
            self.cards_used += 1
            return self.deck[self.cards_used - 1]

    def deal_cards(self, num):
        if (self.cards_used + num) > len(self.deck):
            print("Error: There are not enough cards left in the deck.")
            return []
        else:
            deal = []
            for i in range(num):
                deal.append(self.deal_card())
            return deal

    def __str__(self) -> str:
        tmp_deck = "Deck: "
        for c in self.deck:
            tmp_deck += str(c) + " "
        return tmp_deck
    
class HandRanker:
    RANK_ORDER: list[str] = ['2', '3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K', 'A']
    
    @staticmethod
    def is_straight(cards) -> bool:
        indices: list[int] = sorted([HandRanker.RANK_ORDER.index(card.rank) for card in cards])
        return indices[2] - indices[1] == indices[1] - indices[0] == 1

    @staticmethod
    def is_flush(cards) -> bool:
        return len(set(card.suit for card in cards)) == 1

    @staticmethod
    def rank_counts(cards):
        ranks = [card.rank for card in cards]
        return {rank: ranks.count(rank) for rank in set(ranks)}
    
    @staticmethod
    def rank_hand(cards):
        if HandRanker.is_straight(cards) and HandRanker.is_flush(cards):
            return (1, sorted([card.rank for card in cards], key=lambda x: HandRanker.RANK_ORDER.index(x), reverse=True))
        
        counts = HandRanker.rank_counts(cards)
        if 3 in counts.values():
            return (2, [card.rank for card in cards if counts[card.rank] == 3][0])
        
        if HandRanker.is_straight(cards=cards):
            return (3, sorted([card.rank for card in cards], key=lambda x: HandRanker.RANK_ORDER.index(x), reverse=True))
        
        if HandRanker.is_flush(cards=cards):
            return (4, sorted([card.rank for card in cards], key=lambda x: HandRanker.RANK_ORDER.index(x), reverse=True))
        
        if 2 in counts.values():
            pair_card = [card.rank for card in cards if counts[card.rank] == 2][0]
            non_pair_card = [card.rank for card in cards if counts[card.rank] == 1][0]
            return (5, (pair_card, non_pair_card))
        
        return (6, sorted([card.rank for card in cards], key=lambda x: HandRanker.RANK_ORDER.index(x), reverse=True))
