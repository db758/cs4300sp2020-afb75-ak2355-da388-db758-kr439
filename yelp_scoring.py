import numpy as np
import json
import operator
import csv
import re

def create_python_dict():
  """ Converts json (the yelp data set) to a list of restaurants and python 
  dictionary to be used throughout the program.
  
  Returns: a tuple (list with each element as restaurant dictionary, python 
  dictionary with business id of restaurant as key and the restaurant dictionary as value)
  """
  
  jsonList = []
  with open('yelp-restaurants.txt') as f:
      for jsonObj in f.readlines():
        obj = json.loads(jsonObj)
        jsonList.append(obj)

  tempList = []
  tempDict = {}
  for e in jsonList:
    temp = {}
    temp['business_id'] = e['business_id']
    temp["name"] = e['name']
    temp['address']  = e['address']
    temp['city'] = e['city']
    temp['state'] = e['state']
    temp['stars'] = e['stars']
    temp['review_count'] = e['review_count']
    temp['attributes'] = e['attributes']
    temp['categories'] = e['categories']
    tempList.append(temp)
    tempDict[temp["business_id"]] = temp
  
  return (tempList, tempDict)

def run(mov_attributes, mov_categories, city1, state1, city2, state2):
  """" Runs the main code. If the states are equal for both users, there will be
  one output of a restaurant, otherwise there will be two separate restaurants.
  
  Parameters: city2 and state2 should be None if there is only one user 
  Returns: dictionary of what is printed on app - restuarant, location, etc. """

  #CHECK - what to print if any of the values are empty

  restaurants, restaurant_dict = create_python_dict()

  if state1 == state2:
    #return a restaurant in the same state
    print("inside state1 == state2")
    
    restaurant_locations = restaurant_location(restaurants, state1, city1, city2)
    restaurant_scores, key_words_dict = find_restaurants(mov_categories, mov_attributes, restaurants)
    #key_words_dict is a dictionary with business id as key and value is the key words that intersect with the movie

    final_result = combine_location(restaurant_scores, restaurant_locations)
    #final result is a dictionary with id of restaurant and the score

    # for e in restaurant_locations:
    #   if e['state'] != 'AZ':
    #     print(e)

    if len(final_result) == 0:
      print("Could not find restaurant :( ")

    else:
      first_elem = list(final_result.keys())[0] #gets the first element id of the final result
      first_elem_score = final_result[first_elem] #gets the score
      i = key_words_dict[first_elem]

      print("Restaurant: " + restaurant_dict[first_elem]['name'] + ", Score: " + str(first_elem_score))
      print("Location: " + restaurant_dict[first_elem]['city'] + ", " +  restaurant_dict[first_elem]['state'] + ", Matchings: " + str(i)) 
 
  elif state2 is None:
    #if there is only one user
    print("inside state2 is None")
    
    restaurant_locations = restaurant_location_one_user(restaurants, city1, state1)
    restaurant_scores, key_words_dict = find_restaurants(mov_categories, mov_attributes, restaurants)
    final_result = combine_location(restaurant_scores, restaurant_locations)

    if len(final_result) == 0:
      print("Could not find restaurant :( ")
    
    else:
      first_elem = list(final_result.keys())[0]
      first_elem_score = final_result[first_elem]
      i = key_words_dict[first_elem]
      print("Restaurant: " + restaurant_dict[first_elem]['name'] + ", Score: " + str(first_elem_score))
      print("Location: " + restaurant_dict[first_elem]['city'] + ", " +  restaurant_dict[first_elem]['state'] + ", Matchings: " + str(i)) 

  else:
    #return two restaurants, one for each user

    #user1
    restaurant_locations1 = restaurant_location_one_user(restaurants, city1, state1)
    restaurant_scores1, key_words_dict1 = find_restaurants(mov_categories, mov_attributes, restaurants)
    final_result1 = combine_location(restaurant_scores1, restaurant_locations1)

    print("User 1 Restaurant: ")
    if len(final_result1) == 0:
      print("Could not find restaurant for user 1 :( ")
    else:
      first_elem1 = list(final_result1.keys())[0]
      first_elem_score1 = final_result1[first_elem1]
      i1 = key_words_dict1[first_elem1]
      
      print("Restaurant: " + restaurant_dict[first_elem1]['name'] + ", Score: " + str(first_elem_score1))
      print("Location: " + restaurant_dict[first_elem1]['city'] + ", " +  restaurant_dict[first_elem1]['state'] + ", Matchings: " + str(i1)) 

    #user2
    restaurant_locations2 = restaurant_location_one_user(restaurants, city2, state2)
    restaurant_scores2, key_words_dict2 = find_restaurants(mov_categories, mov_attributes, restaurants)
    final_result2 = combine_location(restaurant_scores2, restaurant_locations2)

    print("User 2 Restaurant: ")
    if len(final_result2) == 0:
      print("Could not find restaurant for user 2 :( ")
    
    else:
      first_elem2 = list(final_result2.keys())[0]
      first_elem_score2 = final_result2[first_elem2]
      i2 = key_words_dict2[first_elem2]
      print("Restaurant: " + restaurant_dict[first_elem2]['name'] + ", Score: " + str(first_elem_score2))
      print("Location: " + restaurant_dict[first_elem2]['city'] + ", " +  restaurant_dict[first_elem2]['state'] + ", Matchings: " + str(i2)) 
  
