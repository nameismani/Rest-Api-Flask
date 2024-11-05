from flask_restful import reqparse

registration_args = reqparse.RequestParser()
registration_args.add_argument('firstName', type=str, required=True, help='First name is required')
registration_args.add_argument('lastName', type=str, required=True, help='Last name is required')
registration_args.add_argument('email', type=str, required=True, help='Email is required')
registration_args.add_argument('password', type=str, required=True, help='Password is required')
registration_args.add_argument('accountType', type=str)
registration_args.add_argument('contact', type=str)
registration_args.add_argument('location', type=str)
registration_args.add_argument('profileUrl', type=str)
registration_args.add_argument('cvUrl', type=str)
registration_args.add_argument('jobTitle', type=str)
registration_args.add_argument('about', type=str)
