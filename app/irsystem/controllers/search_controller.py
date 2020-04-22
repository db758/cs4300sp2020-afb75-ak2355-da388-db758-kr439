from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import csv
from yelp_scoring import run

project_name = "CUpids"
net_id = "Alexa Batino (afb75), Divya Agrawal (da388), Keethu Ramalingam (kr439), Asma Khan (ak2355), Debasmita Bhattacharya (db758)"


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
			restaurantName2 = restaurants[1]['restaurant1']
			restaurantCity2 = restaurants[1]['city1']
			restaurantState2 = restaurants[1]['state1']
			restaurantScore2 = restaurants[1]['score1']
			restaurantWords2 = restaurants[1]['matchings']


		return render_template('result.html', netid=net_id, movieTitle=movie, movieWords=foodCats + foodAttrs,
		restaurantName1=restaurantName1, restaurantCity1=restaurantCity1, restaurantState1=restaurantState1, 
		restaurantScore1=restaurantScore1, restaurantWords1=restaurantWords1, twoRestaurants=twoRestaurants,
		restaurantName2=restaurantName2, restaurantCity2=restaurantCity2, restaurantState2=restaurantState2,
		restaurantScore2=restaurantScore2, restaurantWords2=restaurantWords2)

	return render_template('search.html', name=project_name, netid=net_id)

def getMovieAndFoodWords(user1_movies, user2_movies):
	# List of all movie names inputted by both users 
	input_movie_list = getMovieNames(user1_movies) + getMovieNames(user1_movies)

	# Read in the csv of movies
	movies = list(csv.DictReader(open('new.csv')))

	# Dictionary with movie title as key and list of genres as values
	movie_to_genre = {}
	# Dictionary with movie title as key and list of categories as values
	movie_to_categories = {}
	# Dictionary with movie title as key and list of attributs as values
	movie_to_attributes = {}

	# Generate movie_to_genre, movie_to_categories, and movie_to_attributes dictionaries
	for each_movie in movies:
		if each_movie["Genres"] != "":
			movie_to_genre[str(each_movie["Title"]).lower()] = eval(each_movie["Genres"])
			movie_to_categories[str(each_movie["Title"]).lower()] = eval(each_movie["categories"])
			movie_to_attributes[str(each_movie["Title"]).lower()] = eval(each_movie["attributes"])

	#All the genres in the movies that the user inputted	
	input_movie_genres = getMovieGenres (input_movie_list, movie_to_genre)
	#All unique genres in the movies that the user inputted	
	unique_input_movie_genres = list(set(input_movie_genres))
	#List of all movies
	all_movies = list(movie_to_genre.keys())

	#Gets the movie ranking. Highest scored movie is the last element in the list.
	movie_rank = getMovieRanking(unique_input_movie_genres,input_movie_genres, all_movies, movie_to_genre)

	#Goes through the movie ranking starting from the back
	#If the movie is not one of the inputted movies, then returns the movie
	for i in range(1,len(all_movies)):
		index_movie = movie_rank[len(all_movies)-i]
		if all_movies[index_movie] not in input_movie_list:
			return [all_movies[index_movie], movie_to_categories[all_movies[index_movie]], movie_to_attributes[all_movies[index_movie]]]
	return["","",""]


def getMovieNames(movie_name):
	"""Given a the user input of movie names (which are split by commas)
	the function returns the movie names as a list
	
	Parameters:
	movie_name: a string that has one (or multiple) movie titles
	
	Returns: a list with all the movie titles"""

	return movie_name.lower().split(', ')

def getMovieGenres (input_movie_list, movie_to_genre):
	"""Returns a list of all the genres in all of the inputted movies"""
	input_movie_genres = []
	for each_movie in input_movie_list:
		input_movie_genres = input_movie_genres +  movie_to_genre[each_movie]
	return input_movie_genres

def getMovieRanking(unique_input_movie_genres,input_movie_genres, all_movies, movie_to_genre):
	"""Return a list of indexes where the first index is the lowest scored movie based on genres.
	This is where we do genre frequency * genres in a movie"""

	#Create a numpy matric that is movie_genres by all movies
	genresBYmovies = np.zeros((len(unique_input_movie_genres), len(all_movies)))

	#Set a position 1 if the genre appears in a certain movie
	for m in range(0,len(all_movies)):
		movie_genres = movie_to_genre[all_movies[m]]
		for g in movie_genres:
			if g in unique_input_movie_genres:
				genresBYmovies[unique_input_movie_genres.index(g)][m]=1

	genre_count = []

	#Counts the number of times a genre was inputted
	for i in range(0,len(unique_input_movie_genres)):
		genre_count.append(input_movie_genres.count(unique_input_movie_genres[i]))

	#Multiplies the numpy matrix and the counts to get a scoring and the argsorts it
	return np.argsort(np.sum((genresBYmovies.transpose())*genre_count, axis=1))

	




def getRestaurant(categories, attributes, location_a, location_b):
	city_state = location_a.split(", ")
	cityA, stateA = city_state[0].capitalize(), city_state[1].upper()
	if location_b: 
		city_stateB = location_b.split(", ")
		cityB, stateB = city_stateB[0].capitalize(), city_stateB[1].upper()
	else: 
		cityB, stateB = None, None

	restaurants = run(attributes, categories, cityA, stateA, cityB, stateB)
	
	return restaurants
