from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import JSON
import os
import logging
import sys
import csv
import datetime

def load_matrix_from_csv(csvfile):
	item_sim_matrix = list()
	with open(csvfile, 'r') as csvmodel:
		line_num = 0
		for line in csvmodel:
			item_sim_matrix.append(list())
			temp_num = ''
			for ch in line:
				if ch not in {',','\n', '\r'}:
					temp_num += ch
				else:
					if temp_num != '':
						item_sim_matrix[line_num].append(float(temp_num))
						temp_num = ''

			line_num += 1
		item_sim_matrix = item_sim_matrix[:-1]


	return item_sim_matrix


def processWord(wordin):      # For each item(word), make it all lower case, remove special characters and white spaces
	word = wordin
	word.strip()
	word= word.lower()
	word= word.replace(" ","")
	for ch in word:
		if ch in "`~!@#$%^&*()_-+={[]}|',./?;:":
			word= word.replace(ch, "")

	return word


def processLine(line,itemCounts):      
	'''Identify each item in the line(assumes items are comma separated). Process word then add it to the dictionary)

	itemCounts should end up being a dictionary that looks like:
			{itemName: [itemoccurence,fancyitemName]}
	where itemName is the unique ID(all lowercase) and itemoccurence is an integer counter'''
	line= line.strip()            #Remove leading and trailing whitespace
 	while (line[-1] is ","):
		line= line[ :-1]            #Remove all trailing commas
    
	while ("," in line):
		item= line[ :line.find(",")]        #new substring comprising all characters upto the comma
		#item= processWord(item)             #Make all lower case, remove special xters and white spaces
		
		countItem(item,itemCounts)                     #Add item to dictionary or increase count if its already there

		line= line[line.find(",")+1: ]      #Remove this item from the current line

#When there are no more commas, line still contains 1 word
	while (line[-1] is ","):
		line= line[ :-1]					#REmove all trailing commas
	line= line.strip()
	#line= processWord(line)   
	countItem(line, itemCounts)
	return


def countItem(item,itemCounts):            #Add item to dictionary or increase count if its already there
	_item = processWord(item)
	if _item in itemCounts:
		itemCounts[_item][0] += 1

	else:
		itemCounts[_item] = [1, item]
	return



def get_item_list(itemList_file="Item_list_ALL.txt"):
	itemList = list()
	with open (itemList_file) as items:
		for item in items:
			if not (item.strip() == ''):
				itemList.append(item.strip())

	return itemList 



def text_2_binary_txn(textList, ormClass, sasession):
	"""Takes a 1Xn Text List and returns a 1x169 binary list with 1s where items were present in the original list and zeros otherwise"""
	if not isinstance(textList, list):
		raise TypeError("Input to function <text_2_binary_txn> must be of type <list>")

	indexList=[]
	binList=[]
	for thing in textList:
		temp= sasession.query(ormClass).filter(ormClass.name == thing.strip()).all()
		try:
			assert len(temp) == 1

		except:
			if len(temp) == 0:
				raise ValueError("Unknown item. Item <{}> not in database".format(thing))
		indexList.append(temp[0].item_id)
		#print temp.id


	for i in range(169):
		if i in indexList:
			binList.append(1)
			#print i

		else:
			binList.append(0)

	return binList


#TODO: fix this logger. Currently does not log info or lower

def get_logger():
	log = logging.getLogger(__name__)
	# File handler which logs even debug messages
	fh = logging.FileHandler('hiije.log')
	fh.setLevel(logging.DEBUG)
	# Console handler that logs warnings or higher
	ch = logging.StreamHandler()
	ch.setLevel(logging.INFO)
	# create formatter and add it to the handlers
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	fh.setFormatter(formatter)
	ch.setFormatter(formatter)
	# add the handlers to the logger
	print "Adding a set of handlers now"
	if len(log.handlers)< 2:
		log.addHandler(fh)
		log.addHandler(ch)
	return log
###########End of Global Functions#######################

###########Start of Global Classes########################
#------These are either used for setup or general purposes

log = get_logger()
class UniqueItemFile:
	def __init__(self, infile, outfilename = "Item_IDs"):
		assert isinstance(infile,file)		#infile should be a file object and not a filename
		self.infile = infile
		self.outfilename = outfilename

	def create(self, num_unique_ids = -1):
		tempDict = dict()

		for line in self.infile:
			processLine(line, tempDict)

		triplets = list(tempDict.items())

		item = [[integer, unique, fancy] for (unique, [integer, fancy]) in triplets]
		item.sort(reverse = True)

		assert num_unique_ids < len(item)

		if num_unique_ids < 0:
			count = len(item)
		else:
			count = num_unique_ids

		if not self.outfilename.endswith(".txt"):
			self.outfilename += "_{}.txt".format(count)

		outfile = open(self.outfilename, "w")

		for i in range (count):
			outfile.write(str(i+1))
			outfile.write(",")
			outfile.write(str(item[i][1]))
			outfile.write(",")
			outfile.write(item[i][2])
			outfile.write("\n")

		outfile.close()		#TODO: Save outfile location to global config file

