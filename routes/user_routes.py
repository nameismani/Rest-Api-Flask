from flask import Blueprint, request
from controllers.user_controller import UserController

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/', methods=['GET'])
def get_all_users():
  
    return UserController.get_all_users()

@user_bp.route('/<string:id>', methods=['GET'])
def get_user(id):
    return UserController.get_user(id)

@user_bp.route('/<string:id>', methods=['DELETE'])
def delete_user(id):
    return UserController.delete_user(id)
