from flask_restful import marshal_with, abort
from models.user import User
from fields import user_fields_with_token
from db import get_db

db = get_db()
user_model = User(db)

class AuthController:
    @staticmethod
    @marshal_with(user_fields_with_token)
    def login(email, password):
        user = user_model.verify_user_password(email, password)
        if not user:
            abort(401, message="Invalid email or password")
        token = user_model.create_token(user["_id"])
        user["token"] = token
        return user, 200

    @staticmethod
    @marshal_with(user_fields_with_token)
    def register(user_data):
        existing_user = user_model.find_user_by_email(user_data['email'])
        if existing_user:
            abort(400, message="User with this email already exists")
        new_user_id = user_model.create_user(
            firstName=user_data['firstName'],
            lastName=user_data['lastName'],
            email=user_data['email'],
            password=user_data['password'],
            account_type=user_data.get('accountType'),
            contact=user_data.get('contact'),
            location=user_data.get('location'),
            profileUrl=user_data.get('profileUrl'),
            cvUrl=user_data.get('cvUrl'),
            jobTitle=user_data.get('jobTitle'),
            about=user_data.get('about')
        )
        new_user = user_model.collection.find_one({"_id": new_user_id.inserted_id})
        token = user_model.create_token(new_user["_id"])
        new_user["token"] = token
        return new_user, 201
