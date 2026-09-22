from db import db
from flask_smorest import abort
import logging
from sqlalchemy import func
from models import UserModel
from flask import jsonify


class CommentModel(db.Model):
    __tablename__ = "Comment"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("Recipe.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    users = db.relationship("UserModel", back_populates="comments")
    recipes = db.relationship("RecipeModel", back_populates="comments")

    def __init__(self, recipe_id, user_id, message):
        self.recipe_id = recipe_id
        self.user_id = user_id
        self.message = message

    def add_comment(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            logging.error(f"Failed to add comment: {str(e)}")
            db.session.rollback()
            raise

    @classmethod
    def get_comment(cls, comment_id):
        comment = cls.query.filter_by(id=comment_id).first()
        if comment is None:
            logging.error(f"comment with id {comment_id} not found.")
            return jsonify({"message": "comment with id {comment_id} not found."}), 404

        return comment

    def update_comment(self, comment_data):
        for key, value in comment_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def user_full_name(self):
        user = UserModel.query.get(self.user_id)  # Fetch user if necessary
        if user:
            return f"{user.first_name} {user.last_name}"
        return None  # Handle cases where user might not exist
