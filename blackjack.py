import random

class Card:

  def __init__(self,suit, rank):
    self.rank = rank[0]
    self.value = rank[1]
    self.suit = suit

  def __str__(self):
    return self.rank + " of " + self.suit

class Deck:

  def __init__(self):
    suits = ["Hearts", "Spades", "Clubs", "Diamonds"]
    ranks = [("Ace",11), ("King",10), ("Queen",10), ("Jack",10), ("Ten",10), ("Nine",9), ("Eight",8),     ("Seven",7), ("Six",6),("Five",5),("Four",4),("Three",3), ("Two",2), ("One",1)]

    self.cards = []
    for i in suits:
      for j in ranks:
        self.cards.append(Card(i,j))

  #return random card from deck
  def remove_card(self):
    index = random.randint(0,len(self.cards)-1)
    return self.cards.pop(index)


class Player:

  def __init__(self,deck,is_dealer):
    self.cards = [deck.remove_card(),deck.remove_card]
    self.is_dealer = is_dealer

  def get_sum(self):
    current_sum = 0
    for card in self.cards:
      current_sum += card.value

    #reduce value of ace from 11 to 1
    for card in self.cards:
      if card.rank == "Ace":
        current_sum -= 10
        if current_sum <= 21:
          break

    return current_sum




deck = Deck()
for i in range(0,52):
  card = deck.remove_card()
  print card



