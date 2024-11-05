from flask_restful import Resource, abort, marshal_with
from models.user import User
from fields import user_fields_with_token
from args import registration_args
from db import get_db

db = get_db()
user_model = User(db)

class Register(Resource):
    @marshal_with(user_fields_with_token)
    def post(self):
        args = registration_args.parse_args()
        
        # Check if the email already exists
        existing_user = user_model.find_user_by_email(args['email'])
        if existing_user:
            abort(400, message="User with this email already exists")

        # Create the new user in the database
        new_user_id = user_model.create_user(
            firstName=args['firstName'],
            lastName=args['lastName'],
            email=args['email'],
            password=args['password'],
            account_type=args.get('accountType'),
            contact=args.get('contact'),
            location=args.get('location'),
            profileUrl=args.get('profileUrl'),
            cvUrl=args.get('cvUrl'),
            jobTitle=args.get('jobTitle'),
            about=args.get('about')
        )
        
        # Retrieve the newly created user data
        new_user = user_model.collection.find_one({"_id": new_user_id.inserted_id})

        # Generate JWT token for the new user
        token = user_model.create_token(str(new_user_id.inserted_id))

        # Add token to the user data for the response
        new_user["token"] = token

        return new_user, 201
