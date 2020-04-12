import os
import json
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db
from app.irsystem.models.restaurant import *
from sqlalchemy.exc import IntegrityError


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command("db", MigrateCommand)

@manager.command
def add_yelp_data(file="yelp-restaurants.txt"):
  with open(file) as f:
    for jsonObj in f.readlines():
      obj = json.loads(jsonObj)
      bid = obj['business_id']
      name = obj["name"]
      address = obj['address'] 
      city = obj['city']
      state = obj['state'] 
      stars = float(obj['stars'])
      review_count = int(obj['review_count'])
      attributes = str(obj['attributes'])
      categories = obj['categories']

      r = Restaurant(bid=bid, name=name, address=address, city=city, 
      state=state, stars=stars, review_count=review_count, attributes=attributes,
      categories=categories)
      db.session.add(r)
      try:
        db.session.commit()
      except IntegrityError:
        db.session.rollback()


if __name__ == "__main__":
  manager.run()
