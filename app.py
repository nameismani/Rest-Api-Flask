from flask import Flask, render_template
from flask_restful import Api
from db import get_db
from routes.user_routes import user_bp
from routes.auth_routes import auth_bp

app = Flask(__name__)
api = Api(app)
db = get_db()

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(auth_bp, url_prefix='/api/auth')

@app.route('/')
def index():
    items = [{'_id':1,'name':"Mani",'description':'Check Flask'},{'_id':2,'name':"Gunal",'description':'Check Loop'}]
    return render_template('index.html', items=items)

if __name__ == '__main__':
    app.run(debug=True)
