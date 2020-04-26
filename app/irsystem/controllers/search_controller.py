from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import csv
import yelp_scoring
import movie_scoring

project_name = "CUpids"
net_id = "Alexa Batino (afb75), Divya Agrawal (da388), Keethu Ramalingam (kr439), Asma Khan (ak2355), Debasmita Bhattacharya (db758)"

movieClass = movie_scoring.MovieScoring()
yelp = yelp_scoring.YelpScoring()

all_movies = [mov.title() for mov in movieClass.all_movies]
zipcodes = yelp.zipcodes

@irsystem.route('/', methods=['GET'])
def search():
	movie_a = request.args.get('movie-a')
	movie_b = request.args.get('movie-b')
	location_a = request.args.get('location-a')
	location_b = request.args.get('location-b')
	keywords_a = request.args.get('keywords-a')
	keywords_b = request.args.get('keywords-b')
	actors_a = request.args.get('actors-a')
	actors_b = request.args.get('actors-b')



	if not movie_a and not keywords_a:
		data = []
	else:
		movieResult = movieClass.getMovieAndFoodWords(movie_a, movie_b, keywords_a, keywords_b, actors_a, actors_b)
		movie, foodCats, foodAttrs = movieResult[0].title(), movieResult[1], movieResult[2]
		# Elements 3-5 in movieResult are the second ranked movie
		# Elements 6-8 in movieResult are the third ranked movie
		
		restaurants = getRestaurant(foodCats, foodAttrs, location_a, location_b)

		twoRestaurants = False
		restaurantName1 = restaurants[0]['restaurant1']
		restaurantCity1 = restaurants[0]['city1']
		restaurantState1 = restaurants[0]['state1']
		restaurantScore1 = restaurants[0]['score1']
		restaurantWords1 = restaurants[0]['matchings']

		restaurantName2 = ""
		restaurantCity2 = ""
		restaurantState2 = ""
		restaurantScore2 = ""
		restaurantWords2 = ""

		if len(restaurants) == 2:
			twoRestaurants = True
			restaurantName2 = restaurants[1]['restaurant2']
			restaurantCity2 = restaurants[1]['city2']
			restaurantState2 = restaurants[1]['state2']
			restaurantScore2 = restaurants[1]['score2']
			restaurantWords2 = restaurants[1]['matchings']


		return render_template('result.html', netid=net_id, movieTitle=movie, movieWords=foodCats + foodAttrs,
		restaurantName1=restaurantName1, restaurantCity1=restaurantCity1, restaurantState1=restaurantState1, 
		restaurantScore1=restaurantScore1, restaurantWords1=restaurantWords1, twoRestaurants=twoRestaurants,
		restaurantName2=restaurantName2, restaurantCity2=restaurantCity2, restaurantState2=restaurantState2,
		restaurantScore2=restaurantScore2, restaurantWords2=restaurantWords2)

	return render_template('search.html', name=project_name, netid=net_id, all_movies=all_movies, zipcodes=zipcodes)


def getRestaurant(categories, attributes, zipcode1, zipcode2):
	
	if len(zipcode2) < 1:
		zipcode2 = None
	restaurants = yelp.run(attributes, categories, zipcode1, zipcode2)

	return restaurants



