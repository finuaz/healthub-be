from db import db
from flask_smorest import abort
import logging
from sqlalchemy import func
from flask import jsonify


class NutritionModel(db.Model):
    __tablename__ = "Nutrition"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("Recipe.id"))
    serving_per_container = db.Column(db.Integer, nullable=True)
    serving_size = db.Column(db.String(20), nullable=True)

    calories = db.Column(db.DECIMAL(10, 2), nullable=True)
    total_fat = db.Column(db.DECIMAL(10, 2), nullable=True)
    total_carbohydrate = db.Column(db.DECIMAL(10, 2), nullable=True)
    total_sugar = db.Column(db.DECIMAL(10, 2), nullable=True)
    cholesterol = db.Column(db.DECIMAL(10, 2), nullable=True)
    protein = db.Column(db.DECIMAL(10, 2), nullable=True)
    vitamin_d = db.Column(db.DECIMAL(10, 2), nullable=True)

    sodium = db.Column(db.DECIMAL(10, 2), nullable=True)
    calcium = db.Column(db.DECIMAL(10, 2), nullable=True)
    potassium = db.Column(db.DECIMAL(10, 2), nullable=True)
    iron = db.Column(db.DECIMAL(10, 2), nullable=True)

    created_at = db.Column(
        db.TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    recipes = db.relationship("RecipeModel", back_populates="nutritions")

    def __init__(
        self,
        recipe_id,
        serving_per_container,
        serving_size,
        calories,
        total_fat,
        total_carbohydrate,
        total_sugar,
        cholesterol,
        protein,
        vitamin_d,
        sodium,
        calcium,
        potassium,
        iron,
    ):
        self.recipe_id = recipe_id
        self.serving_per_container = serving_per_container
        self.serving_size = serving_size
        self.calories = calories
        self.total_fat = total_fat
        self.total_carbohydrate = total_carbohydrate
        self.total_sugar = total_sugar
        self.cholesterol = cholesterol
        self.protein = protein
        self.vitamin_d = vitamin_d
        self.sodium = sodium
        self.calcium = calcium
        self.potassium = potassium
        self.iron = iron

    def add_nutrition(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    @classmethod
    def get_nutrition(cls, nutrition_id):
        nutrition = cls.query.filter_by(id=nutrition_id).first()
        if nutrition is None:
            logging.error(f"nutrition with id {nutrition_id} not found.")
            return (
                jsonify({"message": "nutrition with id {nutrition_id} not found."}),
                404,
            )
        return nutrition

    def update_nutrition(self, nutrition_data):
        for key, value in nutrition_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_nutrition(self):
        db.session.delete(self)
        db.session.commit()
