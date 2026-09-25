from sqlalchemy.orm import selectinload

from models import (
    CategoryModel,
    TypeModel,
    OriginModel,
    TagModel,
    RecipeModel,
    RecipeCategoryRelationModel,
    RecipeTypeRelationModel,
    RecipeOriginRelationModel,
    RecipeTagRelationModel,
    RecipeIngredientRelationModel,
    RateModel,
    LikeModel,
)


def find_all_category(recipe_id):
    categories = []
    recipe_categories = RecipeCategoryRelationModel.query.filter_by(
        recipe_id=recipe_id
    ).all()
    for recipe_category in recipe_categories:
        category = CategoryModel.query.get(recipe_category.category_id)
        categories.append(category.category)
    return categories if categories else None


def find_all_type(recipe_id):
    recipe_type = RecipeTypeRelationModel.query.filter_by(recipe_id=recipe_id).first()
    if recipe_type:
        type = TypeModel.query.get(recipe_type.type_id)
        return type.type if type else None


def find_all_origin(recipe_id):
    recipe_origin = RecipeOriginRelationModel.query.filter_by(
        recipe_id=recipe_id
    ).first()
    if recipe_origin:
        origin = OriginModel.query.get(recipe_origin.origin_id)
        return origin.origin if origin else None
    # else:
    #     return None


def find_all_tag(recipe_id):
    tags = []
    recipe_tags = RecipeTagRelationModel.query.filter_by(recipe_id=recipe_id).all()
    for recipe_tag in recipe_tags:
        tag = TagModel.query.get(recipe_tag.tag_id)
        tags.append(tag.tagname)
    return tags if tags else None


def get_likes(recipe_id):
    like_count = LikeModel.query.filter_by(recipe_id=recipe_id).count()
    return like_count


def get_rating(recipe_id):
    rates = RateModel.query.filter_by(recipe_id=recipe_id).all()
    total_value = 0
    for rate in rates:
        total_value += rate.value

    if not rates:
        return 0.0

    avg_rate = total_value / len(rates)
    return avg_rate


FEED_LOAD_OPTIONS = (
    selectinload(RecipeModel.author),
    selectinload(RecipeModel.recipe_categories).selectinload(
        RecipeCategoryRelationModel.categories
    ),
    selectinload(RecipeModel.recipe_types).selectinload(RecipeTypeRelationModel.types),
    selectinload(RecipeModel.recipe_origins).selectinload(
        RecipeOriginRelationModel.origins
    ),
    selectinload(RecipeModel.recipe_tags).selectinload(RecipeTagRelationModel.tags),
    selectinload(RecipeModel.recipe_ingredients).selectinload(
        RecipeIngredientRelationModel.ingredients
    ),
    selectinload(RecipeModel.attachments),
    selectinload(RecipeModel.likes),
    selectinload(RecipeModel.rates),
    selectinload(RecipeModel.comments),
)


def enrich_recipes(recipes):
    recipe_ids = [recipe.id for recipe in recipes]

    if not recipe_ids:
        return recipes

    loaded = (
        RecipeModel.query.options(*FEED_LOAD_OPTIONS)
        .filter(RecipeModel.id.in_(recipe_ids))
        .all()
    )

    for recipe in loaded:
        recipe.author_name = recipe.author.username if recipe.author else None
        recipe.is_chef_recipe = bool(
            recipe.author and recipe.author.role.value == "chef"
        )
        recipe.categories = [
            relation.categories.category for relation in recipe.recipe_categories
        ] or None
        recipe.type = recipe.recipe_types[0].types.type if recipe.recipe_types else None
        recipe.origin = (
            recipe.recipe_origins[0].origins.origin if recipe.recipe_origins else None
        )
        recipe.tags = [
            relation.tags.tagname for relation in recipe.recipe_tags
        ] or None
        recipe.ingredients = [
            [
                relation.ingredients.ingredient,
                relation.amount,
                relation.ingredients.ingredient_image,
            ]
            for relation in recipe.recipe_ingredients
        ]
        recipe.ingredients_count = len(recipe.ingredients)
        recipe.like_count = len(recipe.likes)
        recipe.rating = (
            sum(rate.value for rate in recipe.rates) / len(recipe.rates)
            if recipe.rates
            else 0.0
        )
        recipe.attachment = (
            recipe.attachments[0].attachment_link if recipe.attachments else None
        )

    return recipes


def merge_recipes(recipes, recipe_ids):
    known = {recipe.id for recipe in recipes}
    missing = [
        recipe_id for recipe_id in dict.fromkeys(recipe_ids) if recipe_id not in known
    ]

    if not missing:
        return recipes

    return list(recipes) + RecipeModel.query.filter(RecipeModel.id.in_(missing)).all()
