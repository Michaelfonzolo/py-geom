import math
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

	def __pos__(self):
		return self

	def __neg__(self):
		return self.__class__([-c for c in self._components])

	def __abs__(self):
		return math.sqrt(sum(c*c for c in self._components))

	def __bool__(self):
		return True

	def __eq__(self, other):
		try:
			return all(c1 == c2 for c1, c2 in zip(self._components, other))
		except:
			return False

	def __feq__(self, other):
		try:
			return all(fuzzy_eq_numbers(c1, c2) for c1, c2 in zip(self._components, other))
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

		def dot(self, other):
			return sum(c1 * c2 for c1, c2 in zip(self._components, other))

		def magnitude_squared(self):
			return sum(c * c for c in self._components)

	else:

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

	game_up = down
	game_down = up

class ImmutableVector2(Vector2, immutable=True):

	pass

class Vector3(_BaseVector, metaclass=_VectorMeta):

	__components__ = ("x", "y", "z")

class Vector4(_BaseVector, metaclass=_VectorMeta):

	__components__ = ("x", "y", "z", "w")

class Quaternion(Vector4, metaclass=_VectorMeta):

	pass