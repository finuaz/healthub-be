from db import db
from flask_smorest import abort
import logging
from sqlalchemy import func
from flask import jsonify


class TagModel(db.Model):
    __tablename__ = "Tag"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tagname = db.Column(db.String(20), nullable=False, unique=True)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    recipe_tags = db.relationship("RecipeTagRelationModel", back_populates="tags")

    def __init__(self, tagname):
        self.tagname = tagname

    def add_tag(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    @classmethod
    def get_tag(cls, tag_id):
        tag = cls.query.filter_by(id=tag_id).first()
        if tag is None:
            logging.error(f"tag with id {tag_id} not found.")
            return jsonify({"message": "tag with id {tag_id} not found."}), 404
        return tag

    def update_tag(self, tag_data):
        for key, value in tag_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_tag(self):
        db.session.delete(self)
        db.session.commit()
