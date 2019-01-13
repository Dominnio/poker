import random
import numpy as np

def value_to_number(value):
   if(value == "A"):
     return 14
   if(value == "K"):
     return 13
   if(value == "Q"):
     return 12
   if(value == "J"):
     return 11
   if(value == "T"):
     return 10
   return int(value)

class Card:
  def __init__(self, order, value, color):
    self.order = order
    self.value = value
    self.color = color

  def __str__(self):
    return (self.value + self.color)
  def __repr__(self):
    return str(self)
  def __lt__(self,other):
    x = value_to_number(self.value)
    y = value_to_number(other.value)
    return x < y
  def __gt__(self,other):
    x = value_to_number(self.value)
    y = value_to_number(other.value)
    return x > y
  def __le__(self,other):
    x = value_to_number(self.value)
    y = value_to_number(other.value)
    return x <= y
  def __ge__(self,other):
    x = value_to_number(self.value)
    y = value_to_number(other.value)
    return x >= y
  def __eq__(self,other):
    x = value_to_number(self.value)
    y = value_to_number(other.value)
    return x == y
  def __ne__(self,other):
    x = value_to_number(self.value)
    y = value_to_number(other.value)
    return x != y

class Deck:
  cards = []
  cards.append(Card(1,"2","C"))
  cards.append(Card(2,"3","C"))
  cards.append(Card(3,"4","C"))
  cards.append(Card(4,"5","C"))
  cards.append(Card(5,"6","C"))
  cards.append(Card(6,"7","C"))
  cards.append(Card(7,"8","C"))
  cards.append(Card(8,"9","C"))
  cards.append(Card(9,"T","C"))
  cards.append(Card(10,"J","C"))
  cards.append(Card(11,"Q","C"))
  cards.append(Card(12,"K","C"))
  cards.append(Card(13,"A","C"))
  cards.append(Card(14,"2","D"))
  cards.append(Card(15,"3","D"))
  cards.append(Card(16,"4","D"))
  cards.append(Card(17,"5","D"))
  cards.append(Card(18,"6","D"))
  cards.append(Card(19,"7","D"))
  cards.append(Card(20,"8","D"))
  cards.append(Card(21,"9","D"))
  cards.append(Card(22,"T","D"))
  cards.append(Card(23,"J","D"))
  cards.append(Card(24,"Q","D"))
  cards.append(Card(25,"K","D"))
  cards.append(Card(26,"A","D"))
  cards.append(Card(27,"2","H"))
  cards.append(Card(28,"3","H"))
  cards.append(Card(29,"4","H"))
  cards.append(Card(30,"5","H"))
  cards.append(Card(31,"6","H"))
  cards.append(Card(32,"7","H"))
  cards.append(Card(33,"8","H"))
  cards.append(Card(34,"9","H"))
  cards.append(Card(35,"T","H"))
  cards.append(Card(36,"J","H"))
  cards.append(Card(37,"Q","H"))
  cards.append(Card(38,"K","H"))
  cards.append(Card(39,"A","H"))
  cards.append(Card(40,"2","S"))
  cards.append(Card(41,"3","S"))
  cards.append(Card(42,"4","S"))
  cards.append(Card(43,"5","S"))
  cards.append(Card(44,"6","S"))
  cards.append(Card(45,"7","S"))
  cards.append(Card(46,"8","S"))
  cards.append(Card(47,"9","S"))
  cards.append(Card(48,"T","S"))
  cards.append(Card(49,"J","S"))
  cards.append(Card(50,"Q","S"))
  cards.append(Card(51,"K","S"))
  cards.append(Card(52,"A","S"))

  def get_card(self, num):
    return self.cards[num]
  def __str__(self):
    s = ""
    for card in self.cards:
       s += str(card) + "\n"
    return s

def set_seq(cards):
  n = len(cards)
  while n > 1:
    for i in range(n - 1):
      if(cards[i] < cards[i+1]):
        tmp = cards[i]
        cards[i] = cards[i+1]
        cards[i+1] = tmp
    n = n - 1
  seq = [[cards[0]]]
  seq_idx = 0
  for i in range(1,len(cards)):
    if(cards[i] == cards[i-1]):
      seq[seq_idx].append(cards[i])
    else:
      seq.append([cards[i]])
      seq_idx += 1
  return seq

def set_col(cards):
  n = len(cards)
  while n > 1:
    for i in range(n - 1):
      if(cards[i] < cards[i+1]):
        tmp = cards[i]
        cards[i] = cards[i+1]
        cards[i+1] = tmp
    n = n - 1
  col = [[],[],[],[]]
  for card in cards:
    if(card.color == "C"):
      c = 0
    elif (card.color == "D"):
      c = 1
    elif (card.color == "H"):
      c = 2
    else:
      c = 3
    col[c].append(card)
  return col

