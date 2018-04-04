


class Recommend:

	_basket = list()	#TODO: Determine whether this variable should belong to the class or to the instance
	def __init__(self, basket):
		if not isinstance(basket, list):
			raise TypeError("The input {} to the {} class must be of type {}. It is currently of type {}".format(basket, type(self), type(list()), type(basket)))	#TODO: Make this error message actually give the name of the Recommend class

		elif len(basket) == 0:
			raise TypeError("The input {} to the {} class cannot be an empty list".format(basket, type(self), type(list()), type(basket)))

		else:
			self._basket = set(basket)	#Copy of the unique list elements for internal use in the class

			self._basket = list(self._basket)	#Needs to be a list so it is iterable



