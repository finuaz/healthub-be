import logging

from flask.views import MethodView
from flask_jwt_extended import (
    get_jwt,
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
    jwt_required,
)
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import func, select, update
from sqlalchemy.orm import selectinload
from flask import jsonify, current_app
from passlib.hash import pbkdf2_sha512
from extensions import cache
from db import db
from werkzeug.exceptions import Forbidden

from models import UserModel, UserRole, FollowingModel, SocialModel, RecipeModel
from schemas import (
    UserRegisterSchema,
    UserLoginSchema,
    UserPublicProfileSchema,
    UserGetProfileSchema,
    UserProfileDetailSchema,
    UserListSchema,
    UserUpdateInfoSchema,
    UserUpdateImageSchema,
    UserResetPasswordSchema,
    UserDeletionSchema,
    GetResetPasswordPackage,
)
from utils import (
    count_following,
    count_follower,
    get_social_facebook,
    get_social_instagram,
    get_social_tiktok,
    serialize_user_list,
)

logging.basicConfig(level=logging.INFO)

blp = Blueprint("users", __name__, description="Operations on users")

@blp.route("/health-check")
class HealthCheck(MethodView):
    @blp.response(200)
    def get(self):
        return {"status": "fix user_id type"}

@blp.route("/users/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    @blp.response(201, UserRegisterSchema)
    def post(self, user_data):
        email_existing = UserModel.query.filter_by(email=user_data["email"]).first()
        if email_existing:
            return (
                jsonify({"message": "The email has been used"}),
                409,
            )

        username_existing = UserModel.query.filter_by(
            username=user_data["username"]
        ).first()
        if username_existing:
            return (
                jsonify({"message": "The username has been used"}),
                409,
            )

        try:
            hashed_password = pbkdf2_sha512.hash(user_data["password"])
            user = UserModel(
                username=user_data["username"],
                email=user_data["email"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                reset_password_question=user_data["reset_password_question"],
                reset_password_answer=user_data["reset_password_answer"],
                password=hashed_password,
                role=None,
            )

            user.add_user()

        except IntegrityError:
            abort(400, message="User with that email already exists")
        except ValueError as e:
            abort(400, message=str(e))
        except SQLAlchemyError as e:
            abort(500, message=f"An error occurred while creating the user: {str(e)}")
        return user


@blp.route("/users/login")
class UserLogin(MethodView):

    @blp.arguments(UserLoginSchema)
    def post(self, user_data):
        username_or_email = user_data.get("username_or_email")
        password = user_data.get("password")

        if username_or_email is None:
            return (
                jsonify({"message": "Username or email is required"}),
                400,
            )

        if UserModel.is_valid_email(username_or_email):
            user = UserModel.query.filter_by(email=username_or_email).first()
        else:
            user = UserModel.query.filter_by(username=username_or_email).first()

        if user and pbkdf2_sha512.verify(password, user.password):

            role = user.role.serialize() if user.role else None

            access_token = create_access_token(
                identity={
                    "id": str(user.id),
                    "username": user.username,
                    "email": user.email,
                    "role": role,
                },
                fresh=True,
            )
            refresh_token = create_refresh_token(
                identity={
                    "id": str(user.id),
                    "username": user.username,
                    "email": user.email,
                    "role": role,
                },
            )
            return {
                "message": "you are successfully login",
                "token": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
            }, 200

        else:
            abort(401, "Invalid Credentials")


@blp.route("/users")
class GetAllUsers(MethodView):
    @blp.response(200, UserListSchema(many=True))
    def get(self):
        try:
            users = UserModel.query.order_by(UserModel.id.asc()).all()
            return jsonify(serialize_user_list(users)), 200
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/users/chefs")
class GetAllChefs(MethodView):
    @blp.response(200, UserListSchema(many=True))
    def get(self):
        try:
            chefs = (
                UserModel.query.filter_by(role=UserRole.CHEF)
                .order_by(UserModel.id.asc())
                .all()
            )
            return jsonify(serialize_user_list(chefs)), 200
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/users/profile")
class UserGetOwnProfile(MethodView):

    @jwt_required()
    @blp.response(200, UserGetProfileSchema)
    # @cache.cached(timeout=60)
    def get(self):

        try:
            current_user_id = int(get_jwt_identity()["id"])
            user = UserModel.query.filter_by(id=current_user_id).first()
            if not user:
                return (
                    jsonify({"message": "The user is not found"}),
                    404,
                )

            user.total_following = count_following(user.id)
            user.total_follower = count_follower(user.id)

            user.social_facebook = get_social_facebook(user.id)
            user.social_instagram = get_social_instagram(user.id)
            user.social_tiktok = get_social_tiktok(user.id)

            serialized_user = UserGetProfileSchema().dump(user)
            return jsonify(serialized_user), 200
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


def _fetch_profile_row(user_id=None, username=None):
    following_count = (
        select(func.count(FollowingModel.id))
        .where(FollowingModel.follower_id == UserModel.id)
        .correlate(UserModel)
        .scalar_subquery()
    )
    follower_count = (
        select(func.count(FollowingModel.id))
        .where(FollowingModel.followed_id == UserModel.id)
        .correlate(UserModel)
        .scalar_subquery()
    )
    recipe_count = (
        select(func.count(RecipeModel.id))
        .where(RecipeModel.author_id == UserModel.id)
        .correlate(UserModel)
        .scalar_subquery()
    )

    query = (
        select(
            UserModel,
            following_count.label("total_following"),
            follower_count.label("total_follower"),
            recipe_count.label("total_recipe_count"),
        )
        .options(selectinload(UserModel.socials))
    )

    if user_id is not None:
        query = query.where(UserModel.id == user_id)
    else:
        query = query.where(UserModel.username == username)

    return db.session.execute(query).first()


def _build_profile_payload(row, view_count, updated_at):
    user, total_following, total_follower, total_recipe_count = row
    social = min(user.socials, key=lambda item: item.id) if user.socials else None

    return {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "image": user.image,
        "role": user.role,
        "bio": user.bio,
        "location": user.location,
        "total_following": total_following,
        "total_follower": total_follower,
        "total_recipe_count": total_recipe_count,
        "view_count": view_count,
        "social_facebook": social.facebook if social else None,
        "social_instagram": social.instagram if social else None,
        "social_tiktok": social.tiktok if social else None,
        "created_at": user.created_at,
        "updated_at": updated_at,
    }


def _increment_view_count(user_id):
    return db.session.execute(
        update(UserModel)
        .where(UserModel.id == user_id)
        .values(view_count=func.coalesce(UserModel.view_count, 0) + 1)
        .returning(UserModel.view_count, UserModel.updated_at)
        .execution_options(synchronize_session=False)
    ).one()


@blp.route("/users/<string:username_in_search>")
class GetProfileByUsername(MethodView):

    @blp.response(200, schema=UserPublicProfileSchema)
    def get(self, username_in_search):
        try:
            row = _fetch_profile_row(username=username_in_search)

            if not row:
                return jsonify({"message": "The user is not found"}), 404

            view_count, updated_at = _increment_view_count(row[0].id)
            profile = _build_profile_payload(row, view_count, updated_at)

            serialized_user = UserPublicProfileSchema().dump(profile)
            db.session.commit()
            return jsonify(serialized_user), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/users/<int:user_id_in_search>")
class GetProfileById(MethodView):

    @blp.response(200, schema=UserProfileDetailSchema)
    def get(self, user_id_in_search):
        try:
            row = _fetch_profile_row(user_id=user_id_in_search)

            if not row:
                return jsonify({"message": "The user is not found"}), 404

            view_count, updated_at = _increment_view_count(user_id_in_search)
            profile = _build_profile_payload(row, view_count, updated_at)

            serialized_user = UserProfileDetailSchema().dump(profile)
            db.session.commit()
            return jsonify(serialized_user), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/users/update-info")
class UserUpdateInfo(MethodView):
    @jwt_required()
    @blp.arguments(UserUpdateInfoSchema)
    @blp.response(201, UserUpdateInfoSchema)
    def put(self, user_data):

        try:
            user_id = get_jwt_identity()["id"]

            user = UserModel.query.filter_by(id=user_id).first()

            user.update_user(user_data)

            return UserUpdateInfoSchema().dump(user), 200

        except Forbidden as e:
            abort(403, description=str(e))

        except Exception as e:
            abort(500, description=f"Failed to update user information: {str(e)}")


@blp.route("/users/update-image")
class UserUpdateImage(MethodView):

    @jwt_required()
    @blp.arguments(UserUpdateImageSchema)
    @blp.response(201, UserUpdateImageSchema)
    def put(self, user_data):
        try:
            user_id = get_jwt_identity()["id"]

            user = UserModel.query.filter_by(id=user_id).first()

            user.update_user(user_data)

            return UserUpdateImageSchema().dump(user), 200

        except Forbidden as e:
            abort(403, description=str(e))

        except Exception as e:
            abort(500, description=f"Failed to update user information: {str(e)}")


@blp.route("/users/reset-password/question")
class UserResetPassword(MethodView):

    @jwt_required()
    @blp.response(200, GetResetPasswordPackage)
    def get(self):
        user_id = get_jwt_identity()["id"]

        user = UserModel.query.filter_by(id=user_id).first()
        question = user.reset_password_question

        user.id = user_id
        user.reset_password_question = question

        serialized_question = GetResetPasswordPackage().dump(user)
        return jsonify(serialized_question), 200


@blp.route("/users/reset-password")
class UserResetPassword(MethodView):

    @jwt_required()
    @blp.arguments(UserResetPasswordSchema)
    @blp.response(200, UserResetPasswordSchema)
    def put(self, user_data):
        user_id = get_jwt_identity()["id"]

        user = UserModel.query.filter_by(id=user_id).first()

        # Verify current password before proceeding with the reset
        if user and pbkdf2_sha512.verify(user_data["password"], user.password):
            if user.reset_password_answer == user_data["reset_password_answer"]:
                try:
                    # Update user's password with the new password
                    user.update_password(pbkdf2_sha512.hash(user_data["new_password"]))

                    return UserResetPasswordSchema().dump(user), 200

                except Forbidden as fe:
                    abort(403, description=str(fe))

                except Exception as e:
                    abort(500, description=f"Failed to reset user's password: {str(e)}")
            else:
                return (
                    jsonify({"message", "Incorrect reset password answer"}),
                    400,
                )
        else:
            return (
                jsonify({"message", "Incorrect curent password"}),
                400,
            )


@blp.route("/users/delete")
class UserDelete(MethodView):

    @jwt_required()
    @blp.arguments(UserDeletionSchema)
    @blp.response(204, "your user has been deleted")
    def delete(self, user_data):

        user_id = get_jwt_identity()["id"]

        user = UserModel.query.filter_by(id=user_id).first()

        if user and pbkdf2_sha512.verify(user_data["password"], user.password):
            try:

                SocialModel.query.filter_by(user_id=user_id).delete()
                FollowingModel.query.filter_by(follower_id=user_id).delete()
                FollowingModel.query.filter_by(followed_id=user_id).delete()
                user.delete_user()
                return jsonify({"message": "your user has been deleted"}), 200

            except Forbidden as fe:
                abort(403, description=str(fe))

            except Exception as e:
                abort(500, description=f"Failed to delete user: {str(e)}")


def get_user_id():
    jwt = get_jwt()
    return jwt.get("sub").get("id")
