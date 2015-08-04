import math

from .vector import *
from .compat import *
from .fuzzy import *

scipy = try_import("scipy.integrate")

__all__ = ["BezierCurve"]

def _choose(n, k):
	return math.factorial(n)/math.factorial(k)/math.factorial(n - k)

def bernstein(i, n, x):
	return _choose(n, i)*x**i*(1 - x)**(n - i)

@fill_in_fne
class BezierCurve(FuzzyComparable):

	def __init__(self, *control_polygon):
		self.control_polygon = rectify_vectors(*control_polygon, immutable=True)

	def __repr__(self):
		string = "%s(" % self.__class__.__name__
		n = len(self.control_polygon)
		for i, v in enumerate(self.control_polygon):
			if (i == n - 1):
				string += str(v)
			else:
				string += str(v) + ", "
		return string + ")"

	def __iter__(self):
		return iter(self.control_polygon)

	def __len__(self):
		return len(self.control_polygon)

	def __eq__(self, other):
		try:
			return len(self) == len(other) and all(self[i] == other[i] for i in range(len(self)))
		except:
			return False

	def __feq__(self, other):
		try:
			return len(self) == len(other) and all(fuzzy_eq(self[i], other[i]) for i in range(len(self)))
		except:
			return False

	def evaluate_at(self, time):
		cp = self.control_polygon
		n = len(cp) - 1
		return sum(bernstein(i, n, time) * cp[i] for i in range(n + 1))

	def derivative(self):
		cp = self.control_polygon
		n = len(cp) - 1
		return BezierCurve(*[n*(cp[i + 1] - cp[i]) for i in range(n)])

	@requires("scipy")
	def arclength(self, lo=0, hi=1):
		dt = self.derivative()
		integrand = lambda t: dt(t).magnitude()
		return scipy.integrate.quad(integrand, lo, hi)[0]

	def approximate_arclength(self, line_segments):
		step = 1/line_segments
		tn = 0
		arclength = 0
		previous = self.evaluate_at(tn)
		for i in range(line_segments):
			next = self.evaluate_at(tn + step)
			arclength += (next - previous).magnitude()
			previous = next
			tn += step
		return arclength

