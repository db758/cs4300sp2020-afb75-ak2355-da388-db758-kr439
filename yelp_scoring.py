import numpy as np
import json
import operator

def create_python_dict():
  """ Converts json to python dictionary """
  jsonList = []
  count = 0
  with open('yelp-restaurants.txt') as f:
      for jsonObj in f.readlines():
        obj = json.loads(jsonObj)
        jsonList.append(obj)

  tempList = []
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
  
  return tempList

def run(mov_attributes, mov_categories, city, state):
  """" Runs the main code and returns an ordered dictionary of restaurants. """

  #can change to figure out what to print
  
  restaurants = create_python_dict()
  restaurant_locations = restaurant_location(restaurants, city, state)
  restaurant_scores = find_restaurants(mov_categories, mov_attributes, restaurants)
  return combine_location(restaurant_scores, restaurant_locations)

def tokenize_categories(categories):
  """" Takes in a category string and tokenizes it into separate words. 
  Returns a set of token words. """

  new_categories = set()
  for cat in categories:
    c = set(cat.split(", "))
    new_categories = new_categories.union(c)
  
  return new_categories

def tokenize_attributes(attributes):
  """" Takes in an attribute dictionary and tokenizes it into separate, key words. 
  Returns a set of token words. """

  new_attributes = set()
  for key in attributes:
    try:
      i = int(attributes[key])
      if isinstance(attributes[key], i):
        new_attributes.add(key)
    except ValueError:  
      if key == "Ambience":
        for k, v in attributes['Ambience'].items():
          if v == "True":
            new_attributes.add(k)
      elif attributes[key] != "False":
        new_attributes.add(key)
  
  return new_attributes

def jaccard_sim(set1, set2):
  """" Returns a simple Jaccard Similarity score for set1 and set2 """

  numerator = len(set(set1).intersection(set2))
  denominator = (len(set1) + len(set2)) - numerator
  return float(numerator) / float(denominator)

def restaurant_location(restaurants, city, state):
  """" Takes in a dictionary of restaurants, a string city and a string state.
  Returns an ordered list of restaurant dictionaries that are near the location,
  where the beginning elements are the closest and the later are farther """

  result = []
  for r in restaurants:
    if r['state'] == state:
      if r['city'] == city:
        result = r + result
      else:
        result += r
  return result

def find_restaurants(mov_categories, mov_attributes, restaurants):
  """" Returns a sorted dictionary of restuarants with name of restaurant and 
  the similarity score to the mov_categories and mov_attributes. """
  result = {}
  for r in restaurants:
    res_attributes = tokenize_attributes(r['attributes'])
    res_categories = tokenize_categories(r['categories'])
    sim_attribute = jaccard_sim(mov_attributes, mov_categories)
    sim_category = jaccard_sim(mov_categories, res_categories)

    result[r['name']] = sim_attribute + sim_category
    #can add weights to each
  
  sorted_result = sorted(result.items(), key=operator.itemgetter(1))
  return sorted_result

def combine_location(restaurant_scores, restaurant_locations):
  """" Takes in a sorted dictionary of restaurant names and similarity scores
  and an ordered list of restaurants in a specific location range. 
  Returns a dictionary of restaurants sorted on the highest matching scores. """

  weight = len(restaurant_locations)
  #set the weight to decrease by 1 for each following location

  result = {}
  for r in restaurant_locations:
    score = restaurant_scores[r['name']] + weight
    result[r['name']] = score
  
  sorted_result = sorted(result.items(), key=operator.itemgetter(1))
  return sorted_result


