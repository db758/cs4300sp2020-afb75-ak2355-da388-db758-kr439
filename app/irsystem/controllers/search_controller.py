from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import csv
import yelp_scoring

project_name = "CUpids"
net_id = "Alexa Batino (afb75), Divya Agrawal (da388), Keethu Ramalingam (kr439), Asma Khan (ak2355), Debasmita Bhattacharya (db758)"

yelp = yelp_scoring.YelpScoring()

@irsystem.route('/', methods=['GET'])
def search():
	movie_a = request.args.get('movie-a')
	movie_b = request.args.get('movie-b')
	location_a = request.args.get('location-a')
	location_b = request.args.get('location-b')

	if not movie_a:
		data = []
	else:
		movieResult = getMovieAndFoodWords(movie_a, movie_b)
		movie, foodCats, foodAttrs = movieResult[0], movieResult[1], movieResult[2]
		
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

	return render_template('search.html', name=project_name, netid=net_id)

def getMovieAndFoodWords(movie_a, movie_b):
	user1 = movie_a.lower()
	user1 = user1.split(', ')

	user2 = movie_b.lower()
	user2 = user2.split(', ')

	input_movie_list = user1 + user2

	f = open('new.csv')
	movies = list(csv.DictReader(f))

	movie_to_genre = {}
	input_movie_genres = []
	movie_to_categories = {}
	movie_to_attributes = {}

	for each_movie in movies:
		if each_movie["Genres"] != "":
			movie_to_genre[str(each_movie["Title"]).lower()] = eval(each_movie["Genres"])
			movie_to_categories[str(each_movie["Title"]).lower()] = eval(each_movie["categories"])
			movie_to_attributes[str(each_movie["Title"]).lower()] = eval(each_movie["attributes"])
			

	for each_movie in input_movie_list:
		input_movie_genres = input_movie_genres +  movie_to_genre[each_movie]

	unique_input_movie_genres = list(set(input_movie_genres))

	all_movies = list(movie_to_genre.keys())
	
	genresBYmovies = np.zeros((len(unique_input_movie_genres), len(all_movies)))

	for m in range(0,len(all_movies)):
		movie_genres = movie_to_genre[all_movies[m]]
		for g in movie_genres:
			if g in unique_input_movie_genres:
				genresBYmovies[unique_input_movie_genres.index(g)][m]=1

	genre_count = []

	for i in range(0,len(unique_input_movie_genres)):
		genre_count.append(input_movie_genres.count(unique_input_movie_genres[i]))

	movie_rank =  np.argsort(np.sum((genresBYmovies.transpose())*genre_count, axis=1))

	for i in range(1,len(all_movies)):
		index_movie = movie_rank[len(all_movies)-i]
		if all_movies[index_movie] not in input_movie_list:
			return [all_movies[index_movie], movie_to_categories[all_movies[index_movie]], movie_to_attributes[all_movies[index_movie]]]
			

def getRestaurant(categories, attributes, zipcode1, zipcode2):
	
	if len(zipcode2) < 1:
		zipcode2 = None
	restaurants = yelp.run(attributes, categories, zipcode1, zipcode2)

	return restaurants



