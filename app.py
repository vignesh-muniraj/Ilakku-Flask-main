from flask import Flask
from flask_cors import CORS
from extensions import db, jwt
from routes.users_bp import users_bp
from routes.posts_bp import posts_bp
from os import environ

app = Flask(__name__)
app.config.from_object("config.Config")

# Enable CORS for all origins (development)
# CORS(app, supports_credentials=True)
CORS(posts_bp, origins=["http://localhost:5173"])
# Initialize DB and JWT
db.init_app(app)
jwt.init_app(app)

# JWT error handlers
@jwt.unauthorized_loader
def _unauth(e):
    return {"error": "missing/invalid token"}, 401

@jwt.expired_token_loader
def _expired(h, p):
    return {"error": "token expired"}, 401

# Register blueprints
app.register_blueprint(users_bp, url_prefix="/api/users")
app.register_blueprint(posts_bp, url_prefix="/api/posts")

if __name__ == "__main__":
    port = int(environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
