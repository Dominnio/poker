import random
import numpy as np
import time
import itertools

def number_to_color(number):
  if(number < 13):
    c = "\u2663"
  elif(number < 26):
    c = "\u2666"
  elif(number < 39):
    c = "\u2665"
  else:
    c = "\u2660"
  return c

def number_to_color_value(number):
  if(number < 13):
    cv = 0
  elif(number < 26):
    cv = 1
  elif(number < 39):
    cv = 2
  else:
    cv = 3
  return cv

def number_to_symbol(number):
  number %= 13
  if(number < 8):
    s = str(number + 2)
  elif(number == 11):
    s = "K"
  elif(number == 10):
    s = "Q"
  elif(number == 9):
    s = "J"
  elif(number == 8):
    s = "T"
  else:
    s = "A"
  return s

def number_to_symbol_value(number):
  return (number%13 + 2)

class Card:
  def __init__(self, number):
    self.number = number
    self.symbol_value = number_to_symbol_value(number)
    self.color_value = number_to_color_value(number)

  def __str__(self):
    return (number_to_symbol(self.number) + number_to_color(self.number))

  def __repr__(self):
    return str(self)

  def __lt__(self,other):
    return self.symbol_value < other.symbol_value

  def __gt__(self,other):
    return self.symbol_value > other.symbol_value

  def __le__(self,other):
    return self.symbol_value <= other.symbol_value

  def __ge__(self,other):
    return self.symbol_value >= other.symbol_value

  def __eq__(self,other):
    return self.symbol_value == other.symbol_value

  def __ne__(self,other):
    return self.symbol_value != other.symbol_value

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
    col[card.color_value].append(card)
  return col

def check_two_pair(seq):
  seq_tmp = seq
  for s in seq_tmp: 
    if(len(s) == 2):
      seq_tmp.remove(s)
      for ss in seq:
        if(len(ss) == 2):
          seq_tmp.remove(ss)
          s.append(ss[0])
          s.append(ss[1])
          s.append(seq[0][0])
          return [3,s]
      s.append(seq[0][0])
      s.append(seq[1][0])
      s.append(seq[2][0])
      return [2,s]
  return [1,[seq[0][0],seq[1][0],seq[2][0],seq[3][0],seq[4][0]]]

def check_three(seq):
  for s in seq:
    if(len(s) == 3):
      seq.remove(s)
      s.append(seq[0][0])
      s.append(seq[1][0])
      return [4,s]
  return check_two_pair(seq)

def check_straight(seq,col):
  s = [seq[0][0]]
  for i in range(1,len(seq)):
    if(seq[i][0].symbol_value == seq[i-1][0].symbol_value - 1):
      s.append(seq[i][0])
      if(len(s) == 5):
        return [5, s]
    else:
      s = [seq[i][0]]
  
  if(len(s) == 4 and s[0].symbol_value == 5 and seq[0][0].symbol_value == 14):
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
        ss = ss[:2]
        three.append(ss[0])
        three.append(ss[1])
        return [7,three]
  return check_flush(seq,col)

def check_quads(seq,col):
  for s in seq:
    if(len(s) == 4):
      seq.remove(s) 
      s.append(seq[0][0])  
      return [8, s]
  return check_full_house(seq,col)

def check_straight_flush(seq,col):
  for c in col:
    if(len(c) >= 5):
      s = [c[0]]
      for i in range(1,len(c)):
        if(c[i].symbol_value == c[i-1].symbol_value - 1):
          s.append(c[i])
          if(len(s) == 5):
            return [9, s]
        else:
          s = [c[i]]
      if(len(s) == 4 and s[0].symbol_value == 5 and c[0].symbol_value == 14):
        s.append(c[0])
        return [9,s]
      return check_quads(seq,col)
  return check_quads(seq,col)

def check(cards):
  cards.sort(reverse = True)
  seq = set_seq(cards)
  col = set_col(cards)
  layout = check_straight_flush(seq,col)
  return layout

def compare(x, y):
  if(x[0] > y[0]):
    return True
  if(x[0] < y[0]):
    return False
  for i in range(len(x[1])):
    if(x[1][i] > y[1][i]):
      return True
    if(x[1][i] < y[1][i]):
      return False
  return None

def odds(cards,table,opponents):
  deck = np.arange(52).tolist()
  deck.remove(cards[0].number)
  deck.remove(cards[1].number)
  for e in table:
    deck.remove(e.number)
  n = 5-len(table)+2*opponents
  test = Table()

  win = 0
  tie = 0
  lose = 0 
  N = 1000000
  sets = np.zeros(9)

  for i in range(N):
    rand = random.sample(deck, n)
    test_table = table.copy()
    players = []
    for i in range(int(1+opponents)):
      players.append(Player(int(200)))
    players[0].cards = cards

    for i in range(5 - len(table)):
      test_table.append(Card(rand[i]))
    i = 5-len(table)
    for j in range(1,len(players)):
      players[j].cards = [Card(rand[i]), Card(rand[i+1])]
      i += 2
    test.table = test_table
    test.players = players

    result = test.get_winner()

    flag = True
    if(0 in result[0][0]):
      if(len(result[0][0]) == 1):
        win += 1
      else:
        tie += 1
    else:
      lose += 1
    sets[result[1][0][0] - 1] += 1

  print(cards)
  #print(table)
  print("\nwin: %.4f" % float(win/N*100))
  print("tie: %.4f" % float(tie/N*100))
  print("lose: %.4f" % float(lose/N*100))
  print("all: %.4f" % float((lose+win+tie)/N*100))

  sets = sets/N*100
  sets = np.flip(sets)
  print("\nstraight flush: %.4f" % float(sets[0]))
  print("quads: %.4f" % float(sets[1]))
  print("full house: %.4f" % float(sets[2]))
  print("flush: %.4f" % float(sets[3]))
  print("straight: %.4f" % float(sets[4]))
  print("three of kind: %.4f" % float(sets[5]))
  print("two pair: %.4f" % float(sets[6]))
  print("one pair: %.4f" % float(sets[7]))
  print("high card: %.4f" % float(sets[8]))


