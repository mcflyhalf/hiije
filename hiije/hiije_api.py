from __init__ import get_item_list
from recommender import Recommend
from flask import Flask, request, render_template
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

###########>>>>>>ROUTES<<<<<<<###############

#
#Routes to be consumed by other applications
#

#Get custom number of recommendations
@app.route('/recommendations/<int:num_recoms>/', methods = ['POST'])
def get_multiple_recoms(num_recoms, basket=None):
	if basket == None:
		basket = request.json["basket"] #a csv string
		basket = basket.split(',')

	log.info("Getting recommendation for {}".format(basket))
	result = Recommend(basket)
	json_result = json.dumps(result.recommendation(num_recoms))
	return json_result




#Get 1 recommendation (should call the custom recoms)
#@app.route('/recommendation/', methods = ['POST'])

#
#Routes to be consumed by a web browser (these need a pretty output)
#
#Get recommendations to be rendered to a webpage
@app.route('/viewrecommendation/<int:num_recoms>/', methods = ['POST'])
def view_recoms(num_recoms):
	basket = list()
	for key in request.form:
		basket.append(request.form[key])

	if len(basket) == 0:
		return "Raise appropriate Error for empty list."
	else:
		return get_multiple_recoms(num_recoms, basket)
	#return render_template()

#Landing Html page to ask for recoms graphically
@app.route('/')
@app.route('/index/')
def landing():
	item = get_item_list()
	return render_template('request_recom.html', item = item )


#######>>>>END ROUTES<<<<########


app.debug = True
if __name__ == '__main__':
	app.run(debug = True)

