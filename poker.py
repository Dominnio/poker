import random
import numpy as np
import time

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

def color_to_number(color):
  if(color == "C"):
    c = 0
  elif (color == "D"):
    c = 1
  elif (color == "H"):
    c = 2
  else:
    c = 3
  return c

class Card:
  def __init__(self, order, value, color):
    self.order = order
    self.value = value
    self.color = color
    self.numbered_value = value_to_number(value)
    self.numbered_color = color_to_number(color)

  def __str__(self):
    return (self.value + self.color)
  def __repr__(self):
    return str(self)
  def __lt__(self,other):
    x = self.numbered_value
    y = other.numbered_value
    return x < y
  def __gt__(self,other):
    x = self.numbered_value
    y = other.numbered_value
    return x > y
  def __le__(self,other):
    x = self.numbered_value
    y = other.numbered_value
    return x <= y
  def __ge__(self,other):
    x = self.numbered_value
    y = other.numbered_value
    return x >= y
  def __eq__(self,other):
    x = self.numbered_value
    y = other.numbered_value
    return x == y
  def __ne__(self,other):
    x = self.numbered_value
    y = other.numbered_value
    return x != y

class Deck:
  def __init__(self):
    self.cards = []
    self.cards.append(Card(0,"2","C"))
    self.cards.append(Card(1,"3","C"))
    self.cards.append(Card(2,"4","C"))
    self.cards.append(Card(3,"5","C"))
    self.cards.append(Card(4,"6","C"))
    self.cards.append(Card(5,"7","C"))
    self.cards.append(Card(6,"8","C"))
    self.cards.append(Card(7,"9","C"))
    self.cards.append(Card(8,"T","C"))
    self.cards.append(Card(9,"J","C"))
    self.cards.append(Card(10,"Q","C"))
    self.cards.append(Card(11,"K","C"))
    self.cards.append(Card(12,"A","C"))
    self.cards.append(Card(13,"2","D"))
    self.cards.append(Card(14,"3","D"))
    self.cards.append(Card(15,"4","D"))
    self.cards.append(Card(16,"5","D"))
    self.cards.append(Card(17,"6","D"))
    self.cards.append(Card(18,"7","D"))
    self.cards.append(Card(19,"8","D"))
    self.cards.append(Card(20,"9","D"))
    self.cards.append(Card(21,"T","D"))
    self.cards.append(Card(22,"J","D"))
    self.cards.append(Card(23,"Q","D"))
    self.cards.append(Card(24,"K","D"))
    self.cards.append(Card(25,"A","D"))
    self.cards.append(Card(26,"2","H"))
    self.cards.append(Card(27,"3","H"))
    self.cards.append(Card(28,"4","H"))
    self.cards.append(Card(29,"5","H"))
    self.cards.append(Card(30,"6","H"))
    self.cards.append(Card(31,"7","H"))
    self.cards.append(Card(32,"8","H"))
    self.cards.append(Card(33,"9","H"))
    self.cards.append(Card(34,"T","H"))
    self.cards.append(Card(35,"J","H"))
    self.cards.append(Card(36,"Q","H"))
    self.cards.append(Card(37,"K","H"))
    self.cards.append(Card(38,"A","H"))
    self.cards.append(Card(39,"2","S"))
    self.cards.append(Card(40,"3","S"))
    self.cards.append(Card(41,"4","S"))
    self.cards.append(Card(42,"5","S"))
    self.cards.append(Card(43,"6","S"))
    self.cards.append(Card(44,"7","S"))
    self.cards.append(Card(45,"8","S"))
    self.cards.append(Card(46,"9","S"))
    self.cards.append(Card(47,"T","S"))
    self.cards.append(Card(48,"J","S"))
    self.cards.append(Card(49,"Q","S"))
    self.cards.append(Card(50,"K","S"))
    self.cards.append(Card(51,"A","S"))

  def remove(self, card):
    for i in range(len(self.cards)):
      if(self.cards[i].order == card.order):
        del self.cards[i]
        break

  def __str__(self):
    s = ""
    for card in self.cards:
       s += str(card) + "\n"
    return s

def set_seq(cards):
  n = len(cards)
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
  col = [[],[],[],[]]
  for card in cards:
    col[card.numbered_color].append(card)
  return col

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
  return [1,seq[0][0],seq[1][0],seq[2][0],seq[3][0],seq[4][0]]

def check_three(seq):
  for s in seq:
    if(len(s) == 3):
      seq.remove(s)
      return [4,s,seq[0][0],seq[1][0]]
  return check_two_pair(seq)

def check_straight(seq,col):
  s = [seq[0][0]]
  for i in range(1,len(seq)):
    if(seq[i][0].numbered_value == seq[i-1][0].numbered_value - 1):
      s.append(seq[i][0])
      if(len(s) == 5):
        return [5, s]
    else:
      s = [seq[i][0]]
  
  if(len(s) == 4 and s[0].numbered_value == 5 and seq[0][0].numbered_value == 14):
    s.append(seq[0][0])
    return [5,s]
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
    if(seq[i][0].numbered_value == seq[i-1][0].numbered_value - 1):
      straight.append(seq[i][0])
      if(len(straight) == 5):
        flush = set_col(straight)
        for c in flush:
          if(len(c) == 5):
            return [9, straight]
    else:
      straight = [seq[i][0]]

  if(len(straight) == 4 and straight[0].numbered_value == 5 and seq[0][0].numbered_value == 14):
    straight.append(seq[0][0])
    flush = set_col(straight)
    for c in flush:
      if(len(c) == 5):
        ace = straight.pop(0)
        straight.append(ace)
        return [9, straight]

  return check_quads(seq,col)

def check(cards):
  cards.sort(reverse = True)
  seq = set_seq(cards)
  col = set_col(cards)
  layout = check_straight_flush(seq,col)
  return layout

def flat(layout):
  flat = []
  flat.append(layout[0])
  for i in range(1,len(layout)):
    if(isinstance(layout[i],list)):
      flat.append(layout[i][0].numbered_value)
    else:
      flat.append(layout[i].numbered_value)
  return flat

def compare(x, y):
  for i in range(len(x)):
    if(x[i] > y[i]):
      return True
    if(x[i] < y[i]):
      return False
  return None

def odds(cards,table,opponents):
  d = Deck()
  print(cards)
  d.remove(cards[0])
  d.remove(cards[1])
  print(d)

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

  def get_winner(self):
    table = [self.flop[0],self.flop[1],self.flop[2], self.turn, self.river]
    layout = []
    for player in self.players:
      layout.append(player.cards)
    save = layout.copy()
    n = len(layout)
    order = np.arange(n)
    flat_layout = []
    for i in range(len(self.players)):
      layout[i] = check(table + layout[i])
      flat_layout.append(flat(layout[i]))

    while n > 1:
      for i in range(n - 1):
        c = compare(flat_layout[i],flat_layout[i+1])
        if(c == False):
          tmp = flat_layout[i]
          flat_layout[i] = flat_layout[i+1]
          flat_layout[i+1] = tmp
          tmp = order[i]
          order[i] = order[i+1]
          order[i+1] = tmp
      n = n - 1
    ret_order = [[order[0]]]
    idx = 0
    for i in range(i,len(flat_layout) - 1):
      c = compare(flat_layout[i],flat_layout[i+1])
      if(c == None):
        ret_order[idx].append(order[i+1])
      else:
        ret_order.append([order[i+1]])
        idx += 1

    return [ret_order,layout]


  def set_cards(self):
    n = 5 + len(self.players)*2
    c = random.sample(range(52),n)
    self.flop = []
    self.flop.append(self.deck.cards[c[0]])
    self.flop.append(self.deck.cards[c[1]])
    self.flop.append(self.deck.cards[c[2]])
    self.turn = self.deck.cards[c[3]]
    self.river = self.deck.cards[c[4]]
    self.table = [self.flop,self.turn,self.river]
    i = 5
    for player in self.players:
      player.set_cards(self.deck.cards[c[i]], self.deck.cards[c[i+1]])
      i += 2
 
  def start_part(self):
    self.set_cards()
    table = []#[self.flop[0],self.flop[1],self.flop[2], self.turn, self.river]
    #self.blinds()
    #self.round_of_betting()
    odds(self.players[0].cards,table,5)
    result = self.get_winner()
    '''
    print("\n")
    print("table: " + str(self.table))
    print(result[0])
    for p in range(len(result[1])):
      for i in range(len(result[0])):
        for j in range(len(result[0][i])):
          if(result[0][i][j] == p):
            print(str(result[1][p]) + "\t\t position: " + str(i+1) + "\t cards:" + str(self.players[p].cards))
    '''
  def start_game(self):
    self.dealer = 0
    t = time.time()
    for i in range(10000):
      self.start_part()
    print(time.time() - t)
############################################

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

############################################

  




