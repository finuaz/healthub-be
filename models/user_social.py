from db import db
from flask_smorest import abort
import logging
from sqlalchemy import func
from flask import jsonify


class SocialModel(db.Model):
    __tablename__ = "Socials"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    facebook = db.Column(db.String(255), nullable=True)
    instagram = db.Column(db.String(255), nullable=True)
    tiktok = db.Column(db.String(255), nullable=True)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    users = db.relationship("UserModel", back_populates="socials")

    def __init__(self, user_id, facebook=None, instagram=None, tiktok=None):
        self.user_id = user_id
        self.facebook = facebook
        self.instagram = instagram
        self.tiktok = tiktok

    def add_user_social(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    @classmethod
    def get_user_social(cls, user_id):
        user = cls.query.filter_by(id=user_id).first()
        if user is None:
            logging.error(f"User social with id {user_id} not found.")
            return jsonify({"message": "user social with id {user_id} not found."}), 404
        return user

    def update_user_social(self, platform):
        for key, value in platform.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_user_social(self):
        db.session.delete(self)
        db.session.commit()
