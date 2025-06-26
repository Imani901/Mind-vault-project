from flask import request, jsonify
from flask_restful import Resource
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from models.user import User
from app import db

bcrypt = Bcrypt()

class Register(Resource):
    def options(self):
        return '', 204  # Preflight check

    def post(self):
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return {"error": "Missing required fields"}, 400

        if User.query.filter((User.username == username) | (User.email == email)).first():
            return {"error": "User already exists"}, 409

        user = User(username=username, email=email, role='user')
        user.password = password  
        db.session.add(user)
        db.session.commit()

        token = create_access_token(identity=str(user.id))
        return {
            "user": user.serialize(),
            "token": token
        }, 201



class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return {"error": "Invalid credentials"}, 401  # ✅ plain dict

        access_token = create_access_token(identity=str(user.id))

        return {
            "user": user.serialize(),   # ✅ plain dict
            "token": access_token
        }, 200