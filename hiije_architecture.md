# HIIJE
*Hiije* is a recommendation system currently built for grocery recommendations. The system itself is an implementation of [the work of Karypis and Deshpande](http://glaros.dtc.umn.edu/gkhome/fetch/papers/itemrsTOIS04.pdf). The description there is very technical amd is recommended for people who actually intend to implement, extend or adapt the algorithm in some way. For 


## Hiije Architecture
Hiije is organised into 2 bits:

0. Setup
1. Recommender
2. hiije_api

### Setup
The setup basically comes up with the Item similarity matrix.

This should be done in the following ways:

1. Ready-to-drink database file

	A file that already contains the item-similarity matrix values in some format. This file would come from a separate source where the similarity values were computed and stored in file.

1. Text-based historical record file

	In this case the input is a file containing plain text in csv format. The system will take this file and use it to generate an item similarity matrix. A few things which will also need to be generated along the way are:
	* Unique item list. A list of each unique item appearing in the input file
	* Unique IDs for each unique item. This may be the name as given in the unique item list or a numerical UID or some other form of appropriate unique identifier
	* The item similarity matrix in some form such as a csv file

The setup also 
	* creates default config parameters 
	* creates database tables (it requires the database to be pre existing)
	* populates the database from the Unique item List file and 
	* runs unit/integration tests


### Recommender
Having access to the item similarity matrix, the recommender provides a class whose objects will:
* Accept a list of unique items. This means that 2 hotdogs and a soda will be taken to mean [hotdog, soda].
* Confirm that each item in the list exists in the unique items database. Raise an error if this is not the case.
* Generate a recommendation using the input list and similarity matrix.
* Persist the response in a DB
* Return the reponse as a dictionary with the elements:
	* Reponse_ID- A unique ID for this response
	* Request- The items in the original request
	* Recommendation_num- The number of recommended items
	* Recommendation(s)- The recommended item(s)
	* Recommendation_score(s)- The weight given to each recommendation. This is a number between 0 and 1 where 0 means not recommended at all and 1 means highly recommended.
	* Request_time- Timestamp of the time when the request was received.
	* Request_duration- The amount of time it took to compute and return the recommendations
To do this, a recommender object needs access to the item similarity matrix (file)

### hiije_api
The api provides access to the services of the recommender. Using the api, it is possible to:
* Make a request and receive a recommendation. This uses a post request with a list of either unique item names or UID's. The recommendation is returned as a json object.
* See the last 10 recommendations.
* See a particular recommendation given its recommendation ID
