from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

# Helper functions

def hash_password(password):
    """Hash the password using bcrypt."""
    return generate_password_hash(password)

def verify_password(password, hashed):
    """Verify if the password matches the hash."""
    return check_password_hash(hashed, password)

def create_jwt(user_id):
    """Generate a JWT token for the user."""
    payload = {
        "user_id": str(user_id),
        "exp": datetime.utcnow() + timedelta(days=1)  # Token expires in 1 day
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")


class User:
    def __init__(self, db):
        self.collection = db.users  # MongoDB collection for users

    def create_user(self, firstName, lastName, email, password, **kwargs):
        """Create a new user in MongoDB with hashed password."""
        hashed_password = hash_password(password)
        current_timestamp = int(datetime.utcnow().timestamp())
        user_data = {
            "firstName": firstName,
            "lastName": lastName,
            "email": email,
            "password": hashed_password,
            "accountType": kwargs.get("accountType", "seeker"),
            "contact": kwargs.get("contact"),
            "location": kwargs.get("location"),
            "profileUrl": kwargs.get("profileUrl"),
            "cvUrl": kwargs.get("cvUrl"),
            "jobTitle": kwargs.get("jobTitle"),
            "about": kwargs.get("about"),
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow(),
            # "createdAt": current_timestamp,
            # "updatedAt": current_timestamp,
        }
        return self.collection.insert_one(user_data)

    def find_user_by_email(self, email):
        """Find a user by email."""
        return self.collection.find_one({"email": email})

    def verify_user_password(self, email, password):
        """Verify the user's password."""
        user = self.find_user_by_email(email)
        if user and verify_password(password, user["password"]):
            return user
        return None

    def create_token(self, user_id):
        """Create a JWT token for the user."""
        return create_jwt(user_id)
