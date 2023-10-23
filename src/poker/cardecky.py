import random

# Card and Deck classes combined into one file
# Uses dataclass and field for simplicity

class Card:
    def __init__(self, suit: str, rank: str):
        self.suit = suit
        self.rank = rank
        self.card = self.rank + self.suit

    def __repr__(self) -> str:
        return self.card


class Deck:
    deck: list = field(default_factory=list, init=False)
    cards_used: int = 0
    suits = ['C', 'H', 'D', 'S']
    ranks = ['2', '3', '4', '5', '6',
             '7', '8', '9', '0', 'J', 'Q', 'K', 'A']

    def __post_init__(self):
        for suit in self.suits:
            for rank in self.ranks:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)
        self.cards_used = 0

    def cardsLeft(self):
        return len(self.deck) - self.cards_used

    def deal_card(self):
        if self.cards_used >= len(self.deck):
            print("Error: There are no cards left in the deck.")
        else:
            self.cards_used += 1
            return self.deck[self.cards_used - 1]

    def deal_cards(self, num):
        if (self.cards_used + num) > len(self.deck):
            print("Error: There are not enough cards left in the deck.")
        else:
            deal = []
            for i in range(num):
                deal.append(self.deal_card())
            return deal

    def __str__(self):
        tmp_deck = "Deck: "
        for c in self.deck:
            tmp_deck += str(c) + " "
        return tmp_deck
