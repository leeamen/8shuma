#!/home/python/bin/python
#coding:utf-8

#class Heap(list):
#  def __init__(self):
#    list.__init__(self)
#    self.append(None)
#class MinHeap(Heap):
#  def __init__(self):
#    Heap.__init__(self)
#
#  def append(self, state):
#    self.append(state)
#    self.AdjustUp(len(self) - 1)
#
#  def AdjustUp(self, k):
#    self[0] = self[k]
#    i = k / 2
#    while i > 0 and self[0] <= self[i]:
#      self[k] = self[i]
#      k = i
#      i = k / 2
#    self[k] = self[0]
#
#  def AdjustDown(self,k):
#
#    self[0] = self[k]
#    i = 2 * k
#    while i <= len(self) - 1:
#      if i < len(self) - 1 and self[i+1] < self[i]:
#        i += 1
#      if self[i] < self[0]:
#        self[k] = self[i]
#        k = i
#      else:
#        break
#      i *= 2
#    self[k] = self[0]
#
#  def PopMin(self):
#    minstate = self[1]
#    if len(self) <= 2:
#      self.pop()
#      return minstate
#
#    #print 'here'
#    self[1] = self[len(self) - 1]
#    self.pop()
#    self.AdjustDown(1)
#    return minstate
#

#
#  def Remove(self, s):
#    state = None
#    for i in range(1, len(self)):
#      if self[i] == s:
#        state = self[i]
#        if i != len(self) - 1:
#          self[i] = self[len(self) - 1]
#          self.pop()
#          self.AdjustDown(i)
#        else:
#          self.pop()
#        break
#
#    return state

#  def Empty(self):
#    if len(self) == 1:
#      return True
#    return False
#
#  def Length(self):
#    return len(self) - 1
    
class List(list):
  def __init__(self):
    list.__init__(self)
  def GetIndex(self, s):
    for i in range(0, len(self)):
      if self[i] == s:
        return i
    return len(self)
  def PopMin(self):
    if self.Empty():
      return None
    self.sort()
    return self.pop(0)
  def Length(self):
    return len(self)
  def Empty(self):
    return 0 == len(self)
#节点的状态类
class State:
  def __init__(self, zero_position, state_value):
    self.state_value = state_value
    self.zero_position = zero_position
    self.father = None
    self.f = 0
    self.g = 0

  def __lt__(self, state):
    if self.f < state.f:
      return True
    elif self.f == state.f:
      return self.g < state.g
    return False
  def __le__(self,state):
    if self.f <= state.f:
      return True
    return False
  def __eq__(self, state):
    return self.state_value == state.state_value
  def Copy(self, s):
    while len(self.state_value) != 0:
      self.state_value.pop()
    self.state_value += s.state_value
    self.zero_position = s.zero_position
  def ExchangeIJ(self, i, j):
    self.state_value[i] = self.state_value[i] ^ self.state_value[j]
    self.state_value[j] = self.state_value[i] ^ self.state_value[j]
    self.state_value[i] = self.state_value[i] ^ self.state_value[j]
  def Print(self):
    print self.state_value
#状态a到b的耗散值，本题为1
def g(state_a, state_b):
  return 1
#到目标状态的估计耗散,使用曼哈顿距离
def h(from_state, end_state):
  evaluate_cost = 0
  for pos in range(0, len(from_state.state_value)):
    #不计算空格(即0)
    if from_state.state_value[pos] == 0:
      continue
    pos_i = GetIFromPosition(pos)
    pos_j = GetJFromPosition(pos)

    end_pos = GetPosInState(end_state, from_state.state_value[pos])
    assert(end_pos != len(end_state.state_value))

    end_pos_i = GetIFromPosition(end_pos)
    end_pos_j = GetJFromPosition(end_pos)

    evaluate_cost = evaluate_cost + abs(end_pos_i - pos_i) + abs(end_pos_j - pos_j)
    #print pos_i,pos_j,end_pos_i,end_pos_j,from_state.state_value[pos],end_state.state_value[end_pos],from_state.state_value

  #print evaluate_cost
  return evaluate_cost
def GetPosInState(state, item):
  if item in state.state_value:
    return state.state_value.index(item)
  else:
    return len(state.state_value)

def GetIFromPosition(pos):
  global N
  return pos / N + 1
def GetJFromPosition(pos):
  global N
  return pos % N + 1
def GetNFromIJ(i,j):
  global N
  return (i - 1) * N + j - 1

