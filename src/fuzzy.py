from numbers import Number

__all__ = ["FuzzyComparable", "EPSILON", "fuzzy_eq_numbers", "fuzzy_eq", "fuzzy_ne", "fill_in_fne"]

EPSILON = 1e-8

class FuzzyComparable(object):
	
	def __feq__(self, other, epsilon=EPSILON):
		raise NotImplementedError()

	def __fne__(self, other, epsilon=EPSILON):
		raise NotImplementedError()

def fuzzy_eq_numbers(a, b, epsilon=EPSILON):
	return abs(a - b) <= epsilon

def fuzzy_eq(a, b, epsilon=EPSILON):
	if (isinstance(a, Number) or isinstance(b, Number)):
		return fuzzy_eq_numbers(a, b, epsilon)
	elif (isinstance(a, FuzzyComparable)):
		return a.__feq__(b, epsilon)
	elif (isinstance(b, FuzzyComparable)):
		return b.__feq__(a, epsilon)
	return a.__eq__(b)

def fuzzy_ne(a, b, epsilon=EPSILON):
	if (isinstance(a, Number)):
		return not fuzzy_eq_numbers(a, b, epsilon)
	elif (isinstance(a, FuzzyComparable)):
		return a.__fne__(b, epsilon)
	elif (isinstance(b, FuzzyComparable)):
		return b.__fne__(a, epsilon)
	elif (hasattr(a, "__ne__")):
		return a.__ne__(b)
	return not a.__eq__(b)

def fill_in_fne(cls):
	cls.__fne__ = lambda self, other, epsilon=EPSILON: not self.__feq__(other, epsilon)
	return cls