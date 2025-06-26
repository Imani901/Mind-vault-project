import random
from faker import Faker
from app import create_app, db
from models.user import User
from models.card import KnowledgeCard
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

# Initialize Faker and Flask app
fake = Faker()
app = create_app()

with app.app_context():
    print("🔁 Resetting database...")
    db.drop_all()
    db.create_all()

    # 👥 Create 15 random users
    users = []
    for _ in range(15):
        user = User(
            username=fake.user_name(),
            email=fake.unique.email()
        )
        user.password = "password123"
        db.session.add(user)
        users.append(user)

    # 👑 Create an admin user
    admin = User(
        username="admin",
        email="admin@mindvault.com",
        role="admin"
    )
    admin.password = "adminpass"
    db.session.add(admin)

    db.session.commit()

    # 🧠 Create 70 knowledge cards
    print("🧠 Seeding knowledge cards...")
    for _ in range(70):
        card = KnowledgeCard(
            title=fake.sentence(nb_words=6),
            summary=fake.paragraph(nb_sentences=3),
            tags=','.join(fake.words(nb=3)),
            source_link=fake.url(),
            user_id=random.choice(users).id
        )
        db.session.add(card)
    # Add default cards not tied to any user
    for _ in range(5):
        card = KnowledgeCard(
            title=fake.sentence(),
            summary=fake.paragraph(),
            tags="example,demo",
            source_link=fake.url(),
            user_id=None 
        )
        db.session.add(card)
    

    db.session.commit()
    print("✅ Seeded 15 users, 1 admin, and 70 knowledge cards!")
