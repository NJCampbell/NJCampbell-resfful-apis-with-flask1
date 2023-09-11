from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String(50), nullable=False)
    diameter = db.Column(db.String(50), nullable=False)
    rotation_period = db.Column(db.String(50), nullable=False)
    orbital_period = db.Column(db.String(50), nullable=False)
    gravity = db.Column(db.String(50), nullable=False)
    population = db.Column(db.String(50), nullable=False)
    climate = db.Column(db.String(50), nullable=False)
    terrain = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(1000), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "a_planet_name": self.planet_name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "description": self.description
        }


class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_name = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    vehicle_class = db.Column(db.String(50), nullable=True)
    manufacturer = db.Column(db.String(50), nullable=True)
    cost_in_credits = db.Column(db.String(50), nullable=True)
    length = db.Column(db.String(50), nullable=True)
    crew = db.Column(db.String(50), nullable=True)
    passengers = db.Column(db.String(50), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "a_model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers,

        }


class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    persons_name = db.Column(db.String(50), nullable=False)
    height = db.Column(db.String(50), nullable=True)
    mass = db.Column(db.String(50), nullable=True)
    hair_color = db.Column(db.String(50), nullable=True)
    skin_color = db.Column(db.String(50), nullable=True)
    eye_color = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(50), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    planet = db.relationship(Planets)
    vehicle = db.relationship(Vehicles)

    def serialize(self):
        return {
            "id": self.id,
            "a_persons_name": self.persons_name,
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
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    # persons_name = db.Column(db.String(50), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    # planet_name = db.Column(db.String(50), nullable=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    # vehicle_name = db.Column(db.String(50), nullable=True)
    people = db.relationship(People)
    planet = db.relationship(Planets)
    vehicle = db.relationship(Vehicles)

    def serialize(self):
        return {
            "id": self.id,
            # "persons_name": self.persons_name,
            # "planet_name": self.planet_name,
            # "vehicle_name": self.vehicle_name,
            "user_id": self.user_id,
            "person_id": self.person_id,
            "planet_id": self.planet_id,
            "vehicle_id": self.vehicle_id,
        }
