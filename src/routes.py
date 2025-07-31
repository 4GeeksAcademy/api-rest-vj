from flask import Blueprint, jsonify, request
from models import db, User, People, Planet, Favorite

api = Blueprint('api', __name__)


@api.route('/people', methods=['GET'])
def get_all_people():
    people = People.query.all()
    result = [
        {"id": p.id, "name": p.name, "height": p.height, "gender": p.gender}
        for p in people
    ]
    return jsonify(result), 200


@api.route('/people/<int:people_id>', methods=['GET'])
def get_one_person(people_id):
    person = People.query.get(people_id)
    if person:
        return jsonify({
            "id": person.id,
            "name": person.name,
            "height": person.height,
            "gender": person.gender
        }), 200
    return jsonify({"error": "Person not found"}), 404


@api.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    result = [
        {"id": p.id, "name": p.name, "terrain": p.terrain, "population": p.population}
        for p in planets
    ]
    return jsonify(result), 200


@api.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        return jsonify({
            "id": planet.id,
            "name": planet.name,
            "terrain": planet.terrain,
            "population": planet.population
        }), 200
    return jsonify({"error": "Planet not found"}), 404


@api.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    result = [
        {"id": u.id, "email": u.email, "is_active": u.is_active}
        for u in users
    ]
    return jsonify(result), 200


@api.route('/users/favorites', methods=['GET'])
def get_user_favorites():

    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required as query param"}), 400

    favorites = Favorite.query.filter_by(user_id=user_id).all()
    result = []
    for fav in favorites:
        if fav.planet:
            result.append(
                {"type": "planet", "id": fav.planet.id, "name": fav.planet.name})
        elif fav.people:
            result.append(
                {"type": "people", "id": fav.people.id, "name": fav.people.name})
    return jsonify(result), 200


@api.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_fav_planet(planet_id):
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id required in body"}), 400

    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404

    exists = Favorite.query.filter_by(
        user_id=user_id, planet_id=planet_id).first()
    if exists:
        return jsonify({"message": "Planet already in favorites"}), 200

    fav = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify({"message": "Planet added to favorites"}), 201


@api.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_fav_people(people_id):
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id required in body"}), 400

    person = People.query.get(people_id)
    if not person:
        return jsonify({"error": "Person not found"}), 404

    exists = Favorite.query.filter_by(
        user_id=user_id, people_id=people_id).first()
    if exists:
        return jsonify({"message": "Person already in favorites"}), 200

    fav = Favorite(user_id=user_id, people_id=people_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify({"message": "Person added to favorites"}), 201


@api.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet(planet_id):
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required as query param"}), 400

    fav = Favorite.query.filter_by(
        user_id=user_id, planet_id=planet_id).first()
    if not fav:
        return jsonify({"error": "Favorite not found"}), 404

    db.session.delete(fav)
    db.session.commit()
    return jsonify({"message": "Planet favorite removed"}), 200


@api.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_fav_people(people_id):
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required as query param"}), 400

    fav = Favorite.query.filter_by(
        user_id=user_id, people_id=people_id).first()
    if not fav:
        return jsonify({"error": "Favorite not found"}), 404

    db.session.delete(fav)
    db.session.commit()
    return jsonify({"message": "People favorite removed"}), 200
