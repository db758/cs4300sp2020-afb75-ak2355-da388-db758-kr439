import numpy as np
import json
import operator
import csv
import re
from sklearn.feature_extraction.text import TfidfVectorizer

#gets five restaurants for each user
#goes through all the reviews for each of the five restaurants
#get the key terms from each review

#corpus - all reviews per restaurant

def create_reviews():
  """ Converts json to list of words in all reviews """
  #should it take in the business id and then separate all reviews for that business id?
  jsonList = []
  with open('yelp-reviews.txt') as f:
      for jsonObj in f.readlines():
        obj = json.loads(jsonObj)
        jsonList.append(obj)
  
  reviews = []
  for e in jsonList:
    reviews += tokenize_words(e['text'])
  
  return reviews


def tokenize_words(s):
  """ Converts string s into token words"""
  return re.split(r"\w", s) #fix

def create_term_doc(corpus):
  vectorizer = TfidfVectorizer()
  X = vectorizer.fit_transform(corpus)
