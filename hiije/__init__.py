from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import logging
import sys

def load_matrix_from_csv(csvfile):
	item_sim_matrix = list()
	with open(csvfile, 'r') as csvmodel:
		line_num = 0
		for line in csvmodel:
			item_sim_matrix.append(list())
			temp_num = ''
			for ch in line:
				if ch not in {',','\n'}:
					temp_num += ch
				else:
					if temp_num != '':
						item_sim_matrix[line_num].append(float(temp_num))
						temp_num = ''

			line_num += 1
		item_sim_matrix = item_sim_matrix[:-1]


	return item_sim_matrix


def get_item_list(itemList_file="item_List_ALL.txt"):
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
        indexList.append(temp[0].id)
        #print temp.id
        

    for i in range(169):
        if i in indexList:
            binList.append(1)
            #print i
            
        else:
            binList.append(0)

    return binList


def get_logger():
	log = logging.getLogger(__name__)
	out_hdlr = logging.StreamHandler(sys.stdout)
	out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
	out_hdlr.setLevel(logging.INFO)
	log.addHandler(out_hdlr)
	return log


#create sqlalchemy engine and session

# engine = create_engine('postgresql://{dbuser}:{passwd}@{host}:{port}/{dbname}'.format(\
# 	dbuser = os.environ['POSTGRES_USER'] ,
# 	passwd = os.environ['POSTGRES_PASS'],
# 	host = 'localhost',
# 	port = os.environ['POSTGRES_PORT'],
# 	dbname = os.environ['POSTGRES_HIIJE_DBNAME']))


test_engine = create_engine('postgresql://{dbuser}:{passwd}@{host}:{port}/{dbname}'.format(\
	dbuser = "mcflyhalf" ,
	passwd = "Kasuku",
	host = 'localhost',
	port = "5432",
	dbname = "hiije_test"))

#Session = sessionmaker(bind=engine)
#session = Session()


#Take this to Recommender class
from sqlalchemy import Column, String, Integer
Base = declarative_base()
	
class Item(Base):
	__tablename__ = "item"

	id = Column(Integer, primary_key=True)
	name = Column(String)

	def __init__(self, itemName):
		assert isinstance(itemName, str)
		_name = processWord(itemName)
		#TODO> Confirm that _name is a valid item
		self.name = _name

	def processWord(wordin):      # For each item(word), make it all lower case, remove special characters and white spaces
	    word = wordin
	    word.strip()
	    word= word.lower()
	    word= word.replace(" ","")
	    for ch in word:
	        if ch in "`~!@#$%^&*()_-+={[]}|',./?;:":
	            word= word.replace(ch, "")

	    return word

#res = session.query(Item).filter(Item.name == "rollsbuns").all()
#print res[0].name, res[0].id