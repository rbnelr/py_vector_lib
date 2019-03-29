
class matrix(tuple):
	__slots__ = ()

	#def __repr__(self):
	#	return "v%d(%s)" % (len(self), ", ".join([repr(x) for x in self]))
	#def __str__(self): return repr(self)
	#
	#def __len__(self): # v2(columns, rows)
	#	return self._len

	# column major
	def __getitem__(self, key):
		if Vector.is_vec(key, 2):
			return super(self).__getitem__( key[0] * len(self)[1] + key[1] )
		else:
			return self.get_column(key)
	
	def get_column(self, indx):
		rows = len(self)[1]
		return super(self)[ indx * rows : indx * rows + rows ]

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
