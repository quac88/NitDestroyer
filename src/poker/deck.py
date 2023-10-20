# deck.py
#
# Created by Thomas Nelson on 2014-04-12, tn90ca@gmail.com
#
# This class was developed for public use as part of the 
# Cards package.

import random
from .card import Card

 # The Deck class is used to represent a deck of playing
 # cards each card has a suit and a rank. The deck is 
 # capable of being shuffled and dealing one card at a
 # time.
class Deck:
  
   # Class initializer method creates a new unshuffled deck
   # of cards with all suits and ranks. This deck does not
   # include jokers.
   #
   # @param self  This is a default python class argument
  def __init__(self):
    self.deck = []     # Actual deck representation
    self.cardsUsed = 0 # Keeps track of the cards dealt
  
    self.suits = ['C','H','D','S']
    self.ranks = ['2','3','4','5','6','7','8','9','0','J','Q','K','A']
  
    for suit in self.suits:
      for rank in self.ranks:
        self.deck.append(Card(suit,rank))
  # end def __init__
  
   # Method puts all cards back in the deck and then
   # shuffles the deck.
   #
   # @param self  This is a default python class argument
  def shuffle(self):
    random.shuffle(self.deck)
    self.cardsUsed = 0
  #end def shuffle

   # Method returns the number of cards left in the deck
   # that can be dealt.
   #
   # @param  self       This is a default python class argument
   # @return cardsLeft  This is the number of cards left in the deck
  def cardsLeft(self):
    return len(self.deck) - self.cardsUsed  # Corrected usage
  
  def dealCard(self):
    if self.cardsUsed >= len(self.deck):  # Corrected usage
        print("Error: There are no cards left in the deck.")
    else:
        self.cardsUsed += 1
        return self.deck[self.cardsUsed - 1]  # Corrected usage
        
  def dealCards(self, num):
    if (self.cardsUsed + num) > len(self.deck):  # Corrected usage
        print("Error: There are not enough cards left in the deck.")
    else:
        deal = []
        for i in range(num):
            deal.append(self.dealCard())  # Corrected usage
        return deal
  # end def dealCards

   # When print is called on a deck this method will return
   # the list of cards in the deck as a string representation
   # of each cards suit and rank.
   #
   # @param  self  This is is a default python class argument
   # @return deck  This returns the entire deck to be printed 
  def __str__(self):
    tmpDeck = "Deck: "
    for c in self.deck:
      tmpDeck += str(c) + " "
    return tmpDeck
  # end def __str__
    
# end class Deck