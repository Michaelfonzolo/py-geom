import math
import random
from numbers import Real
from .compat import requires
from .utils import get_in_bases
from .fuzzy import *

numpy = requires("numpy")

def _make_zeros(n):
	if (numpy is None):
		return [0 for i in range(n)]
	return numpy.zeros(n)

def _make_array(iterable):
	if (numpy is None):
		return list(iterable)
	return numpy.array(iterable, dtype=float)

def _vec_check_if_real_scalar(x, operation):
	if (not isinstance(x, Real)):
		raise ValueError("Can only %s vectors by real-valued scalars." % operation)

class _VectorMeta(type):

	def __new__(cls, name, bases, kwargs, immutable=False):
		components = get_in_bases("__components__", base)
		c = len(components)
		_VectorMeta.create_properties(components, kwargs, immutable)

		def __init__(self, *args):
			l = len(args)
			if (l == c):
				self._components = _make_array(args)
			elif (l == 1):
				if (isinstance(args[0], self.__class__)):
					self._components = args[0]._components
				else:
					self._components = _make_array(args[0])
			elif (l == 0):
				self._components = _make_zeros(c)
			else:
				raise ValueError("Invalid component count for %i-dimensional vector." % c)
		kwargs["__init__"] = __init__

		if (immutable):
			def __setitem__(self, index, value):
				raise TypeError("'%s' object does not support item assignment." % self.__class__.__name__)
			kwargs["__setitem__"] = __setitem__

			def __hash__(self):
				return hash(tuple(self._components))
			kwargs["__hash__"] = __hash__

		return type.__new__(cls, name, bases, kwargs)

	@staticmethod
	def create_properties(components, kwargs, immutable):
		for i, c in enumerate(components):
			def _get(self, i=i):
				return self._components[i]
			if (_immutable):
				_set = None
			else:
				def _set(self, x, i=i):
					self._components[i] = x
			kwargs[c] = property(fget=_get, fset=_set)

