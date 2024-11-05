from flask import Blueprint, request
from controllers.auth_controller import AuthController
from flask_restful import reqparse

auth_bp = Blueprint('auth_bp', __name__)

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str, required=True, help="Email is required")
login_parser.add_argument('password', type=str, required=True, help="Password is required")

register_parser = reqparse.RequestParser()
register_parser.add_argument('firstName', type=str, required=True, help="First Name is required")
register_parser.add_argument('lastName', type=str, required=True, help="Last Name is required")
register_parser.add_argument('email', type=str, required=True, help="Email is required")
register_parser.add_argument('password', type=str, required=True, help="Password is required")
register_parser.add_argument('accountType', type=str, default="seeker")
# Add other arguments as needed...

@auth_bp.route('/login', methods=['POST'])
def login():
    args = login_parser.parse_args()
    return AuthController.login(args['email'], args['password'])

@auth_bp.route('/register', methods=['POST'])
def register():
    args = register_parser.parse_args()
    user_data = {
        'firstName': args['firstName'],
        'lastName': args['lastName'],
        'email': args['email'],
        'password': args['password'],
        'accountType': args.get('accountType'),
        # Include other fields here
    }
    return AuthController.register(user_data)
