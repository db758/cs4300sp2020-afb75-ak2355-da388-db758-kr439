from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import json
from collections import defaultdict
from collections import Counter
import math
import string
import time
import numpy as np
from nltk.tokenize import TreebankWordTokenizer
import ast

def movie(query):
	query = query.lower()
	input_movie_list = query.split(', ')

	with open("movie.json") as f:
		movies = json.load(f)
	
	movie_to_genre = {}
	input_movie_genres = []

	for each_movie in movies:
		movie_to_genre[str(each_movie['Title']).lower()] = ast.literal_eval(each_movie['Genres'])

	
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
			return all_movies[index_movie]