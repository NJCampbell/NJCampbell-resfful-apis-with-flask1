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
from models import db, User, People, Planets, Vehicles
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
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

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def handle_people():
    return 'hello people'

@app.route('/people/<int:person_id>', methods=['PUT', 'GET'])
def get_single_person(person_id):
    if request.method =='GET':
        user1 = People.query.get(person_id)
        return jsonify(user1.serialize()), 200
    
    return 'Person not found', 404

@app.route('/planets', methods=['GET'])
def handle_planets():
    return 'hello planets'

@app.route('/planets/<int:planet_id>', methods=['PUT', 'GET'])
def get_single_planet(planet_id):
    if request.method == 'GET':
        planet1 = Planets.query.get(planet_id)
        return jsonify(planet1.serialize()), 200
    
    return 'Planet not found', 404

@app.route('/vehicles', methods=['GET'])
def handle_vehicles():
    return 'hello vehicles'

@app.route('/vehicles/<int:vehicle_id>', methods=['PUT', 'GET'])
def get_single_vehicle(vehicle_id):
    if request.method == 'GET':
        vehicle1 = Vehicles.query.get(vehicle_id)
        return jsonify(vehicle1.serialize()), 200
    
    return 'Vehicle not found', 404
# @app.route('/person', methods=['POST', 'GET'])
# def handle_person():
#     content = {
#         'details': 'Hey, there has been an error on your request.'
#     }
#     return jsonify(content), 400


    #third example
    # response = jsonify(content)      
    # response.status_code = 200
    # return response
 
 
    #second example
    # person1 = {
    #     'name': 'Bob'
    # }
    # return jsonify(person1)



    #first example
    # if request.method == 'POST':
    #     return 'A POST has been received!'
    # else:
    #     return 'A GET has been received!'



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
