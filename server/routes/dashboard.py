from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.card import KnowledgeCard
from collections import Counter
from datetime import datetime, timedelta, timezone
from models.user import User

class DashboardSummaryResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        now = datetime.now(timezone.utc)
        today = now.date()

        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404

        # Fetch all cards for the user (optimization optional)
        cards = KnowledgeCard.query.filter_by(user_id=user_id).all()

        total_cards = len(cards)
        due_today = sum(1 for c in cards if c.next_review_due and c.next_review_due.date() == today)
        overdue = sum(1 for c in cards if c.next_review_due and c.next_review_due.date() < today)

        # Extract and count tags
        all_tags = [
            tag.strip()
            for card in cards
            for tag in (card.tags or '').split(',')
            if tag.strip()
        ]
        top_tags = [tag for tag, _ in Counter(all_tags).most_common(3)]

        return {
            "user": {
                "username": user.username,
                "email": user.email,
                "role": user.role
            },
            "total_cards": total_cards,
            "due_today": due_today,
            "overdue": overdue,
            "top_tags": top_tags
        }, 200

