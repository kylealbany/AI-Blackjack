import random

class Stats:

  def __init__(self):
    self.total_games = 0
    self.total_hit_games = 0
    self.total_stand_games = 0
    self.hit_wins = 0
    self.stand_wins = 0

  def decide_move(self): pass
    # while (total_games < 1000):
    #   #chosse randomly

    # hit_win_ratio = self.hit_wins / self.total_hit_games
    # stand_win_ratio - self.stand_wins / self.total_stand_games

    # optimal_move = if hit_win_ratio > stand_win_ratio: "hit" else: "stand"

    # non_optimal_chance = .5 - self.total_games




class Tables:

  def __init__(self):
    self.states_no_ace = []
    self.states_ace = []
    #sum of players
    for i in range (2,12):
      #dealers card
      no_ace = []
      ace = []
      for j in range(1,22):
        no_ace.append(Stats())
        ace.append(Stats())
      self.states_no_ace.append(no_ace)
      self.states_ace.append(ace)

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
    self.cards = [deck.remove_card(),deck.remove_card()]
    self.is_dealer = is_dealer
    self.deck = deck
    self.score = self.get_sum()

  def get_sum(self):
    current_sum = 0
    for card in self.cards:
      current_sum += card.value

    #reduce value of ace from 11 to 1
    for card in self.cards:
      if card.rank == "Ace":
        if current_sum <= 21:
          break
        current_sum -= 10

    return current_sum

  def hit (self):
    card = self.deck.remove_card()
    self.cards.append(card)
    self.score = self.get_sum()

  def stay (self):
    return get_sum()

  def play(self):
      while self.get_sum() <= 17:
        self.hit()

      return self.get_sum()

class Game:

  def __init__(self, num_players):
    self.deck = Deck()
    self.num_players = num_players
    self.players = []
    for i in range(num_players):
      self.players.append(Player(self.deck,False))

    self.players.append(Player(self.deck,True))


  def play(self):
    player_scores = []

    for player in self.players:
      player.play()

    dealer_score = self.players[-1].score
    print "Dealer score is: " + str(self.players[-1].score)

    count = 0
    for player in self.players:
      print "player: " + str(count)
      count +=1
      for i in player.cards:
        print i.rank
      print player.get_sum()
      print "\n"

    for i in range(self.num_players):
      score = self.players[i].score

      if ((dealer_score > score and dealer_score <= 21) or (score > 21)):
        print "Player: " + str(i) + "lost"
      elif dealer_score < score or dealer_score > 21 :
        print "Player: " + str(i) + "won"
      else:
       print "Player: " + str(i) + "pushed"



game = Game(15)
game.play()
# table = Table()


