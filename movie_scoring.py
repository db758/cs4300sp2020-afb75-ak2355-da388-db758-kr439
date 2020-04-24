from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from nltk.tokenize import TreebankWordTokenizer
from collections import Counter
import operator
import math
import numpy as np
import csv

def getMovieAndFoodWords(user1_movies, user2_movies, user1_keywords, user2_keywords):
	# List of inputted key words
	input_keywords_list = getKeywords(user1_keywords, user2_keywords)
	
	# List of all movie names inputted by both users 
	input_movie_list = getMovieNames(user1_movies, user2_movies)

	# Read in the csv of movies
	movies = list(csv.DictReader(open('new.csv')))

	# Dictionary with movie title as key and list of genres as values
	movie_to_genre = {}
	# Dictionary with movie title as key and list of categories as values
	movie_to_categories = {}
	# Dictionary with movie title as key and list of attributes as values
	movie_to_attributes = {}
	# Dictionary with movie title as key and list of summaries as values
	movie_to_summaries = {}
	# Dictionary with movie title as key and list of actors as value
	movie_to_cast = {}

	# Generate dictionaries
	for each_movie in movies:
		#Creates the genre list
		if each_movie["Genres"] == "":
			movie_to_genre[str(each_movie["Title"]).lower()] = []
		else:
			movie_to_genre[str(each_movie["Title"]).lower()] = eval(each_movie["Genres"])
		
		movie_to_categories[str(each_movie["Title"]).lower()] = eval(each_movie["categories"])
		movie_to_attributes[str(each_movie["Title"]).lower()] = eval(each_movie["attributes"])
		movie_to_summaries[str(each_movie["Title"]).lower()] = (each_movie["Plot"])

	#List of all movies
	all_movies = list(movie_to_genre.keys())


	input_movie_list, input_keywords_list = cleanInputMovieList(input_movie_list, input_keywords_list, all_movies)
	print(input_movie_list)
	print(input_keywords_list)

	#GENRE SCORES
	if len(input_movie_list) == 0:
		genre_score_array = np.zeros((len(all_movies)))
	else:
		#All the genres in the movies that the user inputted	
		input_movie_genres = getMovieGenres (input_movie_list, movie_to_genre)
		#All unique genres in the movies that the user inputted	
		unique_input_movie_genres = list(set(input_movie_genres))
		#Genre Scores of All movies
		genre_score_array = getGenreScore(unique_input_movie_genres,input_movie_genres, input_movie_list, all_movies, movie_to_genre)
		genre_score_array = genre_score_array/(max(genre_score_array))

	#COSSINE SCORES
	if len(input_keywords_list) == 0:
		cosine_score_array = np.zeros((len(all_movies)))
	else:
		cosine_score_array = []
		cosine_score_dict = getCosine(movie_to_summaries, input_keywords_list)
		for each_movie in all_movies:
			if each_movie in cosine_score_dict:
				cosine_score_array.append(cosine_score_dict[each_movie]*2)
			else:
				cosine_score_array.append(0)

	#TOTAL SCORE
	total_score = genre_score_array+cosine_score_array 
	total_score_rank =  np.argsort(total_score)

	#FINDING BEST MOVIE FROM ALL RANKED MOVIES
	movie = ""
	for i in range(1,len(all_movies)):
		index_movie = total_score_rank[len(all_movies)-i]
		if all_movies[index_movie] not in input_movie_list:
			movie = all_movies[index_movie]
			break
	
	return [movie, movie_to_categories[movie], movie_to_attributes[movie]] 
	#return["","",""]


def getKeywords(user1_keywords,user2_keywords):
	""" Give the inputted keywords of both users returns a list with all the keywords
	"""
	if len(user1_keywords) == 0 and len(user2_keywords) == 0 :
		return []
	elif len(user1_keywords) == 0:
		return user2_keywords.lower().split(' ')
	elif len(user2_keywords) == 0 :
		return user1_keywords.lower().split(' ')
	else:
		keywords = user1_keywords+ " " + user2_keywords
		return keywords.lower().split(' ')


def getMovieNames(user1_movies, user2_movies):
	"""Given a the user input of movie names (which are split by commas)
	the function returns the movie names as a list
	
	Parameters:
	movie_name: a string that has one (or multiple) movie titles
	
	Returns: a list with all the movie titles"""
	if len(user1_movies) == 0 and len(user2_movies) == 0 :
		return []
	elif len(user1_movies) == 0:
		return user2_movies.lower().split(', ')
	elif len(user2_movies) == 0 :
		return user1_movies.lower().split(', ')
	else:
		movies = user1_movies+ ", " + user2_movies
		return movies.lower().split(', ')

