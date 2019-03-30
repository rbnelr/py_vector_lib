import operator
import math

def isvec(obj): # type can be iterated like a Vector
	try:
		len(obj)
		return True
	except:
		return False # object not iterable

class Vector(tuple):
	__slots__ = ()

	def __repr__(self):
		return "Vector%d(%s)" % (len(self), ", ".join(repr(x) for x in self))
	def __str__(self): return repr(self)

	size = property(lambda self: len(self))

	# sadly this: v.x = 5 is impossible in python if i want to base my vectors on immutable types

	# v2(1)					-> v2(1,1)
	# v2(v2(1,2))
	#   or v2((1,2))
	#   or v2([1,2])
	#   etc.				-> v2(2,3)
	# v2(2,3)				-> v2(2,3)
	# v3(v2(1,2),3)			-> v3(1,2,3)
	# v3(v2(1,2),3)			-> v3(1,2,3)
	# v3(1,v2(2,3))			# not allowed
	def __new__(cls, *args, size=None):
		l = len(args)
			
		if l == 1:
			if isvec(args[0]):
				arr = args[0] # tuple/list/etc. passed in
			else:
				if not size:
					raise ValueError("Vector(scalar): single scalar for all size, size needs to be specified")
				arr = (args[0],) * size # single scalar for all size

		elif all(not isvec(arg) for arg in args):
			arr = args # all scalars specified
		elif l > 1:
			if not isvec(args[0]) or len(args[0]) < 2:
				raise ValueError("Vector(Vector, scalars): Vector needs to be at least v2")
				
			arr = args[0] # tuple/list/etc. as first arg

			arr = tuple(arr) + args[1:]
		else:
			raise ValueError("Vector() needs at least one argument")

		if size and size < len(arr):
			arr = arr[:size] # downcast
		elif size and size > len(arr): # upcast
			remain = size -len(arr)
			
			arr = list(arr)
			if remain > 1:
				arr += [0 for i in range(remain -1)]
			arr.append(1)

		return tuple.__new__(cls, arr)
	
	x = property(lambda self: self[0] if 0 < self.size else None)
	y = property(lambda self: self[1] if 1 < self.size else None)
	z = property(lambda self: self[2] if 2 < self.size else None)
	w = property(lambda self: self[3] if 3 < self.size else None)
		
	# with this way of implementing the operators a 'v2() + v2()' is ~60x slower than a tuple concat, which seems ridiculous to me
	# this probably is because of the creation of temporary tuples and lists (which i think is implossible to prevent while my vectors are based on immutable tuples)
	# function call overhead might also be a source of big overhead
	# the only way of making it faster (reduce temp tuples, lists and func calls) (but still slower than tuple concat) is to write the operators for each Vector size and each op manually
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

	def divmod(self, other): # elementwise divmod would return Vector of tuples, we want tuple of vectors
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
			raise ValueError("Vector must be of size %d for operation ('%s')" % (size, repr(self)))

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

class v2(Vector):
	def __new__(cls, *args):	return Vector.__new__(cls, *args, size=2)
	def __repr__(self):
		return "v2(%s)" % (", ".join([repr(x) for x in self]))
class v3(Vector):
	def __new__(cls, *args):	return Vector.__new__(cls, *args, size=3)
	def __repr__(self):
		return "v3(%s)" % (", ".join([repr(x) for x in self]))
class v4(Vector):
	def __new__(cls, *args):	return Vector.__new__(cls, *args, size=4)
	def __repr__(self):
		return "v4(%s)" % (", ".join([repr(x) for x in self]))

shorthand_vectors = { 2:v2, 3:v3, 4:v4 }

def length_sqr(self):
	return sum(self * self)

def length(v):
	return math.sqrt( sum(v * v) )

def normalize(v):
	return v / length(v)

def normalize_or_zero(v):
	len = length(v)
	if len == 0:
		return 0
	return v / len

def dot(l, r):
	Vector.same_vecs(l, r)
	return sum(l * r)

def cross(l, r): # cross(v3,v3): cross product,  cross(v2,v2):  cross product hack, same as cross(v3(self, 0), v3(other, 0)).z, ie. the cross product of the 2d vectors on the z=0 plane in 3d space and then return the z coord of that (signed mag of cross product)
	Vector.same_vecs(l, r)

	if len(l) == 3:
		return v3(	l.y * r.z - l.z * r.y,
					l.z * r.x - l.x * r.z,
					l.x * r.y - l.y * r.x )
	elif len(l) == 2:
		return l.x * r.y - l.y * r.x
	else:
		raise ValueError("Vectors must be of size 2 or 3 for cross product ('%s')" % (size, repr(self)))

def vmax(l, *args):
	return l.__class__([max(*x) for x in zip(l,*args)])
def vmin(l, *args):
	return l.__class__([min(*x) for x in zip(l,*args)])

def clamp(v, a,b):
	return vmin( vmax(v,a), b)

def lerp(a, b, t):
	return (a * (1-t)) +(b * t)

def map(x, in_a, in_b, out_a=0, out_b=1):
	return (x - in_a) / (in_b - in_a) * (out_b - out_a) + out_a
	

def rotate90(v): # rotate v2 by 90 degrees counter clockwise
	Vector.is_vec(v, 2)
	return v2(-v.y, v.x)

def rotate_unit(ang):
	s,c = math.sin(ang), math.cos(ang)
	return Matrix(c, s)
