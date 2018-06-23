#Tests for the hiije framework
import unittest

#Core framework tests

class TestRecommendations(unittest.TestCase):

	def test_minimum_recoms(self):
		pass

	def test_negative_recoms(self):
		pass

	def test_maximum_recoms(self):
		pass





#Integration tests (for integration with external dependencies)

class TestDatabase(unittest.TestCase):


	def test_db_connection(self):
		try:
			from __init__ import engine
			conn= engine.connect()
			res=conn.execute("SELECT * FROM testitems LIMIT 1")

		except:
			self.fail("Database Failure>> Could not connect to database or issue query")
	
	def test_random_thing(self):
		self.assertEqual(2,1+1)

