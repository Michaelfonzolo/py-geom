import math

from .fuzzy import *
from .vector import *
from .functools import reduce

scipy = try_import("scipy")


class Ellipse(object):

	def __init__(self, a, b):
		self.a = a
		self.b = b

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
		x, y = change_vector_dimension(point, 2)
		return (x/self.a)**2 + (y/self.b)**2 <= 1		

class Ellipsoid3D(object):

	__dimension__ = 3

	def __init__(self, a, b, c):
		self.a = a
		self.b = b
		self.c = c

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
		x, y, z = change_vector_dimension(point, 3)
		return (x/self.a)**2 + (y/self.b)**2 + (z/self.c)**2 <= 1


