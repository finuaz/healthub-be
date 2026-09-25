from marshmallow import Schema, fields
from collections import OrderedDict

# from models import UserModel

# from schemas import CommentSchema


class CategorySchema(Schema):
    id = fields.Integer(dump_only=True)
    category = fields.String()


class OriginSchema(Schema):
    id = fields.Integer(dump_only=True)
    origin = fields.String()


class CommentSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer()
    recipe_id = fields.Integer()
    message = fields.String()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class RecipeSchema(Schema):
    id = fields.Integer(dump_only=True)
    author_id = fields.Integer()
    title = fields.String()
    description = fields.String()
    nutriscore = fields.Integer()
    cooktime = fields.Integer()
    complexity = fields.String()
    servings = fields.Integer()
    budget = fields.String()
    instruction = fields.String()
    view_count = fields.Integer()

    categories = fields.List(fields.String())
    type = fields.String()
    origin = fields.String()
    tags = fields.List(fields.String())

    attachment = fields.String()

    # Ingredient group
    ingredients = fields.List(fields.List(fields.String()))

    # Nutrition group
    serving_per_container = fields.Integer()
    serving_size = fields.String()

    calories = fields.Decimal(places=2, rounding=None)
    total_fat = fields.Decimal(places=2, rounding=None)
    total_carbohydrate = fields.Decimal(places=2, rounding=None)
    total_sugar = fields.Decimal(places=2, rounding=None)
    cholesterol = fields.Decimal(places=2, rounding=None)
    protein = fields.Decimal(places=2, rounding=None)
    vitamin_d = fields.Decimal(places=2, rounding=None)

    sodium = fields.Decimal(places=2, rounding=None)
    calcium = fields.Decimal(places=2, rounding=None)
    potassium = fields.Decimal(places=2, rounding=None)
    iron = fields.Decimal(places=2, rounding=None)

    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class RecipePlusPlusSchema(Schema):
    id = fields.Integer(dump_only=True)
    author_id = fields.Integer()
    author_name = fields.String()
    author_facebook = fields.String()
    author_instagram = fields.String()
    author_tiktok = fields.String()
    title = fields.String()
    description = fields.String()
    nutriscore = fields.Integer()
    cooktime = fields.Integer()
    complexity = fields.String()
    servings = fields.Integer()
    budget = fields.String()
    instruction = fields.String()
    view_count = fields.Integer()

    categories = fields.List(fields.String())
    type = fields.String()
    origin = fields.String()
    tags = fields.List(fields.String())

    attachment = fields.String()

    # Ingredient group
    ingredients = fields.List(fields.List(fields.String()))
    ingredients_count = fields.Integer(dump_only=True)

    # Nutrition group
    serving_per_container = fields.Integer()
    serving_size = fields.String()

    calories = fields.Decimal(places=2, rounding=None)
    total_fat = fields.Decimal(places=2, rounding=None)
    total_carbohydrate = fields.Decimal(places=2, rounding=None)
    total_sugar = fields.Decimal(places=2, rounding=None)
    cholesterol = fields.Decimal(places=2, rounding=None)
    protein = fields.Decimal(places=2, rounding=None)
    vitamin_d = fields.Decimal(places=2, rounding=None)

    sodium = fields.Decimal(places=2, rounding=None)
    calcium = fields.Decimal(places=2, rounding=None)
    potassium = fields.Decimal(places=2, rounding=None)
    iron = fields.Decimal(places=2, rounding=None)

    like_count = fields.Integer()
    rating = fields.Decimal(rounding=None)
    comments = fields.List(fields.Nested(CommentSchema), many=True)

    is_chef_recipe = fields.Boolean()

    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class RecipeImageSchema(Schema):
    id = fields.Integer(dump_only=True)
    recipe_id = fields.Integer()
    attachment_link = fields.String()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class RecipeInstructionSchema(Schema):
    id = fields.Integer(dump_only=True)
    order = fields.Integer()
    instruction = fields.String()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
