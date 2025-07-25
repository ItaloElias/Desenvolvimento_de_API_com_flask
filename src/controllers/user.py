from flask import Blueprint, request 
from src.app import User, db
from http import HTTPStatus
from sqlalchemy import inspect
from flask_jwt_extended import jwt_required
from src.controllers.utils import requires_role


app = Blueprint('user', __name__, url_prefix='/users')

def _create_user():
    data = request.get_json(force=True)
    user = User(
        username=data["username"],
        password=data["password"],
        role_id=data["role_id"],
    )
    db.session.add(user)
    db.session.commit()

def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    return [
        {
            'id': user.id, 
            'username': user.username,
            'role': {
                "id": user.role.id,
                "name": user.role.name,
            },
        }
        for user in users
    ]


@app.route('/', methods=['GET', 'POST'])
@jwt_required()
@requires_role('admin')
def list_of_create_user():
    if request.method == 'POST':
        _create_user()
        return {'massage': 'User created successfully'}, HTTPStatus.CREATED
    else:
        return {'users': _list_users()}
    
@app.route('/<int:user_id>')
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return {
            'id': user.id, 
            'username': user.username,
    }

@app.route('/<int:user_id>', methods=["PATCH"])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json


    mapper = inspect(User)
    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])
    db.session.commit()

    return {
            'id': user.id, 
            'username': user.username,
    }

@app.route('/<int:user_id>', methods=["DELETE"])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT
