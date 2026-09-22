import logging

from flask.views import MethodView
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask import jsonify

from models import RecipeModel, LikeModel
from schemas import (
    LikeSchema,
)

logging.basicConfig(level=logging.INFO)

blp = Blueprint("likes", __name__, description="Operations on likes")


@blp.route("/recipes/like/<int:recipe_in_search>")
class RecipeLike(MethodView):
    @blp.response(201, LikeSchema)
    @jwt_required()
    def post(self, recipe_in_search):
        try:
            current_user_id = get_jwt_identity()["id"]

            recipe = RecipeModel.query.get(recipe_in_search)

            if recipe.author_id == current_user_id:
                return jsonify({"message": "you cannot like your own recipe"}), 403

            like = LikeModel(recipe_id=recipe_in_search, user_id=current_user_id)

            like.add_like()

            return jsonify({"message": "you successfully liking this recipe"}), 200

        except IntegrityError:
            abort(400, message="recipe with that title already exists")
        except SQLAlchemyError as e:
            abort(500, message=f"An error occurred while creating the recipe: {str(e)}")


@blp.route("/recipes/unlike/<int:recipe_in_search>")
class RecipeUnlike(MethodView):
    @blp.response(201, LikeSchema)
    @jwt_required()
    def post(self, recipe_in_search):
        try:
            current_user_id = get_jwt_identity()["id"]

            recipe = RecipeModel.query.filter_by(id=recipe_in_search).first()

            if not recipe:
                return (
                    jsonify({"message": "The recipe does not exist"}),
                    404,
                )

            like_exist = LikeModel.query.filter_by(
                user_id=current_user_id, recipe_id=recipe_in_search
            ).first()

            if not like_exist:
                return (
                    jsonify({"message": "You haven't liked this recipe yet"}),
                    403,
                )

            like_exist.delete_like()

            return jsonify({"message": "you successfully unliking this recipe"}), 200

        except IntegrityError:
            abort(400, message="recipe with that title already exists")
        except SQLAlchemyError as e:
            abort(500, message=f"An error occurred while creating the recipe: {str(e)}")
