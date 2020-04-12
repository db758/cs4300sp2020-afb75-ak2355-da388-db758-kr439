from app import db 

class Restaurant(db.Model):
  __tablename__ = 'Restaurant'
  bid = db.Column(db.String(30), primary_key=True)
  name = db.Column(db.String(200))
  address = db.Column(db.String(500))
  city = db.Column(db.String(1000))
  state = db.Column(db.String(1000))
  stars = db.Column(db.Float)
  review_count = db.Column(db.Integer)
  attributes = db.Column(db.String(2000))
  categories = db.Column(db.String(2000))

  def __init__(self, bid, name, address, city, state, stars, review_count, attributes, categories):
    self.bid = bid
    self.name = name
    self.address = address
    self.city = city
    self.state = state
    self.stars = stars
    self.review_count = review_count
    self.attributes = attributes
    self.categories = categories
