import random
import math
import csv

class Stats:

  def __init__(self):
    self.total_games = 0.
    self.total_hit_games = 0.
    self.total_stand_games = 0.
    self.hit_wins = 0.
    self.stand_wins = 0.
    self.total_double_games = 0.
    self.double_wins = 0.

  def export_stats(self):
    hit_win_ratio = self.hit_wins / max(self.total_hit_games,1)
    stand_win_ratio = self.stand_wins / max(self.total_stand_games,1)
    optimal_move = "hit"
    if hit_win_ratio < stand_win_ratio:
      optimal_move = "stay"
    return optimal_move

  def get_optimal(self):
    hit_win_ratio = self.hit_wins / max(self.total_hit_games,1)
    stand_win_ratio = self.stand_wins / max(self.total_stand_games,1)
    double_win_ratio = self.double_wins / max(self.total_double_games,1)

    if hit_win_ratio > stand_win_ratio and hit_win_ratio > double_win_ratio:
      return 0
    if stand_win_ratio > hit_win_ratio and stand_win_ratio > double_win_ratio:
      return 1
    else:
      return 2


  def decide_move(self, can_double):
    double_win_ratio = self.double_wins / max(self.total_double_games,1)

    options = ["hit","stay","double"]

    if can_double:
      optimal = self.get_optimal()
      options.pop(optimal)
      non_optimal_chance = .6666 * math.e ** -((self.total_games/1000) ** 2)
      prob = random.random()

      if prob < non_optimal_chance:
        prob = random.randint(0,1)
        if prob == 0:
          move = options[0]
        else:
          move = options[1]
      else:
          move = optimal
      return move



    else:
      hit_win_ratio = self.hit_wins / max(self.total_hit_games,1)
      stand_win_ratio = self.stand_wins / max(self.total_stand_games,1)
      optimal_move = "hit"
      non_optimal_move = "stay"

      if hit_win_ratio < stand_win_ratio:
        optimal_move = "stay"
        non_optimal_move = "hit"

      non_optimal_chance = .5 * math.e ** -((self.total_games/1000) ** 2)
      prob = random.random()

      if prob < non_optimal_chance:
        return non_optimal_move
      else:
        return optimal_move

class Tables:

  def __init__(self):
    self.no_ace = []
    self.ace = []
    #sum of players
    for i in range (2,12):
      #dealers card
      no_ace = []
      ace = []
      for j in range(2,22):
        no_ace.append(Stats())
        ace.append(Stats())
      self.no_ace.append(no_ace)
      self.ace.append(ace)

  def export_stats_table(self):
    for i in range(len(self.no_ace)):
      row = []
      for j in range(len(self.no_ace[i])):
        row.append("(" + str(i+2) + "," +str(j+2) + ") " + str(self.no_ace[i][j].export_stats()))
      with open('blackjack.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)

    for i in range(len(self.ace)):
      row = []
      for j in range(len(self.ace[i])):
        row.append("(" + str(i+2) + "," +str(j+2) + ") " + str(self.ace[i][j].export_stats()))
      with open('blackjack_ace.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)

class Card:

  def __init__(self,suit,rank):
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

  def __init__(self,deck,is_dealer,table):
    self.cards = [deck.remove_card(),deck.remove_card()]
    self.is_dealer = is_dealer
    self.deck = deck
    self.score = self.get_sum()
    self.table = table
    self.states = []

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

  def hit (self,dealer_card):
    card = self.deck.remove_card()
    self.cards.append(card)
    self.score = self.get_sum()
    if self.get_sum() <= 21:
      self.play(dealer_card)

  def stay (self):
    return self.get_sum()

  def double (self):
    card = self.deck.remove_card()
    self.cards.append(card)
    return self.get_sum()


  def split (self): pass



  def play (self,dealer_card):
    if self.is_dealer:
      while self.get_sum() < 17:
        card = self.deck.remove_card()
        self.cards.append(card)
        self.score = self.get_sum()
      return self.stay()

    else:
      has_ace = False
      for card in self.cards:
        if card.rank == "Ace":
          has_ace = True

      stat = None
      if has_ace:
        stat = self.table.no_ace[dealer_card.value -2][self.get_sum()-2]
      else:
        stat = self.table.ace[dealer_card.value -2][self.get_sum()-2]

      if (len(self.cards)>2):
        next_move = stat.decide_move(False)
      else:
        next_move = stat.decide_move(True)

      self.states.append((stat,next_move))

      #next move returns 1 for hit and 0 for stay and 2 for double
      if next_move == "hit":
        self.hit(dealer_card)
      if next_move == "double":
        self.double()
      else:
        self.stay()



class Game:

  def __init__(self, num_players,table):
    self.deck = Deck()
    self.num_players = num_players
    self.players = []
    self.table = table
    self.wins = 0
    for i in range(num_players):
      self.players.append(Player(self.deck,False,self.table))

    self.players.append(Player(self.deck,True,self.table))

  def update_stats(self,player,outcome):
    #outcome 0 = loss 1 = win 2 = push
    for stat in player.states:

      stat[0].total_games += 1

      #hit
      if stat[1] == "hit":
        stat[0].total_hit_games +=1
        if outcome == 1:
           stat[0].hit_wins +=1
        if outcome == 2:
            stat[0].hit_wins += 0.5
        return "hit"

      elif stat[1] == "double":
        stat[0].total_double_games += 1
        if outcome == 1:
          stat[0].double_wins +=2
        if outcome == 2:
          stat[0].double_wins += 1
        else:
          stat[0].total_double_games += 1

          return "double"

      #stand
      else:
        stat[0].total_stand_games += 1
        if outcome == 1:
          stat[0].stand_wins += 1
        if outcome == 2:
          stat[0].stand_wins += 0.5

        return "stand"

  def play(self):
    player_scores = []
    dealer_card = self.players[-1].cards[0]

    for player in self.players:
      player.play(dealer_card)

    dealer_score = self.players[-1].score
    # print "Dealer score is: " + str(self.players[-1].score)

    count = 0
    for player in self.players:
      # print "player: " + str(count)
      count +=1
      # for i in player.cards:
      #   print i.rank
      # print player.get_sum()
      # print "\n"

    #update stats for each players
    for i in range(self.num_players):
      score = self.players[i].score

      if ((dealer_score > score and dealer_score <= 21) or (score > 21)):
        self.update_stats(self.players[i],0)

        # print "Player: " + str(i) + "lost"
      elif dealer_score < score or dealer_score > 21 :
        updated = self.update_stats(self.players[i],1)
        self.wins += 1
        if updated == "double":
          # print "won on double"
          self.wins +=1

        # print "Player: " + str(i) + "won"
      else:
       # print "Player: " + str(i) + "pushed"
       self.wins += .5
       updated = self.update_stats(self.players[i],2)
       if updated == "double":
          print "pushed on double"
          self.wins += .5

    return self.wins


table = Tables()
total_wins = 0.
for i in range(300000):
  game = Game(10,table)
  total_wins += game.play()
  if i %10000 == 0:
    print "totalwin ratio " + str(total_wins/100000)
    total_wins = 0
table.export_stats_table()
