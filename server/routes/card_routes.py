from flask import request, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.card import KnowledgeCard
from app import db
from datetime import datetime, timedelta, timezone

class PublicCardListResource(Resource):
    def get(self):
        public_cards = KnowledgeCard.query.filter_by(user_id=None).all()
        return [card.serialize() for card in public_cards], 200


class CardListResource(Resource):
    @jwt_required()
    def get(self):
        try:
            user_id = get_jwt_identity()
            print("🔍 Getting cards for user:", user_id)

            tag_query = request.args.get('tag')
            search_query = request.args.get('q')
            query = KnowledgeCard.query.filter_by(user_id=user_id)

            if tag_query:
                query = query.filter(KnowledgeCard.tags.ilike(f"%{tag_query}%"))
            if search_query:
                query = query.filter(
                    KnowledgeCard.title.ilike(f"%{search_query}%") |
                    KnowledgeCard.summary.ilike(f"%{search_query}%")
                )

            cards = query.all()
            return [card.serialize() for card in cards], 200

        except Exception as e:
            print("❌ Error fetching cards:", e)
            return {"error": "Server error"}, 500

    @jwt_required()
    def post(self):
        try:
            user_id = get_jwt_identity()
            data = request.get_json()
            now = datetime.now(timezone.utc)

            new_card = KnowledgeCard(
                title=data.get("title"),
                summary=data.get("summary"),
                tags=','.join(data.get("tags", [])),
                source_link=data.get("source_link", ""),
                user_id=user_id,
                last_reviewed=now,
                next_review_due=now + timedelta(days=1)
            )

            db.session.add(new_card)
            db.session.commit()
            return new_card.serialize(), 201

        except Exception as e:
            print("❌ Error saving card:", e)
            return {"error": "Failed to save card"}, 500


class CardDetailResource(Resource):
    @jwt_required()
    def patch(self, card_id):
        user_id = get_jwt_identity()
        data = request.get_json()

        card = KnowledgeCard.query.filter_by(id=card_id, user_id=user_id).first()
        if not card:
            return {"error": "Card not found"}, 404

        # Update fields if provided
        if "title" in data:
            card.title = data["title"]
        if "summary" in data:
            card.summary = data["summary"]
        if "tags" in data:
            card.tags = ','.join(data["tags"]) if isinstance(data["tags"], list) else data["tags"]
        if "source_link" in data:
            card.source_link = data["source_link"]

        db.session.commit()
        return card.serialize(), 200

    @jwt_required()
    def delete(self, card_id):
        user_id = get_jwt_identity()
        card = KnowledgeCard.query.filter_by(id=card_id, user_id=user_id).first()
        if not card:
            return {"error": "Card not found"}, 404

        db.session.delete(card)
        db.session.commit()
        return {"message": "Card deleted"}, 200


class CardReviewResource(Resource):
    

    @jwt_required()
    def patch(self, card_id):
        user_id = get_jwt_identity()
        data = request.get_json()
        success = data.get("success", False)

        card = KnowledgeCard.query.filter_by(id=card_id, user_id=user_id).first()
        if not card:
            return {"error": "Card not found"}, 404

        now = datetime.now(timezone.utc)
        card.last_reviewed = now

        if success:
            card.review_score = min(card.review_score + 1, 5)
        else:
            card.review_score = max(card.review_score - 1, 0)

        delay_map = [1, 2, 4, 7, 15, 30]
        card.next_review_due = now + timedelta(days=delay_map[card.review_score])

        db.session.commit()
        return card.serialize(), 200
