import logging

from flask.views import MethodView
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask import jsonify, request

from models import RecipeModel, RateModel
from schemas import (
    RateSchema,
)

logging.basicConfig(level=logging.INFO)

blp = Blueprint("rates", __name__, description="Operations on rates")


@blp.route("/recipes/rate/<int:recipe_in_search>")
class RecipeRate(MethodView):
    @blp.response(201, RateSchema)
    @jwt_required()
    def post(self, recipe_in_search):
        try:
            current_user_id = get_jwt_identity()["id"]
            rate_value = request.json.get("value")
            existing_rate = RateModel.query.filter_by(
                recipe_id=recipe_in_search, user_id=current_user_id
            ).first()
            recipe = RecipeModel.query.filter_by(id=recipe_in_search).first()

            if not recipe:
                return (
                    jsonify({"message": "The recipe does not exist"}),
                    404,
                )

            if recipe.author_id == current_user_id:
                return jsonify({"message": "you cannot rate your own recipe"}), 403

            if not rate_value:
                return (
                    jsonify({"message": "The rate value is required"}),
                    404,
                )

            if existing_rate:

                existing_rate.value = rate_value
                existing_rate.update_rate(rate_data={"value": rate_value})

                response_data = {
                    "id": existing_rate.id,
                    "user_id": existing_rate.user_id,
                    "recipe_id": existing_rate.recipe_id,
                    "value": existing_rate.value,
                }
                return jsonify(response_data)

            rate = RateModel(
                recipe_id=recipe_in_search,
                user_id=current_user_id,
                value=rate_value,
            )

            rate.add_rate()

            rate.value = rate.value

            serialized_rate = RateSchema().dump(rate)
            return jsonify(serialized_rate), 200

        except IntegrityError:
            abort(400, message="recipe with that title already exists")
        except SQLAlchemyError as e:
            abort(500, message=f"An error occurred while creating the recipe: {str(e)}")


@blp.route("/recipes/unrate/<int:recipe_in_search>")
class RecipeUnrate(MethodView):
    @blp.response(201, RateSchema)
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

            rate_exist = RateModel.query.filter_by(
                user_id=current_user_id, recipe_id=recipe_in_search
            ).first()

            if not rate_exist:
                return (
                    jsonify({"message": "You have not rated this recipe yet"}),
                    404,
                )

            rate_exist.delete_rate()

            return jsonify({"message": "you successfully unrating this recipe"}), 200

        except IntegrityError:
            abort(400, message="recipe with that title already exists")
        except SQLAlchemyError as e:
            abort(500, message=f"An error occurred while creating the recipe: {str(e)}")
