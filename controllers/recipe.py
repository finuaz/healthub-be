import logging
import random

from flask.views import MethodView
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask import jsonify, current_app
from db import db
from werkzeug.exceptions import Forbidden

from models import (
    RecipeModel,
    CategoryModel,
    RecipeCategoryRelationModel,
    TypeModel,
    RecipeTypeRelationModel,
    OriginModel,
    RecipeOriginRelationModel,
    TagModel,
    RecipeTagRelationModel,
    IngredientModel,
    RecipeIngredientRelationModel,
    AttachmentModel,
    NutritionModel,
    LikeModel,
    RateModel,
    CommentModel,
    UserModel,
    SocialModel,
)
from schemas import RecipeSchema, RecipePlusPlusSchema, CommentSchema
from utils import (
    find_category,
    find_type,
    find_origin,
    find_tag,
    find_attachment,
    increment_view,
    find_serving_per_container,
    find_serving_size,
    find_calories,
    find_total_fat,
    find_total_carbohydrate,
    find_total_sugar,
    find_cholesterol,
    find_protein,
    find_vitamin_d,
    find_sodium,
    find_calcium,
    find_potassium,
    find_iron,
    find_ingredient,
    get_likes,
    get_rating,
    get_comments,
    chef_recipe_check,
    ingredient_default_images,
    get_author_name,
    get_author_facebook,
    get_author_tiktok,
    get_author_instagram,
)

logging.basicConfig(level=logging.INFO)

blp = Blueprint("recipes", __name__, description="Operations on recipes")


