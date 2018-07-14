from hiije import get_logger 
from hiije import get_item_list
from hiije.core.recommender import Recommend
from flask import Flask, request, render_template
import json

log = get_logger()
#log.Set_logging_level

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

	log.info("Recommendation json representation\n\n{}".format(json_result))
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
		for product in request.form.getlist(key):
			basket.append(product)

	if len(basket) == 0:
		return "Raise appropriate Error for empty list."
	else:
		result = get_multiple_recoms(num_recoms, basket)
		result = json.loads(result)
		str_nums = list()
		for i in range (1,num_recoms+1):
			str_nums.append(str(i))
		return render_template('view_recom.html', result = result, num_recoms = num_recoms, str_nums=str_nums)
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

