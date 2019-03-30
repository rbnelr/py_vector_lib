from vector import *

def range_column_major(w,h):
	for x in range(w):
		for y in range(h):
			yield x,y
def range_row_major(w,h):
	for y in range(h):
		for x in range(w):
			yield x,y

class Matrix(tuple):
	#__slots__ = ("size", "translate") # no filled slots on tuple

	# cells are stored flattened in column major order

	def __repr__(self):
		if self.size[0] == self.size[1]:
			type_ = "Matrix%d(" % self.size[0]
		else:
			type_ = "Matrix%dx%d(" % (self.size[0], self.size[1])

		rows = ", ".join(repr(x) for x in self.get_row(0))

		for row in range(1, self.size[1]):
			rows += ",\n"+ " "*len(type_) +", ".join(repr(x) for x in self.get_row(row))

		return type_+ rows +")"
	def __str__(self): return repr(self)
	
	def __len__(self): # columns
		return self.size[0]

	def __getitem__(self, key):
		if isvec(key) and len(key) == 2:
			if not (	0 <= key[0] < self.size[0] and \
						0 <= key[1] < self.size[1] ):
				raise IndexError("Matrix[%s] out of range, size=%s" % (repr(key), repr(self.size)))

			return super().__getitem__( key[0] * self.size[1] + key[1] )
		else:
			return self.get_column(key)
	
	def get_column(self, indx):
		rows = self.size[1]
		v = [self[indx,y] for y in range(rows)]
		return shorthand_vectors[rows](v) if rows in shorthand_vectors else Vector(v)

	def get_row(self, indx):
		cols = self.size[0]
		v = [self[x,indx] for x in range(cols)]
		return shorthand_vectors[cols](v) if cols in shorthand_vectors else Vector(v)
	
	columns	= property(fget = lambda self: tuple([ self.get_column(col)	for col in range(self.size[0]) ]))
	rows	= property(fget = lambda self: tuple([ self.get_row(row)	for row in range(self.size[1]) ]))

	def __new__(cls, *args, order='rows', size=None):
		l = len(args)
		
		if not (size == None or (isvec(size) and len(size) == 2)):
			raise ValueError("Matrix(): size must be None or v2")
				
		if l > 0 and isvec(args[0]): # 2d args or Matrix
			if not all( (isvec(arg) for arg in args) ): # all args are vectors
				raise ValueError("Matrix(): mixed vectors and scalars as arguments are invalid")
			if not size:
				if not all(len(args[0]) == len(arg) for arg in args): # all args are vectors of same size
					raise ValueError("Matrix(): need row or column vectors of equal sizes")
			
			args_ = args
			order_ = order

			if l==1 and isinstance(args[0], Matrix):
				args_ = args[0]
				order_ = 'columns'
			
			def get(a,b):
				if size and (a >= len(args_) or b >= len(args_[a])):
					return 1 if a==b else 0
				return args_[a][b]

			if order_=='rows':
				size_ = size if size else v2(len(args_[0]), len(args_))
				flattened = [ get(y,x) for x,y in range_column_major(*size_) ]
			elif order_=='columns':
				size_ = size if size else v2(len(args_), len(args_[0]))
				flattened = [ get(x,y) for x,y in range_column_major(*size_) ]
			else:
				raise ValueError("order must be 'rows' or 'columns'")
		
		else: # flat args

			if not size:
				raise ValueError("Matrix(): size must be specified if args are not 2d")
				
			size_ = v2(size)

			if l == 0: # Matrix(size=(x,y)) => identity matrix
				flattened = [ 1 if x==y else 0 for x,y in range_column_major(*size) ]
			else:
				if not len(args) == size[0]*size[1]:
					raise ValueError("Matrix(size=%s): need %d cells as args" % (str(size), size[0]*size[1]))
				
				if order=='rows':
					flattened = [ args[y * size[0] + x] for x,y in range_column_major(*size_) ]
				elif order=='columns':
					#flattened = [ args[x * size[1] + y] for x,y in range_column_major(*size_) ]
					flattened = args
				else:
					raise ValueError("order must be 'rows' or 'columns'")

		obj = super(Matrix, cls).__new__(cls, flattened)

		obj.size = size_

		return obj

	def identity(size):
		return Matrix(size=size)

	def translate(vec):
		transl = (*vec,1)
		size = (len(transl),)*2
		return Matrix(*((1 if x==y else 0) if x < (size[0]-1) else transl[y] for x,y in range_column_major(*size)), order='columns', size=size)

	def scale(vec):
		size = (len(vec),)*2
		return Matrix(*(vec[x] if x==y else 0 for x,y in range_column_major(*size)), order='columns', size=size)


	def __mul__(self, r):
		if isinstance(r, Vector):
			return _mul_mv(self, r)
		elif isinstance(r, Matrix):
			return _mul_mm(self, r)
		else:
			return NotImplemented

