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

  def export_stats(self):
    hit_win_ratio = self.hit_wins / max(self.total_hit_games,1)
    stand_win_ratio = self.stand_wins / max(self.total_stand_games,1)
    optimal_move = 1
    if hit_win_ratio < stand_win_ratio:
      optimal_move = 0
    return optimal_move

  def decide_move(self):

    hit_win_ratio = self.hit_wins / max(self.total_hit_games,1)
    stand_win_ratio = self.stand_wins / max(self.total_stand_games,1)
    optimal_move = 1
    non_optimal_move = 0

    if hit_win_ratio < stand_win_ratio:
      optimal_move = 0
      non_optimal_move = 1

    non_optimal_chance = .5 * math.e ** -((self.total_games/100) ** 2)
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

  def play(self,dealer_card):
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

        next_move = stat.decide_move()
        self.states.append((stat,next_move))

        #next move returns 1 for hit and 0 for stay
        if next_move == 1:
          self.hit(dealer_card)



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
      if stat[1] == 1:
        stat[0].total_hit_games +=1
        if outcome == 1:
           stat[0].hit_wins +=1
        if outcome == 2:
            stat[0].hit_wins += 0.5
      #stand
      else:
        stat[0].total_stand_games += 1
        if outcome == 1:
          stat[0].stand_wins += 1
        if outcome == 2:
          stat[0].stand_wins += 0.5

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
        self.update_stats(self.players[i],1)
        self.wins += 1
        # print "Player: " + str(i) + "won"
      else:
       # print "Player: " + str(i) + "pushed"
       self.wins += .5
       self.update_stats(self.players[i],2)

    return self.wins


table = Tables()
total_wins = 0.
for i in range(100000):
  game = Game(10,table)
  total_wins += game.play()
  if i %10000 == 0:
    print "totalwin ratio " + str(total_wins/100000)
    total_wins = 0
table.export_stats_table()
