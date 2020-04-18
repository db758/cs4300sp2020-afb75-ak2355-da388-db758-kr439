import numpy as np
import json
import operator
import csv
import re

def create_python_dict():
  """ Converts json to python dictionary """
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
    tempDict[temp["name"]] = temp
  
  return (tempList, tempDict)

def get_key_words():
  """" Returns the category and attribute final list in csv. """
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
  

def run(mov_attributes, mov_categories, city1, state1, city2, state2):
  """" Runs the main code and returns an ordered dictionary of restaurants. """

  #can change to figure out what to print

  restaurants, restaurant_dict = create_python_dict()

  if state1 == state2:
    #return a restaurant in the same state
    restaurant_locations = restaurant_location(restaurants, state1, city1, city2)
    restaurant_scores, key_words_dict = find_restaurants(mov_categories, mov_attributes, restaurants)
    final_result = combine_location(restaurant_scores, restaurant_locations)

    if len(final_result) == 0:
      print("Could not find restaurant :( ")
      return "Could not find restaurant :( "
    else:
      first_elem = list(final_result.keys())[0]
      first_elem_score = final_result[first_elem]
      i = key_words_dict[first_elem]
      print("Restaurant: " + str(first_elem) + ", Score: " + str(first_elem_score))
      print("Location: " + restaurant_dict[first_elem]['city'] + ", " +  restaurant_dict[first_elem]['state'] + ", Matchings: " + str(i)) 
      return "Restaurant: " + str(first_elem) + ", Score: " + str(first_elem_score)
 
  elif state2 is None:
    #if there is only one user
    print("inside state2 is None")
    restaurant_locations = restaurant_location_one_user(restaurants, city1, state1)
    restaurant_scores, key_words_dict = find_restaurants(mov_categories, mov_attributes, restaurants)

    # for e in restaurant_locations:
    #   if e['state'] != 'AZ':
    #     print(e)

    final_result = combine_location(restaurant_scores, restaurant_locations)

    if len(final_result) == 0:
      print("Could not find restaurant :( ")
      return "Could not find restaurant :( "
    else:
      first_elem = list(final_result.keys())[1]
      first_elem_score = final_result[first_elem]
      i = key_words_dict[first_elem]
      print("Restaurant: " + str(first_elem) + ", Score: " + str(first_elem_score))
      print("Location: " + restaurant_dict[first_elem]['city'] + ", " +  restaurant_dict[first_elem]['state'] + ", Matchings: " + str(i)) 
      return "Restaurant: " + str(first_elem) + ", Score: " + str(first_elem_score)

  else:
    #return two restaurants, one for each user

    #user1
    restaurant_locations1 = restaurant_location_one_user(restaurants, city1, state1)
    restaurant_scores1, key_words_dict1 = find_restaurants(mov_categories, mov_attributes, restaurants)
    final_result1 = combine_location(restaurant_scores1, restaurant_locations1)

    print("User 1 Restaurant: ")
    if len(final_result1) == 0:
      print("Could not find restaurant for user 1 :( ")
      return "Could not find restaurant for user 1 :( "
    else:
      first_elem1 = list(final_result1.keys())[0]
      first_elem_score1 = final_result1[first_elem]
      i1 = key_words_dict1[first_elem1]
      print("Restaurant: " + str(first_elem1) + ", Score: " + str(first_elem_score1))
      print("Location: " + restaurant_dict[first_elem1]['city'] + ", " +  restaurant_dict[first_elem1]['state'] + ", Matchings: " + str(i1)) 
      return "Restaurant: " + str(first_elem1) + ", Score: " + str(first_elem_score1)

    #user2
    restaurant_locations2 = restaurant_location_one_user(restaurants, city2, state2)
    restaurant_scores2, key_words_dict2 = find_restaurants(mov_categories, mov_attributes, restaurants)
    final_result2 = combine_location(restaurant_scores2, restaurant_locations2)

    print("User 2 Restaurant: ")
    if len(final_result2) == 0:
      print("Could not find restaurant for user 2 :( ")
    else:
      first_elem2 = list(final_result2.keys())[0]
      first_elem_score2 = final_result2[first_elem]
      i2 = key_words_dict2[first_elem2]
      print("Restaurant: " + str(first_elem2) + ", Score: " + str(first_elem_score2))
      print("Location: " + restaurant_dict[first_elem2]['city'] + ", " +  restaurant_dict[first_elem2]['state'] + ", Matchings: " + str(i2)) 
  
  
