from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

# Flask server created and mongo connection string configured in App
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/python-test'
mongo = PyMongo(app)


@app.route('/users', methods=['POST'])
def create_user():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    if username and password and email:
        hashed_password = generate_password_hash(password)
        print(hashed_password)
        id = mongo.db.users.insert({
            'username': username, "email": email, "password": hashed_password
        })

        response = {
            "id": str(id),
            "username": username,
            "password": hashed_password,
            "email": email
        }
        return response
    else:
        return not_found()

    return {'message': 'received'}


@app.errorhandler(404)
def not_found(error=None):
    response = jsonify(
        {
            "message": "Resource not found: " + request.url,
            "status": 404
        }
    )
    # Asignamos el status a la respuesta. Por defecto Flask envía 200
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(debug=True)
