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
			from hiije import test_engine as engine
			conn= engine.connect()
			res=conn.execute("SELECT * FROM item LIMIT 1")

		
		except ImportError:
			self.fail("Import Failure>> Could not import database engine")

		except KeyError:
			self.fail("OS Environment Failure>> Could not find certain environment variables")


		except:
			self.fail("General DB failure>> Try to manually issue the statements in test_hiije.TestDatabase.test_db_connection and see the resulting errors")

	
	def test_random_thing(self):
		self.assertEqual(2,1+1)

