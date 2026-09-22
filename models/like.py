from db import db
from flask_smorest import abort
import logging
from sqlalchemy import func
from flask import jsonify


class LikeModel(db.Model):
    __tablename__ = "Like"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    recipe_id = db.Column(db.Integer, db.ForeignKey("Recipe.id"))
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    users = db.relationship("UserModel", back_populates="likes")
    recipes = db.relationship("RecipeModel", back_populates="likes")

    def __init__(self, user_id, recipe_id):
        self.user_id = user_id
        self.recipe_id = recipe_id

    def add_like(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    @classmethod
    def get_like(cls, like_id):
        like = cls.query.filter_by(id=like_id).first()
        if like is None:
            logging.error(f"like with id {like_id} not found.")
            return jsonify({"message": "like with id {like_id} not found."}), 404
        return like

    def update_like(self, like_data):
        for key, value in like_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_like(self):
        db.session.delete(self)
        db.session.commit()