class Player:
  def __init__(self, stack):
    self.stack = stack
  def __str__(self):
    s = ("chips: " + str(self.stack))
    if(len(self.cards) != 0):
      s += ", cards: " + str(self.cards[0]) + " " + str(self.cards[1])
    else:
      s += ", cards: -"
    return s
  def bet(self,bet):
    self.stack -= bet
    self.paid += bet
    return self.paid
  def take(self,prize):
    self.stack += prize

class Table:
  def get_winner(self):
    layouts = []
    n = len(self.players)
    for i in range(n):
      layouts.append(check(self.table + self.players[i].cards))   
    save = layouts.copy()
    order = np.arange(n)
    while n > 1:
      for i in range(n - 1):
        c = compare(layouts[i],layouts[i+1])
        if(c == False):
          tmp = layouts[i]
          layouts[i] = layouts[i+1]
          layouts[i+1] = tmp
          tmp = order[i]
          order[i] = order[i+1]
          order[i+1] = tmp
      n = n - 1
    ret_order = [[order[0]]]
    idx = 0
    for i in range(i,len(layouts) - 1):
      c = compare(layouts[i],layouts[i+1])
      if(c == None):
        ret_order[idx].append(order[i+1])
      else:
        ret_order.append([order[i+1]])
        idx += 1
    return [ret_order,save]

  def set_cards(self):
    n = 5 + len(self.players)*2
    c = random.sample(range(52),n)
    self.table = [Card(c[0]),Card(c[1]),Card(c[2]),Card(c[3]),Card(c[4])]
    idx = 5
    for i in range(len(self.players)):
      self.players[i].cards = [Card(c[idx]), Card(c[idx+1])]
      idx += 2

  def all_7_comb(self,a,b,c,d,e,f,g):
    self.table = [Card(a),Card(b),Card(c),Card(d),Card(e)]
    self.players[0].cards = [Card(f), Card(g)]

  def start_part(self):
    n = 3	#input("Number of players: ") max 23 min 1
    c = 300	#input("Players chips: ")
    N = 52
    self.players = []
    for i in range(int(n)):
      self.players.append(Player(int(c)))

    self.set_cards()
    odds(self.players[0].cards, [], n - 1)
    result = self.get_winner()

    print("===========================================================\n")
    print("table: " + str(self.table))
    print(str(result[0]) + "\n")
    for i in range(len(result[1])):
      for x in range(len(result[0])):
        for y in result[0][x]:
          if(i == y):
            print("> position: " + str(x+1))
      print(str(result[1][i]) + "\t\tplayer: " + str(i) + "\tcards: " + str(self.players[i].cards))

  def start_game(self):
    for i in range(1):
      self.start_part()


############################################

Table().start_game();

############################################


# Sets probability
'''
  Hand                Possibilities        Probability		My program       
  ---------------     -------------        -----------		-----------      
  Royal Flush              4,324              0.00324%		                 
  Straight Flush          37,260              0.0279%               41,584 
  4 of a kind            224,848              0.168%               224,848	
  Full House           3,473,184              2.60%              3,473,184
  Flush                4,047,644              3.03%              4,047,644    
  Straight             6,180,020              4.62%		 6,180,020
  Three of a Kind      6,461,620              4.83%		 6,461,620
  Two Pair            31,433,400             23.50%	        31,433,400	
  Pair                58,627,800             43.82%             58,627,800		
  High Card           23,294,460             17.41%             23,294,460

  All		     133,784,560            100.00%            133,784,560    


Src: http://mathforum.org/library/drmath/view/65306.html

'''
 
# All combination check test
'''
    num = 0 
    for a in range(N):
      fil = open("result.txt",'a')
      fil.write(str(sets) + "\n\n")
      fil.close()
      for b in range(a+1,N):
        for c in range(b+1,N):
          for d in range(c+1,N):
            for e in range(d+1,N):
              for f in range(e+1,N):
                for g in range(f+1,N): 
                  print(str(a)+ " " + str(b)+ " " + str(c)+ " " + str(d)+ " " + str(e)+ " " + str(f)+ " " + str(g))
                  self.all_7_comb(a,b,c,d,e,f,g) 
                  #self.set_cards()
                  #odds(self.players[0].cards, [], n - 1)
                  result = self.get_winner()
                  for p in result[1]:
                    sets[p[0] - 1] += 1
'''


