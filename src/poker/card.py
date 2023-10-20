# card.py
#
# Created by Thomas Nelson on 2014-04-12, tn90ca@gmail.com
#
# This class was developed for public use as part of the 
# Cards package.

 # The Card class is used to represent a single playing card
 # from a deck of 52 or 54. The card has a suit and a rank.
class Card:

   # Class initializer method creates a new playing card with
   # a desired rank and suit provided through the creation
   # parameters.
   #
   # @param self  This is a default python class argument
   # @param suit  Card suit denoted by char (C,H,D,S)
   # @param rank  Card rank denoted by char (2,3,4,5,6,7,8,9,0,J,Q,K,A)
  def __init__(self,suit,rank):
    self.suit = suit
    self.rank = rank
    self.card = rank + suit
  # end def __init__
    
   # Method returns the class rank as a character
   # 2,3,4,5,6,7,8,9,0,J,Q,K,A
   #
   # @param  self  This is a default python class argument
   # @return rank  Returns the rank of the card
  def getRank(self):
    return self.rank
  # end def getRank

   # Method returns the class suit as a character
   # C,H,D,S
   #
   # @param  self  This is a default python class argument
   # @return suit  Returns the suit of the card
  def getSuit(self):
    return self.suit
  # end def getSuit
    
   # When print is called on a card this method will return
   # the card as a string representation of its suit and
   # rank. (i.e. 3C,AH,0D,KS)
   #
   # @param  self  This is is a default python class argument
   # @return card  Returns the card as a string
  def __str__(self):
    return self.card
  # end def __str__
  
# end class Card