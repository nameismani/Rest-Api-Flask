from flask import Flask, request, jsonify, render_template, redirect, url_for, Response
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from bson.objectid import ObjectId
from resources import Register
from datetime import datetime
from db import get_db
from models.user import User

import os

app = Flask(__name__)
db = get_db()
user_model = User(db)
api = Api(app)

user_args = reqparse.RequestParser()
user_args.add_argument('firstName', type=str, required=True, help="First Name is required!")
user_args.add_argument('lastName', type=str, required=True, help="Last Name is required!")
user_args.add_argument('email', type=str, required=True, help="Email is required!")
user_args.add_argument('password', type=str, required=True, help="Password is required!")
user_args.add_argument('accountType', type=str, default="seeker", help="Account Type (default is 'seeker').")
user_args.add_argument('contact', type=str, help="Contact number (optional).")
user_args.add_argument('location', type=str, help="Location (optional).")
user_args.add_argument('profileUrl', type=str, help="Profile URL (optional).")
user_args.add_argument('cvUrl', type=str, help="CV URL (optional).")
user_args.add_argument('jobTitle', type=str, help="Job Title (optional).")
user_args.add_argument('about', type=str, help="About (optional).")

login_auth_args = reqparse.RequestParser()
login_auth_args.add_argument('email', type=str, required=True, help="Email is required!")
login_auth_args.add_argument('password', type=str, required=True, help="Password is required!")

registration_args = reqparse.RequestParser()
registration_args.add_argument('firstName', type=str, required=True, help="First Name is required")
registration_args.add_argument('lastName', type=str, required=True, help="Last Name is required")
registration_args.add_argument('email', type=str, required=True, help="Email is required")
registration_args.add_argument('password', type=str, required=True, help="Password is required")
registration_args.add_argument('accountType', type=str, default="seeker")
registration_args.add_argument('contact', type=str)
registration_args.add_argument('location', type=str)
registration_args.add_argument('profileUrl', type=str)
registration_args.add_argument('cvUrl', type=str)
registration_args.add_argument('jobTitle', type=str)
registration_args.add_argument('about', type=str)

user_fields = {
    'id': fields.String(attribute="_id"),
    'firstName': fields.String,
    'lastName': fields.String,
    'email': fields.String,
    'accountType': fields.String,
    'contact': fields.String,
    'location': fields.String,
    'profileUrl': fields.String,
    'cvUrl': fields.String,
    'jobTitle': fields.String,
    'about': fields.String,
    # 'createdAt': fields.DateTime,
    # 'updatedAt': fields.DateTime,
    'createdAt': fields.Integer, 
    'updatedAt': fields.Integer,  
}


user_fields_with_token = {
    'id': fields.String(attribute="_id"),
    'firstName': fields.String,
    'lastName': fields.String,
    'email': fields.String,
    'accountType': fields.String,
    'contact': fields.String,
    'location': fields.String,
    'profileUrl': fields.String,
    'cvUrl': fields.String,
    'jobTitle': fields.String,
    'about': fields.String,
     'token': fields.String,
    # 'createdAt': fields.DateTime,
    # 'updatedAt': fields.DateTime,
    'createdAt': fields.Integer, 
    'updatedAt': fields.Integer,  
}

class Users(Resource):
    @marshal_with(user_fields)
    def get(self):
        users = list(user_model.collection.find({}))
        for user in users:
            user['_id'] = str(user['_id'])  # Convert ObjectId to string for JSON serialization
        return users

    @marshal_with(user_fields)
    def post(self):
        args = user_args.parse_args()
        user = user_model.create_user(
            firstName=args['firstName'],
            lastName=args['lastName'],
            email=args['email'],
            password=args['password'],
            account_type=args.get('account_type'),
            contact=args.get('contact'),
            location=args.get('location'),
            profileUrl=args.get('profileUrl'),
            cvUrl=args.get('cv_url'),
            jobTitle=args.get('jobTitle'),
            about=args.get('about')
        )
        created_user = user_model.collection.find_one({"_id": user.inserted_id})
        created_user['_id'] = str(created_user['_id'])
        return 
    

