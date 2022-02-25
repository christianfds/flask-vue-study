from flask import Flask
from blueprints.auth import auth_app
from blueprints.photos import photos_app

app = Flask(__name__)
app.url_map.strict_slashes = False

app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(photos_app, url_prefix='/photos')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
