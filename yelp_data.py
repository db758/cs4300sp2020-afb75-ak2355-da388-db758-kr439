import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt; plt.rcdefaults()

import json

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
    if "Restaurant" in element['categories']:
      finalList.append(element)
      categories.add(element['categories'])
      for key in element['attributes']:
        attributes.add(key)

new_categories = set()
for cat in categories:
  c = set(cat.split(", "))
  print(c)
  new_categories = new_categories.union(c)

categories_dict = {}
for n in new_categories:
  categories_dict[n] = 0

for f in finalList:
  for el in new_categories:
    if el in f['categories']:
      categories_dict[el] += 1

print(categories_dict)

objects = categories_dict.keys()
y_pos = np.arange(len(objects))
performance = categories_dict.values()

# plt.bar(y_pos, performance, align='center', alpha=0.5)
# plt.xticks(y_pos, objects)
# plt.ylabel('Usage')
# plt.title('Programming language usage')

plt.barh(y_pos, performance, align='center', alpha=0.5)
plt.yticks(y_pos, objects)
plt.xlabel('Categories')
plt.title('Restaurant Categories')

plt.show()



#Data Sets:

#business
#{"business_id":"f9NumwFMBDn751xgFiRbNA","name":"The Range At Lake Norman","address":"10913 Bailey Rd","city":"Cornelius","state":"NC","postal_code":"28031","latitude":35.4627242,"longitude":-80.8526119,"stars":3.5,"review_count":36,"is_open":1,"attributes":{"BusinessAcceptsCreditCards":"True","BikeParking":"True","GoodForKids":"False","BusinessParking":"{'garage': False, 'street': False, 'validated': False, 'lot': True, 'valet': False}","ByAppointmentOnly":"False","RestaurantsPriceRange2":"3"},"categories":"Active Life, Gun\/Rifle Ranges, Guns & Ammo, Shopping","hours":{"Monday":"10:0-18:0","Tuesday":"11:0-20:0","Wednesday":"10:0-18:0","Thursday":"11:0-20:0","Friday":"11:0-20:0","Saturday":"11:0-20:0","Sunday":"13:0-18:0"}}


#check in
#{"business_id":"--1UhMGODdWsrMastO9DZw","date":"2016-04-26 19:49:16, 2016-08-30 18:36:57, 2016-10-15 02:45:18, 2016-11-18 01:54:50, 2017-04-20 18:39:06, 2017-05-03 17:58:02, 2019-03-19 22:04:48"}


#review
#tip
#user