@blp.route("/recipes/create")
class RecipeRegister(MethodView):

    @blp.arguments(RecipeSchema)
    @blp.response(201, RecipePlusPlusSchema)
    @jwt_required()
    def post(self, recipe_data):
        current_user_id = get_jwt_identity()["id"]

        existing_recipe = RecipeModel.query.filter_by(
            title=recipe_data["title"]
        ).first()
        if existing_recipe:
            return (
                jsonify({"message": "Recipe with the same title already exists"}),
                404,
            )

        try:
            recipe = RecipeModel(
                author_id=current_user_id,
                title=recipe_data["title"],
                description=recipe_data["description"],
                nutriscore=recipe_data["nutriscore"],
                cooktime=recipe_data["cooktime"],
                complexity=recipe_data["complexity"],
                servings=recipe_data["servings"],
                budget=recipe_data["budget"],
                instruction=recipe_data["instruction"],
            )

            recipe.add_recipe()

            # add categories
            if "categories" in recipe_data:
                categories = recipe_data["categories"]

                for category_name in categories:
                    category = CategoryModel.query.filter_by(
                        category=category_name
                    ).first()

                    if not category:
                        category = CategoryModel(category=category_name)
                        category.add_category()

                    recipe_category = RecipeCategoryRelationModel(
                        recipe_id=recipe.id,
                        category_id=category.id,
                    )

                    recipe_category.add_recipe_category()
                recipe.categories = categories

            # add type
            if "type" in recipe_data:
                type = TypeModel.query.filter_by(type=recipe_data["type"]).first()

                if not type:
                    type = TypeModel(type=recipe_data["type"])
                    type.add_type()

                recipe_type = RecipeTypeRelationModel(
                    recipe_id=recipe.id,
                    type_id=type.id,
                )

                recipe_type.add_recipe_type()
                recipe.type = type.type

            # add origin
            if "origin" in recipe_data:
                origin = OriginModel.query.filter_by(
                    origin=recipe_data["origin"]
                ).first()

                if not origin:
                    origin = OriginModel(origin=recipe_data["origin"])
                    origin.add_origin()

                recipe_origin = RecipeOriginRelationModel(
                    recipe_id=recipe.id,
                    origin_id=origin.id,
                )

                recipe_origin.add_recipe_origin()
                recipe.origin = origin.origin

            # add tag
            if "tags" in recipe_data:
                tags = recipe_data["tags"]

                for tag_name in tags:
                    tag = TagModel.query.filter_by(tagname=tag_name).first()

                    if not tag:
                        tag = TagModel(tagname=tag_name)
                        tag.add_tag()

                    recipe_tag = RecipeTagRelationModel(
                        recipe_id=recipe.id,
                        tag_id=tag.id,
                    )

                    recipe_tag.add_recipe_tag()
                recipe.tags = tags

            # add attachment
            if "attachment" in recipe_data:
                attachment = AttachmentModel(
                    recipe_id=recipe.id,
                    attachment_link=recipe_data["attachment"],
                )

                attachment.add_attachment()
                recipe.attachment = attachment.attachment_link

            # add nutrition
            nutrition = NutritionModel(
                recipe_id=recipe.id,
                serving_per_container=recipe_data.get("serving_per_container"),
                serving_size=recipe_data.get("serving_size"),
                calories=recipe_data.get("calories"),
                total_fat=recipe_data.get("total_fat"),
                total_carbohydrate=recipe_data.get("total_carbohydrate"),
                total_sugar=recipe_data.get("total_sugar"),
                cholesterol=recipe_data.get("cholesterol"),
                protein=recipe_data.get("protein"),
                vitamin_d=recipe_data.get("vitamin_d"),
                sodium=recipe_data.get("sodium"),
                calcium=recipe_data.get("calcium"),
                potassium=recipe_data.get("potassium"),
                iron=recipe_data.get("iron"),
            )

            nutrition.add_nutrition()

            recipe.serving_per_container = nutrition.serving_per_container
            recipe.serving_size = nutrition.serving_size
            recipe.calories = nutrition.calories
            recipe.total_fat = nutrition.total_fat
            recipe.total_carbohydrate = nutrition.total_carbohydrate
            recipe.total_sugar = nutrition.total_sugar
            recipe.cholesterol = nutrition.cholesterol
            recipe.protein = nutrition.protein
            recipe.vitamin_d = nutrition.vitamin_d
            recipe.sodium = nutrition.sodium
            recipe.calcium = nutrition.calcium
            recipe.potassium = nutrition.potassium
            recipe.iron = nutrition.iron

            # add ingredients
            if "ingredients" in recipe_data:
                ingredients = recipe_data["ingredients"]
                recipe.ingredients = []

                for ingredient_member in ingredients:

                    ingredient = IngredientModel.query.filter_by(
                        ingredient=ingredient_member[0]
                    ).first()

                    if not ingredient:

                        ingredient = IngredientModel(
                            ingredient=ingredient_member[0],
                            ingredient_image=random.choice(ingredient_default_images),
                        )

                        ingredient.add_ingredient()

                    recipe_ingredient = RecipeIngredientRelationModel(
                        recipe_id=recipe.id,
                        ingredient_id=ingredient.id,
                        amount=ingredient_member[1],
                    )
                    recipe_ingredient.add_recipe_ingredient()

                    recipe.ingredients.append(ingredient_member)

            recipe.like_count = get_likes(recipe.id)
            recipe.rating = get_rating(recipe.id)
            recipe.is_chef_recipe = chef_recipe_check(recipe.id)
            recipe.author_name = get_author_name(recipe.id)
            recipe.author_facebook = get_author_facebook(recipe.id)
            recipe.author_instagram = get_author_instagram(recipe.id)
            recipe.author_tiktok = get_author_tiktok(recipe.id)

        except IntegrityError:
            abort(400, message="recipe with that title already exists")
        except SQLAlchemyError as e:
            abort(500, message=f"An error occurred while creating the recipe: {str(e)}")
        return recipe