def check_high_card(seq):
  return [1,seq[0][0],seq[1][0],seq[2][0],seq[3][0],seq[4][0]]

def check_two_pair(seq):
  seq_tmp = seq
  for s in seq_tmp: 
    if(len(s) == 2):
      seq_tmp.remove(s)
      for ss in seq:
        if(len(ss) == 2):
          seq_tmp.remove(ss)
          return [3,s,ss,seq[0][0]]
      return [2,s,seq[0][0],seq[1][0],seq[2][0]]
  return check_high_card(seq)

def check_three(seq):
  for s in seq:
    if(len(s) == 3):
      seq.remove(s)
      return [4,s,seq[0][0],seq[1][0]]
  return check_two_pair(seq)

def check_straight(seq,col):
  s = [seq[0][0]]
  for i in range(1,len(seq)):
    if(value_to_number(seq[i][0].value) == value_to_number(seq[i-1][0].value) - 1):
      s.append(seq[i][0])
      if(len(s) == 5):
        return [5, s]
    else:
      s = [seq[i][0]]
  return check_three(seq)

def check_flush(seq,col):
  for c in col:
    if(len(c) >= 5):
      return [6,c[:5]]
  return check_straight(seq,col)
      
def check_full_house(seq,col):
  three = None
  for s in seq:
    if(len(s) == 3):
      three = s
  if(three):
    for ss in seq:
      if(len(ss) >= 2 and ss[0] != three[0]):
        return [7,three,ss[:2]]
  return check_flush(seq,col)

def check_quads(seq,col):
  for s in seq:
    if(len(s) == 4):
      seq.remove(s)   
      return [8, s, seq[0][0]]
  return check_full_house(seq,col)

def check_straight_flush(seq,col):
  straight = [seq[0][0]]
  for i in range(1,len(seq)):
    if(value_to_number(seq[i][0].value) == value_to_number(seq[i-1][0].value) - 1):
      straight.append(seq[i][0])
      if(len(straight) == 5):
        flush = set_col(straight)
        for c in flush:
          if(len(c) == 5):
            return [9, straight]
    else:
      s = [seq[i][0]]
  return check_quads(seq,col)

def check(cards):
  seq = set_seq(cards)
  col = set_col(cards)
  layout = check_straight_flush(seq,col)
  return layout

def compare(cards_x, cards_y, table):
  x = check(table + cards_x)
  y = check(table + cards_y)
  if(x[0] > y[0]):
    return [1,x,y]
  if(x[0] < y[0]):
    return [-1,x,y]
  
  if(x[0] == 9 or x[0] == 6):
    for (card_x,card_y) in zip(x[1],x[1]):
      if(card_x > card_y):
        return [1,x,y]
      if(card_x < card_y):
        return [-1,x,y]
    return [0,x,y]

  for i in range(1,len(x)):
    if(isinstance(x[i],list)):
      if(x[i][0] > y[i][0]):
        return [1,x,y]
      if(x[i][0] < y[i][0]):
        return [-1,x,y]
    else:
      if(x[i] > y[i]):
        return [1,x,y]
      if(x[i] < y[i]):
        return [-1,x,y]
  return [0,x,y]

def get_winner(cards, table):
  save = cards.copy()
  order = np.arange(len(cards))
  n = len(cards)
  while n > 1:
    for i in range(n - 1):
      c = compare(cards[i],cards[i+1],table)[0]
      if(c == -1):
        tmp = cards[i]
        cards[i] = cards[i+1]
        cards[i+1] = tmp
        tmp = order[i]
        order[i] = order[i+1]
        order[i+1] = tmp
    n = n - 1
  ret_order = [[order[0]]]
  idx = 0
  for i in range(i,len(cards) - 1):
    c = compare(cards[i],cards[i+1],table)[0]
    if(c == 0):
      ret_order[idx].append(order[i+1])
    else:
      ret_order.append([order[i+1]])
      idx += 1
  for i in range(len(save)): 
    cards[i] = check(table + save[i])
  return [ret_order,cards]

def odds(cards, table, opponents):
  deck = Deck()
  deck.cards.pop(cards[0].order - 1)
  deck.cards.pop(cards[1].order - 1)
  for i in range(len(table)):
    deck.cards.pop(table[i].pop(table[i].order - 1))

  players = []
  for i in range(int(len(opponents))):
    players.append(Player(int(200)))

  for i in range(1000):
    n = len(opponents)*2
    c = random.sample(range(len(deck)),n)
    for player in self.players:
      player.set_cards(deck.get_card(c[i]), deck.get_card(c[i+1]))
      i += 2
    

