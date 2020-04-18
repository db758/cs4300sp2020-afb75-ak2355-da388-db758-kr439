from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import csv
import pandas as pd
from yelp_scoring import run

project_name = "CUpids"
net_id = "Alexa Batino (afb75), Divya Agrawal (da388), Keethu Ramalingam (kr439), Asma Khan (ak2355), Deb Bhattacharya (db758)"


@irsystem.route('/', methods=['GET'])
def search():
	movie_a = request.args.get('movie-a')
	movie_b = request.args.get('movie-b')

	if not movie_a:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + movie_a

		movie(movie_a)
		# restaurant = Restaurant.query.filter(Restaurant.name.contains(query)).first()
		# data = [restaurant.name, restaurant.city, restaurant.state]
		data = range(5)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)

def movie(query):
	# with open("new.csv", newline='') as csvfile:
	# 	csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	# 	count = 0
	# 	for f in csvreader:
	# 		print(row[10])
	# 		count = count + 1
	# 		# cats = row[10]
	# 		# attrs = row[11]
	# 		# print(cats)
	# 		# print(attrs)


	# df = pd.read_csv('new.csv')
	cat = ['Family']
	att = ['romantic']		
	# for index, row in df.iterrows():
			# cat = df.at[index, 'categories']
			# att = df.at[index, 'attributes']


		# if df.at[index, 'Title'] == query:
		# 	cat = df.at[index, 'categories']
		# 	att = df.at[index, 'attributes']


	result = run(att, cat,'Phoenix', 'AZ')

	print(result)
	
	return (cat, att)




# def movie(query):
# 	query = query.lower()
# 	input_movie_list = query.split(', ')

# 	with open("new.csv") as f:
# 		movies = json.load(f)
	
# 	movie_to_genre = {}
# 	input_movie_genres = []

# 	for each_movie in movies:
# 		movie_to_genre[str(each_movie['Title']).lower()] = ast.literal_eval(each_movie['Genres'])

	
# 	for each_movie in input_movie_list:
# 		input_movie_genres = input_movie_genres +  movie_to_genre[each_movie]

# 	unique_input_movie_genres = list(set(input_movie_genres))

# 	all_movies = list(movie_to_genre.keys())
	
# 	genresBYmovies = np.zeros((len(unique_input_movie_genres), len(all_movies)))

# 	for m in range(0,len(all_movies)):
# 		movie_genres = movie_to_genre[all_movies[m]]
# 		for g in movie_genres:
# 			if g in unique_input_movie_genres:
# 				genresBYmovies[unique_input_movie_genres.index(g)][m]=1

# 	genre_count = []

# 	for i in range(0,len(unique_input_movie_genres)):
# 		genre_count.append(input_movie_genres.count(unique_input_movie_genres[i]))

# 	movie_rank =  np.argsort(np.sum((genresBYmovies.transpose())*genre_count, axis=1))

# 	for i in range(1,len(all_movies)):
# 		index_movie = movie_rank[len(all_movies)-i]
# 		if all_movies[index_movie] not in input_movie_list:
# 			return all_movies[index_movie]