@blp.route("/recipes/details/<int:recipe_in_details_by_id>")
class RecipeDetailsById(MethodView):
    @blp.response(201, RecipePlusPlusSchema)
    def get(self, recipe_in_details_by_id):
        try:
            recipe = RecipeModel.query.filter_by(id=recipe_in_details_by_id).first()
            if not recipe:
                return jsonify({"message": "the recipe is not found"}), 404

            recipe.author_name = get_author_name(recipe_in_details_by_id)
            recipe.author_facebook = get_author_facebook(recipe_in_details_by_id)
            recipe.author_instagram = get_author_instagram(recipe_in_details_by_id)
            recipe.author_tiktok = get_author_tiktok(recipe_in_details_by_id)

            # finding category, type, origin, tag, attachment
            recipe.categories = find_category(recipe_in_details_by_id)
            recipe.type = find_type(recipe_in_details_by_id)
            recipe.origin = find_origin(recipe_in_details_by_id)
            recipe.tags = find_tag(recipe_in_details_by_id)
            recipe.attachment = find_attachment(recipe_in_details_by_id)

            # ingredient and chef recipe
            recipe.ingredients = find_ingredient(recipe_in_details_by_id)
            recipe.is_chef_recipe = chef_recipe_check(recipe_in_details_by_id)

            # find nutrition data
            recipe.serving_per_container = find_serving_per_container(
                recipe_in_details_by_id
            )
            recipe.serving_size = find_serving_size(recipe_in_details_by_id)
            recipe.calories = find_calories(recipe_in_details_by_id)
            recipe.total_fat = find_total_fat(recipe_in_details_by_id)
            recipe.total_carbohydrate = find_total_carbohydrate(recipe_in_details_by_id)
            recipe.total_sugar = find_total_sugar(recipe_in_details_by_id)
            recipe.cholesterol = find_cholesterol(recipe_in_details_by_id)
            recipe.protein = find_protein(recipe_in_details_by_id)
            recipe.vitamin_d = find_vitamin_d(recipe_in_details_by_id)
            recipe.sodium = find_sodium(recipe_in_details_by_id)
            recipe.calcium = find_calcium(recipe_in_details_by_id)
            recipe.potassium = find_potassium(recipe_in_details_by_id)
            recipe.iron = find_iron(recipe_in_details_by_id)

            # like, rate, comment
            recipe.like_count = get_likes(recipe_in_details_by_id)
            recipe.rating = get_rating(recipe_in_details_by_id)
            recipe.comments = get_comments(recipe_in_details_by_id)

            increment_view(recipe)

            comments = get_comments(recipe_in_details_by_id)
            serialized_comments = CommentSchema().dump(comments, many=True)

            serialized_recipe = RecipePlusPlusSchema().dump(recipe)
            serialized_recipe["comments"] = serialized_comments
            return jsonify(serialized_recipe), 200
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/recipes/details/<string:recipe_in_details_by_title>")
class RecipeDetailsByTitle(MethodView):

    @blp.response(201, RecipePlusPlusSchema)
    def get(self, recipe_in_details_by_title):
        try:
            recipe = RecipeModel.query.filter_by(
                title=recipe_in_details_by_title
            ).first()
            if not recipe:
                return (
                    jsonify({"message": "The recipe is not found"}),
                    404,
                )

            recipe.author_name = get_author_name(recipe.id)
            recipe.author_facebook = get_author_facebook(recipe.id)
            recipe.author_instagram = get_author_instagram(recipe.id)
            recipe.author_tiktok = get_author_tiktok(recipe.id)

            # finding category, type, origin, tag, attachment
            recipe.categories = find_category(recipe.id)
            recipe.type = find_type(recipe.id)
            recipe.origin = find_origin(recipe.id)
            recipe.tags = find_tag(recipe.id)
            recipe.attachment = find_attachment(recipe.id)

            # ingredient and chef recipe
            recipe.ingredients = find_ingredient(recipe.id)
            recipe.is_chef_recipe = chef_recipe_check(recipe.id)

            # find nutrition data
            recipe.serving_per_container = find_serving_per_container(recipe.id)
            recipe.serving_size = find_serving_size(recipe.id)
            recipe.calories = find_calories(recipe.id)
            recipe.total_fat = find_total_fat(recipe.id)
            recipe.total_carbohydrate = find_total_carbohydrate(recipe.id)
            recipe.total_sugar = find_total_sugar(recipe.id)
            recipe.cholesterol = find_cholesterol(recipe.id)
            recipe.protein = find_protein(recipe.id)
            recipe.vitamin_d = find_vitamin_d(recipe.id)
            recipe.sodium = find_sodium(recipe.id)
            recipe.calcium = find_calcium(recipe.id)
            recipe.potassium = find_potassium(recipe.id)
            recipe.iron = find_iron(recipe.id)

            # like, rate, comment
            recipe.like_count = get_likes(recipe.id)
            recipe.rating = get_rating(recipe.id)
            recipe.comments = get_comments(recipe.id)

            increment_view(recipe)

            comments = get_comments(recipe.id)
            serialized_comments = CommentSchema().dump(comments, many=True)

            serialized_recipe = RecipePlusPlusSchema().dump(recipe)
            serialized_recipe["comments"] = serialized_comments
            return jsonify(serialized_recipe), 200
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


# def get_author_facebook(recipe_id):
#     recipe = RecipeModel.query.filter_by(id=recipe_id).first()
#     author = UserModel.query.filter_by(id=recipe.author_id).first()
#     social = SocialModel.query.filter_by(user_id=author.id).first()

#     return social.facebook if social.facebook else None


