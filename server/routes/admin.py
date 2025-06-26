from flask_restful import Resource
from flask_jwt_extended import jwt_required
from utils.decorators import admin_required
from models.user import User
from flask import jsonify

class AdminUserListResource(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        users = User.query.all()
        return jsonify([user.serialize() for user in users]), 200
