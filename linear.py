from .vector import *
from .compat import *
from .fuzzy import *

numpy = try_import("numpy")

class _LineBase(object):

	def __init__(self, start, end):
		self._start = change_vector_dimension(start, self.__dimension__, True)
		self._end = change_vector_dimension(end, self.__dimension__, True)

	def __getitem__(self, index):
		if (index == 0):
			return self._start
		elif (index == 1):
			return self._end
		raise IndexError("%s index out of range" % self.__class__.__name__)

	def is_point_in_range(self, point):
		raise NotImplementedError()

	def is_orthogonal(self, epsilon=EPSILON):
		return (self._end - self._start).is_orthogonal(epsilon)

	def is_parallel_with(self, other, epsilon=EPSILON):
		s1, e1, s2, e2 = rectify_vectors(self._start, self._end, other[0], other[1])
		return fuzzy_eq(e1 - s1, e2 - s2, epsilon)

	def perpendicular_distance(self, point):
		a = self._start
		p = rectify_vector(a, point)
		n = self._end - a
		b = a - p
		return (b - b.dot(n)*n).magnitude()

	@requires("numpy")
	def point_of_intersection(self, other):
		poi = self._poi(other)
		is_in_range = self.is_point_in_range(poi)
		if (is_in_range and isinstance(other, _LineBase)):
			is_in_range &= other.is_point_in_range(poi)
		if (not is_in_range):
			return None
		return poi

	def _poi(self, other):
		s1, e1, s2, e2 = rectify_vectors(self._start, self._end, other[0], other[1])
		a1, a2 = s1, s2
		d1, d2 = e1 - s1, e2 - s2
		b = numpy.matrix([list(a2 - a1)]).transpose()
		A = numpy.matrix([list(d1), list(-d2)]).transpose()
		T = numpy.linalg.pinv(A) * b
		t1 = T[0, 0]
		t2 = T[1, 0]

		p1 = a1 + t1*d1
		p2 = a2 + t2*d2
		if (fuzzy_eq(p1, p2)):
			return p1
		return None # Lines are skew

	@requires("numpy")
	def is_skew_with(self, other, epsilon=EPSILON):
		s1, e1, s2, e2 = rectify_vectors(self._start ,self._end, other[0], other[1])
		A = numpy.matrix([
				list(s1 - e1),
				list(e1 - s2),
				list(s2 - e2)
			])
		V = abs(numpy.linalg.det(A))
		return fuzzy_eq_numbers(V, 0, epsilon)

class _Line2DBase(_LineBase):

	__dimension__ = 2

	@property
	def slope(self):
		return (self._end[1] - self._start[1])/(self._end[0] - self._start[0])

	def is_vertical(self, epsilon=EPSILON):
		return fuzzy_eq(self._start[0], self._end[0], epsilon)

	def is_horizontal(self, epsilon=EPSILON):
		return fuzzy_eq(self._start[1], self._end[1], epsilon)

	def _poi(self, other):
		s1, e1, s2, e2 = rectify_vectors(self._start, self._end, other[0], other[1])
		if (len(s1) != self.__dimension__):
			return super()._poi(other)
		poi = self.
		x1, y1 = s1
		x2, y2 = e1
		x3, y3 = s2
		x4, y4 = e2

		if x1 == x2 and x3 == x4:
		    return None

		if x1 == x2:
		    m1 = (y4 - y3)/(x4 - x3)
		    b1 = y3 - m1*x3
		    py = m1*x1 + b1
		    return Vector2(x1, py)

		elif x3 == x4:
		    m1 = (y2 - y1)/(x2 - x1)
		    b1 = y1 - m1*x1
		    py = m1*x3 + b1
		    return Vector2(x3, py)

		m1 = (y2 - y1)/(x2 - x1)
		m2 = (y4 - y3)/(x4 - x3)

		if m1 == m2:
		    return None

		b1 = y1 - m1*x1
		b2 = y3 - m2*x3

		px = (b2 - b1)/(m1 - m2)
		py = m1 * px + b1

		return Vector2(px, py)

	def is_skew_with(self, other, epsilon=EPSILON):
		s1, e1, s2, e2 = rectify_vectors(self._start, self._end, other[0], other[1])
		if (len(s1) != self.__dimension__):
			return super().is_skew_with(other, epsilon)
		return fuzzy_eq((e1 - s1).normalize(), (e2 - s2).normalize(), epsilon)

	is_parallel_with = is_skew_with

class _Line3DBase(_LineBase):

	__dimension__ = 3

class Line2D(_Line2DBase):

	@property
	def y_intercept(self):
		x1, y1 =  self._start
		x2, y2 = self._end
		if x1 == x2:
		    return None
		m = self._slope
		return y1 - m*x1

	@property
	def x_intercept(self):
		x1, y1 = self._start
		x2, y2 = self._end
		if y1 == y2:
		    return None
		if x1 == x2:
		    return x1
		m = self._slope
		b = self._y_intercept
		return -b/m

	def is_point_in_range(self, point):
		return True

	def length(self):
		return float('inf')

class Ray2D(_Line2DBase):

	def is_point_in_range(self, point):
		px, py = change_vector_dimension(point, self.__dimension__)
		x1, y1 = self._start
		x2, y2 = self._end
		if x1 == x2:
		    return (y1 < py) == (y1 < y2)
		return (x1 < px) == (x1 < x2)

	def length(self):
		return float('inf')

class Segment2D(_Line2DBase):

	def is_point_in_range(self, point):
		px, py = change_vector_dimension(point, self.__dimension__)
		x1, y1 = self._start
		x2, y2 = self._end
		if x1 == x2:
		    return (y1 < py) == (py < y2)
		return (x1 < px) == (px < x2)

	def length(self):
		return (self._end - self._start).magnitude()

class Line3D(_Line3DBase):

	def is_point_in_range(self, point):
		return True
