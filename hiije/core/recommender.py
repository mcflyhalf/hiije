#TODO:> Clean up imports. Have the ones in init go back to their place

from sqlalchemy import Column, String, Integer
import hiije
from hiije import Item, session
Base = hiije.declarative_base()
from numpy import dot

log = hiije.get_logger()
	
# class Item(Base):
# 	__tablename__ = "item"

# 	id = Column(Integer, primary_key=True)
# 	name = Column(String)

# 	def __init__(self, itemName):
# 		assert isinstance(itemName, str)
# 		_name = processWord(itemName)
# 		#TODO> Confirm that _name is a valid item
# 		self.name = _name

# 	def processWord(wordin):      # For each item(word), make it all lower case, remove special characters and white spaces
# 	    word = wordin
# 	    word.strip()
# 	    word= word.lower()
# 	    word= word.replace(" ","")
# 	    for ch in word:
# 	        if ch in "`~!@#$%^&*()_-+={[]}|',./?;:":
# 	            word= word.replace(ch, "")

# 	    return word


class Recommend:

	_basket = list()	#TODO: Determine whether this variable should belong to the class or to the instance
	def __init__(self, basket):
		if not isinstance(basket, list):
			raise TypeError("The input <{}> to the <{}> class must be of type <{}>. It is currently of type <{}>".format(basket, self.__class__.__name__, list().__class__.__name__, basket.__class__.__name__))

		elif len(basket) == 0:
			raise TypeError("The input <{}> to the <{}> class cannot be an empty list".format(basket, self.__class__.__name__, list().__class__.__name__, basket.__class__.__name__))

		else:
			self._basket = set(basket)	#Copy of the unique list elements for internal use in the class

			self._basket = list(self._basket)	#Needs to be a list so it is iterable

	#@property
	def recommendation(self, num_recommendations = 1, model_filename = 'II Similarity matrix (cosine_sim)NORMALISED10.csv'):
		'''Function that returns the recommended item(s) limited to 5 recommendations max'''
		max_recommendations = 5

		if num_recommendations <= 0:
			raise ValueError("Cannot give {} recommendations".format(num_recommendations))

		elif num_recommendations > max_recommendations:
			raise ValueError("Cannot give more than {} recommendations. Requested for {} recommendations".format(max_recommendations, num_recommendations))

		assert isinstance(model_filename, str)

		item_similarity_matrix = hiije.load_matrix_from_csv(model_filename)
		likelihoods = list()

		binary_transaction = hiije.text_2_binary_txn(self._basket, Item, hiije.session)

		for i in range(len(item_similarity_matrix)):
			prob= dot(binary_transaction, item_similarity_matrix[i])      #How likely is the customer likely to buy item i given their current basket
			likelihoods.append(prob)

		#Set probability of items already in the basket to zero
		for i in range(len(self._basket)):
			if self._basket[i] == 1:
				likelihoods[i] = 0

		sorted_likelihoods = likelihoods[:]
		sorted_likelihoods.sort(reverse=True)

		assert len(sorted_likelihoods) > max_recommendations
		_recommendation = dict()

		for i in range(num_recommendations):
			recommended_item_index = likelihoods.index(sorted_likelihoods[i])
			recommended_item_name =  session.query(Item).filter(Item.item_id == recommended_item_index).all()
			if len(recommended_item_name) == 0:
				_recommendation.update({"Error":"No further recommendations available for the selected basket"})

			else:
				recommended_item_name = recommended_item_name[0].name
				_recommendation.update({i+1:[recommended_item_name, sorted_likelihoods[i]]})	#i+1 makes this dict seem like it is 1 indexed in the json response

		recom_result = dict()

		recom_result.update({"Requested basket":self._basket})
		recom_result.update({"Hiije top {} recommendation".format(num_recommendations): _recommendation})
		recom_result.update({"Requested recommendations":num_recommendations})

		return recom_result

