from db import db
from flask_smorest import abort
import logging
from sqlalchemy import func
from flask import jsonify


class RecipeCategoryRelationModel(db.Model):
    __tablename__ = "Recipe_category"

    recipe_id = db.Column(
        db.Integer, db.ForeignKey("Recipe.id"), primary_key=True, nullable=False
    )
    category_id = db.Column(
        db.Integer, db.ForeignKey("Category.id"), primary_key=True, nullable=False
    )
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )

    recipes = db.relationship("RecipeModel", back_populates="recipe_categories")
    categories = db.relationship("CategoryModel", back_populates="recipe_categories")

    def __init__(self, recipe_id, category_id):
        self.recipe_id = recipe_id
        self.category_id = category_id

    def add_recipe_category(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    @classmethod
    def get_recipe_category(cls, recipe_category_id):
        recipe_category = cls.query.filter_by(id=recipe_category_id).first()
        if recipe_category is None:
            logging.error(f"recipe_category with id {recipe_category_id} not found.")
            return (
                jsonify({"message": "category with id {category_id} not found."}),
                404,
            )
        return recipe_category

    def update_recipe_category(self, recipe_category_data):
        for key, value in recipe_category_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_recipe_category(self):
        db.session.delete(self)
        db.session.commit()
