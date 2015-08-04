from .vector import *
from .compat import *
from .fuzzy import *

pygame = try_import("pygame")

__all__ = ["Rect"]

@fill_in_fne
class Rect(FuzzyComparable):

	def __init__(self, x, y, w, h):
		self.center = ImmutableVector2(x, y)
		self.width = w
		self.height = h

	def __repr__(self):
		return "%s(%s, %s, %s)" % \
			(
				self.__class__.__name__,
				self.center,
				self.width,
				self.height
			)

	def __iter__(self):
		return iter([self.center.x, self.center.y, self.width, self.height])

	def __eq__(self, other):
		try:
			return all(self[i] == other[i] for i in range(4))
		except:
			return False

	def __feq__(self, other, epsilon=EPSILON):
		try:
			return all(fuzzy_eq_numbers(self[i], other[i], epsilon) for i in range(4))
		except:
			return False

	def __getitem__(self, index):
		if (index == 0):
			return self.center.x
		elif (index == 1):
			return self.center.y
		elif (index == 2):
			return self.width
		elif (index == 3):
			return self.height
		raise index_out_of_range(type(self))

	@property
	def corners(self):
		x, y = self.center
		w = self.width
		h = self.height
		return [
			center,
			ImmutableVector2(x + w, y),
			ImmutableVector2(x + w, y + h),
			ImmutableVector2(x, y + h)
		]

	@property
	def area(self):
		return w*h

	@property
	def perimeter(self):
		return 2*(w + h)

	def is_square(self):
		return w == h

	def contains_point(self, point):
		x, y, w, h = self
		px, py = point
		return (x <= px) == (px <= x + w) and \
			   (y <= py) == (py <= y + h)

	def collides_rect(self, rect):
		x1, y1, w1, h1 = self
		x2, y2, w2, h2 = rect

		return x1 <= x2 + w2 and \
		       x1 + w1 >= x2 and \
		       y1 <= y2 + h2 and \
		       y1 + h1 >= y2

	def contains_rect(self, rect):
		x1, y1, w1, h1 = self
		x2, y2, w2, h2 = rect

		return x1 <= x2 and \
		       x1 + w1 >= x2 + w2 and \
		       y1 <= y2 and \
		       y1 + h1 >= y2 + h2

	def crosses_rect(self, rect):
		x1, y1, w1, h1 = self
		x2, y2, w2, h2 = rect

		return (
		        x1 <= x2 and \
		        x1 + w1 >= x2 + w2 and \
		        y1 >= y2 and \
		        y1 + h1 <= y2 + h2
		    ) or (
		        x1 >= x2 and \
		        x1 + w1 <= x2 + w2 and \
		        y1 <= y2 and \
		        y1 + h1 <= y2 + h2
		    )

	def translate(self, delta):
		self.center += change_vector_dimension(delta, 2)

	def union(self, rect):
		x1, y1, w1, h1 = self
		x2, y2, w2, h2 = rect

		ux, uy = min(x1, x2), min(y1, y2)
		max_x, max_y = max(x1 + w1, x2 + w2), max(y1 + h1, y2 + h2)

		uw, uh = max_x - ux, max_y - uy
		return Rect(ux, uy, max_x, max_y)

	def fuse(self, rect):
		x1, y1, w1, h1 = self
		x2, y2, w2, h2 = rect

		return Rect(x1, y1, max(w1, w2), max(h1, h2))

	@requires("pygame")
	def to_pygame_rect(self):
		return pygame.Rect(self.center.x, self.center.y, self.width, self.height)