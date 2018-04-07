#from __init__ import *
from recommender import Recommend
from flask import Flask, request
import logging
import sys
import json

log = logging.getLogger(__name__)
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
out_hdlr.setLevel(logging.INFO)
log.addHandler(out_hdlr)

log.setLevel(logging.DEBUG)

app = Flask(__name__)

#Get custom number of recommendations
@app.route('/recommendations/<int:num_recoms>/', methods = ['POST'])
def get_multiple_recoms(num_recoms):
	basket = request.json["basket"]
	basket = basket.split(',')
	#log.debug("Getting recommendation for {}".format(basket))
	result = Recommend(basket)
	json_result = json.dumps(result.recommendation(num_recoms))
	return json_result



#Get 1 recommendation (should call the custom recoms)
#@app.route('/recommendation/', methods = ['POST'])


#Show Previous recommendations??




#Landing Html page to ask for recoms graphically
@app.route('/')
def landing():
	return "Hello welcome to Hiije recommender"

app.debug = True
if __name__ == '__main__':
	app.run(debug = True)

