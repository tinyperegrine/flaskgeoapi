from . import db
from geoalchemy2.types import Geometry
from geoalchemy2.functions import ST_AsGeoJSON


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class CoffeeShop(db.Model):
    __tablename__ = 'coffee_shops'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(50))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    zip = db.Column(db.String(10))
    lat = db.Column(db.Numeric())
    lon = db.Column(db.Numeric())
    geom = db.Column(Geometry(geometry_type='POINT', srid=4326))

    def to_geojson(self):
        geojson_geometry = db.session.scalar(ST_AsGeoJSON(self.geom))
        return geojson_geometry

    def __repr__(self):
        return '<CoffeShop %r>' % self.name
