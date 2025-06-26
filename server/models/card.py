from datetime import datetime, timedelta
from app import db

class KnowledgeCard(db.Model):
    __tablename__ = 'knowledge_cards'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    summary = db.Column(db.Text)
    tags = db.Column(db.String)
    source_link = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    last_reviewed = db.Column(db.DateTime, default=datetime.utcnow)
    next_review_due = db.Column(db.DateTime, default=datetime.utcnow)
    review_score = db.Column(db.Integer, default=0)  # 0–5 scale

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "summary": self.summary,
            "tags": self.tags.split(",") if self.tags else [],
            "source_link": self.source_link,
            "user_id": self.user_id,
            "last_reviewed": self.last_reviewed.isoformat() if self.last_reviewed else None,
            "next_review_due": self.next_review_due.isoformat() if self.next_review_due else None,
            "review_score": self.review_score,
        }