def tokenize_categories(categories):
  """" Takes in a category string and tokenizes it into separate words. 
  Returns a set of token words. """

  new_categories = set()
  c = set(categories.split(", "))
  new_categories = new_categories.union(c)
  
  return new_categories

def tokenize_attributes(attributes):
  """" Takes in an attribute dictionary and tokenizes it into separate, key words. 
  Returns a set of token words. """

  new_attributes = set()
  for key in attributes:
    try:
      i = int(attributes[key])
      if isinstance(i, int):
        new_attributes.add(key)
    except ValueError:  
      if key == "Ambience":
        text = attributes['Ambience']
        # attribute_dictionary = json.loads(text)
        # a = set(text.split(", "))
        new_attributes = new_attributes.union(set(re.split(r'[:,]\s*', text)))
        # words = set()
        # for tup in a:
        #   temp = set(tup.split(": "))
        #   print(temp)
        #   NoneType = type(None)
          # for w in temp:
          #   if not isinstance(w, NoneType) and w != 'False' and w != 'True':
          #     words = words.add(w)
      elif attributes[key] != "False":
        new_attributes.add(key)
  
  return new_attributes

def intersection_fun(set1, set2):
  result = set()
  for word1 in set1:
    for word2 in set2:
      if word1.lower() in word2.lower():
        result.add(word1.lower())
      elif word2.lower() in word1.lower():
        result.add(word2.lower())
  return result


def jaccard_sim(set1, set2):
  """" Returns a tuple with a simple Jaccard Similarity score for set1 and set2
  and the set of intersection words. """

  intersection = intersection_fun(set1, set2)
  numerator = len(intersection)
  denominator = (len(set1) + len(set2)) - numerator
  return (float(numerator) / float(denominator), intersection)

def restaurant_location_one_user(restaurants, city, state):
  """" Takes in a dictionary of restaurants, a string city and a string state.
  Returns an ordered list of restaurant dictionaries that are near the location,
  where the beginning elements are the closest and the later are farther """

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
  Returns an ordered list of restaurant dictionaries that are near the location,
  where the beginning elements are the closest and the later are farther """

  #function only called when the state of both users is the same
  result = []
  for r in restaurants:
    if r['state'] == state:
      if r['city'] == city1 or r['city'] == city2:
        result = [r] + result
      else:
        result += [r]
  return result

def find_restaurants(mov_categories, mov_attributes, restaurants):
  """" Returns a sorted dictionary of restuarants with name of restaurant and 
  the similarity score to the mov_categories and mov_attributes. """
  result = {}
  output = {}
  for r in restaurants:
    res_categories = set()
    res_attributes = set()
    if r['attributes'] is not None:
      res_attributes = tokenize_attributes(r['attributes'])
    if r['categories'] is not None:
      res_categories = tokenize_categories(r['categories'])
    jac_attribute = jaccard_sim(set(mov_attributes), res_attributes)
    jac_cattegory = jaccard_sim(set(mov_categories), res_categories)
    sim_attribute = jac_attribute[0]
    sim_category = jac_cattegory[0]

    result[r['name']] = sim_attribute + sim_category
    output[r['name']] = jac_attribute[1].union(jac_cattegory[1])

    #can add weights to each
  
  # sorted_result = sorted(result.items(), key=operator.itemgetter(1))
  sorted_dict = {r: result[r] for r in sorted(result, key=result.get, reverse=True)}
  return (sorted_dict, output)

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
  
  sorted_result = {r: result[r] for r in sorted(result, key=result.get, reverse=True)}
  return sorted_result

print("Method")
run(['romantic'],['Family'],'Phoenix', 'AZ', None, None)
# res = create_python_dict()
# loc = restaurant_location(res, 'Phoenix', 'AZ')
# f = find_restaurants(['Family', 'Waffle'], ['romantic', 'casual'], res)
# result = combine_location(f, loc)
# k = next(iter(result))
# k2 = list(result.keys())[2]
# print(result[k])
# print(result[k2])

