from app import db
from flask_bcrypt import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    role = db.Column(db.String, default='user')  # 'user' or 'admin'

    # One-to-many: A user has many knowledge cards
    cards = db.relationship("KnowledgeCard", backref="user", lazy=True)

    # Write-only password property
    @property
    def password(self):
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password).decode("utf-8")

    # Check a password
    def check_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)

    # Check if user is an admin
    def is_admin(self):
        return self.role == "admin"

    # Serialize user data for JSON responses
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role
        }

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"