@blp.route("/recipes/edit/<int:recipe_in_details_by_id>")
class RecipeUpdate(MethodView):

    @blp.arguments(RecipeSchema)
    @blp.response(201, RecipePlusPlusSchema)
    @jwt_required()
    def put(self, recipe_data, recipe_in_details_by_id):

        user_id = get_jwt_identity()["id"]
        recipe = RecipeModel.query.filter_by(id=recipe_in_details_by_id).first()

        if recipe.author_id != user_id:
            return (
                jsonify({"message": "You are not authorized to edit this recipe"}),
                403,
            )

        try:

            recipe.update_recipe(recipe_data)

            # update category
            if "categories" in recipe_data:
                updated_categories = recipe_data["categories"]

                # Remove existing category relations for the recipe
                RecipeCategoryRelationModel.query.filter_by(
                    recipe_id=recipe.id
                ).delete()

                # Add new category relations
                for category_name in updated_categories:
                    category = CategoryModel.query.filter_by(
                        category=category_name
                    ).first()

                    if not category:
                        category = CategoryModel(category=category_name)
                        category.add_category()

                    recipe_category = RecipeCategoryRelationModel(
                        recipe_id=recipe.id,
                        category_id=category.id,
                    )
                    recipe_category.add_recipe_category()
                recipe.categories = updated_categories

            # update type
            if "type" in recipe_data:
                existing_type = TypeModel.query.filter_by(
                    type=recipe_data["type"]
                ).first()

                if existing_type:
                    recipe_type = RecipeTypeRelationModel.query.filter_by(
                        recipe_id=recipe.id
                    ).first()

                    recipe_type.type_id = existing_type.id
                    db.session.commit()
                    recipe.type = existing_type.type

                else:
                    RecipeTypeRelationModel.query.filter_by(
                        recipe_id=recipe.id
                    ).delete()

                    new_type = TypeModel(type=recipe_data["type"])
                    new_type.add_type()

                    recipe_type = RecipeTypeRelationModel(
                        recipe_id=recipe.id,
                        type_id=new_type.id,
                    )

                    recipe_type.add_recipe_type()
                    recipe.type = new_type.type

            # update origin
            if "origin" in recipe_data:

                existing_origin = OriginModel.query.filter_by(
                    origin=recipe_data["origin"]
                ).first()

                if existing_origin:

                    recipe_origin = RecipeOriginRelationModel.query.filter_by(
                        recipe_id=recipe.id
                    ).first()

                    recipe_origin.origin_id = existing_origin.id
                    db.session.commit()
                    recipe.origin = existing_origin.origin

                else:

                    RecipeOriginRelationModel.query.filter_by(
                        recipe_id=recipe.id
                    ).delete()

                    new_origin = OriginModel(origin=recipe_data["origin"])
                    new_origin.add_origin()

                    recipe_origin = RecipeOriginRelationModel(
                        recipe_id=recipe.id,
                        origin_id=new_origin.id,
                    )

                    recipe_origin.add_recipe_origin()
                    recipe.origin = new_origin.origin

            # update tag
            if "tag" in recipe_data:
                updated_tags = recipe_data["tag"]

                # Remove existing tag relations for the recipe
                RecipeTagRelationModel.query.filter_by(recipe_id=recipe.id).delete()

                # Add new tag relations
                for tag_name in updated_tags:
                    tag = TagModel.query.filter_by(tagname=tag_name).first()

                    if not tag:
                        tag = TagModel(tagname=tag_name)
                        tag.add_tag()

                    recipe_tag = RecipeTagRelationModel(
                        recipe_id=recipe.id,
                        tag_id=tag.id,
                    )
                    recipe_tag.add_recipe_tag()
                recipe.tags = updated_tags

            # update attachment

            if "attachment" in recipe_data:

                existing_attachment = AttachmentModel.query.filter_by(
                    attachment_link=recipe_data["attachment"]
                ).first()

                if existing_attachment:

                    # check if the image has been used by other recipe
                    # if existing_attachment.recipe_id != recipe.id:
                    #     abort(403, "Attachment has been used by other recipe")

                    if existing_attachment.attachment_link == recipe_data["attachment"]:
                        recipe.attachment = existing_attachment.attachment_link

                    else:
                        AttachmentModel.query.filter_by(recipe_id=recipe.id).delete()

                        new_attachment = AttachmentModel(
                            recipe_id=recipe.id,
                            attachment_link=recipe_data["attachment"],
                        )

                        new_attachment.add_attachment()
                        recipe.attachment = new_attachment.attachment_link

                else:
                    new_attachment = AttachmentModel(
                        recipe_id=recipe.id,
                        attachment_link=recipe_data["attachment"],
                    )

                    new_attachment.add_attachment()
                    recipe.attachment = new_attachment.attachment_link

            # update nutrition
            nutrition = NutritionModel.query.filter_by(
                recipe_id=recipe_in_details_by_id
            ).first()
            nutrition.update_nutrition(recipe_data)

            recipe.serving_per_container = find_serving_per_container(recipe.id)
            recipe.serving_size = find_serving_size(recipe.id)
            recipe.calories = find_calories(recipe.id)
            recipe.total_fat = find_total_fat(recipe.id)
            recipe.total_carbohydrate = find_total_carbohydrate(recipe.id)
            recipe.total_sugar = find_total_sugar(recipe.id)
            recipe.cholesterol = find_cholesterol(recipe.id)
            recipe.protein = find_protein(recipe.id)
            recipe.vitamin_d = find_vitamin_d(recipe.id)
            recipe.sodium = find_sodium(recipe.id)
            recipe.calcium = find_calcium(recipe.id)
            recipe.potassium = find_potassium(recipe.id)
            recipe.iron = find_iron(recipe.id)

            # update ingredient

            for ingredient_data in recipe_data.get("ingredients", []):
                ingredient, amount = ingredient_data

                existing_ingredient = IngredientModel.query.filter_by(
                    ingredient=ingredient
                ).first()

                if not existing_ingredient:
                    ingredient = IngredientModel(
                        ingredient=ingredient,
                        ingredient_image=random.choice(ingredient_default_images),
                    )

                    ingredient.add_ingredient()

                    recipe_ingredient = RecipeIngredientRelationModel(
                        recipe_id=recipe.id,
                        ingredient_id=ingredient.id,
                        amount=amount,
                    )
                    recipe_ingredient.add_recipe_ingredient()

                else:
                    recipe_ingredient = RecipeIngredientRelationModel(
                        recipe_id=recipe.id,
                        ingredient_id=existing_ingredient.id,
                        amount=amount,
                    )

                    recipe_ingredient.amount = amount
                    db.session.commit()

            recipe.author_name = get_author_name(recipe.id)
            recipe.like_count = get_likes(recipe.id)
            recipe.rating = get_rating(recipe.id)

            # recipe.author_name = get_author_name(recipe.id)
            # recipe.author_facebook = get_author_facebook(recipe.id)
            # recipe.author_instagram = get_author_instagram(recipe.id)
            # recipe.author_tiktok = get_author_tiktok(recipe.id)

            return RecipePlusPlusSchema().dump(recipe), 200

        except Forbidden as e:
            abort(403, description=str(e))

        except Exception as e:
            abort(500, description=f"Failed to update recipe information: {str(e)}")