# hpf = open("historical_purchases.csv" ,  "r")
# histpur = UniqueItemFile(hpf)
# histpur.create()

class CreateSimilarityMatrix:
	def __init__(self, filename,historical_transactions):	
		if filename.endswith(".csv"):
			self.filename = filename
			#										TODO: Also check that the filename doesnt already have another filetype e.g .txt or something
		else:
			self.filename = filename + ".csv"

	def cosineSim(self, k=50):
		#Create cosine similarity matrix
		#Remember to save the location of the matrix in the config file
		pass

	def conditionalProb(self, k=50):
		#Create conditional probability matrix
		#Remember to save the location of the matrix in config file
		pass






#create sqlalchemy engine (for actual use), test engine(for testing db connection) and session (only for the engine)

engine = create_engine('postgresql://{dbuser}:{passwd}@{host}:{port}/{dbname}'.format(\
	dbuser = os.environ['POSTGRES_USER'] ,
	passwd = os.environ['POSTGRES_PASS'],
	host = 'localhost',
	port = os.environ['POSTGRES_PORT'],
	dbname = os.environ['POSTGRES_HIIJE_DBNAME']))

Session = sessionmaker(bind=engine)
session = Session()

test_engine = create_engine('postgresql://{dbuser}:{passwd}@{host}:{port}/{dbname}'.format(\
	dbuser = os.environ['POSTGRES_USER'] ,
	passwd = os.environ['POSTGRES_PASS'],
	host = 'localhost',
	port = os.environ['POSTGRES_PORT'],
	dbname = os.environ['POSTGRES_HIIJE_TEST_DBNAME']))

TestSession = sessionmaker(bind=test_engine)
test_session = TestSession()



#Take this to Recommender class
from sqlalchemy import Column, String, Integer, DateTime
Base = declarative_base()
	
class Item(Base):
	__tablename__ = "item"

	item_id = Column(Integer, primary_key=True)
	name = Column(String)
	fancy_name = Column(String)

	def __init__(self, itemName):
		#The only param provided is itemName and not FancyName. This is because even if fancyName is provided, we can work out
		#itemName using processWord method. FancyName, if required, will be retrieved from the item DB which is the source of truth for fancy names
		assert isinstance(itemName, str)
		_name = processWord(itemName)
		#TODO> Confirm that _name is a valid item
		self.name = _name

	#processWord method used to live here but has been moved to be global

	def get_fancyName(self):
		pass


class Transaction(Base):
	__tablename__ = "transaction"

	transaction_id = Column(Integer, primary_key = True)
	transaction_datetime = Column(DateTime(), nullable = False)
	transaction_details = Column(JSON)

	def __init__(self,txn_details):
		self.transaction_details = txn_details
		dt = datetime.datetime.utcnow()
		self.transaction_datetime = dt.isoformat()
		#transaction id is autoincremented in psql



#res = session.query(Item).filter(Item.name == "rollsbuns").all()
#print res[0].name, res[0].id



class PopulateDB:
	def __init__(self, itemList_filename, is_empty = True):
		assert isinstance(itemList_filename, str)
		self.itemList_filename = itemList_filename
		self.DB_isempty = is_empty

	def populate_item_database(self):
		#Use csv.reader as shown in https://docs.python.org/2/library/csv.html
		with open(self.itemList_filename, "r") as csvfile:
			csvreader = csv.reader(csvfile, delimiter = ",")
			for data in csvreader:
				#read quantities
				if not data == []:
					item_id = data[0]
					uniqueName = data[1]
					fancyName = data[2]

					item = Item(uniqueName)
					item.fancy_name = fancyName.title()
					item.item_id = int(item_id)

					#store quantities in db
					try:
						session.add(item)
						log.info("adding item with unique ID {}, name {} and fancy name {} to database <<DBname to be added>>".format(item.item_id, item.name, item.fancy_name))	#TODO >> mAKE THIS WORK

					except:
						log.error("Failed to add item with unique ID {}, name {} and fancy name {} to database <<DBname to be Added>>. FATAL ERROR".format(item.item_id, item.name, item.fancy_name, ))
						raise
				

	def populate_transaction_database(self):
		#This method is put here but will never be needed because the transaction DB is populated by a
		#request for recommendation and not at initialisation.
		pass


# log.debug('debug message')
# log.info('info message')
# log.warn('warn message')
# log.error('error message')
# log.critical('critical message')

#How to actually populate the DB. This is implemented in setup.py
# populatedb = PopulateDB("Item_IDs_169.txt")
# populatedb.populate_item_database()

# line = "Juicy Fruit, Candy, CaNdy, Cola, Anti-freeze, cola, rolls/buns, shampoo"
# items = dict()

# processLine(line,items)