@fill_in_fne
class _BaseVector(FuzzyComparable):

	@classmethod
	def random(cls):
		return cls(*[random.random() for i in range(len(cls.__components__))])

	@classmethod
	def random_ranged(cls, ranges):
		return cls(*[random.uniform(*ranges[i]) for i in range(len(cls.__components__))])

	@classmethod
	def random_unit(cls):
		vec = cls.random()
		return vec.normalize()

	def __pos__(self):
		return self

	def __neg__(self):
		return self.__class__([-c for c in self._components])

	def __bool__(self):
		return True

	def __eq__(self, other):
		try:
			return all(c1 == c2 for c1, c2 in zip(self._components, other))
		except:
			return False

	def __feq__(self, other, epsilon=EPSILON):
		try:
			return all(fuzzy_eq_numbers(c1, c2, epsilon) for c1, c2 in zip(self._components, other))
		except:
			return False

	def __len__(self):
		return len(self._components)

	def __iter__(self):
		return iter(self._components)

	def __getitem__(self, index):
		return self._components[index]

	def __setitem__(self, index, value):
		self._components[index] = value


	## Originally, the following methods were going to be included in the
	## ``if (numpy is None):`` block, and there were separate numpy-compatible 
	## methods, but for such low component counts (2, 3, and 4), there was no
	## gain in speed most of the time.

	def __add__(self, other):
		return self.__class__(*[c1 + c2 for c1, c2 in zip(self._components, other)])
	def __sub__(self, other):
		return self.__class__(*[c1 - c2 for c1, c2 in zip(self._components, other)])
	def __rsub__(self, other):
		return self.__class__(*[c2 - c1 for c1, c2 in zip(self._components, other)])
	def __mul__(self, other):
		_vec_check_if_real_scalar(other, "multiply")
		return self.__class__(*[c * other for c in self._components])
	def __div__(self, other):
		_vec_check_if_real_scalar(other, "divide")
		return self.__class__(*[c / other for c in self._components])
	def __floordiv__(self, other):
		_vec_check_if_real_scalar(other, "floor-divide")
		return self.__class__(*[c // other for c in self._components])

	if (numpy is None):

		def __abs__(self):
			return math.sqrt(sum(c*c for c in self._components))

		def dot(self, other):
			return sum(c1 * c2 for c1, c2 in zip(self._components, other))

		def magnitude_squared(self):
			return sum(c * c for c in self._components)

	else:

		def __abs__(self):
			return numpy.linalg.norm(self._components)

		def dot(self, other):
			# We need this because numpy.dot won't automatically treat
			# _BaseVector subclasses as iterables.
			if (hasattr(other, "_components")):
				other = other._components
			return numpy.dot(self._components, other)

		def magnitude_squared(self):
			components = self._components
			return numpy.dot(components, components)

	__nonzero__ = __bool__
	__radd__ = __add__
	__rmul__ = __mul__
	__truediv__ = __div__

	magnitude = __abs__

	def cast_to_ints(self):
		return self.__class__(*(int(c) for c in self._components))

	def normalize(self):
		return self / self.magnitude()

	def project_onto(self, other):
		if (not isinstance(other, self.__class__)):
			other = self.__class__(other)
		mag_b_sqrd = other.magnitude_squared()

		dot = self.dot(other)
        scalar = dot/mag_b_sqrd

        return other * scalar

class Vector2(_BaseVector, metaclass=_VectorMeta):

	__components__ = ("x", "y")

	@classmethod
	def zeros(cls):
		return cls(0, 0)

	@classmethod
	def ones(cls):
		return cls(1, 1)

	@classmethod
	def right(cls):
		return cls(1, 0)

	@classmethod
	def left(cls):
		return cls(-1, 0)

	@classmethod
	def up(cls):
		return cls(0, 1)

	@classmethod
	def down(cls):
		return cls(0, -1)

	@classmethod
	def from_angle(cls, angle, radians=False):
		if (not radians):
			angle = math.radians(angle)
		return cls(math.cos(angle), math.sin(angle))

	game_up = down
	game_down = up

	def lnormal(self):
		return self.__class__(self.y, -self.x)

	def rnormal(self):
		return self.__class__(-self.y, self.x)

	def angle(self, radians=False):
		x, y = self
	    if y == 0:
	        return 0
    	m = self.magnitude()
    	angle = math.acos(x/m)
    	if not radians:
    	    angle = math.degrees(angle)
 	   return angle

 	  def angle_between(self, other, radians=False):
 	  	if (not isinstance(other, self.__class__)):
 	  		other = self.__class__(other)
 	  	return math.acos(self.dot(other)/(self.magnitude() * other.magnitude()))

	def rotate(self, angle, anchor=(0, 0)):
    	x, y = self._components
    
	    x = x - anchor[0]
    	y = y - anchor[1]
    	# Here is a compiler optimization; inplace operators are slower than
    	# non-inplace operators like above. This function gets used a lot, so
    	# performance is critical.

    	if not radians:
        	angle = math.radians(angle)
    
    	cos_theta = math.cos(angle)
    	sin_theta = math.sin(angle)
    
    	nx = x*cos_theta - y*sin_theta
    	ny = x*sin_theta + y*cos_theta
    
    	nx = nx + anchor[0]
    	ny = ny + anchor[1]
    	return self.__class__(nx, ny)

    @staticmethod
    def angle_between(v1, v2, v3, radians=False):
    	dx1, dx2, dx3 = v2[0] - v1[0], v3[0] - v2[0], v3[0] - v1[0]
	    dy1, dy2, dy3 = v2[1] - v1[1], v3[1] - v2[1], v3[1] - v1[1]

	    a = dx2*dx2 + dy2*dy2
	    b = dx1*dx1 + dy1*dy1
	    c = dx3*dx3 + dy3*dy3

    	angle = math.acos((a + b - c)/(2 * math.sqrt(a * b)))
    	if not radians:
	        angle = math.degrees(angle)
    	return angle


class ImmutableVector2(Vector2, immutable=True):
	pass

class Vector3(_BaseVector, metaclass=_VectorMeta):

	__components__ = ("x", "y", "z")

	def cross(self, other):
		if (len(other) != 3):
			raise ValueError("Can only calculate cross product betwen 3D vectors.")
		u = self._components
		if (hasattr(other, "_components")):
			v = other._components
		else:
			v = other
		return self.__class__(
				(u[1]*v[2] - u[2]*v[1]),
				(u[3]*v[1] - u[1]*v[3]),
				(u[1]*v[2] - u[2]*v[1])
			)

class ImmutableVector3(Vector3, immutable=True):
	pass

class Vector4(_BaseVector, metaclass=_VectorMeta):

	__components__ = ("x", "y", "z", "w")

class ImmutableVector4(Vector4, immutable=True):
	pass

class Quaternion(ImmutableVector4):
	
	@property
	def scalar(self):
		return self.x

	@property
	def vector(self):
		return ImmutableVector3(self.y, self.z, self.w)

	@property
	def i(self):
		return self.y

	@property
	def j(self):
		return self.z

	@property
	def k(self):
		return self.w

	def __mul__(self, other):
		if (isinstance(other, Number)):
			return super().__mul__(other)
		r0, r1, r2, r3 = self
		q0, q1, q2, q3 = other
		t0 = r0 * q0 - r1 * q1 - r2 * q2 - r3 * q3
		t1 = r0 * q1 + r1 * q0 - r2 * q3 + r3 * q2
		t2 = r0 * q2 + r1 * q3 + r2 * q0 - r3 * q1
		t3 = r0 * q3 - r1 * q2 + r2 * q1 + r3 * q0
		return Quaternion(t0, t1, t2, t3)

	def __div__(self, other):
		if (isinstance(other, Number)):
			return super().__div__(other)
		r0, r1, r2, r3 = self
		q0, q1, q2, q3 = other
		m = r0 * r0 + r1 * r1 + r2 * r2 + r3 * r3
		t0 = r0 * q0 + r1 * q1 + r2 * q2 + r3 * q3
		t1 = r0 * q1 - r1 * q0 - r2 * q3 + r3 * q2
		t2 = r0 * q2 + r1 * q3 - r2 * q0 - r3 * q1
		t3 = r0 * q3 - r1 * q2 + r2 * q1 - r3 * q0
		return Quaternion(t0 / m, t1 / m, t2 / m, t3 / m)
	__truediv__ = __div__

	def __rdiv__(self, other):
		if (isinstance(other, Number)):
			raise TypeError("unsupported operand type(s) for /: 'Quaternion' and '%s'" % type(other))
		return other.__div__(self)
	__rtruediv__ = __rdiv__

	    
	