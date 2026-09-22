from db import db
from flask_smorest import abort
import logging
from sqlalchemy import func
from flask import jsonify


class TypeModel(db.Model):
    __tablename__ = "Type"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(20), nullable=False, unique=True)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    recipe_types = db.relationship("RecipeTypeRelationModel", back_populates="types")

    def __init__(self, type):
        self.type = type

    def add_type(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    @classmethod
    def get_type(cls, type_id):
        type = cls.query.filter_by(id=type_id).first()
        if type is None:
            logging.error(f"type with id {type_id} not found.")
            return jsonify({"message": "type with id {type_id} not found."}), 404
        return type

    def update_type(self, type_data):
        for key, value in type_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_type(self):
        db.session.delete(self)
        db.session.commit()
