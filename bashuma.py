#!/home/python/bin/python
#coding:utf-8

class Heap(list):
	def __init__(self):
		list.__init__(self)
		self.append(None)
class MinHeap(Heap):
	def __init__(self):
		Heap.__init__(self)

	def Add(self, state):
		self.append(state)
		self.AdjustUp(len(self) - 1)

	def AdjustUp(self, k):
		self[0] = self[k]
		i = k / 2
		while i > 0 and self[0] < self[i]:
			self[k] = self[i]
			k = i
			i = k / 2
		self[k] = self[0]

	def AdjustDown(self,k):

		self[0] = self[k]
		i = 2 * k
		while i <= len(self) - 1:
			if i < len(self) - 1 and self[i+1] < self[i]:
				i += 1
			if self[i] < self[0]:
				self[k] = self[i]
				k = i
			else:
				break
			i *= 2
		self[k] = self[0]

	def PopMin(self):
		minstate = self[1]
		if len(self) <= 2:
			self.pop()
			return minstate

		#print 'here'
		self[1] = self[len(self) - 1]
		self.pop()
		self.AdjustDown(1)
		return minstate

	def Has(self, s):
		for i in range(1, len(self)):
			if self[i] == s:
				return True
		return False

	def Get(self, s):
		for i in range(1, len(self)):
			if self[i] == s:
				return self[i]
		return None

	def Empty(self):
		if len(self) == 1:
			return True
		return False
		
class List(list):
	def __init__(self):
		list.__init__(self)
	def Add(self,s):
		self.append(s)
	def Insert(self, pos, s):
		self.insert(pos, s)
	
	def Has(self, s):
		for item in self:
			if item == s:
				return True
		return False

	def Remove(self, s):
		for i in range(0, len(self)):
			if self[i] == s:
				return self[i]
		return None

class State:
	def __init__(self, zero_position, state_value):
		self.state_value = List()
		for i in range(0, len(state_value)):
			self.state_value.append(state_value[i])
		self.zero_position = zero_position
		self.father = None
		self.f = 0
		self.g = 0

	def __lt__(self, state):
		if self.f < state.f:
			return True
		elif self.f == state.f:
			#print self.f,state.f,self.g,state.g
			#print self.state_value,state.state_value
			return self.g < state.g

	def __eq__(self, state):
		for i in range(0, len(self.state_value)):
			if self.state_value[i] != state.state_value[i]:
				return False
		return True

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

def g(state_a, state_b):
	return 1
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
	for pos in range(0, len(state.state_value)):
		if state.state_value[pos] == item:
			return pos
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

def GetStateFromState(direction, state, next_state):
	global N
	next_state.Copy(state)
	pos = state.zero_position
	i = GetIFromPosition(pos)
	j = GetJFromPosition(pos)

	new_i = 0
	new_j = 0
	if direction == 'up':
		new_i = i - 1
		new_j = j
	elif direction == 'down':
		new_i = i + 1
		new_j = j
	elif direction == 'left':
		new_i = i
		new_j = j - 1
	elif direction == 'right':
		new_i = i
		new_j = j + 1
	else:
		return False

	if new_i >= 1 and new_i <= N and new_j >= 1 and new_j <= N:
		new_pos = GetNFromIJ(new_i, new_j)
		next_state.ExchangeIJ(pos, new_pos)
		next_state.zero_position = new_pos
		return True

	return False

def Expand(from_state):
	expand_list = List()
	next_state = State(-1,[])
	if GetStateFromState('up', from_state, next_state):
		expand_list.Add(next_state)

	next_state = State(-1,[])
	if GetStateFromState('down', from_state, next_state):
		expand_list.Add(next_state)

	next_state = State(-1,[])
	if GetStateFromState('left', from_state, next_state):
		expand_list.Add(next_state)

	next_state = State(-1,[])
	if GetStateFromState('right', from_state, next_state):
		expand_list.Add(next_state)

	return expand_list

#A*算法dijstra
def AStar(start_state, end_state, open_list,close_list):
	#加入open表
	open_list.Add(start_state)
	#open_list小跟堆,第1状态从1开始
	while open_list.Empty() == False:
		#f最小
		from_state = open_list.PopMin()
		#加入close表，已经访问过
		close_list.Add(from_state)

		#找到结束状态
		if from_state == end_state:
			return from_state
		
		#扩展状态
		expand_list = Expand(from_state)
		assert(len(expand_list) <= 4)
		for next_state in expand_list:
			#计算f
			next_state.g = from_state.g + g(from_state, next_state)
			next_state.f = next_state.g + h(next_state, end_state)
			
			if open_list.Has(next_state):
				real_same_state = open_list.Get(next_state)
				if real_same_state.g > next_state.g:
					#print real_same_state.g, next_state.g
					real_same_state.g = next_state.g
					real_same_state.f = next_state.f
					real_same_state.father = from_state
			elif close_list.Has(next_state):
				real_same_state = close_list.Remove(next_state)
				if real_same_state.g > next_state.g:
					real_same_state.g = next_state.g
					real_same_state.f = next_state.f

					real_same_state.father = from_state
					#加入open表从新计算他的扩展状态
					open_list.Add(real_same_state)
			else:
				next_state.father = from_state
				open_list.Add(next_state)

	return None
		
def PrintPath(state):
	global N
	a = List()
	while state:
		a.Insert(0, state.state_value)
		state = state.father

	print '####变换如下:###'
	i = 0
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
#open_list = MinHeap()
#close_list = List()
##call A*
#end_state = AStar(start_state, end_state, open_list, close_list)
##print path
#PrintPath(end_state)
##
##
#start_state = State(4,[1,5,2,4,0,3,6,7,8])
#end_state = State(4,[1,2,3,4,0,5,6,7,8])
#open_list = MinHeap()
#close_list = List()
##call A*
#end_state = AStar(start_state, end_state, open_list, close_list)
##print path
#PrintPath(end_state)
#
#
start_state = State(4,[7,2,4,5,0,6,8,3,1])
end_state = State(0,[0,1,2,3,4,5,6,7,8])
open_list = MinHeap()
close_list = List()
#call A*
end_state = AStar(start_state, end_state, open_list, close_list)
#print path
PrintPath(end_state)

#s1 = State(-1, [])
#s1.f = 1
#s2 = State(-1, [])
#s2.f = 2
#s3 = State(-1, [])
#s3.f = 3
#s4 = State(-1, [])
#s4.f = 4
#s5 = State(-1, [])
#s5.f = 5
#s6 = State(-1, [])
#s6.f = 0
#s7 = State(-1, [])
#s7.f = 0
#
#minh = MinHeap()
#
#minh.Add(s2)
#minh.Add(s1)
#minh.Add(s3)
#minh.Add(s4)
#
#st = minh.PopMin()
#print st.f
#
#minh.Add(s5)
#minh.Add(s6)
#minh.Add(s7)
#
#while False == minh.Empty():
#	st = minh.PopMin()
#	print st.f
