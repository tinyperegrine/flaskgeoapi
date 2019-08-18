from sqlalchemy import exc
from . import db
from geoalchemy2.types import Geometry
from geoalchemy2.functions import ST_AsGeoJSON


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def _save(self):
        """ Helper method for saving a new user or an updated user """
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except exc.IntegrityError as e:
            # for duplicates if they occur and more processing/recording is needed
            # errorInfo = e.orig.args
            # print(errorInfo[0])  #This will give the error message if needed
            db.session.rollback()
            raise
        except:
            db.session.rollback()
            raise

    @classmethod
    def create(cls, username, email):
        """ Create a new user """
        user = cls(username=username, email=email)
        return user._save()

    def delete(self):
        """ Delete the user """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            raise

    def update(self, username, email):
        """ Update the user"""
        data_changed = False
        if (self.username != username):
            self.username = username
            data_changed = True
        if (self.email != email):
            self.email = email
            data_changed = True
        if data_changed:
            return self._save()
        else:  
            return False

    def to_dict(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}


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
