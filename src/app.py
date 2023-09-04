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
from models import db, User, People, Planets, Vehicles, User_Favorites
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


@app.route('/user', methods=['GET'])
def handle_users():
    user = User.query.all()
    if user is None:
        return jsonify(msg='No user found')
    else:
        return jsonify(data=[user.serialize() for user in user]), 200


@app.route('/user/<int:user_id>', methods=['PUT', 'GET'])
def get_single_user(user_id):
    if request.method == 'GET':
        user1 = User.query.get(user_id)
        return jsonify(user1.serialize()), 200


@app.route('/user/favorites', methods=['GET'])
def handle_user_faves():
    user_faves = User_Favorites.query.all()
    if user_faves is None:
        return jsonify(msg='No favorites found')
    else:
        return jsonify(data=[user_faves.serialize() for user_faves in user_faves]), 200

# this method is returning 400


@app.route('/user/<int:user_id>/favorites/planets/<int:planet_id>', methods=['POST'])
def create_fave_planet(planet_id):
    body = request.get_json(planet_id)
    if body is None:
        return 'The request body is null', 400
    if 'planet_id' not in body:
        return 'You need to select a planet', 400
    return 'ok', 200


@app.route('/user/<int:user_id>/favorites/planets/<int:planet_id>', methods=['DELETE'])
def remove_fave_planet():
    body = request.get_json()
    if body is None:
        return 'The request body is null', 400
    if 'planet_id' not in body:
        return 'You need to select a planet', 400
    return 'ok', 200

# this method is returning 500


@app.route('/favorites/people/<int:person_id>', methods=['POST'])
def create_fave_person():
    favorites = User_Favorites.query.all()
    body = request.get_json()
    print("Incoming request with the following body", body)
    favorites.append(body)
    return jsonify(favorites)


@app.route('/user/<int:user_id>/favorites/people/<int:person_id>', methods=['DELETE'])
def remove_fave_person(position):
    person = request.get_json()
    print("This is the position to delete: ", position)
    del person[position]
    return jsonify(person)


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
