import math

from .vector import *
from .compat import *

scipy = try_import("scipy.integrate")

def _choose(n, k):
	return math.factorial(n)/math.factorial(k)/math.factorial(n - k)

def bernstein(i, n, x):
	return _choose(n, i)*x**i*(1 - x)**(n - i)

class BezierCurve(object):

	def __init__(self, *control_polygon):
		self.control_polygon = rectify_vectors(*control_polygon, immutable=True)

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
		for i in range(line_segments):
			arclength += (self.evaluate_at(tn) + self.evaluate_at(tn + step)).magnitude()
			tn += step
		return arclength