class User(Resource):
    @marshal_with(user_fields)
    def get(self, id):
        user = user_model.collection.find_one({"_id": ObjectId(id)})
        print(user,"fgdfg")
        if not user:
            abort(404, message="User not found")
        user['_id'] = str(user['_id'])
        return user

    @marshal_with(user_fields)
    def patch(self, id):
        args = user_args.parse_args()
        updated_data = {key: value for key, value in args.items() if value is not None}
        updated_data["updated_at"] = datetime.utcnow()
        user_model.collection.update_one({"_id": ObjectId(id)}, {"$set": updated_data})
        updated_user = user_model.collection.find_one({"_id": ObjectId(id)})
        if not updated_user:
            abort(404, message="User not found")
        updated_user['_id'] = str(updated_user['_id'])
        return updated_user

    def delete(self, id):
        result = user_model.collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            abort(404, message="User not found")
        return '', 204


class Login(Resource):
    @marshal_with(user_fields_with_token)
    def post(self):
        args = login_auth_args.parse_args()
        
        # Verify the user's credentials
        user = user_model.verify_user_password(args['email'], args['password'])
        
        if not user:
            abort(401, message="Invalid email or password")
        
        # Generate JWT token
        token = user_model.create_token(user["_id"])

        # Convert `createdAt` and `updatedAt` to Unix timestamps
        # user["createdAt"] = int(user["createdAt"].timestamp())
        # user["updatedAt"] = int(user["updatedAt"].timestamp())
        
        # Add token to the user data for the response
        user["token"] = token

        return user, 200
    
# class Register(Resource):
#     @marshal_with(user_fields_with_token)
#     def post(self):
     
#         args = registration_args.parse_args()
        
#         # Check if the email already exists
#         existing_user = user_model.find_user_by_email(args['email'])
#         if existing_user:
#             abort(400, message="User with this email already exists")

#         # Create the new user in the database
#         new_user_id = user_model.create_user(
#             firstName=args['firstName'],
#             lastName=args['lastName'],
#             email=args['email'],
#             password=args['password'],
#             account_type=args.get('accountType'),
#             contact=args.get('contact'),
#             location=args.get('location'),
#             profileUrl=args.get('profileUrl'),
#             cvUrl=args.get('cvUrl'),
#             jobTitle=args.get('jobTitle'),
#             about=args.get('about')
#         )
        
#         # Retrieve the newly created user data
#         new_user = user_model.collection.find_one({"_id": new_user_id.inserted_id})

#         # Generate JWT token for the new user
#         token = user_model.create_token(new_user["_id"])

#         # Convert `createdAt` and `updatedAt` to Unix timestamps
#         # new_user["createdAt"] = int(new_user["createdAt"].timestamp())
#         # new_user["updatedAt"] = int(new_user["updatedAt"].timestamp())
        
#         # Add token to the user data for the response
#         new_user["token"] = token

#         return new_user, 201
    

# Add resources to the API
api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<string:id>')
api.add_resource(Login, '/api/auth/login')
api.add_resource(Register, '/api/auth/register')



@app.route('/')
def index():
    # items = mongo.db.items.find()
    items = [{'_id':1,'name':"Mani",'description':'Check Flask'},{'_id':2,'name':"Gunal",'description':'Check Loop'}]
    return render_template('index.html', items=items)


# Create Route
@app.route('/create', methods=['POST'])
def create_item():
    name = request.form.get('name')
    description = request.form.get('description')
    print(name,description)
    # if name and description:
    #     mongo.db.items.insert_one({'name': name, 'description': description})
    return redirect(url_for('index'))

# Read Route
@app.route('/item/<id>', methods=['GET'])
def read_item(id):
    # item = mongo.db.items.find_one({"_id": ObjectId(id)})
    item = {'_id':1,'name':"Mani",'description':'Check Flask'}
    if item:
        return jsonify({"id": str(item['_id']), "name": item['name'], "description": item['description']})
    return jsonify({"error": "Item not found"}), 404

# Update Route
@app.route('/update/<id>', methods=['POST'])
def update_item(id):
    name = request.form.get('name')
    description = request.form.get('description')
    print(name,description,id)
    # if name and description:
        # mongo.db.items.update_one({"_id": ObjectId(id)}, {"$set": {"name": name, "description": description}})
    return redirect(url_for('index'))

# Delete Route
@app.route('/delete/<id>', methods=['POST'])
def delete_item(id):
    # mongo.db.items.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)