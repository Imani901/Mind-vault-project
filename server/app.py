from flask import request, jsonify, Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import Config
import os

load_dotenv()

# Extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # CORS setup with credentials
    CORS(
        app,
        origins=app.config["ALLOWED_ORIGINS"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["Content-Type", "Authorization"],
        supports_credentials=True
    )

    # Handle OPTIONS preflight and CORS headers
    @app.after_request
    def add_cors_headers(response):
        origin = request.headers.get("Origin")
        if origin in app.config["ALLOWED_ORIGINS"]:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
            response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS,PATCH"
        return response

    @app.before_request
    def handle_options():
        if request.method == "OPTIONS":
            response = app.make_default_options_response()
            origin = request.headers.get("Origin")
            if origin in app.config["ALLOWED_ORIGINS"]:
                headers = response.headers
                headers["Access-Control-Allow-Origin"] = origin
                headers["Access-Control-Allow-Credentials"] = "true"
                headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
                headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
            return response

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"error": "Token has expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"error": "Invalid token"}), 422

    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        return jsonify({"error": "Missing token"}), 401

    
   

    # Register API routes
    from routes.auth_routes import Register, Login
    from routes.card_routes import CardDetailResource, CardListResource, PublicCardListResource
    from routes.admin import AdminUserListResource
    from routes.dashboard import DashboardSummaryResource

    api = Api(app)
    api.add_resource(Register, "/register")
    api.add_resource(Login, "/login")
    api.add_resource(CardListResource, "/cards")
    api.add_resource(CardDetailResource, "/cards/<int:card_id>")
    api.add_resource(AdminUserListResource, "/admin/users")
    api.add_resource(DashboardSummaryResource, "/dashboard/summary")
    api.add_resource(PublicCardListResource, "/cards/public")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
