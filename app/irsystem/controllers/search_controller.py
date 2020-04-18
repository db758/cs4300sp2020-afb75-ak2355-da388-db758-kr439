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
import csv

project_name = "CUpids"
net_id = "Alexa Batino (afb75), Divya Agrawal (da388), Keethu Ramalingam (kr439), Asma Khan (ak2355), Deb Bhattacharya (db758)"


@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query
		#restaurant = Restaurant.query.filter(Restaurant.name.contains(query)).first()
		data = movie(query)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)


def movie(query):
	query = query.lower()
	input_movie_list = query.split(', ')

	f = open('new.csv')
	movies = list(csv.DictReader(f))

	movie_to_genre = {}
	input_movie_genres = []

	for each_movie in movies:
		if each_movie["Genres"] != "":
			movie_to_genre[str(each_movie["Title"]).lower()] = eval(each_movie["Genres"])

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