translate = Matrix.translate
scale = Matrix.scale

def rotate2(ang):
	s,c = math.sin(ang), math.cos(ang)
	return Matrix((+c, -s),
				  (+s, +c))

def rotate3_X(ang):
	s,c = math.sin(ang), math.cos(ang)
	return Matrix(( 1,  0,  0),
				  ( 0, +c, -s),
				  ( 0, +s, +c))
def rotate3_Y(ang):
	s,c = math.sin(ang), math.cos(ang)
	return Matrix((+c,  0, +s),
				  ( 0,  0,  0),
				  (-s,  0, +c))
def rotate3_Z(ang):
	s,c = math.sin(ang), math.cos(ang)
	return Matrix((+c, -s,  0),
				  (+s, +c,  0),
				  ( 0,  0,  1))

def calc_orthographic_projection_Matrix (size, near=-1.0, far=100.0):
	x = 1 / (size.x / 2)
	y = 1 / (size.y / 2)

	a = 1 / (far -near)
	b = near * a

	return Matrix((x, 0, 0, 0),
				  (0, y, 0, 0),
				  (0, 0, a, b),
				  (0, 0, 0, 1))


def _mul_mm(l, r):
	
	if l.size[0] == l.size[1] and r.size[0] == r.size[1]: # only for square mats?
		if l.size[0] > r.size[1]:
			r = Matrix(r, size=l.size)
		else:
			l = Matrix(l, size=r.size)

	elif l.size[0] != r.size[1]:
		return ValueError("Matrix%dx%d * Matrix%dx%d: Matricies do not match" % (l.size[0], l.size[1], r.size[0], r.size[1]))

	return Matrix(*[_mul_mv(l, r_col) for r_col in r.columns], order='columns')

def _mul_mv(l, r):
	vec = r.__class__

	if r.size > l.size[0]:
		return ValueError("Matrix%dx%d * Vector%d: Vector too large" % (l.size[0], l.size[1], r.size))

	v = r
	if r.size < l.size[0]:
		v = Vector(r, size=l.size[0])

	v = sum(mat_col * vec_cell for mat_col, vec_cell in zip(l.columns, v))

	return vec(v)

#	ret.x = m.arr[0].x * v.x  +m.arr[1].x * v.y  +m.arr[2].x * v.z  +m.arr[3].x * v.w;
#	ret.y = m.arr[0].y * v.x  +m.arr[1].y * v.y  +m.arr[2].y * v.z  +m.arr[3].y * v.w;
#	ret.z = m.arr[0].z * v.x  +m.arr[1].z * v.y  +m.arr[2].z * v.z  +m.arr[3].z * v.w;
#	ret.w = m.arr[0].w * v.x  +m.arr[1].w * v.y  +m.arr[2].w * v.z  +m.arr[3].w * v.w;
#
#
#	ret.x = m.arr[0].x * v.x  +m.arr[1].x * v.y  +m.arr[2].x * v.z  +m.arr[3].x * v.w;
#	ret.y = m.arr[0].y * v.x  +m.arr[1].y * v.y  +m.arr[2].y * v.z  +m.arr[3].y * v.w;
#	ret.z = m.arr[0].z * v.x  +m.arr[1].z * v.y  +m.arr[2].z * v.z  +m.arr[3].z * v.w;
#	ret.w = m.arr[0].w * v.x  +m.arr[1].w * v.y  +m.arr[2].w * v.z  +m.arr[3].w * v.w;
#	return ret;
#}
#VEC_INL M4 operator* (M4 l, M4 r) {
#	M4 ret;
#	ret.arr[0] = l * r.arr[0];
#	ret.arr[1] = l * r.arr[1];
#	ret.arr[2] = l * r.arr[2];
#	ret.arr[3] = l * r.arr[3];