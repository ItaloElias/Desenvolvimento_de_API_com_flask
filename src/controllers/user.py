from flask import Blueprint, request 
from src.app import User, db
from http import HTTPStatus


app = Blueprint('user', __name__, url_prefix='/users')

def _create_user():
    data = request.json
    user = User(username=data["username"])
    db.session.add(user)
    db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'POST':
        _create_user()
        return {'massage': 'User created successfully'}, HTTPStatus.CREATED
    else:
        return {'users': []}
