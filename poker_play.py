import random
import numpy

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

class Player:
  def __init__(self, stack):
    self.stack = stack
    self.cards = []
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

class Players:
  players = []
  def add(self, player):
     self.players.append(player)
  def remove(self, player):
     self.players.remove(player)
  def __str__(self):
    s = ""
    for players in self.players:
       s += str(players) + "\n"
    return s
  def __len__(self):
    return len(self.players)

class Table:
  deck = Deck()
  players = Players()
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
    for player in self.players.players:
      player.set_cards(self.deck.get_card(c[i]), self.deck.get_card(c[i+1]))
      i += 2

def check_high_card(cards):
  n = len(cards)
  while n > 1:
    for i in range(n - 1):
      if(cards[i] < cards[i+1]):
        tmp = cards[i]
        cards[i] = cards[i+1]
        cards[i+1] = tmp
    n = n - 1
  return [0, cards[:len(cards)]]

def check_one_pair(cards):
  cards = check_high_card(cards)
  for card in cards[1]:
    count = 0 
    for other in cards[1]:
      if(card == other and card.color != other.color):
        same = other
        count += 1
      if(count == 1):
        cards[1].remove(same)
        cards[1].remove(card)
        return [1,[card,same], cards[1]]
  return cards

def check_two_pairs(cards):
  first = check_one_pair(cards)
  if(first[0] == 0):
    return first
  second = check_one_pair(first[2])
  if(second[0] == 0):
    return first
  else:
    if(first[1][0] < second[1][0]):
      tmp = first
      first = second
      second = tmp
    return [2,first[1],second[1],second[2]]

def check_three_of_a_kind_AND_full_AND_quads(cards):
  pairs = check_two_pairs(cards)
  if(pairs[0] == 0):
    return pairs
  if(pairs[0] == 1):
    for card in pairs[2]:
      if(card == pairs[1][0]):
        pairs[1].append(card)
        pairs[2].remove(card)
        return [3, pairs[1], pairs[2]]
    return pairs
  if(pairs[0] == 2):
    if(pairs[1][0] == pairs[2][0]):
      pairs[1].append(pairs[2][0])
      pairs[1].append(pairs[2][1])
      return [8, pairs[1], pairs[3]]
    one = check_one_pair(pairs[3])
    if(one[0] == 1):
      if(one[1][0] == pairs[2][0]):
        one[1].append(pairs[2][0])
        one[1].append(pairs[2][1])
        rest = pairs[3]
        rest.append(pairs[1][0])
        rest.append(pairs[1][0])
        rest.remove(one[1][0])
        rest.remove(one[1][0])
        rest = check_high_card(rest)
        return [7, one[1], rest[1]]
  if(pairs[0] == 2):
    for card in pairs[3]:
      if(card == pairs[1][0]):
        pairs[1].append(card)
        pairs[3].remove(card)
        return [6, pairs[1], pairs[2], pairs[3]]
    return pairs

def check_straight(cards):
  n = len(cards)
  while n > 1:
    for i in range(n - 1):
      if(cards[i] < cards[i+1]):
        tmp = cards[i]
        cards[i] = cards[i+1]
        cards[i+1] = tmp
    n = n - 1
  flag = True
  for i in range(3):
    for j in range(5):
      print(i+j)
      print(i+j+1)
      if(cards[i+j] == cards[i+j+1]):
        continue
      else:
        flag = False
        break
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    if(flag):
      rest = []
      for k in range(i):
        rest.append(cards[k])
      for j in range(7):
        rest.append(cards[j])
      return [4, [cards[i],cards[i+1],cards[i+2],cards[i+3],cards[i+4]], rest]
  return check_three_of_a_kind_AND_full_AND_quads(cards)
  

def check(set_of_cards):
  #check_royal_flush(a,b,c,d,e,f,g) # 9
  #check_straight_flush(a,b,c,d,e,f,g) # 8
  #check_flush(a,b,c,d,e,f,g) # 5
  c = check_straight(set_of_cards) # 4
  print(c)
  return c[0]

def start_game():
  main = Table()
  main.players.add(Player(200))
  
  w = 0;
  while w != 4:
    main.set_cards()
    print("flop: " + str(main.flop[0]) + " " + str(main.flop[1]) + " " + str(main.flop[2]))
    print("turn: " + str(main.turn))
    print("river: "+ str(main.river) + "\n")
    print(main.players)
    set_of_cards = [main.flop[0],main.flop[1],main.flop[2], main.turn, main.river, main.players.players[0].cards[0], main.players.players[0].cards[1]]
    w = check(set_of_cards)

start_game();

  




