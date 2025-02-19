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
from models import db, User, People, Planet, Favorite_people, Favorite_planet
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

#-------------------ENDPOINTS DE USERS-------------------------------------------------

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_info = [user.serialize() for user in users ]
    return jsonify(user_info), 200


@app.route('/users/<int:id>/favorites', methods=['GET'])
def get_favorites_users(id):
    user = User.query.get(id)
    user_info = user.serialize()
    favorite_user_planet = user_info['favorite_planet']
    favorite_user_people = user_info['favorite_people']
    return jsonify({"planet" : favorite_user_planet, "people": favorite_user_people}), 200

@app.route('/favorites', methods=['GET'])
def get_all_favorites():
    favorite_people = Favorite_people.query.all()
    favorite_planet = Favorite_planet.query.all()
    people = [people.serialize() for people in favorite_people]
    planets = [planet.serialize() for planet in favorite_planet]

    return jsonify({"people": people, "planets" :  planets})



#-----------------------------ENDPOINTS TRAER USUARIOS-------------------------

@app.route('/user/<int:user_id>/favorite/people/<int:people_id>', methods=['POST'])
def add_people_favorite(user_id, people_id):
    exist = Favorite_people.query.filter_by(relation_user=user_id, relation_people=people_id).first()
    if exist:
        return jsonify({"msg": "el character ya existe en la lista de favoritos"})
    
    new_favorite_people = Favorite_people(relation_user = user_id, relation_people = people_id)
    db.session.add(new_favorite_people)
    db.session.commit()
    return jsonify({"msg" : "people agregado correctamente"})



#----------------------ENDPOINTS AGREGAR O ELIMINAR USUARIOS-------------------------

@app.route('/user/<int:user_id>/favorite/planet/<int:planet_id>', methods=['POST'])
def add_planet_favorite(user_id, planet_id):
    exist = Favorite_planet.query.filter_by(relation_user=user_id, relation_planet = planet_id).first()
    if exist:
        return jsonify({"msg": "el planeta ya existe en la lista de favoritos"})
    
    new_favorite_planet = Favorite_planet(relation_user = user_id, relation_planet = planet_id)
    db.session.add(new_favorite_planet)
    db.session.commit()
    return jsonify({"msg" : "planet agregado correctamente"})


@app.route('/user/<int:user_id>/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_people_favorite(user_id, people_id):
    exist = Favorite_people.query.filter_by(relation_user=user_id, relation_people=people_id).first()
    if exist:    
        db.session.delete(exist)
        db.session.commit()
        return jsonify({"msg" : "people eliminado correctamente"})
    

@app.route('/user/<int:user_id>/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet_favorite(user_id, planet_id):
    exist = Favorite_planet.query.filter_by(relation_user=user_id, relation_planet = planet_id).first()
    if exist:
        db.session.delete(exist)
        db.session.commit()
        return jsonify({"msg" : "planet eliminado correctamente"})


#--------------------ENDPOINTS TRAER PEOPLE Y PLANETS-------------------------------------

@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    character_info = [character.serialize() for character in people ]
    return jsonify(character_info), 200

@app.route('/people/<int:id>', methods=['GET'])
def get_people_individual(id):
    people = People.query.get(id)
    character_info = people.serialize()
    return jsonify(character_info), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    planet_info = [planet.serialize() for planet in planets ]
    return jsonify(planet_info), 200


@app.route('/planets/<int:id>', methods=['GET'])
def get_planet_individual(id):
    planet = Planet.query.get(id)
    planet_info = planet.serialize()
    return jsonify(planet_info), 200

#-------------ENDPOINTS AGREGAR Y ELIMINAR PEOPLE--------------

@app.route('/people', methods=['POST'])
def add_people():
    data = request.get_json()
    
    new_people = People(
        name=data["name"],
        height=data["height"],
        mass=data["mass"],
        hair_color=data["hair_color"],
        eye_color = data["eye_color"],
        birth_year =data["birth_year"],
        gender = data["gender"],
        homeworld = data["homeworld"],
        url = data["url"]
    )
    db.session.add(new_people)
    db.session.commit()
    return jsonify({'msg' : 'people agregado sastifactoriamente'}), 200


@app.route('/people/<int:id_people>', methods=['PUT'])
def update_people(id_people):
    people = People.query.get(id_people)
    data = request.get_json()

    people.name = data["name"]
    people.height=data["height"]
    people.mass=data["mass"]
    people.hair_color=data["hair_color"]
    people.eye_color = data["eye_color"]
    people.birth_year =data["birth_year"]
    people.gender = data["gender"]
    people.homeworld = data["homeworld"]
    people.url = data["url"]
    
    db.session.commit()
    return jsonify({'msg' : f'actualizado {people.name}'})

@app.route('/people/<int:id_people>', methods=['DELETE'])
def delete_people(id_people):
    character = People.query.get(id_people)

    db.session.delete(character)
    db.session.commit()

    return jsonify({'msg' : f'el character {character.name} fue eliminado'})


#-------------ENDPOINTS AGREGAR Y ELIMINAR PLANETS--------------
@app.route('/planet', methods=['POST'])
def add_planet():
    data = request.get_json()
    
    new_people = Planet(
        name=data["name"],
        diameter=data["diameter"],
        rotation_period=data["rotation_period"],
        orbital_period=data["orbital_period"],
        gravity = data["gravity"],
        population =data["population"],
        climate = data["climate"],
        terrain = data["terrain"],
        url = data["url"]
    )
    db.session.add(new_people)
    db.session.commit()
    return jsonify({'msg' : 'planet agregado sastifactoriamente'}), 200


@app.route('/planet/<int:id_planet>', methods=['PUT'])
def update_planet(id_planet):
    planet = Planet.query.get(id_planet)
    data = request.get_json()

    planet.name = data["name"]
    planet.diameter=data["diameter"]
    planet.rotation_period=data["rotation_period"]
    planet.orbital_period=data["orbital_period"]
    planet.gravity = data["gravity"]
    planet.population =data["population"]
    planet.climate = data["climate"]
    planet.terrain = data["terrain"]
    planet.url = data["url"]
    
    db.session.commit()
    return jsonify({'msg' : f'actualizado {planet.name}'})


@app.route('/planet/<int:id_planet>', methods=['DELETE'])
def delete_planet(id_planet):
    planet = Planet.query.get(id_planet)

    db.session.delete(planet)
    db.session.commit()

    return jsonify({'msg' : f'el planeta {planet.name} fue eliminado'})

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
