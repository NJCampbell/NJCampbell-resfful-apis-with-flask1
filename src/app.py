"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Vehicles, Favorites
import json
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/people', methods=['GET'])
def handle_people():
    people = People.query.all()
    if people is None:
        return jsonify(msg="No records found")
    else:
        return jsonify(data=[people.serialize() for people in people]), 200


@app.route('/people/<int:person_id>', methods=['PUT', 'GET'])
def get_single_person(person_id):
    if request.method == 'GET':
        user1 = People.query.get(person_id)
        return jsonify(user1.serialize()), 200

    return 'Person not found', 404


@app.route('/planets', methods=['GET'])
def handle_planets():
    planets = Planets.query.all()
    if planets is None:
        return jsonify(msg="No records found")
    else:
        return jsonify(data=[planets.serialize() for planets in planets]), 200


@app.route('/planets/<int:planet_id>', methods=['PUT', 'GET'])
def get_single_planet(planet_id):
    if request.method == 'GET':
        planet1 = Planets.query.get(planet_id)
        return jsonify(planet1.serialize()), 200

    return 'Planet not found', 404


@app.route('/vehicles', methods=['GET'])
def handle_vehicles():
    vehicles = Vehicles.query.all()
    if vehicles is None:
        return jsonify(msg='No records found')
    else:
        return jsonify(data=[vehicles.serialize() for vehicles in vehicles]), 200


@app.route('/vehicles/<int:vehicle_id>', methods=['PUT', 'GET'])
def get_single_vehicle(vehicle_id):
    if request.method == 'GET':
        vehicle1 = Vehicles.query.get(vehicle_id)
        return jsonify(vehicle1.serialize()), 200

    return 'Vehicle not found', 404


@app.route('/users', methods=['GET'])
def handle_users():
    user = User.query.all()
    if user is None:
        return jsonify(msg='No user found')
    else:
        return jsonify(data=[user.serialize() for user in user]), 200


@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_favorites = Favorites.query.all()
    if request.method == 'GET':
        if user_favorites is None:
            return jsonify({'message': 'No favorites found'}), 404
        else:
            return jsonify(data=[user_favorites.serialize() for user_favorites in user_favorites]), 200


@app.route('/favorite/planet/', methods=['POST'])
def add_favorite_planet():

    data = request.get_json()
    new_favorite_planet = Favorites(planet_id=data.planet_id)
    if request.method == 'POST':
        db.session.add(new_favorite_planet)
        db.session.commit()

    return jsonify(new_favorite_planet.serialize()), 200


@app.route('/favorite/people/', methods=['POST'])
def add_favorite_people():
    data = request.get_json()
    new_favorite_person = People(person_id=data["person_id"])
    db.session.add(new_favorite_person)
    db.session.commit()

    return jsonify(data), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    favorite_planet_to_delete = Favorites.query.get(planet_id)
    db.session.delete(favorite_planet_to_delete)
    db.session.commit()

    return jsonify({'message': 'Favorite successfully deleted.'}), 200


@app.route('/favorite/people/<int:person_id>', methods=['DELETE'])
def delete_favorite_people(person_id):
    favorite_person_to_delete = Favorites.query.get(person_id)
    db.session.delete(favorite_person_to_delete)
    db.session.commit()

    return jsonify({'message': 'Favorite successfully deleted.'}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
