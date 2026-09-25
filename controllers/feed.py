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
from schemas import CategorySchema, OriginSchema, RecipePlusPlusSchema
from utils import enrich_recipes, merge_recipes

logging.basicConfig(level=logging.INFO)

blp = Blueprint("feeds", __name__, description="Operations on feeds")


@blp.route("/feeds/categories/all")
class GetAllCategories(MethodView):

    @blp.response(200, CategorySchema(many=True))
    def get(self):
        try:
            categories = CategoryModel.query.order_by(CategoryModel.id.asc()).all()
            serialized_categories = CategorySchema(many=True).dump(categories)
            return jsonify(serialized_categories), 200

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/feeds/origins/all")
class GetAllOrigins(MethodView):

    @blp.response(200, OriginSchema(many=True))
    def get(self):
        try:
            origins = OriginModel.query.order_by(OriginModel.id.asc()).all()
            serialized_origins = OriginSchema(many=True).dump(origins)
            return jsonify(serialized_origins), 200

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/feeds/recipes/all")
class GetAllFeeds(MethodView):

    @blp.response(200, RecipePlusPlusSchema(many=True))
    # @cache.cached(timeout=60 * 3)
    def get(self):
        try:

            recipes = RecipeModel.query.order_by(desc(RecipeModel.nutriscore)).all()

            if not recipes:
                return jsonify({"message": "No recipe has been created"}), 404

            enrich_recipes(recipes)

            serialized_recipes = RecipePlusPlusSchema(many=True).dump(recipes)

            return jsonify(serialized_recipes), 200

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/feeds/recipes/filter-by/category/<int:category_id>")
class GetFeedsByCategoryId(MethodView):

    @blp.response(200, RecipePlusPlusSchema(many=True))
    # @cache.cached(timeout=60 * 3)
    def get(self, category_id):
        try:
            category = CategoryModel.query.filter_by(id=category_id).first()

            if category is None:
                return jsonify({"message": "Category not found"}), 404

            recipes = (
                RecipeModel.query.join(
                    RecipeCategoryRelationModel,
                    RecipeCategoryRelationModel.recipe_id == RecipeModel.id,
                )
                .filter(RecipeCategoryRelationModel.category_id == category.id)
                .order_by(desc(RecipeModel.nutriscore), RecipeModel.id)
                .all()
            )

            if not recipes:
                return (
                    jsonify(
                        {"message": "No recipe has created under the category name"}
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


@blp.route("/feeds/recipes/filter-by/type/<string:recipe_type_in_search>")
class GetFeedsByType(MethodView):

    @blp.response(200, RecipePlusPlusSchema(many=True))
    # @cache.cached(timeout=60 * 3)
    def get(self, recipe_type_in_search):
        try:
            type = TypeModel.query.filter_by(type=recipe_type_in_search).first()

            if type is None:
                return jsonify({"message": "Type not found"}), 404

            recipes = (
                RecipeModel.query.join(
                    RecipeTypeRelationModel,
                    RecipeTypeRelationModel.recipe_id == RecipeModel.id,
                )
                .filter(RecipeTypeRelationModel.type_id == type.id)
                .order_by(desc(RecipeModel.nutriscore), RecipeModel.id)
                .all()
            )

            if not recipes:
                return (
                    jsonify(
                        {"message": "No recipe has been created under the type name"}
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


@blp.route("/feeds/recipes/filter-by/origin/<int:origin_id>")
class GetFeedsByOriginId(MethodView):

    @blp.response(200, RecipePlusPlusSchema(many=True))
    # @cache.cached(timeout=60 * 3)
    def get(self, origin_id):
        try:
            origin = OriginModel.query.filter_by(id=origin_id).first()

            if origin is None:
                return jsonify({"message": "Origin not found"}), 404

            recipes = (
                RecipeModel.query.join(
                    RecipeOriginRelationModel,
                    RecipeOriginRelationModel.recipe_id == RecipeModel.id,
                )
                .filter(RecipeOriginRelationModel.origin_id == origin.id)
                .order_by(desc(RecipeModel.nutriscore), RecipeModel.id)
                .all()
            )

            if not recipes:
                return (
                    jsonify(
                        {"message": "No recipe has been created under the origin name"}
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


@blp.route("/feeds/recipes/filter-by/tag/<string:recipe_tag_in_search>")
class GetFeedsByTag(MethodView):

    @blp.response(200, RecipePlusPlusSchema(many=True))
    # @cache.cached(timeout=60 * 3)
    def get(self, recipe_tag_in_search):
        try:
            tag = TagModel.query.filter_by(tagname=recipe_tag_in_search).first()

            if tag is None:
                return jsonify({"message": "Tag not found"}), 404

            recipes = (
                RecipeModel.query.join(
                    RecipeTagRelationModel,
                    RecipeTagRelationModel.recipe_id == RecipeModel.id,
                )
                .filter(RecipeTagRelationModel.tag_id == tag.id)
                .order_by(desc(RecipeModel.nutriscore), RecipeModel.id)
                .all()
            )

            if not recipes:
                return (
                    jsonify(
                        {"message": "No recipe has been created under the tag name"}
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

            recipe_ids = []

            # Search in CategoryModel
            categories = CategoryModel.query.filter(
                CategoryModel.category.ilike(f"%{search_keyword}%")
            ).all()

            if categories:
                recipe_category_relations = RecipeCategoryRelationModel.query.filter(
                    RecipeCategoryRelationModel.category_id.in_(
                        category.id for category in categories
                    )
                ).all()
                recipe_ids.extend(
                    relation.recipe_id for relation in recipe_category_relations
                )

            # Search in TypeModel
            types = TypeModel.query.filter(
                TypeModel.type.ilike(f"%{search_keyword}%")
            ).all()

            if types:
                recipe_type_relations = RecipeTypeRelationModel.query.filter(
                    RecipeTypeRelationModel.type_id.in_(type.id for type in types)
                ).all()
                recipe_ids.extend(
                    relation.recipe_id for relation in recipe_type_relations
                )

            # Search in OriginModel
            origins = OriginModel.query.filter(
                OriginModel.origin.ilike(f"%{search_keyword}%")
            ).all()

            if origins:
                recipe_origin_relations = RecipeOriginRelationModel.query.filter(
                    RecipeOriginRelationModel.origin_id.in_(
                        origin.id for origin in origins
                    )
                ).all()
                recipe_ids.extend(
                    relation.recipe_id for relation in recipe_origin_relations
                )

            # Search in TagModel
            tags = TagModel.query.filter(
                TagModel.tagname.ilike(f"%{search_keyword}%")
            ).all()

            if tags:
                recipe_tag_relations = RecipeTagRelationModel.query.filter(
                    RecipeTagRelationModel.tag_id.in_(tag.id for tag in tags)
                ).all()
                recipe_ids.extend(relation.recipe_id for relation in recipe_tag_relations)

            # Search in IngredientModel
            ingredients = IngredientModel.query.filter(
                IngredientModel.ingredient.ilike(f"%{search_keyword}%")
            ).all()

            if ingredients:
                recipe_ingredient_relations = (
                    RecipeIngredientRelationModel.query.filter(
                        RecipeIngredientRelationModel.ingredient_id.in_(
                            ingredient.id for ingredient in ingredients
                        )
                    ).all()
                )
                recipe_ids.extend(
                    relation.recipe_id for relation in recipe_ingredient_relations
                )

            recipes = merge_recipes(recipes, recipe_ids)

            if not recipes:
                return (
                    jsonify(
                        {"message": "No recipes found for the given search keyword"}
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
