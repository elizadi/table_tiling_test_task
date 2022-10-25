import numpy as np

class Polyomino:
	def __init__(self, h, w):
		self.arr = np.ones((h, w), dtype=int)
		self.s = h*w

	def rotate(self):
		self.arr = np.rot90(self.arr)	

class P_Polyomino(Polyomino):
	def __init__(self, h, w):
		super().__init__(h, w)
		self.arr = np.array([1 if x < w or x % w == 0 or x % w == w - 1 else 0 for x in range(h * w)]).reshape(h, w)
		self.s = h*w-(h-2)*(w-1)
		if h < 2 or w < 3: 				#print a warning that the given shape cannot be a p_polyomino 
			print(h, w, ' - it`s not p_polyomino')

class Table:
	def __init__(self, H, W):
		self.M = H
		self.N = W
		self.arr = np.zeros((self.M, self.N), dtype=int)
		self.filled_polyomino_coord = []


	def push_polyomino(self, polyomino, cord):                          #polyomino - object type of Polyomino(P_Polyomino), cord - tuple (x, y) size of 2
		self.arr[cord[0]:cord[0]+polyomino.arr.shape[0], cord[1]:cord[1]+polyomino.arr.shape[1]] += polyomino.arr

	def pop_polyomino(self, polyomino, cord):
		self.arr[cord[0]:cord[0]+polyomino.arr.shape[0], cord[1]:cord[1]+polyomino.arr.shape[1]] -= polyomino.arr

	def position_free(self, polyomino, cord):
		return np.all(np.add(self.arr[cord[0]:cord[0]+polyomino.arr.shape[0], cord[1]:cord[1]+polyomino.arr.shape[1]], polyomino.arr) < 2)

	def place_generation(self, polyomino):
		rot_num = 4 if isinstance(polyomino, P_Polyomino) else 2        #number of posible turns; for P-polyomino number = 4, for rectangle = 2 
		for _ in range(rot_num):
			for i in range(self.M - polyomino.arr.shape[0] + 1):
				for j in range(self.N - polyomino.arr.shape[1] + 1):
					cord = (i,j)
					if self.position_free(polyomino, cord):
						self.push_polyomino(polyomino, cord)
						self.filled_polyomino_coord.append(cord)
						yield True
			polyomino.rotate()
		yield False			
		
	def filling(self, p_polyominos, polyominos):                                      #check of the filling status
		S = 0
		for p_polyomino in p_polyominos:
			if np.max(p_polyomino.arr.shape) > max(self.T1, self.T2) or np.min(p_polyomino.arr.shape) > min(self.T1, self.T2):
				return False
			S += p_polyomino.s

		for polyomino in polyominos:
			if np.max(polyomino.arr.shape) > max(self.M, self.N) or np.min(polyomino.arr.shape) > min(self.M, self.N):
				return False
			S += polyomino.s
		if S > self.M * self.N:
			return False

		status = [self.place_generation(p_polyomino) for p_polyomino in p_polyominos]
		status = [self.place_generation(polyomino) for polyomino in polyominos]
		d = 0
		a = 0
		while 0 <= d + a < len(polyominos) + len(polyominos):
			if next(status[d]):
				d += 1
			else:
				if d == 0:
					break
				self.pop_polyomino(p_polyominos[d-1], self.filled_polyomino_coord[-1])
				self.filled_polyomino_coord.pop()
				status[d] = self.place_generation(p_polyominos[d])
				d -= 1
				
			if next(status[a]):
				a += 1
			else:
				if a == 0:
					break
				self.pop_polyomino(polyominos[a-1], self.filled_polyomino_coord[-1])
				self.filled_polyomino_coord.pop()
				status[a] = self.place_generation(polyominos[a])
				a -= 1

		if d + a == len(polyominos) + len(p_polyominos):
			return True
		else:
			return False

if __name__ == '__main__':
	polyominos = []
	p_polyominos = []
	with open('data.txt') as data:
		T1, T2 = data.readline().split()					            #table size
		n1 = int(data.readline())							            #number of types rectangle polyomino
		for i in range(n1):
			n_power = int(data.readline())					            #number of polyomino of size S1, S2
			S1, S2 = data.readline().split()                            #size of rectangle polyomino
			for j in range(n_power):
				p = Polyomino(int(S1), int(S2))
				polyominos.append(p)

		n2 = int(data.readline())							            #number of types P-polyomino
		for i in range(n2):
			n_power = int(data.readline())					            #number of polyomino of size Q1, Q2
			Q1, Q2 = data.readline().split()				            #size of P-polyomino
			for j in range(n_power):
				p = P_Polyomino(int(Q1), int(Q2))
				p_polyominos.append(p)
	
	t = Table(int(T1), int(T2))
	print(t.filling(p_polyominos, polyominos))