def intersection_fun(set1, set2):
  """" Gets the intersection of the two sets.
  Returns: a set of the words in both sets. """

  result = set()
  for word1 in set1:
    for word2 in set2:
      if word1.lower() in word2.lower():
        result.add(word1.lower())
      elif word2.lower() in word1.lower():
        result.add(word2.lower())
  return result

def jaccard_sim(set1, set2):
  """" Gets the simple Jaccard Similarity between the two sets.
  Returns: a tuple with a simple Jaccard Similarity score for set1 and set2
  and the set of intersecting words. """

  #CHECK - condition when denominator is 0, when BOTH restaurant and movie sets have empty categories or empty attributes
  #fix with smoothing!

  intersection = intersection_fun(set1, set2)
  numerator = len(intersection)
  denominator = (len(set1) + len(set2)) - numerator
  return (float(numerator) / (1.0 + float(denominator)), intersection)

def restaurant_location_one_user(restaurants, city, state):
  """" Takes in a dictionary of restaurants, a string city and a string state. 
  Returns: an ordered list of restaurant dictionaries that are near the location,
  where the beginning elements are the closest and the later are farther. 
  The list will only contain restaurants in the state.
  """

  #CHECK - the result will be empty when there are no restaurants in that state (must handle this case)

  result = []
  for r in restaurants:
    if r['state'] == state:
      if r['city'] == city:
        result = [r] + result
      else:
        result += [r]
  return result

def restaurant_location(restaurants, state, city1, city2):
  """" Takes in a dictionary of restaurants, a string city and a string state.
  Returns: an ordered list of restaurant dictionaries that are near the location,
  where the beginning elements are the closest and the later are farther """

  #CHECK - the result will be empty when there are no restaurants in that state (must handle this case)

  #function only called when the state of both users is the same and cities are different
  result = []
  for r in restaurants:
    if r['state'] == state:
      if r['city'] == city1 or r['city'] == city2:
        result = [r] + result
      else:
        result += [r]
  return result

