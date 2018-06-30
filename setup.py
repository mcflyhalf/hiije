from setuptools import setup
from sqlalchemy import *
from hiije import test_engine
from hiije import engine
from hiije import get_logger
from hiije import PopulateDB
import ConfigParser

setup()

logger = get_logger()

config_defaults = dict()

config_defaults.update({'itemTableName':'item'})
config_defaults.update({'transactionTableName':'transaction'})
config_defaults.update({'num_similarity_models':'1'})
config_defaults.update({'similarity model type':'Cosine similarity'})
config_defaults.update({'similarity model filename':'/media/ajossie/Ajossie/wamp/www/hiije/hiije/II Similarity matrix (cosine_sim)NORMALISED10.csv'})


class HiijeConfig:
	def __init__(self, config_defaults = config_defaults, config_filename = 'hiije_config.cfg'):
		self.config = ConfigParser.RawConfigParser(config_defaults, allow_no_value = True)
		self.config_filename = config_filename

	def configure_preferences(self, config_vals):
		self.config.add_section('User Values')
		for key,value in config_vals.iteritems():
			 self.config.set('User Values', key, value)
			 logger.debug("Configuring User value {} to {}".format(key,value))

			#The allowed keys are shown below with example values
				# self.config.set('User Values', 'itemTableName', 'item')
				# self.config.set('User Values', 'transactionTableName', 'transaction')
				# self.config.set('User Values','num_similarity_models', '1')
				# self.config.set('User Values','similarity model type', 'Cosine Similarity')
				# self.config.set('User Values','similarity model filename', '/opt/Cosine_sim_model' )

		with open(self.config_filename, 'wb') as configfile:
			self.config.write(configfile)
			logger.debug("Written config info to file {}".format(self.config_filename))

	def configure_database(self):
		#Create(but not populate) the database and db tables
		metadata = MetaData()
		item_table_name = self.config.get('User Values', 'itemTableName')
		transaction_table_name = self.config.get('User Values','transactionTableName')

		#Table > item
		## --------------------------------------
		##	ID		| 	Name	|	Fancy_name	|
		##----------------------------------------
		##
		## This table contains a list of all the items in the DB.
		# It will be used when converting the basket from a textual list to a binary transaction
		# which is required for the recommendation.
		# The fancy name field is the user readable version of the item's name whereas the 
		# Name is the fancy name in all lower case and with whitespace and non alpha 
		# characters removed. This is necessary so when requesting recoms, the request is 
		# case insensitive

		item = Table(item_table_name, metadata, 
			Column(item_table_name + "_id", Integer, primary_key=True),
			Column("name", String(25), nullable = False),
			Column("fancy_name", String(35)))



		# Table > transaction

		# -------------------------------------------------------------------------
		# 	Transaction ID	|	Transaction datetime	|	Transaction details	|
		# -------------------------------------------------------------------------

		# This table stores all the details of past transactions. Transaction ID is a Unique
		# ID for each transaction. Datetime is the timestamp of when the request was 
		# received by the server and details will be the json response that the recommender 
		# returns. This response contains the original basket and the recommendations
		# as well as datetime information.
		# Datetime is duplicated in the table as well so that recommendations can be ordered
		#  by time of request if necessary. 

		transaction = Table(transaction_table_name, metadata, 
			Column(transaction_table_name + "_id", Integer, primary_key=True),
			Column(transaction_table_name + "_datetime", DateTime(), nullable = False),
			Column(transaction_table_name +"_details", JSON))

		#Actually create the tables
		metadata.create_all(engine)
		logger.debug("The tables {} and {} currently exist".format(item_table_name,transaction_table_name))



#Create testdb and test table
config_vals = config_defaults
logger.warn("Creating Config values and creating databases")
hiijeconfig = HiijeConfig()
hiijeconfig.configure_preferences(config_vals)
logger.warn("Configured preferences in {}".format(hiijeconfig.config_filename))
hiijeconfig.configure_database()
logger.warn("Created databases for Hiije")

#populate db
itemIDfilename = "Item_IDs_169.txt"
logger.warn("Populating item Database from file {}".format(itemIDfilename))
populatedb = PopulateDB(itemIDfilename)
populatedb.populate_item_database()
logger.warn("Populated item Database")


#populate test db



#Create similarity matrix >>Now done in hiije.__init__



#Run test suite


