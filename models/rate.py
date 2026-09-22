from db import db
from flask_smorest import abort
import logging
from sqlalchemy import func
from flask import jsonify


class RateModel(db.Model):
    __tablename__ = "Rate"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    recipe_id = db.Column(db.Integer, db.ForeignKey("Recipe.id"))
    value = db.Column(db.Integer, nullable=False)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    users = db.relationship("UserModel", back_populates="rates")
    recipes = db.relationship("RecipeModel", back_populates="rates")

    def __init__(self, user_id, recipe_id, value):
        self.user_id = user_id
        self.recipe_id = recipe_id
        self.value = value

    def add_rate(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    @classmethod
    def get_rate(cls, rate_id):
        rate = cls.query.filter_by(id=rate_id).first()
        if rate is None:
            logging.error(f"rate with id {rate_id} not found.")
            return jsonify({"message": "rate with id {rate_id} not found."}), 404
        return rate

    def update_rate(self, rate_data):
        for key, value in rate_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_rate(self):
        db.session.delete(self)
        db.session.commit()
