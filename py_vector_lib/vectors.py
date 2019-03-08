import operator
import math

dimension_names = ("x","y","z","w")

def isvec(obj): # type can be iterated like a vector
	try:
		len(obj)
		return True
	except:
		return False # object not iterable

class Vector(tuple):
	__slots__ = ()

	def __repr__(self):
		return "v%d(%s)" % (len(self), ", ".join([repr(x) for x in self]))
	def __str__(self): return repr(self)

	# sadly this: v.x = 5 is impossible in python if i want to base my vectors on immutable types

	def create_class(dims):
		dict = { "__slots__": () }

		# v2(1)					-> v2(1,1)
		# v2(v2(1,2))
		#   or v2((1,2))
		#   or v2([1,2])
		#   etc.				-> v2(2,3)
		# v2(2,3)				-> v2(2,3)
		# v3(v2(1,2),3)			-> v3(1,2,3)
		# v3(v2(1,2),3)			-> v3(1,2,3)
		# v3(1,v2(2,3))			# not allowed
		def __new__(cls, *args):
			l = len(args)
			
			if l == 1:
				if isvec(args[0]):
					if len(args[0]) != dims:
						raise ValueError("v%d(%s): single argument needs to be v%d or scalar" % (dims, str(args[0]), dims))
					arr = args[0] # tuple/list/etc. passed in
				else:
					arr = (args[0],) * dims # single scalar for all dims

			elif l == dims:
				arr = args # all dims specified
			elif l > 1:
				if not isvec(args[0]):
					raise ValueError("v%d(%s): first argument needs to be at least v2" % (dims, str(args)))
				
				arr = args[0] # tuple/list/etc. as first arg

				if (len(args[0]) + len(args) -1) != dims:
					raise ValueError("v%d(%s): first argument dimensions plus remaining args needs to add up to %d scalars (for ex. v3(v2(), 1) or v4(v2(), 1,1) or v4(v3(), 1))" % (dims, str(args[0]), dims))
				
				arr = tuple(arr) + args[1:]
			else:
				raise ValueError("v%d() needs at least one argument" % dims)

			return super(Vector, cls).__new__(cls, arr)
		dict["__new__"] = __new__

		for i in range(min(dims, len(dimension_names))):
			dict[dimension_names[i]] = property(operator.itemgetter(i))
			
		return type("v%d" % dims, (Vector,), dict)

	# with this way of implementing the operators a 'v2() + v2()' is ~60x slower than a tuple concat, which seems rediculous to me
	# but the only way of making it faster (still slower than tuple concat) is to write the operators for each vector size and each op manually
	# TODO: is there any way of having this be abstract but still fast?
	# i tried to use cython (in visual studio on windows), which i eventually got to work, but it seems like a pain to work with, and after updating my python version i started to get a crash with cython, so i abandoned this for now
	
	# unary
	def elementwise_unary(op):
		def f(self):
			return self.__class__([op(a) for a in self])
		return f
	
	# binary
	def elementwise(op):
		def f(self, other=None): # optional second argument for __round__(self[, ndigits])
			if isvec(other):
				if len(self) != len(other):
					return NotImplemented

				return self.__class__([op(a,b) for a,b in zip(self,other)])
			else:
				return self.__class__([op(a, other) for a in self])
		return f
	def relementwise(op):
		def f(self, other=None):
			if isvec(other):
				if len(self) != len(other):
					return NotImplemented

				return self.__class__([op(b,a) for a,b in zip(self,other)])
			else:
				return self.__class__([op(other, a) for a in self])
		return f
	
	# ternary
	def elementwise_ternary(op):
		def f(self, other, modulo=None):
			if isvec(other):
				if len(self) != len(other):
					return NotImplemented
			else:
				other = (other,) * len(self)

			if isvec(modulo):
				if len(self) != len(modulo):
					return NotImplemented
			else:
				modulo = (modulo,) * len(self)

			return self.__class__([op(a,b,c) for a,b,c in zip(self,other,modulo)])
		return f

	def divmod(self, other): # elementwise divmod would return vector of tuples, we want tuple of vectors
		res = Vector.elementwise(divmod)(self, other)
		d,m = zip(*res)
		return self.__class__(d), self.__class__(m)
	def rdivmod(self, other):
		res = Vector.relementwise(divmod)(self, other)
		d,m = zip(*res)
		return self.__class__(d), self.__class__(m)
	
	__lt__			= elementwise(operator.lt)
	__le__			= elementwise(operator.le)
	__eq__			= elementwise(operator.eq)
	__ne__			= elementwise(operator.ne)
	__gt__			= elementwise(operator.gt)
	__ge__			= elementwise(operator.ge)

	__add__			= elementwise(operator.add)
	__sub__			= elementwise(operator.sub)
	__mul__			= elementwise(operator.mul)
	#del __matmul__
	__truediv__		= elementwise(operator.truediv)
	__floordiv__	= elementwise(operator.floordiv)
	__mod__			= elementwise(operator.mod)
	__divmod__		= divmod
	__pow__			= elementwise_ternary(pow)
	__lshift__		= elementwise(operator.lshift)
	__rshift__		= elementwise(operator.rshift)
	__and__			= elementwise(operator.and_)
	__xor__			= elementwise(operator.xor)
	__or__			= elementwise(operator.or_)

	__radd__		= relementwise(operator.add)
	__rsub__		= relementwise(operator.sub)
	__rmul__		= relementwise(operator.mul)
	__rtruediv__	= relementwise(operator.truediv)
	__rfloordiv__	= relementwise(operator.floordiv)
	__rmod__		= relementwise(operator.mod)
	__rdivmod__		= rdivmod
	__rpow__		= relementwise(operator.pow)
	__rlshift__		= relementwise(operator.lshift)
	__rrshift__		= relementwise(operator.rshift)
	__rand__		= relementwise(operator.and_)
	__rxor__		= relementwise(operator.xor)
	__ror__			= relementwise(operator.or_)
	
	__neg__			= elementwise_unary(operator.neg)
	__pos__			= elementwise_unary(operator.pos)
	__abs__			= elementwise_unary(operator.abs)
	__invert__		= elementwise_unary(operator.invert)

	#__complex__
	#__int__
	#__float__

	#__index__

	__round__		= elementwise(round)
	__trunc__		= elementwise_unary(math.trunc)
	__floor__		= elementwise_unary(math.floor)
	__ceil__		= elementwise_unary(math.ceil)
	
	def is_vec(self, size):
		valid = False
		try:
			valid = len(self) == size
		except:
			pass
		if not valid:
			raise ValueError("Vector must be of size %d operation ('%s')" % (size, repr(self)))

	def same_vecs(self, other):
		valid = False
		try:
			valid = len(self) == len(other)
		except:
			pass
		if not valid:
			raise ValueError("Vectors must be of same size for operation ('%s', '%s')" % (repr(self), repr(other)))

	def are_vecs(self, other, size):
		valid = False
		try:
			valid = len(self) == size and len(other) == size
		except:
			pass
		if not valid:
			raise ValueError("Vectors must both be of size %d for operation ('%s', '%s')" % (size, repr(self), repr(other)))

