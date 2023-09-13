from flask_sqlalchemy import SQLAlchemy
import json
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Planets(db.Model):
    __tablename__ = "planets"

    id = db.Column(db.Integer, primary_key=True)
    diameter = db.Column(db.String(250), nullable=True)
    rotation_period = db.Column(db.String(250), nullable=True)
    orbital_period = db.Column(db.String(250), nullable=True)
    population = db.Column(db.String(250), nullable=True)
    climate = db.Column(db.String(250), nullable=True)
    terrain = db.Column(db.String(250), nullable=True)
    description = db.Column(db.String(250), nullable=True)

    def serialize(self):
        return {
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "description": self.description
        }


class Vehicles(db.Model):
    __tablename__ = "vehicles"

    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(250), nullable=False)
    vehicle_class = db.Column(db.String(250), nullable=True)
    manufacturer = db.Column(db.String(250), nullable=True)
    cost_in_credits = db.Column(db.String(250), nullable=True)
    length = db.Column(db.String(250), nullable=True)
    crew = db.Column(db.String(250), nullable=True)
    passengers = db.Column(db.String(250), nullable=True)

    def serialize(self):
        return {
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers
        }


class People(db.Model):
    __tablename__ = "people"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.String(250), nullable=True)
    mass = db.Column(db.String(250), nullable=True)
    hair_color = db.Column(db.String(250), nullable=True)
    skin_color = db.Column(db.String(250), nullable=True)
    eye_color = db.Column(db.String(250), nullable=True)
    gender = db.Column(db.String(250), nullable=True)
    description = db.Column(db.String(250), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey(
        'planets.id'), nullable=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey(
        'vehicles.id'), nullable=True)
    planets = db.relationship(Planets)
    vehicles = db.relationship(Vehicles)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "planet_id": self.planet_id,
            "vehicle_id": self.vehicle_id
        }


class Favorites(db.Model):
    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User)
    person_id = db.Column(
        db.Integer, db.ForeignKey('people.id'), nullable=True)
    people = db.relationship(People)
    planet_id = db.Column(db.Integer, db.ForeignKey(
        'planets.id'), nullable=True)
    planets = db.relationship(Planets)
    vehicles_id = db.Column(
        db.Integer, db.ForeignKey('vehicles.id'), nullable=True)
    vehicles = db.relationship(Vehicles)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "person_id": self.character_id,
            "planet_id": self.planet_id,
            "vehicles_id": self.vehicles_id
        }