def find_restaurants(mov_categories, mov_attributes, restaurants):
  """" Gets the score for each restaurant based on its Jaccard Similarity scores.
  
  Returns: a tuple (sorted dictionary of restuarants with id of restaurant and 
  the similarity score to the mov_categories and mov_attributes, dictionary with id as key 
  and value as the list of matching attributes and categories). """

  #CHECK - need to redistribute the weight of words/categories/attributes

  result = {}
  output = {}
  for r in restaurants:
    res_categories = set()
    res_attributes = set()
    if r['attributes'] is not None: #used to check if restaurant has this as empty
      res_attributes = tokenize_attributes(r['attributes'])
    if r['categories'] is not None:
      res_categories = tokenize_categories(r['categories'])
    jac_attribute = jaccard_sim(set(mov_attributes), res_attributes)
    jac_cattegory = jaccard_sim(set(mov_categories), res_categories)
    sim_attribute = jac_attribute[0]
    sim_category = jac_cattegory[0]

    result[r['business_id']] = sim_attribute + sim_category
    output[r['business_id']] = jac_attribute[1].union(jac_cattegory[1])
  
  sorted_dict = {r: result[r] for r in sorted(result, key=result.get, reverse=True)}
  return (sorted_dict, output)

def combine_location(restaurant_scores, restaurant_locations):
  """" Takes in a sorted dictionary of restaurant ids and similarity scores
  and an ordered list of restaurants in a specific location range. 

  Returns: a dictionary of restaurants sorted on the highest matching scores.
  Will only include restaurants from the restaurant locations input.
  """

  #CHECK - fix weighting and somehow all the restaurants in restaurant locations isn't in the final result?

  weight = len(restaurant_locations)
  #set the weight to decrease by 1 for each following location

  result = {} 
  for r in restaurant_locations:
    score = restaurant_scores[r['business_id']] + weight
    result[r['business_id']] = score
  
  # print(weight)
  # print(len(result))
  

  sorted_result = {r: result[r] for r in sorted(result, key=result.get, reverse=True)}
  return sorted_result

def tokenize_categories(categories):
  """" Takes in a category string and tokenizes it into separate words. 
  Returns: a set of token words. """

  new_categories = set()
  c = set(categories.split(", "))
  new_categories = new_categories.union(c)
  
  return new_categories

def tokenize_attributes(attributes):
  """" Takes in an attribute dictionary and tokenizes it into separate, key words. 
  Returns: a set of token words. """

  #CHECK - if this includes all attributes from yelp-restaurants that might be necessary

  new_attributes = set()
  for key in attributes:
    try:
      i = int(attributes[key])
      if isinstance(i, int):
        new_attributes.add(key)
    except ValueError:  
      if key == "Ambience":
        text = attributes['Ambience']
        new_attributes = new_attributes.union(set(re.split(r'[:,]\s*', text)))
      elif attributes[key] != "False":
        new_attributes.add(key)
  
  return new_attributes

def get_key_words():
  """" Used to create the key words for the restaurant data set.
  Returns: the category and attribute final list in csv called 'output'. 
  """
  
  restaurants, restaurant_dict = create_python_dict()
  result_cat = set()
  result_att = set()
  for res in restaurants:
    if res['categories'] is not None:
      c = tokenize_categories(res['categories'])
      result_cat = result_cat.union(c)
    if res['attributes'] is not None:
      result_att = result_att.union(tokenize_attributes(res['attributes']))
  
  with open('output.csv', mode='w') as csv_file:
    fieldnames = ['category', 'attribute']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    length = max(len(result_att), len(result_cat))
    for c in result_cat:
      writer.writerow({'category': c})
    for a in result_att:
      writer.writerow({'attribute': a})


#TESTING

# run(['romantic, hipster'],['Family', 'bagel'],'Phoenix', 'AZ', None, None)
# run(['romantic'],['Family', 'Kid'],'Phoenix', 'AZ', 'Las Vegas', 'NV')
# run(['trendy'],['Waffle'],'Scottsdale', 'AZ', 'Mesa', 'AZ')
# run([],[],'Mesa', 'AZ', 'Mesa', 'AZ')


#bugs
# run(['trendy', 'hipster'],['Kid'],'Mesa', 'AZ', 'Mesa', 'AZ')





# res = create_python_dict()
# loc = restaurant_location(res, 'Phoenix', 'AZ')
# f = find_restaurants(['Family', 'Waffle'], ['romantic', 'casual'], res)
# result = combine_location(f, loc)
# k = next(iter(result))
# k2 = list(result.keys())[2]
# print(result[k])
# print(result[k2])

