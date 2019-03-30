from Vector import *

# TODO:
#  matricies
#  -hmat ?
#  -no m2 m3 etc., let mats be flexible?
#  -mats are inherited from tuple
#  quaternions

def timeit():
	import timeit
	
	setup = '''
	import vectors as v
	a = v.v2(3,5)
	b = v.v2(-1,55)
	'''
	time = timeit.Timer('c = a +b', setup=setup).repeat()
	time = [t / 1000000 * 1000 * 1000 for t in time] # in us

#timeit()

a = (3,5)

#a = v2()
b = v2(1)
#c = v2((1,))
d = v2((1,2))
e = v3(d,7)
f = v3(1,-7,7)

#b.z = 4 # slots prevent this (and make class more efficient)

p = b.y

#b.y = 7
b = v2(b.x, 7)
#b.y -= 7
b = v2(b.x, b.y -7)

#b[0] = b[1]
#b[2]

g = b - d
g = b - 2
g = 2 - b

a = 2

a -= b

g -= 2
#g += e

a = v2(1,2) + -2
a = 5 - v2(1,2)
a = v2(2,3) * v2(4,5)
a = v2(2,3) * 4
a = 5 * v2(2,3)
a = v2(2,3) / 2
a = v2(2,3) // 2
a = v2(2,3) % 2
a = divmod(v2(2,3), 2)

a = pow(v2(2,2), v2(3,4))
a = pow(v2(2,2), v2(3,4), v2(None, 2))

a = pow(v2(2,2), v2(3,4), 10)
a = pow(2, v2(3,4))

a = 1 << v2(2,4)
a = 1024 >> v2(9,8)
a = 3 & v2(1,2)
a = 1 | v2(2,4)
a = 3 ^ v2(1,2)

a = -v2(-1,3)
a = +v2(-1,3)
a = abs(v2(-1,66))
a = ~v2(-1,0xffff)

a = round(v2(0.5,1.5))
a = round(v2(0.9999,100000000.2), 3)
a = math.ceil(v2(-0.5,+0.5))
a = math.floor(v2(-0.5,+0.5))
a = math.trunc(v2(-0.5,+0.5))

a = all(v3(True, False, True))
a = all(v3(True, True, True))
a = any(v3(False, True, False))
a = any(v3(False, False, False))

a = v2(1,2) < v2(1,1)
a = v2(1,2) > 1
a = 1 <= v2(1,2)
a = 1 >= v2(1,2)
a = 1 != v2(1,2)
a = 1 == v2(1,2)

a = any(v2(1,1) == v2(1,2))

a = length_sqr(v2(5,5))
a = length(v2(5,5))
a = dot(v2(0,5), v2(-20,0))
a = dot(v2(1,0), v2(2,0))
a = dot(v2(1,2), v2(2,-0.4))

a = cross(v3(1,1,0), v3(-1,-1,0))
a = cross(v3(1,1,0), v3(+1,-1,0))

a = cross(v2(1,1), v2(+1,-1))
a = cross(v2(0,1), v2(1,0))

a = rotate90(v2(1,2))

a = repr(v2(1,2))
a = repr(Vector(1,2))

a = vmax(Vector(-2,-1,0,1,2), Vector(0,0,0,0,0))
a = vmin(Vector(-2,-1,0,1,2), Vector(0,0,0,0,0))

a = clamp(	Vector(-5,5,3,2),
			Vector(0,0,2,2),
			Vector(2,3,3,3) )

a = [lerp(1,2, x*0.25) for x in range(5)]

a = [map(x, 0,4, 0,2) for x in range(5)]

a = v4(1,2,3,4)
b = v2(a)

a = Vector(1,2, size=4)

b = v3(a)

pass
