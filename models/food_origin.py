from db import db
from flask_smorest import abort
import logging
from sqlalchemy import func
from flask import jsonify


class OriginModel(db.Model):
    __tablename__ = "Origin"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    origin = db.Column(db.String(20), nullable=False, unique=True)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    recipe_origins = db.relationship(
        "RecipeOriginRelationModel", back_populates="origins"
    )

    def __init__(self, origin):
        self.origin = origin

    def add_origin(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    @classmethod
    def get_origin(cls, origin_id):
        origin = cls.query.filter_by(id=origin_id).first()
        if origin is None:
            logging.error(f"origin with id {origin_id} not found.")
            return jsonify({"message": "origin with id {origin_id} not found."}), 404
        return origin

    def update_origin(self, origin_data):
        for key, value in origin_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_origin(self):
        db.session.delete(self)
        db.session.commit()
