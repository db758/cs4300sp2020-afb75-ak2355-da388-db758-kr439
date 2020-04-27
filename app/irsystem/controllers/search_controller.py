from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import csv
import yelp_scoring
import movie_scoring

project_name = "CUpids"
net_id = "Alexa Batino (afb75), Divya Agrawal (da388), Keethu Ramalingam (kr439), Asma Khan (ak2355), Debasmita Bhattacharya (db758)"

print("enter yelp")
yelp = yelp_scoring.YelpScoring()
print("done yelp")

all_movies = [mov.title() for mov in movieClass.all_movies]
zipcodes = yelp.zipcodes

@irsystem.route('/', methods=['GET'])
def search():
	movieClass = movie_scoring.MovieScoring()

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
		movie2, foodCats2, foodAttrs2 = movieResult[3].title(), movieResult[4], movieResult[5]
		movie3, foodCats3, foodAttrs3 = movieResult[6].title(), movieResult[7], movieResult[8]
		# Elements 3-5 in movieResult are the second ranked movie
		# Elements 6-8 in movieResult are the third ranked movie

		movie1 = {"title": movie, "food_words": foodCats+foodAttrs}
		movie2 = {"title": movie2, "food_words": foodCats2+foodAttrs2}
		movie3 = {"title": movie3, "food_words": foodCats3+foodAttrs3}
		movieList = [movie1, movie2, movie3]
		
		yelp_result1 = getRestaurant(foodCats, foodAttrs, location_a, location_b)
		yelp_result2 = getRestaurant(foodCats2, foodAttrs2, location_a, location_b)
		yelp_result3 = getRestaurant(foodCats3, foodAttrs3, location_a, location_b)

		twoRestaurants = False
		their_restaurant1 = {}
		their_restaurant2 = {}
		their_restaurant3 = {}
		if len(yelp_result1) == 2:
			twoRestaurants = True
			their_restaurant1 = yelp_result1[1]
			their_restaurant2 = yelp_result2[1]
			their_restaurant3 = yelp_result3[1]

		your_restaurant1 = yelp_result1[0]
		your_restaurant2 = yelp_result2[0]
		your_restaurant3 = yelp_result3[0]

		user1Restaurants = [your_restaurant1, your_restaurant2, your_restaurant3]
		user2Restaurants = [their_restaurant1, their_restaurant2, their_restaurant3]

		return render_template('result.html', netid=net_id, movieList=movieList, 
		twoRestaurants=twoRestaurants, user1Restaurants=user1Restaurants, 
		user2Restaurants=user2Restaurants)


	return render_template('search.html', name=project_name, netid=net_id, all_movies=all_movies, zipcodes=zipcodes)


def getRestaurant(categories, attributes, zipcode1, zipcode2):
	
	if len(zipcode2) < 1:
		zipcode2 = None
	restaurants = yelp.run(attributes, categories, zipcode1, zipcode2)

	return restaurants