def GetNextStateListFromState(direction, state):
  global N
  next_state = State(-1,[])
  next_state.Copy(state)
  pos = state.zero_position
  i = GetIFromPosition(pos)
  j = GetJFromPosition(pos)

  new_i = 0
  new_j = 0
  if direction == 'down':
    new_i = i + 1
    new_j = j
  elif direction == 'up':
    new_i = i - 1
    new_j = j
  elif direction == 'right':
    new_i = i
    new_j = j + 1
  elif direction == 'left':
    new_i = i
    new_j = j - 1
  else:
    return None

  if new_i >= 1 and new_i <= N and new_j >= 1 and new_j <= N:
    new_pos = GetNFromIJ(new_i, new_j)
    next_state.ExchangeIJ(pos, new_pos)
    next_state.zero_position = new_pos
    return next_state

  return None

def Expand(from_state):
  expand_list = List()

  next_state = GetNextStateListFromState('up', from_state )
  if next_state != None:
    expand_list.append(next_state)

  next_state = GetNextStateListFromState('down', from_state)
  if next_state != None:
    expand_list.append(next_state)

  next_state = GetNextStateListFromState('left', from_state)
  if next_state != None:
    expand_list.append(next_state)

  next_state = GetNextStateListFromState('right', from_state)
  if next_state != None:
    expand_list.append(next_state)

  return expand_list

#A*算法dijstra
def AStar(start_state, end_state, open_list,close_list):
  #加入open表
  open_list.append(start_state)
  #open_list小跟堆,第1状态从1开始
  while open_list.Empty() == False:
    #f最小
    from_state = open_list.PopMin()
    #加入close表，已经访问过
    close_list.append(from_state)

    #找到结束状态
    if from_state == end_state:
      print '#####close_list长度',close_list.Length()
      return from_state
    
    #扩展状态
    expand_list = Expand(from_state)
    assert(len(expand_list) <= 4)
    for next_state in expand_list:
      #计算f
      next_state.g = from_state.g + g(from_state, next_state)
      next_state.f = next_state.g + h(next_state, end_state)

      if next_state in open_list:
        idx = open_list.index(next_state)
        real_same_state = open_list[idx]
        if real_same_state.g > next_state.g:
          print real_same_state.g, next_state.g
          real_same_state.g = next_state.g
          real_same_state.f = next_state.f
          real_same_state.father = from_state

      elif next_state in close_list:
        idx = close_list.index(next_state)
        real_same_state = close_list[idx]
        if real_same_state.g > next_state.g:
          real_same_state.g = next_state.g
          real_same_state.f = next_state.f

          real_same_state.father = from_state
          #从close表中删除
          close_list.pop(idx)
          #加入open表从新计算他的扩展状态
          open_list.append(real_same_state)
      else:
        next_state.father = from_state
        open_list.append(next_state)
  return None

def PrintPath(state):
  global N
  a = List()
  while state:
    a.insert(0, state.state_value)
    state = state.father

  print '####变换如下:###'
  i = 0
  print a[0]
  while i < N:
    j = 0
    while j < N:
      if a[0][i*N + j] == 0:
        print ' ',
      else:
        print a[0][i*N + j],
      j += 1
    print 
    i += 1
  for idx in range(1, len(a)):
    print '第%d步:'%(idx)
    print a[idx]
    i = 0
    while i < N:
      j = 0
      while j < N:
        if a[idx][i*N + j] == 0:
          print ' ',
        else:
          print a[idx][i*N + j],
        j += 1
      print 
      i += 1


#3阶 pos = (i-1) * N + j - 1
# i = pos / N + 1 , j = pos % N + 1
N = 3
#start_state = State(4, [2,8,3,1,0,4,7,6,5])
#end_state = State(4, [1,2,3,8,0,4,7,6,5])
#open_list = List()
#close_list = List()
##call A*
#end_state = AStar(start_state, end_state, open_list, close_list)
##print path
#PrintPath(end_state)
##
##
#start_state = State(4,[1,5,2,4,0,3,6,7,8])
#end_state = State(4,[1,2,3,4,0,5,6,7,8])
#open_list = List()
#close_list = List()
##call A*
#end_state = AStar(start_state, end_state, open_list, close_list)
##print path
#PrintPath(end_state)
#
#
start_state = State(4,[7,2,4,5,0,6,8,3,1])
end_state = State(0,[0,1,2,3,4,5,6,7,8])
open_list = List()
close_list = List()
#call A*
end_state = AStar(start_state, end_state, open_list, close_list)
#print path
PrintPath(end_state)

