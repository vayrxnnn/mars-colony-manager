from flask import jsonify
from flask_restful import Resource, abort

from data import db_session
from data.users import User
from data.parser import parser


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.get(User, user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.get(User, user_id)

        return jsonify({
            'user': {
                'surname': user.surname,
                'name': user.name,
                'age': user.age,
                'position': user.position,
                'speciality': user.speciality,
                'address': user.address,
                'email': user.email,
                'city_from': user.city_from,
                'avatar': user.avatar
            }
        })

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.get(User, user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()

        return jsonify({
            'users': [
                {
                    'surname': item.surname,
                    'name': item.name,
                    'age': item.age,
                    'position': item.position,
                    'speciality': item.speciality,
                    'address': item.address,
                    'email': item.email
                }
                for item in users
            ]
        })

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            hashed_password=args['hashed_password']
        )

        session.add(user)
        session.commit()

        return jsonify({'success': 'OK'})
