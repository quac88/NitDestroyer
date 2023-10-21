from poker.deck import Deck

class Pot:
    def __init__(self) -> None:
        self.total: float = 0

    def reset_pot(self) -> None:
        self.total = 0
    
    def add_to_pot(self, amount: float) -> None:
        self.total += amount

    def award_pot(self, player) -> None:
        player.stack += self.total

    def split_pot(self, players: list) -> None:
        for player in players:
            player.stack += self.total / len(players)
        

class Dealer:
    def __init__(self, deck, pot) -> None:
        self.pot: float = pot
        self.deck = deck
        self.current_bet = 0
        self.button = 0

    # Rhode Island Hold'em
    def deal_hand(self, players) -> None:
        for player in players:
            if player is not None:  # Only deal to non-empty seats
                player.hand = self.deck.dealCards(1)


    def move_button(self, players: list) -> None:
        self.button = (self.button + 1) % len(players)

    # we don't need blind setting functions for now

class Player:
    def __init__(self, name, stack, hand, status, chips_in_play) -> None:
        self.name: str = name
        self.stack: float = stack # change to integer later
        self.hand = hand
        self.status: bool = status
        self.bet: float = chips_in_play

    def __str__(self) -> str:
        return self.name
    
    def post_ante(self, ante) -> None:
        self.stack -= ante
        self.bet += ante

class Table:
    def __init__(self, seats) -> None:
        self.seats = seats
        self.seats: list[None] = [None] * seats
    
    def __str__(self) -> str:
        return str(self.seats)
    
    def seat_player(self, player, seat) -> None:
        self.seats[seat] = player

    





    










