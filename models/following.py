from db import db
from flask_smorest import abort
import logging
from sqlalchemy import func
from flask import jsonify


class FollowingModel(db.Model):
    __tablename__ = "Following"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    follower_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    follower_users = db.relationship(
        "UserModel",
        back_populates="follower",
        foreign_keys="[FollowingModel.follower_id]",
    )
    followed_users = db.relationship(
        "UserModel",
        back_populates="followed",
        foreign_keys="[FollowingModel.followed_id]",
    )

    def __init__(self, follower_id, followed_id):
        self.follower_id = follower_id
        self.followed_id = followed_id

    def add_following(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            logging.error(f"Failed to add following: {str(e)}")
            db.session.rollback()
            raise

    @classmethod
    def get_following(cls, following_id):
        following = cls.query.filter_by(id=following_id).first()
        if following is None:
            logging.error(f"following with id {following_id} not found.")
            return (
                jsonify({"message": "following with id {following_id} not found."}),
                404,
            )
        return following

    def update_following(self, following_data):
        for key, value in following_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_following(self):
        db.session.delete(self)
        db.session.commit()