class Player:
  def __init__(self, stack):
    self.stack = stack
    self.cards = []
    self.paid = 0
    self.is_active = True
    self.done = 0
  def __str__(self):
    s = ("chips: " + str(self.stack))
    if(len(self.cards) != 0):
      s += ", cards: " + str(self.cards[0]) + " " + str(self.cards[1])
    else:
      s += ", cards: -"
    return s
  def set_cards(self, card_1, card_2):
    self.cards = []
    self.cards.append(card_1)
    self.cards.append(card_2)
  def bet(self,bet):
    self.stack -= bet
    self.paid += bet
    return self.paid
  def take(self,prize):
    self.stack += prize

class Table:
  def __init__(self,players,sb,bb,ante,game_type):
    self.deck = Deck()
    self.players = players
    self.sb = sb
    self.bb = bb
    self.ante = ante
    self.game_type = game_type

  def set_cards(self):
    n = 5 + len(self.players)*2
    c = random.sample(range(52),n)
    self.flop = []
    self.flop.append(self.deck.get_card(c[0]))
    self.flop.append(self.deck.get_card(c[1]))
    self.flop.append(self.deck.get_card(c[2]))
    self.turn = self.deck.get_card(c[3])
    self.river = self.deck.get_card(c[4])
    i = 5
    for player in self.players:
      player.set_cards(self.deck.get_card(c[i]), self.deck.get_card(c[i+1]))
      i += 2

  def blinds(self):
    self.pot = 0
    if(len(players) == 2):
      self.players[self.dealer].bet(self.sb)
      self.players[(self.dealer+1)%2].bet(self.bb)
      self.active = self.dealer
    else:
      self.players[(self.dealer+1)%len(self.players)].bet(self.sb)
      self.players[(self.dealer+2)%len(self.players)].bet(self.sb)
      self.active = (self.dealer+3)%len(self.players)
    self.pot += sb
    self.pot += bb
    self.highest = bb

  def round_of_betting(self):
    while(True):
      for i in range(self.active, len(self.players)):
        if(not self.players[i].is_active):
          continue
        action = random.randint(0,2)
        if(action == 0):
          bet = self.highest + random.randint(0,self.players[i].stack + 1)
          if(bet < self.players[i].stack):
            self.highest = self.players[i].bet(bet)
            self.players[i].done = True
        if(action == 1):
          bet_to_check = self.highest - self.players[i].paid
          if(bet_to_check <= self.players[i].stack):
            self.players[i].bet(bet_to_check)
            self.players[i].done = True
        if(action == 2):
          self.players[i].done = True
          self.players[i].is_active = False
        
      for i in range(self.active):
        if(not self.players[i].is_active):
          continue
        action = random.randint(0,2)
        if(action == 0):
          bet = self.highest + random.randint(0,self.players[i].stack + 1)
          if(bet < self.players[i].stack):
            self.highest = self.players[i].bet(bet)
            self.players[i].done = True
        if(action == 1):
          bet_to_check = self.highest - self.players[i].paid
          if(bet_to_check <= self.players[i].stack):
            self.players[i].bet(bet_to_check)
            self.players[i].done = True
        if(action == 2):
          self.players[i].done = True
          self.players[i].is_active = False
      
      flag = True
      for player in players:
        print(player.done)
        if(not player.done):
          flag = False
      if(not flag):
        continue
      else:
        break
 
  def start_part(self):
    self.set_cards()
    self.blinds()
    self.round_of_betting()
    
    #print("flop: 1" + str(main.flop[0]) + " " + str(main.flop[1]) + " " + str(main.flop[2]))
    #print("turn: " + str(main.turn))
    #print("river: "+ str(main.river) + "\n")
    #print(main.players)
    table = [self.flop[0],self.flop[1],self.flop[2], self.turn, self.river]
    cards_x = [self.players[0].cards[0], self.players[0].cards[1]]
    cards_y = [self.players[1].cards[0], self.players[1].cards[1]]
    cards_z = [self.players[2].cards[0], self.players[2].cards[1]]
    result = get_winner([cards_x,cards_y,cards_z],table)
  
  def start_game(self):
    self.dealer = 0
    for i in range(1):
      self.start_part()

n 	= 6	#input("Number of players: ")
c 	= 300	#input("Players chips: ")
sb 	= 1	#input("Small blind: ")
bb 	= 2	#input("Big blind: ")
ante 	= 0	#input("Ante: ")
gtype	= 0
players = []
for i in range(int(n)):
  players.append(Player(int(c)))

Table(players,sb,bb,ante,gtype).start_game();

  