def length_sqr(self):
	return sum(self * self)

def length(self):
	return math.sqrt( sum(self * self) )

def normalize(self):
	return self / length(self)

def normalize_or_zero(self):
	len = length(self)
	if len == 0:
		return 0
	return self / len

def dot(self, other):
	Vector.same_vecs(self, other)
	return sum(self * other)

def cross(self, other): # cross(v3,v3): cross product,  cross(v2,v2):  cross product hack, same as cross(v3(self, 0), v3(other, 0)).z, ie the cross product of the 2d vectors on the z=0 plane in 3d space and then return the z coord of that (signed mag of cross product)
	if (len(self) == 3):
		Vector.are_vecs(self, other, 3)
		return v3(	self.y * other.z - self.z * other.y,
					self.z * other.x - self.x * other.z,
					self.x * other.y - self.y * other.x )
	else:
		Vector.are_vecs(self, other, 2)
		return self.x * other.y - self.y * other.x

def rotate90(self): # rotate v2 by 90 degrees counter clockwise
	Vector.is_vec(self, 2)
	return v2(-self.y, self.x)


vector_classes = [Vector.create_class(dim) for dim in range(2,4 +1)]

v2 = vector_classes[0]
v3 = vector_classes[1]
v4 = vector_classes[2]

#def length_sqr(v):
#	return np.sum(v**2)
#def length(v):
#	return np.sqrt(np.sum(v**2))
#
#def normalize(v):
#	return v / np.sqrt(np.sum(v**2))
#def normalize_or_zero(v):
#	len = np.sqrt(np.sum(v**2))
#	return np.zeros(v.shape) if len == 0 else v / len
#
#
#class Matrix(np.ndarray):
#	
#	def __repr__(self):
#		rows = [ "(%s)" % ", ".join([repr(cell) for cell in row]) for row in self ]
#		tmp = ",\n   ".join(rows)
#		return "m%d(%s)" % (self.shape[0], tmp)
#	def __str__(self): return repr(self)
#
#	def create_class(sqr_dims):
#		vec_class = vector_classes[sqr_dims -2]
#
#		dict = {}
#		
#		def __new__(cls, mat):
#			if not (isinstance(mat, Matrix) and mat.shape[0] < sqr_dims and mat.shape[1] < sqr_dims):
#				raise ValueError("m%d(): argument must be a matrix of smaller size than %d" % (sqr_dims, str(args[0]), dims, sqr_dims))
#			m = cls.ident()
#			m[:mat.shape[0],:mat.shape[1]] = mat
#			return m 
#		dict["__new__"] = __new__
#
#		def ident(cls):
#			obj = np.identity(sqr_dims).view(cls)
#			return obj
#		dict["ident"] = classmethod(ident)
#		
#		def zero(cls):
#			obj = np.zeros((sqr_dims,sqr_dims)).view(cls)
#			return obj
#		dict["zero"] = classmethod(zero)
#		
#		def rows(cls, *args):
#			if len(args) == (sqr_dims ** 2):
#				obj = np.asarray(args).reshape((sqr_dims,sqr_dims)).view(cls)
#			else:
#				if not (len(args) == sqr_dims and all([len(a) == sqr_dims for a in args])):
#					raise ValueError("m%d(): needs %d row vectors of length %d or %d scalars" % (sqr_dims, sqr_dims, sqr_dims ** 2))
#
#				obj = np.asarray(args).view(cls)
#			return obj
#		dict["rows"] = classmethod(rows)
#		
#		def columns(cls, *args):
#			return cls.rows(*args).T
#		dict["columns"] = classmethod(columns)
#
#		def __init__(self):
#			def __getitem__(self, key):
#				return self[key].view(vec_class)
#			dict["__getitem__"] = __getitem__
#
#		return type("m%d" % sqr_dims, (Matrix,), dict)
#
#matrix_classes = [Matrix.create_class(dim) for dim in range(2,4 +1)]
#
#m2 = matrix_classes[0]
#m3 = matrix_classes[1]
#m4 = matrix_classes[2]
#
#def rotate2(ang):
#	s,c = np.sin(ang), np.cos(ang)
#	return m2.rows(+c, -s,
#				   +s, +c)
#
#def translate4(vec):
#	return m4.rows(1,0,0,vec.x,
#				   0,1,0,vec.y,
#				   0,0,1,vec.z,
#				   0,0,0,1)
#
#def calc_orthographic_projection_matrix (size, near=-1.0, far=100.0):
#	x = 1.0 / (size.x / 2)
#	y = 1.0 / (size.y / 2)
#
#	a = 1.0 / (far -near)
#	b = near * a
#
#	return m4.rows(	x, 0, 0, 0,
#					0, y, 0, 0,
#					0, 0, a, b,
#					0, 0, 0, 1 )
#
#a = m2.ident()
#b = m2.zero()
#c = m2.rows((1,2),
#			(3,4))
#d = m2.rows(1.0,2.0,
#			3.0,4.0)
#e = m2.columns(	(1,2),
#				(3,4))
#
#r = rotate2(1)
#
#s = m4(r)
#
#a = m4(rotate2(1)) * translate4(v3(1,2,3))
#b = translate4(v3(1,2,3)) * m4(rotate2(1))
#
#pass
#