def cleanInputMovieList(input_movie_list, input_keywords_list, all_movies):
	"""
	Check if all inputted movies are in the db otherwise appends them to keywords
	"""
	for each_movie in input_movie_list:
		if each_movie not in all_movies:
			input_movie_list.remove(each_movie)
			input_keywords_list.append(each_movie)
	return input_movie_list, input_keywords_list


def getMovieGenres (input_movie_list, movie_to_genre):
	"""Returns a list of all the genres in all of the inputted movies"""
	input_movie_genres = []
	for each_movie in input_movie_list:
		input_movie_genres = input_movie_genres +  movie_to_genre[each_movie]
	return input_movie_genres

def getGenreScore(unique_input_movie_genres,input_movie_genres,input_movie_list, all_movies, movie_to_genre):
	"""Return a the genre score"""
	if input_movie_genres == "":
		return 0

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

	movie_scoring = np.sum((genresBYmovies.transpose())*genre_count, axis=1)
	return movie_scoring
	# #Multiplies the numpy matrix and the counts to get a scoring and the argsorts it
	# movie_rank =  np.argsort(movie_scoring)

	# #Goes through the movie ranking starting from the back
	# #If the movie is not one of the inputted movies, then returns the movie
	# for i in range(1,len(all_movies)):
	# 	index_movie = movie_rank[len(all_movies)-i]
	# 	if all_movies[index_movie] not in input_movie_list:
	# 		return movie_scoring[index_movie]
	# 		#return [all_movies[index_movie], movie_to_categories[all_movies[index_movie]], movie_to_attributes[all_movies[index_movie]]]



#Cosine Similarity

def token(movie_summaries):
	result = {}
	for mov in movie_summaries:
		result[mov] = movie_summaries[mov].lower().split(" ")
	return result

def tokenize_plot(movie_summaries):
	result = {}
	#use treebank tokenizer?
	tokenizer = TreebankWordTokenizer()
	for mov in movie_summaries:
		result[mov] = tokenizer.tokenize(movie_summaries[mov].lower())
	return result
	

#Build the inverted index - term - list of movies it is in
def buildInvertedIndex(movie_summaries, query_words):
	#input should be the a dictionary with key as movie title and value as movie_summaries
	#takes in the list of words that the user inputted
	"""
	This just builds an inverted index with the movie summaries. {word: [(movie title, count of word), ...]}
	
	"""
	inverted_index = {}
	for mov in movie_summaries:
		words = Counter(movie_summaries[mov]) #dictionary of word and its count
		for word in words.keys():
			if word in inverted_index.keys():
				inverted_index[word].append((mov, words[word]))
			else:
				inverted_index[word] = [(mov, words[word])]
	return inverted_index
	#inverted index only has the query term words

def compute_idf(inv_idx, n_docs, min_df=10, max_df_ratio=0.1):
	"""
	This just builds computes idf for the movie summaries. {word: idf value}
	
	"""
	idf_dict = {}
	for key in inv_idx.keys():
		ratio = len(inv_idx[key])/n_docs
		if ((len(inv_idx[key]) >= min_df) and (ratio <= max_df_ratio)):
			idf = [n_docs/(1 + len(inv_idx[key]))]
			idf_dict[key] = np.log2(idf)[0]
	return idf_dict

def compute_doc_norms(index, idf, n_docs):
	"""
	norms: {movie title: norm of movie summary}
	"""
	norms = {}
	sum = 0
	for word in idf.keys():
		words = index[word]
		for t in words:
			power = math.pow(idf[word]*t[1], 2)
			if t[0] in norms:
				norms[t[0]] += power
			else:
				norms[t[0]] = power
	
	for n in norms:
		norms[n] = math.sqrt(norms[n])
	return norms

