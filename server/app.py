from flask import request, session, jsonify, Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_bcrypt import Bcrypt
import os

load_dotenv()

# Extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__, static_folder="../client/build", static_url_path="/")
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # CORS for frontend
    CORS(app, 
         supports_credentials=True,
         origins=["https://mind-vault-project-jb298tlj8-imani901s-projects.vercel.app"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
         expose_headers=["Access-Control-Allow-Origin"],
         max_age=600)


    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"error": "Token has expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"error": "Invalid token"}), 422

    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        return jsonify({"error": "Missing token"}), 401
    

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_react(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, "index.html")


    # Flask-RESTful API routes
    from routes.auth_routes import Register, Login
    from routes.card_routes import CardDetailResource, CardListResource
    from routes.admin import AdminUserListResource
    from routes.dashboard import DashboardSummaryResource
    from routes.card_routes import PublicCardListResource

    api = Api(app)

    api.add_resource(Register, "/register")
    api.add_resource(Login, "/login")
    api.add_resource(CardListResource, "/cards")
    api.add_resource(CardDetailResource, "/cards/<int:card_id>/review")
    api.add_resource(AdminUserListResource, "/admin/users")
    api.add_resource(DashboardSummaryResource, "/dashboard/summary")
    api.add_resource(PublicCardListResource, "/cards/public")

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
