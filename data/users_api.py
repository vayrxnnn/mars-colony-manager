from flask import Blueprint, jsonify, request, make_response

from data import db_session
from data.users import User

blueprint = Blueprint('users_api', __name__, template_folder='templates')


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()

    users = db_sess.query(User).all()

    return jsonify({
        'users': [
            item.to_dict(only=(
                'id',
                'surname',
                'name',
                'age',
                'position',
                'speciality',
                'address',
                'city_from',
                'email'
            ))
            for item in users
        ]
    })


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()

    user = db_sess.get(User, user_id)

    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)

    return jsonify({
        'user': user.to_dict(
            only=(
                'id',
                'surname',
                'name',
                'age',
                'position',
                'speciality',
                'address',
                'email',
                'city_from',
                'avatar'
            )
        )
    })


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)

    required = [
        'surname',
        'name',
        'age',
        'position',
        'speciality',
        'address',
        'city_from',
        'email',
        'hashed_password'
    ]

    if not all(key in request.json for key in required):
        return make_response(jsonify({'error': 'Bad request'}), 400)

    db_sess = db_session.create_session()

    user = User(
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        city_from=request.json['city_from'],
        email=request.json['email'],
        hashed_password=request.json['hashed_password']
    )

    db_sess.add(user)
    db_sess.commit()

    return jsonify({'id': user.id})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()

    user = db_sess.get(User, user_id)

    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)

    db_sess.delete(user)
    db_sess.commit()

    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)

    db_sess = db_session.create_session()
    user = db_sess.get(User, user_id)

    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    if 'surname' in request.json:
        user.surname = request.json['surname']
    if 'name' in request.json:
        user.name = request.json['name']
    if 'age' in request.json:
        user.age = request.json['age']
    if 'position' in request.json:
        user.position = request.json['position']
    if 'speciality' in request.json:
        user.speciality = request.json['speciality']
    if 'address' in request.json:
        user.address = request.json['address']
    if 'city_from' in request.json:
        user.city_from = request.json['city_from']
    if 'email' in request.json:
        user.email = request.json['email']
    if 'hashed_password' in request.json:
        user.hashed_password = request.json['hashed_password']
    db_sess.commit()

    return jsonify({'success': 'OK'})
