from matrix import *

#a = Matrix()
#a = Matrix(0)

a = Matrix(size=(3,3))
a = Matrix(	(1,2),
			(3,4), size=(4,4))

#a = Matrix(	1,2,
#			3,4, size=(4,4))

a = Matrix("blah", "blah")

b = str(a)
a = Matrix((1,2,3), (4,5,6), (7,8,9))

a = Matrix(1,2,3, 4,5,6, 7,8,9, size=(3,3))

a = Matrix(1,2,3,4,5,6, size=(2,3))
a = Matrix(1,2,3,4,5,6, size=(3,2))

a = Matrix((1,2,3),(4,5,6), order='columns')

a = Matrix(1,2,3,4,5,6, order='columns', size=(2,3))
a = Matrix(1,2,3,4,5,6, order='columns', size=(3,2))

a = Matrix((1,2,3),(4,5,6), order='columns')

a = Matrix.identity((4,3))

a = translate(v2(1,2))
a = translate(v3(1,2,3))

a = scale(v2(-2,3))
a = scale(v3(-2,3,4))

str(a.columns)

str(a)

a = Matrix(translate(v2(1,2)), size=(20,20))

a = scale(v3(-2,3,1/2)) * translate((0,1,2))
a = translate((0,1,2)) * scale(v3(-2,3,1/2))

a = translate((0,1,2)) * v2(5,5)

pass
