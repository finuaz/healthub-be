from db import db
from flask_smorest import abort
import logging
from sqlalchemy import func
from flask import jsonify


class IngredientModel(db.Model):
    __tablename__ = "Ingredient"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ingredient = db.Column(db.Text, nullable=False)
    ingredient_image = db.Column(db.String, nullable=True)

    created_at = db.Column(
        db.TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    recipe_ingredients = db.relationship(
        "RecipeIngredientRelationModel", back_populates="ingredients"
    )

    def __init__(
        self,
        ingredient,
        ingredient_image=None,
    ):
        self.ingredient = ingredient
        self.ingredient_image = ingredient_image

    def add_ingredient(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    @classmethod
    def get_ingredient(cls, ingredient_id):
        ingredient = cls.query.filter_by(id=ingredient_id).first()
        if ingredient is None:
            logging.error(f"ingredient with id {ingredient_id} not found.")
            return (
                jsonify({"message": "ingredient with id {ingredient_id} not found."}),
                404,
            )
        return ingredient

    def update_ingredient(self, ingredient_data):
        for key, value in ingredient_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_ingredient(self):
        db.session.delete(self)
        db.session.commit()
