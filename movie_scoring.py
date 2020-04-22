from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import csv

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
	i=0
	for each_movie in movies:
		if each_movie["Genres"] != "":
			movie_to_genre[str(each_movie["Title"]).lower()] = eval(each_movie["Genres"])
			i += 1
			movie_to_categories[str(each_movie["Title"]).lower()] = eval(each_movie["categories"])
			movie_to_attributes[str(each_movie["Title"]).lower()] = eval(each_movie["attributes"])
	
	print(i)

	#All the genres in the movies that the user inputted	
	input_movie_genres = getMovieGenres(input_movie_list, movie_to_genre)
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

def getAllMovies():
	"""Used for drop down for movie.
	
	Returns: a list with all the movie titles"""

	movies = list(csv.DictReader(open('new.csv')))
	all_movies = []
	for each_movie in movies:
		all_movies.append(str(each_movie["Title"].lower()))
	
	with open("all_movies.txt", "w") as output:
		for mov in all_movies:
			output.write(mov+ '\n')

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


getAllMovies()