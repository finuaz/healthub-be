import logging

from flask.views import MethodView
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify, current_app
from sqlalchemy import desc
from extensions import cache
from db import db

from models import (
    RecipeModel,
    UserModel,
    LikeModel,
    FollowingModel,
    UserRole,
)
from schemas import RecipePlusPlusSchema, UserGetProfileSchema
from utils import (
    enrich_recipes,
    count_follower,
    count_following,
)

logging.basicConfig(level=logging.INFO)

blp = Blueprint("collections", __name__, description="Operations on collections")


@blp.route("/collection/recipes/self-created")
class GetAllSelfCreatedRecipes(MethodView):

    @blp.response(200, RecipePlusPlusSchema(many=True))
    # @cache.cached(timeout=60 / 2)
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()["id"]

        try:
            recipes = (
                RecipeModel.query.filter_by(author_id=current_user_id)
                .order_by(desc(RecipeModel.nutriscore), RecipeModel.id)
                .all()
            )

            if not recipes:
                return jsonify({"message": "You have not created any recipe yet"}), 404

            enrich_recipes(recipes)

            serialized_recipes = RecipePlusPlusSchema(many=True).dump(recipes)
            return jsonify(serialized_recipes), 200

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/collection/recipes/creator/<int:author_id>")
class GetAllRecipesCreatedByUser(MethodView):

    @blp.response(200, RecipePlusPlusSchema(many=True))
    # @cache.cached(timeout=60 / 2)
    # @jwt_required()
    def get(self, author_id):

        try:
            recipes = (
                RecipeModel.query.filter_by(author_id=author_id)
                .order_by(desc(RecipeModel.nutriscore), RecipeModel.id)
                .all()
            )

            if not recipes:
                return jsonify({"message": "The user has not created any recipe"}), 404

            enrich_recipes(recipes)

            serialized_recipes = RecipePlusPlusSchema(many=True).dump(recipes)
            return jsonify(serialized_recipes), 200

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/collection/recipes/creator/<string:author_name_in_search>")
class GetAllRecipesCreatedByUser(MethodView):

    @blp.response(200, RecipePlusPlusSchema(many=True))
    # @cache.cached(timeout=60 / 2)
    # @jwt_required()
    def get(self, author_name_in_search):
        user = UserModel.query.filter_by(first_name=author_name_in_search).first()

        if not user:
            user = UserModel.query.filter_by(last_name=author_name_in_search).first()

            if not user:
                user = UserModel.query.filter_by(username=author_name_in_search).first()

                if not user:
                    abort(404, message="The user is not found")

        try:
            recipes = (
                RecipeModel.query.filter_by(author_id=user.id)
                .order_by(desc(RecipeModel.nutriscore), RecipeModel.id)
                .all()
            )

            if not recipes:
                return jsonify({"message": "The user has not created any recipe"}), 404

            enrich_recipes(recipes)

            serialized_recipes = RecipePlusPlusSchema(many=True).dump(recipes)
            return jsonify(serialized_recipes), 200

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/collection/recipes/liked")
class GetAllLikedRecipes(MethodView):

    @blp.response(200, RecipePlusPlusSchema(many=True))
    # @cache.cached(timeout=60 / 2)
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()["id"]

        try:
            liked_recipe_ids = [
                liked_recipe.recipe_id
                for liked_recipe in LikeModel.query.filter_by(
                    user_id=current_user_id
                ).all()
            ]

            if not liked_recipe_ids:
                return jsonify({"message": "You have not liked any recipes yet"}), 404

            recipes = (
                RecipeModel.query.filter(RecipeModel.id.in_(liked_recipe_ids))
                .order_by(desc(RecipeModel.nutriscore), RecipeModel.id)
                .all()
            )

            enrich_recipes(recipes)

            serialized_recipes = RecipePlusPlusSchema(many=True).dump(recipes)
            return jsonify(serialized_recipes), 200

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/collection/recipes/followed")
class GetAllRecipesFromFollowedUser(MethodView):

    @blp.response(200, RecipePlusPlusSchema(many=True))
    # @cache.cached(timeout=60 / 2)
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()["id"]

        try:
            followed_user_ids = db.session.query(FollowingModel.followed_id).filter(
                FollowingModel.follower_id == current_user_id
            )

            recipes = (
                RecipeModel.query.filter(RecipeModel.author_id.in_(followed_user_ids))
                .order_by(desc(RecipeModel.nutriscore), RecipeModel.id)
                .all()
            )

            if not recipes:
                return (
                    jsonify(
                        {
                            "message": "No recipes have been created by the users "
                            "you follow"
                        }
                    ),
                    404,
                )

            enrich_recipes(recipes)

            serialized_recipes = RecipePlusPlusSchema(many=True).dump(recipes)
            return jsonify(serialized_recipes), 200

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/collection/recipes/creator/chef")
class GetAllRecipesCreatedByChef(MethodView):

    @blp.response(200, RecipePlusPlusSchema(many=True))
    # @cache.cached(timeout=60 / 2)
    @jwt_required()
    def get(self):
        try:
            chef_ids = [
                chef.id for chef in UserModel.query.filter_by(role=UserRole.CHEF).all()
            ]

            if not chef_ids:
                return jsonify({"message": "There is no chef here"}), 404

            recipes = (
                RecipeModel.query.filter(RecipeModel.author_id.in_(chef_ids))
                .order_by(desc(RecipeModel.nutriscore), RecipeModel.id)
                .all()
            )

            if not recipes:
                return jsonify({"message": "Chefs have not created any recipe yet"}), 404

            enrich_recipes(recipes)

            serialized_recipes = RecipePlusPlusSchema(many=True).dump(recipes)
            return jsonify(serialized_recipes), 200

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/collection/list/user-followers")
class GetAllUserFollowers(MethodView):

    @blp.response(200, UserGetProfileSchema(many=True))
    # @cache.cached(timeout=60 / 2)
    @jwt_required()
    def get(self):
        try:
            current_user_id = get_jwt_identity()["id"]

            followers = FollowingModel.query.filter_by(
                followed_id=current_user_id
            ).all()

            if not followers:
                abort(404, message="You have no any follower")

            users = []

            for follower in followers:
                user = UserModel.query.filter_by(id=follower.follower_id).first()
                if user:
                    user.total_following = count_following(user.id)
                    user.total_follower = count_follower(user.id)
                    users.append(user)

            serialized_user = UserGetProfileSchema(many=True).dump(users)
            return jsonify(serialized_user), 200
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/collection/list/followed-users")
class GetAllFollowedUsers(MethodView):

    @blp.response(200, UserGetProfileSchema(many=True))
    # @cache.cached(timeout=60 / 2)
    @jwt_required()
    def get(self):
        try:
            current_user_id = get_jwt_identity()["id"]

            followed_users = FollowingModel.query.filter_by(
                follower_id=current_user_id
            ).all()

            if not followed_users:
                return jsonify({"message": "You have not following any user yet"}), 404

            users = []

            for followed_user in followed_users:
                user = UserModel.query.filter_by(id=followed_user.followed_id).first()
                if user:
                    user.total_following = count_following(user.id)
                    user.total_follower = count_follower(user.id)
                    users.append(user)

            serialized_user = UserGetProfileSchema(many=True).dump(users)
            return jsonify(serialized_user), 200
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")