@blp.route("/recipes/delete/<int:recipe_in_details_by_id>")
class RecipeDelete(MethodView):

    @blp.response(204, "Recipe deleted successfully")
    @jwt_required()
    def delete(self, recipe_in_details_by_id):

        user_id = get_jwt_identity()["id"]
        recipe = RecipeModel.query.filter_by(id=recipe_in_details_by_id).first()

        if not recipe:
            return (
                jsonify({"message": "The recipe is not found"}),
                404,
            )

        if recipe.author_id != user_id:
            return (
                jsonify({"message": "You are not authorized to delete the recipe"}),
                403,
            )

        try:

            CommentModel.query.filter_by(recipe_id=recipe.id).delete()
            LikeModel.query.filter_by(recipe_id=recipe.id).delete()
            RateModel.query.filter_by(recipe_id=recipe.id).delete()
            RecipeIngredientRelationModel.query.filter_by(recipe_id=recipe.id).delete()
            NutritionModel.query.filter_by(recipe_id=recipe.id).delete()
            AttachmentModel.query.filter_by(recipe_id=recipe.id).delete()
            RecipeCategoryRelationModel.query.filter_by(recipe_id=recipe.id).delete()
            RecipeTypeRelationModel.query.filter_by(recipe_id=recipe.id).delete()
            RecipeOriginRelationModel.query.filter_by(recipe_id=recipe.id).delete()
            RecipeTagRelationModel.query.filter_by(recipe_id=recipe.id).delete()
            recipe.delete_recipe()

            return jsonify({"message": "Recipe deleted successfully"}), 200

        except Forbidden as e:
            abort(403, description=str(e))

        except Exception as e:
            abort(500, description=f"Failed to delete recipe: {str(e)}")
