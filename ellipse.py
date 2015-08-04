import math

from .exception import *
from .vector import *
from .fuzzy import *
from .functools import reduce

scipy = try_import("scipy")


class Ellipse(object):

	def __init__(self, x, y, a, b):
		self.center = ImmutableVector2(x, y)
		self.a = a
		self.b = b

	def __repr__(self):
		return "%s(%s, %s, %s)" %
			(
				self.__class__.__name__,
				self.center,
				self.a,
				self.b
			)

	def __getitem__(self, index):
		if (index == 0):
			return self.center.x
		elif (index == 1):
			return self.center.y
		elif (index == 2):
			return self.a
		elif (index == 3):
			return self.b
		raise index_out_of_range(type(self))

	def __iter__(self):
		return iter([self.center.x, self.center.y, self.a, self.b])

	def __eq__(self, other):
		return all(self[i] == other[i] for i in range(4))

	def __feq__(self, other, epsilon=EPSILON):
		return all(fuzzy_eq_numbers(self[i], other[i], epsilon) for i in range(4))

	@property
	def eccentricity(self):
		return math.sqrt(1 - (self.b/self.a)**2)

	if (scipy is None):

		@property
		def circumference(self):
			a, b = self.a, self.b
			h = 3*((a - b)/(a + b))**2
			return math.pi*(a + b)*(1 + h/(10 + math.sqrt(4 - 3*h)))

	else:

		@property
		def circumference(self):
			return 4*self.a*scipy.special.ellipe(self.eccentricity)

	def is_circle(self, epsilon=EPSILON):
		return fuzzy_eq_numbers(self.a, self.b, epsilon)

	def contains_point(self, point):
		x, y = change_vector_dimension(point, 2) - self.center
		return (x/self.a)**2 + (y/self.b)**2 <= 1

	def translate(self, delta):
		self.center += change_vector_dimension(delta, 2)

class Ellipsoid3D(object):

	__dimension__ = 3

	def __init__(self, x, y, z, a, b, c):
		self.center = ImmutableVector3(x, y, z)
		self.a = a
		self.b = b
		self.c = c

	def __repr__(self):
		return "%s(%s, %s, %s, %s)" %
			(
				self.__class__.__name__,
				self.center,
				self.a,
				self.b,
				self.c
			)

	def __getitem__(self, index):
		if (index == 0):
			return self.center.x
		elif (index == 1):
			return self.center.y
		elif (index == 2):
			return self.center.z
		elif (index == 3):
			return self.a
		elif (index == 4):
			return self.b
		elif (index == 5):
			return self.c
		raise index_out_of_range(type(self))

	def __iter__(self):
		return iter([self.center.x, self.center.y, self.center.z, self.a, self.b, self.c])

	def __eq__(self, other):
		return all(self[i] == other[i] for i in range(6))

	def __feq__(self, other, epsilon=EPSILON):
		return all(fuzzy_eq_numbers(self[i], other[i], epsilon) for i in range(6))

	if (scipy is None):

		@property
		def surface_area(self):
			p = 1.6075
			a, b, c = self.a, self.b, self.c
			return 4*math.pi*(((a*b)**p + (b*c)**p + (a*c)**p)/3)**p

	else:

		@property
		def surface_area(self):
			a, b, c = self.a, self.b, self.c
			c_sqrd = c*c
			k = a/b * math.sqrt((b*b - c_sqrd)/(a*a - c_sqrd))
			phi = math.acos(c/a)
			return 2*math.pi*(
				c_sqrd + a*b/math.sin(phi)*(
					scipy.special.ellipeinc(phi, k)*math.sin(phi)**2 +
					scipy.special.ellipkinc(phi, k)*math.cos(phi)**2
					)
				)

	def is_spherical(self, epsilon=EPSILON):
		return fuzzy_eq_numbers(self.a, self.b, EPSILON) and 
			   fuzzy_eq_numbers(self.b, self.c, EPSILON) and
			   fuzzy_eq_numbers(self.a, self.c, EPSILON)
			   # fuzzy_eq(a, b) and fuzzy_eq(b, c) does not imply fuzzy_eq(a, c)

	def contains_point(self, point):
		x, y, z = change_vector_dimension(point, 3) - self.center
		return (x/self.a)**2 + (y/self.b)**2 + (z/self.c)**2 <= 1

	def translate(self, delta):
		self.center += change_vector_dimension(delta, 3)


