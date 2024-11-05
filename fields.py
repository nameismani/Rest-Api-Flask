from flask_restful import fields

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
    'createdAt': fields.DateTime,
    'updatedAt': fields.DateTime,
}

user_fields_with_token = user_fields.copy()
user_fields_with_token.update({'token': fields.String})
