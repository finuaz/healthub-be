from db import db
from flask_smorest import abort
import logging
from sqlalchemy import func
from flask import jsonify


class RecipeTagRelationModel(db.Model):
    __tablename__ = "Recipe_tag"

    recipe_id = db.Column(
        db.Integer, db.ForeignKey("Recipe.id"), primary_key=True, nullable=False
    )
    tag_id = db.Column(
        db.Integer, db.ForeignKey("Tag.id"), primary_key=True, nullable=False
    )
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )

    recipes = db.relationship("RecipeModel", back_populates="recipe_tags")
    tags = db.relationship("TagModel", back_populates="recipe_tags")

    def __init__(self, recipe_id, tag_id):
        self.recipe_id = recipe_id
        self.tag_id = tag_id

    def add_recipe_tag(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    @classmethod
    def get_recipe_tag(cls, recipe_tag_id):
        recipe_tag = cls.query.filter_by(id=recipe_tag_id).first()
        if recipe_tag is None:
            logging.error(f"recipe_tag with id {recipe_tag_id} not found.")
            return (
                jsonify({"message": "recipe tag with id {recipe_tag_id} not found."}),
                404,
            )
        return recipe_tag

    def update_recipe_tag(self, recipe_tag_data):
        for key, value in recipe_tag_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_recipe_tag(self):
        db.session.delete(self)
        db.session.commit()
