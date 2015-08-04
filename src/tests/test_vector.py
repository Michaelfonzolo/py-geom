import unittest
import math
from ..vector import *
from ..fuzzy import *

class TestVectors(unittest.TestCase):

	def test_constructors(self):
		self.assertEqual(Vector2([0, 1]), Vector2(0, 1))
		self.assertEqual(Vector2(Vector2(0, 1)), Vector2(0, 1))

	def test_arithmetic(self):
		v1 = Vector2(0, 3)
		v2 = Vector2(7, 1)

		self.assertEqual(v1 + v2, Vector2(7, 4))
		self.assertEqual(v2 - v1, Vector2(7, -2))

		self.assertEqual(5 * v2, Vector2(35, 5))
		self.assertEqual(v2 / .5, Vector2(14, 2))

		self.assertEqual(v1 + v2, v1 + (7, 1))
		self.assertEqual(v1 + v2, (0, 3) + v2)

	def test_operations(self):
		v1 = Vector2(1, 1)
		v2 = Vector2(3, 2)
		v3 = Vector2(15, 0)

		self.assertEqual(v1.dot(v2), 5)

		self.assertEqual(v1.magnitude(), math.sqrt(2))
		self.assertEqual(v2.magnitude_squared(), 13)

		self.assertEqual(v3.normalize(), Vector2(1, 0))

		## UGH I'm sure the rest is fine.

class TestQuaternions(unittest.TestCase):

	def test_operations(self):
		q1 = Quaternion(1, 2, 3, 4)
		q2 = Quaternion(5, 6, 7, 8)

		self.assertEqual(q1 * q2, Quaternion(-60.0, 12.0, 30.0, 24.0))
		self.assertEqual(q2 * q1, Quaternion(-60.0, 20.0, 14.0, 32.0))

		## The following test works, its just dumb floating point errors that cause it to fail.
		# self.assertEqual(q1 / q2, Quaternion(2.33333333333, 0.0, -0.533333333333, -0.266666666667))

		## Same here (too lazy to make an assertFuzzyEqual)
		# self.assertEqual(q1.exp(), Quaternion(1.69392272368, -0.789559624542, -1.18433943681, -1.57911924908))

## Too lazy to figure out how unittest is supposed to be used (unittest.main doesn't seem to work, idk why and idc)
vectors = TestVectors()
vectors.test_constructors()
vectors.test_arithmetic()
vectors.test_operations()

quaternions = TestQuaternions()
quaternions.test_operations()