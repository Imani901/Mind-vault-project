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

        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404

        total_cards = KnowledgeCard.query.filter_by(user_id=user_id).count()
        due_today = KnowledgeCard.query.filter(
            KnowledgeCard.user_id == user_id,
            KnowledgeCard.next_review_due <= now
        ).count()
        overdue = KnowledgeCard.query.filter(
            KnowledgeCard.user_id == user_id,
            KnowledgeCard.next_review_due < now - timedelta(days=1)
        ).count()

        all_tags = [
            tag.strip()
            for card in KnowledgeCard.query.filter_by(user_id=user_id).all()
            for tag in (card.tags or '').split(',')
            if tag
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
