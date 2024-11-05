from flask_restful import marshal_with, abort
from flask import jsonify
from bson.objectid import ObjectId
from models.user import User
from datetime import datetime
from fields import user_fields
from db import get_db

db = get_db()
user_model = User(db)

class UserController:
    @staticmethod
    @marshal_with(user_fields)
    def get_all_users():
        users = list(user_model.collection.find({}))
        for user in users:
            user['_id'] = str(user['_id'])
        return users ,200

    @staticmethod
    @marshal_with(user_fields)
    def get_user(id):
        user = user_model.collection.find_one({"_id": ObjectId(id)})
        if not user:
            abort(404, message="User not found")
        user['_id'] = str(user['_id'])
        return user

    @staticmethod
    def delete_user(id):
        result = user_model.collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            abort(404, message="User not found")
        return '', 204
