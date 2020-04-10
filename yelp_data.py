import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

import json

# with open('path_to_file/person.json') as f:
#   data = json.load(f)

jsonList = []
count = 0
with open('yelp-business-100.txt') as f:
  
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

finalList = []
attributes = set()
categories = set()
for element in tempList:
  if element['stars'] > 3 and element['review_count'] > 10:
    # for key in element['attributes']:
    #   if "Restaurant" in key:
    #     attributes.add(key)
    #     finalList.append(element)
    #     categories.add(element['categories'])
    #     break
    if "Restaurant" in element['categories']:
      finalList.append(element)
      categories.add(element['categories'])
      for key in element['attributes']:
        attributes.add(key)

attribute_dict = {}
for a in attributes:
  attribute_dict[a] = 0

for f in finalList:
  for att in f['attributes']:
    attribute_dict[att] += 1

print(attribute_dict)

# print(finalList)
# print(attributes)

#x = [21,22,23,4,5,6,77,8,9,10,31,32,33,34,35,36,37,18,49,50,100]
# num_bins = 5
# n, bins, patches = plt.hist(x, num_bins, facecolor='blue')
# plt.show()
# plt.savefig('output.png')

names = list(attribute_dict.keys())
values = list(attribute_dict.values())




#Data Sets:

#business
#{"business_id":"f9NumwFMBDn751xgFiRbNA","name":"The Range At Lake Norman","address":"10913 Bailey Rd","city":"Cornelius","state":"NC","postal_code":"28031","latitude":35.4627242,"longitude":-80.8526119,"stars":3.5,"review_count":36,"is_open":1,"attributes":{"BusinessAcceptsCreditCards":"True","BikeParking":"True","GoodForKids":"False","BusinessParking":"{'garage': False, 'street': False, 'validated': False, 'lot': True, 'valet': False}","ByAppointmentOnly":"False","RestaurantsPriceRange2":"3"},"categories":"Active Life, Gun\/Rifle Ranges, Guns & Ammo, Shopping","hours":{"Monday":"10:0-18:0","Tuesday":"11:0-20:0","Wednesday":"10:0-18:0","Thursday":"11:0-20:0","Friday":"11:0-20:0","Saturday":"11:0-20:0","Sunday":"13:0-18:0"}}


#check in
#{"business_id":"--1UhMGODdWsrMastO9DZw","date":"2016-04-26 19:49:16, 2016-08-30 18:36:57, 2016-10-15 02:45:18, 2016-11-18 01:54:50, 2017-04-20 18:39:06, 2017-05-03 17:58:02, 2019-03-19 22:04:48"}


#review
#tip
#user