def cosine_score(query_words, inv_index, idf, doc_norms):
	"""
	results, list of tuples (score, movie title) Sorted list of results such that the first element has
	the highest score.
	"""

	results = {}

	#get the counts for each word in user input/query
	count_query = {} #{word: count}
	for term in query_words:
		if term in count_query.keys():
			count_query[term] += 1
		else:
			count_query[term] = 1
	
	total = 0
	#WHAT TO DO HERE SINCE MOST OFTEN IT WONT HAVE IDF?
	#If the query has no words that relate, then it would just be 0?
	query_numbers = {} #{word in query: tf*idf, ...} 
	for key in count_query.keys():
		if key in idf.keys():
			top = count_query[key] * idf[key]
			query_numbers[key] = top
			total += top**2

	query_den = math.sqrt(total)
	
	doc_dict = {} #{movie title: {word: count in movie, word: count in movie ...}
	for word in inv_index.keys():
		for tup in inv_index[word]:
			if tup[0] in doc_dict.keys():
				val = doc_dict[tup[0]]
				val[word] = tup[1]
				doc_dict[tup[0]] = val              
			else:
				val = {}
				val[word] = tup[1]
				doc_dict[tup[0]] = val
	
	for document in doc_dict.keys():
		num = 0
		for word in query_numbers.keys():
			if word in doc_dict[document].keys():
				num += query_numbers[word]*doc_dict[document][word]*idf[word]
				den = query_den * doc_norms[document]
				results[document] = num/den
				# final_tuple = (num/den, document)
				# results += [final_tuple]
	
	# results.sort(key=lambda x: x[0])
	# results.reverse()
	return results


def getCosine(movie_summaries, query_words):
	""" Main function for cosine! """
	movies = token(movie_summaries)
	inv_idx = buildInvertedIndex(movies, query_words)
	idf = compute_idf(inv_idx, len(movie_summaries), min_df=10, max_df_ratio=0.1)
	inv_idx = {key: val for key, val in inv_idx.items() if key in idf}
	doc_norms = compute_doc_norms(inv_idx, idf, len(movie_summaries))
	return cosine_score(query_words, inv_idx, idf, doc_norms)


	
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


def getActorsScore(movies_to_cast, actors):
	"""
	Assumes parameter is a list of words that are divided based on commas (list of actors), all lowercase.
	
	Returns: sorted list: [(movie title, score), ...]. Will be empty if no inputed actors
	match any of the movie cast members.

	"""
	movie_act_dict = {}
	for mov in movies_to_cast:
		movie_actors = (movies_to_cast[mov].lower()).split(", ")
		for actor in movie_actors:
			if actor in actors:
				if mov in movie_act_dict:
					movie_act_dict[mov] += 1
				else:
					movie_act_dict[mov] = 1
	movie_act_dict_sorted = sorted(movie_act_dict.items(), key=operator.itemgetter(1))
	return movie_act_dict_sorted

def getTitleScore(movie_titles, keywords):
	"""
	Parameter: list of movie titles, list of user inputed keywords all lowercase
	
	Returns: sorted list: [(movie title, score), ...]. Will be empty if no keywords
					 match the words in the movie titles.
	"""

	title_dict = {}
	for mov in movie_titles:
		#tokenize movie title based on space
		title = mov.lower().split(" ")
		for word in keywords:
			if word in title:
				if mov in title_dict:
					title_dict[mov] += 1
				else:
					title_dict[mov] = 1
	title_dict_sorted = sorted(title_dict.items(), key=operator.itemgetter(1))
	return title_dict_sorted


def test():
	"""
	Used to test that cosine works. Cosine will return an empty list if there's
	no matching.
	"""

	all_movies = {}

	# with open('new_cast.csv', mode='r') as csv_file:
	# 	csv_reader = csv.DictReader(csv_file)
	# 	for row in csv_reader:
	# 		if row["Cast"] != "":
	# 			all_movies[row["Title"].lower()] = row["Cast"]

	# a = ['maleficent', 'guardians of the galaxy', 'the legend of tarzan']
	# print(getTitleScore(a, []))

	
	# i = getCosine(all_movies, ["christmas", "princess"])
	# print(i[0])
	# print(all_movies[i[0][1]])
	
	# with open("possible_inputs.txt", "w") as output:
	# 	for mov in i:
	# 		output.write(mov+ '\n')

# print("Method")
# test()


#CASES:
#check that the movie returned isnt a movie inputted
#pre-computed inverted index
#return a default movie!

#make sure that movie inputed is in database --> make sure its a dropdown list of movies

#movie if it doesn't have a genre --> genre score should be 0
#movie keywords - title and summary have cosine sim score of 0 

#if genre + cosine sim score = 0 --> default movie

#for food, if there is no restaurant, display popcorn is always a good option

# Questions:
# movie categories/attributes if empty
# how are we dividing user input (actors have to be full names & exact)


