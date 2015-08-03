from numbers import Real

EPSILON = 1e-8

class FuzzyComparable(object):
	
	def __feq__(self, other, epsilon=EPSILON):
		raise NotImplementedError()

	def __fne__(self, other, epsilon=EPSILON):
		raise NotImplementedError()

def fuzzy_eq_numbers(a, b, epsilon=EPSILON):
	return abs(a - b) <= epsilon

def fuzzy_eq(a, b, epsilon=EPSILON):
	if (isinstance(a, Complex) or isinstance(b, Complex)):
		return fuzzy_eq_numbers(a, b, epsilon)
	elif (isinstance(a, FuzzyComparable)):
		return a.__feq__(b)
	elif (isinstance(b, FuzzyComparable)):
		return b.__feq__(a)
	return a.__eq__(b)

def fill_in_fne(cls):
	cls.__fne__ = lambda self, other, epsilon=EPSILON: not self.__feq__(other, epsilon)
	return cls