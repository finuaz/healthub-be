import logging

from flask.views import MethodView
from flask_smorest import Blueprint, abort, Page
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify, current_app, request

# from extensions import cache
from sqlalchemy import desc, or_

from models import (
    RecipeModel,
    RecipeCategoryRelationModel,
    CategoryModel,
    RecipeTypeRelationModel,
    TypeModel,
    RecipeOriginRelationModel,
    OriginModel,
    RecipeTagRelationModel,
    TagModel,
    IngredientModel,
    RecipeIngredientRelationModel,
)
from schemas import RecipePlusPlusSchema
from utils import (
    find_all_category,
    find_all_type,
    find_all_origin,
    find_all_tag,
    get_likes,
    get_rating,
    find_attachment,
    chef_recipe_check,
    get_author_name,
)

logging.basicConfig(level=logging.INFO)

blp = Blueprint("feeds", __name__, description="Operations on feeds")


@blp.route("/feeds/recipes/all")
class GetAllFeeds(MethodView):

    @blp.response(200, RecipePlusPlusSchema(many=True))
    # @cache.cached(timeout=60 * 3)
    def get(self):
        try:

            recipes = RecipeModel.query.order_by(desc(RecipeModel.nutriscore)).all()

            if not recipes:
                return jsonify({"message": "No recipe has been created"}), 404

            for recipe in recipes:
                recipe.author_name = get_author_name(recipe.id)
                recipe.categories = find_all_category(recipe.id)
                recipe.type = find_all_type(recipe.id)
                recipe.origin = find_all_origin(recipe.id)
                recipe.tags = find_all_tag(recipe.id)
                recipe.like_count = get_likes(recipe.id)
                recipe.rating = get_rating(recipe.id)
                recipe.attachment = find_attachment(recipe.id)
                recipe.is_chef_recipe = chef_recipe_check(recipe.id)

            serialized_recipes = RecipePlusPlusSchema(many=True).dump(recipes)

            return jsonify(serialized_recipes), 200

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/feeds/recipes/filter-by/category/<string:recipe_category_in_search>")
class GetFeedsByCategory(MethodView):

    @blp.response(200, RecipePlusPlusSchema(many=True))
    # @cache.cached(timeout=60 * 3)
    def get(self, recipe_category_in_search):
        try:
            category = CategoryModel.query.filter_by(
                category=recipe_category_in_search
            ).first()

            recipe_categories = RecipeCategoryRelationModel.query.filter_by(
                category_id=category.id
            ).all()

            recipes = []

            for recipe_category in recipe_categories:
                recipes.extend(
                    RecipeModel.query.filter_by(id=recipe_category.recipe_id)
                    .order_by(desc(RecipeModel.nutriscore))
                    .all()
                )

            if not recipes:
                return (
                    jsonify(
                        {"message": "No recipe has created under the category name"}
                    ),
                    404,
                )

            for recipe in recipes:
                recipe.author_name = get_author_name(recipe.id)
                recipe.categories = find_all_category(recipe.id)
                recipe.type = find_all_type(recipe.id)
                recipe.origin = find_all_origin(recipe.id)
                recipe.tags = find_all_tag(recipe.id)
                recipe.like_count = get_likes(recipe.id)
                recipe.rating = get_rating(recipe.id)
                recipe.attachment = find_attachment(recipe.id)
                recipe.is_chef_recipe = chef_recipe_check(recipe.id)

            serialized_recipes = RecipePlusPlusSchema(many=True).dump(recipes)
            return jsonify(serialized_recipes), 200

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/feeds/recipes/filter-by/type/<string:recipe_type_in_search>")
class GetFeedsByType(MethodView):

    @blp.response(200, RecipePlusPlusSchema(many=True))
    # @cache.cached(timeout=60 * 3)
    def get(self, recipe_type_in_search):
        try:
            type = TypeModel.query.filter_by(type=recipe_type_in_search).first()

            recipe_types = RecipeTypeRelationModel.query.filter_by(
                type_id=type.id
            ).all()

            recipes = []

            for recipe_type in recipe_types:
                recipes.extend(
                    RecipeModel.query.filter_by(id=recipe_type.recipe_id)
                    .order_by(desc(RecipeModel.nutriscore))
                    .all()
                )

            if not recipes:
                return (
                    jsonify(
                        {"message": "No recipe has been created under the type name"}
                    ),
                    404,
                )

            for recipe in recipes:
                recipe.author_name = get_author_name(recipe.id)
                recipe.categories = find_all_category(recipe.id)
                recipe.type = find_all_type(recipe.id)
                recipe.origin = find_all_origin(recipe.id)
                recipe.tags = find_all_tag(recipe.id)
                recipe.like_count = get_likes(recipe.id)
                recipe.rating = get_rating(recipe.id)
                recipe.attachment = find_attachment(recipe.id)
                recipe.is_chef_recipe = chef_recipe_check(recipe.id)

            serialized_recipes = RecipePlusPlusSchema(many=True).dump(recipes)
            return jsonify(serialized_recipes), 200

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/feeds/recipes/filter-by/origin/<string:recipe_origin_in_search>")
class GetFeedsByOrigin(MethodView):

    @blp.response(200, RecipePlusPlusSchema(many=True))
    # @cache.cached(timeout=60 * 3)
    def get(self, recipe_origin_in_search):
        try:
            origin = OriginModel.query.filter_by(origin=recipe_origin_in_search).first()

            recipe_origins = RecipeOriginRelationModel.query.filter_by(
                origin_id=origin.id
            ).all()

            recipes = []

            for recipe_origin in recipe_origins:
                recipes.extend(
                    RecipeModel.query.filter_by(id=recipe_origin.recipe_id)
                    .order_by(desc(RecipeModel.nutriscore))
                    .all()
                )

            if not recipes:
                return (
                    jsonify(
                        {"message": "No recipe has been created under the origin name"}
                    ),
                    404,
                )

            for recipe in recipes:
                recipe.author_name = get_author_name(recipe.id)
                recipe.categories = find_all_category(recipe.id)
                recipe.type = find_all_type(recipe.id)
                recipe.origin = find_all_origin(recipe.id)
                recipe.tags = find_all_tag(recipe.id)
                recipe.like_count = get_likes(recipe.id)
                recipe.rating = get_rating(recipe.id)
                recipe.attachment = find_attachment(recipe.id)
                recipe.is_chef_recipe = chef_recipe_check(recipe.id)

            serialized_recipes = RecipePlusPlusSchema(many=True).dump(recipes)
            return jsonify(serialized_recipes), 200

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/feeds/recipes/filter-by/tag/<string:recipe_tag_in_search>")
class GetFeedsByTag(MethodView):

    @blp.response(200, RecipePlusPlusSchema(many=True))
    # @cache.cached(timeout=60 * 3)
    def get(self, recipe_tag_in_search):
        try:
            tag = TagModel.query.filter_by(tagname=recipe_tag_in_search).first()

            recipe_tags = RecipeTagRelationModel.query.filter_by(tag_id=tag.id).all()

            recipes = []

            for recipe_tag in recipe_tags:
                recipes.extend(
                    RecipeModel.query.filter_by(id=recipe_tag.recipe_id).all()
                )

            if not recipes:
                return (
                    jsonify(
                        {"message": "No recipe has been created under the tag name"}
                    ),
                    404,
                )

            for recipe in recipes:
                recipe.author_name = get_author_name(recipe.id)
                recipe.categories = find_all_category(recipe.id)
                recipe.type = find_all_type(recipe.id)
                recipe.origin = find_all_origin(recipe.id)
                recipe.tags = find_all_tag(recipe.id)
                recipe.like_count = get_likes(recipe.id)
                recipe.rating = get_rating(recipe.id)
                recipe.attachment = find_attachment(recipe.id)
                recipe.is_chef_recipe = chef_recipe_check(recipe.id)

            serialized_recipes = RecipePlusPlusSchema(many=True).dump(recipes)
            return jsonify(serialized_recipes), 200

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/feeds/recipes/search/<string:search_keyword>")
class GetFeedsByCategory(MethodView):

    @blp.response(200, RecipePlusPlusSchema(many=True))
    # @cache.cached(timeout=60 * 3)
    def get(self, search_keyword):
        try:
            # Search in Recipe Model
            recipes = RecipeModel.query.filter(
                or_(
                    RecipeModel.title.ilike(f"%{search_keyword}%"),
                    (RecipeModel.description.ilike(f"%{search_keyword}%")),
                )
            ).all()

            # Search in CategoryModel
            categories = CategoryModel.query.filter(
                CategoryModel.category.ilike(f"%{search_keyword}%")
            ).all()

            for category in categories:
                recipe_category_relations = RecipeCategoryRelationModel.query.filter_by(
                    category_id=category.id
                ).all()

                for recipe_category in recipe_category_relations:
                    recipe = RecipeModel.query.get(recipe_category.recipe_id)

                    if recipe not in recipes:
                        recipes.append(recipe)

            # Search in TypeModel
            types = TypeModel.query.filter(
                TypeModel.type.ilike(f"%{search_keyword}%")
            ).all()

            for type in types:
                recipe_type_relations = RecipeTypeRelationModel.query.filter_by(
                    type_id=type.id
                ).all()

                for recipe_type in recipe_type_relations:
                    recipe = RecipeModel.query.get(recipe_type.recipe_id)

                    if recipe not in recipes:
                        recipes.append(recipe)

            # Search in OriginModel
            origins = OriginModel.query.filter(
                OriginModel.origin.ilike(f"%{search_keyword}%")
            ).all()

            for origin in origins:
                recipe_origin_relations = RecipeOriginRelationModel.query.filter_by(
                    origin_id=origin.id
                ).all()

                for recipe_origin in recipe_origin_relations:
                    recipe = RecipeModel.query.get(recipe_origin.recipe_id)

                    if recipe not in recipes:
                        recipes.append(recipe)

            # Search in TagModel
            tags = TagModel.query.filter(
                TagModel.tagname.ilike(f"%{search_keyword}%")
            ).all()

            for tag in tags:
                recipe_tag_relations = RecipeTagRelationModel.query.filter_by(
                    tag_id=tag.id
                ).all()

                for recipe_tag in recipe_tag_relations:
                    recipe = RecipeModel.query.get(recipe_tag.recipe_id)

                    if recipe not in recipes:
                        recipes.append(recipe)

            # Search in IngredientModel
            ingredients = IngredientModel.query.filter(
                IngredientModel.ingredient.ilike(f"%{search_keyword}%")
            ).all()

            for ingredient in ingredients:
                recipe_ingredient_relations = (
                    RecipeIngredientRelationModel.query.filter_by(
                        ingredient_id=ingredient.id
                    ).all()
                )

                for recipe_ingredient in recipe_ingredient_relations:
                    recipe = RecipeModel.query.get(recipe_ingredient.recipe_id)

                    if recipe not in recipes:
                        recipes.append(recipe)

            if not recipes:
                return (
                    jsonify(
                        {"message": "No recipes found for the given search keyword"}
                    ),
                    404,
                )

            for recipe in recipes:
                recipe.author_name = get_author_name(recipe.id)
                recipe.categories = find_all_category(recipe.id)
                recipe.type = find_all_type(recipe.id)
                recipe.origin = find_all_origin(recipe.id)
                recipe.tags = find_all_tag(recipe.id)
                recipe.like_count = get_likes(recipe.id)
                recipe.rating = get_rating(recipe.id)
                recipe.attachment = find_attachment(recipe.id)
                recipe.is_chef_recipe = chef_recipe_check(recipe.id)

            serialized_recipes = RecipePlusPlusSchema(many=True).dump(recipes)
            return jsonify(serialized_recipes), 200

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")
