import random

import click
from passlib.hash import pbkdf2_sha512

from app import create_app
from db import db
from models import (
    UserModel,
    UserRole,
    SocialModel,
    FollowingModel,
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
)
from utils import ingredient_default_images

app = create_app()

SEED_PASSWORD = "Healthub123!"

USER_SEEDS = [
    {
        "username": "chef_andre",
        "first_name": "Andre",
        "last_name": "Wijaya",
        "email": "chef@healthub.io",
        "password": pbkdf2_sha512.hash(SEED_PASSWORD),
        "role": UserRole.CHEF,
        "bio": "Professional chef crafting delicious yet healthy recipes.",
        "phone": "081234567801",
        "location": "Jakarta, ID",
        "image": "https://placehold.co/200x200?text=Chef+Andre",
    },
    {
        "username": "admin_healthub",
        "first_name": "Budi",
        "last_name": "Santoso",
        "email": "admin@healthub.io",
        "password": pbkdf2_sha512.hash(SEED_PASSWORD),
        "role": UserRole.ADMIN,
        "bio": "Platform admin keeping HealthHub running smoothly.",
        "phone": "081234567802",
        "location": "Surabaya, ID",
        "image": "https://placehold.co/200x200?text=Admin",
    },
    {
        "username": "expert_ria",
        "first_name": "Ria",
        "last_name": "Puspita",
        "email": "expert@healthub.io",
        "password": pbkdf2_sha512.hash(SEED_PASSWORD),
        "role": UserRole.EXPERT,
        "bio": "Registered dietitian and nutrition expert.",
        "phone": "081234567803",
        "location": "Bandung, ID",
        "image": "https://placehold.co/200x200?text=Ria",
    },
    {
        "username": "user_demo",
        "first_name": "Dewi",
        "last_name": "Lestari",
        "email": "user@healthub.io",
        "password": pbkdf2_sha512.hash(SEED_PASSWORD),
        "role": UserRole.USER,
        "bio": "Foodie on a healthy journey.",
        "phone": "081234567804",
        "location": "Denpasar, ID",
        "image": "https://placehold.co/200x200?text=Dewi",
    },
]

RECIPE_SEEDS = [
    {
        "author": "chef_andre",
        "title": "Nasi Goreng Sehat",
        "description": "A healthier take on the classic Indonesian fried rice, packed with vegetables and lean protein.",
        "nutriscore": 4,
        "cooktime": 25,
        "complexity": "Medium",
        "servings": 2,
        "budget": "$",
        "instruction": (
            "1. Cook the brown rice and let it cool.\n"
            "2. Saute garlic and carrot in a little oil until fragrant.\n"
            "3. Add chicken breast and cook until golden.\n"
            "4. Push to the side, scramble the egg, then mix in the rice.\n"
            "5. Season with sweet soy sauce, stir-fry for 2 minutes and serve."
        ),
        "categories": ["Main Dishes", "Rice"],
        "type": "Dinner",
        "origin": "Indonesia",
        "tags": ["rice", "fried rice", "umami", "indonesian"],
        "ingredients": [
            ["Brown rice", "2 cups"],
            ["Egg", "1 pc"],
            ["Chicken breast", "150 g"],
            ["Carrot", "1 pc"],
            ["Garlic", "2 cloves"],
            ["Sweet soy sauce", "2 tbsp"],
        ],
        "attachment": "https://placehold.co/600x400?text=Nasi+Goreng+Sehat",
        "nutrition": {
            "serving_per_container": 2,
            "serving_size": "2 bowls",
            "calories": 420.50,
            "total_fat": 12.00,
            "total_carbohydrate": 58.00,
            "total_sugar": 9.00,
            "cholesterol": 90.00,
            "protein": 22.00,
            "vitamin_d": 0.50,
            "sodium": 480.00,
            "calcium": 45.00,
            "potassium": 320.00,
            "iron": 2.50,
        },
    },
    {
        "author": "chef_andre",
        "title": "Grilled Salmon with Quinoa",
        "description": "Perfectly grilled salmon fillet served over fluffy quinoa with steamed broccoli.",
        "nutriscore": 5,
        "cooktime": 30,
        "complexity": "Easy",
        "servings": 1,
        "budget": "$$",
        "instruction": (
            "1. Season the salmon with salt, pepper and a squeeze of lemon.\n"
            "2. Grill skin-side down for 4 minutes, then flip and cook 3 more.\n"
            "3. Meanwhile cook quinoa per package instructions.\n"
            "4. Steam broccoli until bright green.\n"
            "5. Plate quinoa, top with salmon and broccoli, drizzle olive oil."
        ),
        "categories": ["Seafood", "Main Dishes"],
        "type": "Dinner",
        "origin": "Norway",
        "tags": ["salmon", "omega-3", "grilled", "high protein"],
        "ingredients": [
            ["Salmon fillet", "200 g"],
            ["Quinoa", "1 cup"],
            ["Broccoli", "150 g"],
            ["Olive oil", "1 tbsp"],
            ["Lemon", "1 pc"],
        ],
        "attachment": "https://placehold.co/600x400?text=Grilled+Salmon",
        "nutrition": {
            "serving_per_container": 1,
            "serving_size": "1 plate",
            "calories": 550.00,
            "total_fat": 25.00,
            "total_carbohydrate": 40.00,
            "total_sugar": 6.00,
            "cholesterol": 85.00,
            "protein": 42.00,
            "vitamin_d": 16.00,
            "sodium": 240.00,
            "calcium": 60.00,
            "potassium": 890.00,
            "iron": 2.80,
        },
    },
    {
        "author": "expert_ria",
        "title": "Berry Overnight Oats",
        "description": "No-cook overnight oats layered with chia seeds and fresh berries. Perfect meal prep.",
        "nutriscore": 4,
        "cooktime": 10,
        "complexity": "Easy",
        "servings": 2,
        "budget": "$",
        "instruction": (
            "1. Mix rolled oats, almond milk and chia seeds in a jar.\n"
            "2. Stir in honey and half the berries.\n"
            "3. Cover and refrigerate overnight.\n"
            "4. Top with the remaining berries before serving."
        ),
        "categories": ["Breakfast"],
        "type": "Brunch",
        "origin": "United States",
        "tags": ["vegan", "oats", "berries", "no cook"],
        "ingredients": [
            ["Rolled oats", "1 cup"],
            ["Almond milk", "1 cup"],
            ["Chia seeds", "1 tbsp"],
            ["Mixed berries", "150 g"],
            ["Honey", "1 tsp"],
        ],
        "attachment": "https://placehold.co/600x400?text=Overnight+Oats",
        "nutrition": {
            "serving_per_container": 2,
            "serving_size": "2 jars",
            "calories": 310.00,
            "total_fat": 9.00,
            "total_carbohydrate": 48.00,
            "total_sugar": 14.00,
            "cholesterol": 0.00,
            "protein": 11.00,
            "vitamin_d": 1.20,
            "sodium": 70.00,
            "calcium": 180.00,
            "potassium": 240.00,
            "iron": 1.90,
        },
    },
    {
        "author": "admin_healthub",
        "title": "Quinoa Power Bowl",
        "description": "A colorful vegetarian bowl with quinoa, chickpeas, avocado and tahini dressing.",
        "nutriscore": 5,
        "cooktime": 20,
        "complexity": "Easy",
        "servings": 2,
        "budget": "$$",
        "instruction": (
            "1. Cook quinoa and let it cool slightly.\n"
            "2. Toss chickpeas, cherry tomatoes and greens together.\n"
            "3. Divide quinoa into two bowls and top with the veggie mix.\n"
            "4. Add sliced avocado and drizzle with tahini dressing."
        ),
        "categories": ["Vegetarian", "Salads"],
        "type": "Lunch",
        "origin": "Peru",
        "tags": ["vegetarian", "quinoa", "bowl", "meal prep"],
        "ingredients": [
            ["Quinoa", "1 cup"],
            ["Chickpeas", "150 g"],
            ["Avocado", "1 pc"],
            ["Cherry tomatoes", "100 g"],
            ["Mixed greens", "2 cups"],
            ["Tahini dressing", "2 tbsp"],
        ],
        "attachment": "https://placehold.co/600x400?text=Quinoa+Power+Bowl",
        "nutrition": {
            "serving_per_container": 2,
            "serving_size": "2 bowls",
            "calories": 480.00,
            "total_fat": 18.00,
            "total_carbohydrate": 62.00,
            "total_sugar": 11.00,
            "cholesterol": 0.00,
            "protein": 17.00,
            "vitamin_d": 0.00,
            "sodium": 310.00,
            "calcium": 90.00,
            "potassium": 640.00,
            "iron": 3.20,
        },
    },
    {
        "author": "user_demo",
        "title": "Matcha Protein Smoothie",
        "description": "Energizing green smoothie with matcha, banana and Greek yogurt for a post-workout boost.",
        "nutriscore": 4,
        "cooktime": 5,
        "complexity": "Easy",
        "servings": 1,
        "budget": "$",
        "instruction": (
            "1. Add all ingredients to a blender.\n"
            "2. Blend until completely smooth.\n"
            "3. Pour into a glass and enjoy immediately."
        ),
        "categories": ["Drinks"],
        "type": "Snack",
        "origin": "Japan",
        "tags": ["matcha", "protein", "smoothie", "post workout"],
        "ingredients": [
            ["Matcha powder", "1 tsp"],
            ["Banana", "1 pc"],
            ["Greek yogurt", "150 g"],
            ["Oat milk", "1 cup"],
            ["Honey", "1 tsp"],
        ],
        "attachment": "https://placehold.co/600x400?text=Matcha+Smoothie",
        "nutrition": {
            "serving_per_container": 1,
            "serving_size": "1 glass",
            "calories": 290.00,
            "total_fat": 4.00,
            "total_carbohydrate": 40.00,
            "total_sugar": 20.00,
            "cholesterol": 5.00,
            "protein": 24.00,
            "vitamin_d": 2.00,
            "sodium": 90.00,
            "calcium": 200.00,
            "potassium": 420.00,
            "iron": 1.10,
        },
    },
]

SOCIAL_SEEDS = {
    "chef_andre": {
        "facebook": "https://facebook.com/andre.wijaya",
        "instagram": "https://instagram.com/chef.andre",
    },
    "expert_ria": {
        "instagram": "https://instagram.com/ria.nutrition",
        "tiktok": "https://tiktok.com/@ria.nutrition",
    },
    "user_demo": {"instagram": "https://instagram.com/dewi.eats"},
}

FOLLOW_SEEDS = [
    ("user_demo", "chef_andre"),
    ("user_demo", "expert_ria"),
    ("user_demo", "admin_healthub"),
    ("expert_ria", "chef_andre"),
    ("admin_healthub", "chef_andre"),
    ("admin_healthub", "expert_ria"),
]

LIKE_SEEDS = [
    ("user_demo", "Nasi Goreng Sehat"),
    ("user_demo", "Grilled Salmon with Quinoa"),
    ("user_demo", "Berry Overnight Oats"),
    ("user_demo", "Matcha Protein Smoothie"),
    ("chef_andre", "Berry Overnight Oats"),
    ("chef_andre", "Matcha Protein Smoothie"),
    ("expert_ria", "Nasi Goreng Sehat"),
    ("expert_ria", "Grilled Salmon with Quinoa"),
    ("admin_healthub", "Quinoa Power Bowl"),
]

RATE_SEEDS = [
    ("user_demo", "Nasi Goreng Sehat", 4),
    ("user_demo", "Grilled Salmon with Quinoa", 5),
    ("user_demo", "Berry Overnight Oats", 5),
    ("user_demo", "Quinoa Power Bowl", 4),
    ("expert_ria", "Nasi Goreng Sehat", 5),
    ("expert_ria", "Grilled Salmon with Quinoa", 5),
    ("expert_ria", "Berry Overnight Oats", 4),
    ("expert_ria", "Quinoa Power Bowl", 5),
    ("admin_healthub", "Nasi Goreng Sehat", 4),
    ("admin_healthub", "Matcha Protein Smoothie", 4),
]

COMMENT_SEEDS = [
    ("user_demo", "Nasi Goreng Sehat", "Enyak dan sehat, wajib coba!"),
    ("expert_ria", "Grilled Salmon with Quinoa", "Perfect balance of protein and omega-3."),
    ("admin_healthub", "Berry Overnight Oats", "Staple for my meal prep every week."),
    ("user_demo", "Quinoa Power Bowl", "Loved the tahini dressing."),
    ("chef_andre", "Matcha Protein Smoothie", "Great post-workout pick-me-up."),
    ("user_demo", "Grilled Salmon with Quinoa", "Cooked this twice this week already."),
]


def _commit(obj):
    db.session.add(obj)
    db.session.commit()


def _get_or_create(model, lookup_field, value, **extra):
    obj = model.query.filter_by(**{lookup_field: value}).first()
    if obj is None:
        obj = model(**{lookup_field: value}, **extra)
        _commit(obj)
    return obj


def seed_users():
    users = {}
    for data in USER_SEEDS:
        if UserModel.query.filter_by(username=data["username"]).first():
            users[data["username"]] = UserModel.query.filter_by(
                username=data["username"]
            ).first()
            continue
        user = UserModel(**data)
        user.add_user()
        users[data["username"]] = user
    return users


def seed_recipes(users):
    recipes = {}
    for data in RECIPE_SEEDS:
        if RecipeModel.query.filter_by(title=data["title"]).first():
            recipes[data["title"]] = RecipeModel.query.filter_by(
                title=data["title"]
            ).first()
            continue

        recipe = RecipeModel(
            author_id=users[data["author"]].id,
            title=data["title"],
            description=data["description"],
            nutriscore=data["nutriscore"],
            cooktime=data["cooktime"],
            complexity=data["complexity"],
            servings=data["servings"],
            budget=data["budget"],
            instruction=data["instruction"],
        )
        recipe.add_recipe()

        for category_name in data["categories"]:
            category = _get_or_create(CategoryModel, "category", category_name)
            RecipeCategoryRelationModel(
                recipe_id=recipe.id, category_id=category.id
            ).add_recipe_category()

        recipe_type = _get_or_create(TypeModel, "type", data["type"])
        RecipeTypeRelationModel(
            recipe_id=recipe.id, type_id=recipe_type.id
        ).add_recipe_type()

        origin = _get_or_create(OriginModel, "origin", data["origin"])
        RecipeOriginRelationModel(
            recipe_id=recipe.id, origin_id=origin.id
        ).add_recipe_origin()

        for tag_name in data["tags"]:
            tag = _get_or_create(TagModel, "tagname", tag_name)
            RecipeTagRelationModel(
                recipe_id=recipe.id, tag_id=tag.id
            ).add_recipe_tag()

        AttachmentModel(
            recipe_id=recipe.id, attachment_link=data["attachment"]
        ).add_attachment()

        nutrition = NutritionModel(recipe_id=recipe.id, **data["nutrition"])
        nutrition.add_nutrition()

        for ingredient_name, amount in data["ingredients"]:
            ingredient = _get_or_create(
                IngredientModel,
                "ingredient",
                ingredient_name,
                ingredient_image=random.choice(ingredient_default_images),
            )
            RecipeIngredientRelationModel(
                recipe_id=recipe.id,
                ingredient_id=ingredient.id,
                amount=amount,
            ).add_recipe_ingredient()

        recipes[data["title"]] = recipe
    return recipes


def seed_socials(users, recipes):
    for username, links in SOCIAL_SEEDS.items():
        if SocialModel.query.filter_by(user_id=users[username].id).first():
            continue
        SocialModel(user_id=users[username].id, **links).add_user_social()

    for follower, followed in FOLLOW_SEEDS:
        existing = FollowingModel.query.filter_by(
            follower_id=users[follower].id, followed_id=users[followed].id
        ).first()
        if existing:
            continue
        FollowingModel(
            follower_id=users[follower].id, followed_id=users[followed].id
        ).add_following()

    for username, title in LIKE_SEEDS:
        if LikeModel.query.filter_by(
            user_id=users[username].id, recipe_id=recipes[title].id
        ).first():
            continue
        LikeModel(
            user_id=users[username].id, recipe_id=recipes[title].id
        ).add_like()

    for username, title, value in RATE_SEEDS:
        if RateModel.query.filter_by(
            user_id=users[username].id, recipe_id=recipes[title].id
        ).first():
            continue
        RateModel(
            user_id=users[username].id, recipe_id=recipes[title].id, value=value
        ).add_rate()

    for username, title, message in COMMENT_SEEDS:
        if CommentModel.query.filter_by(
            user_id=users[username].id, recipe_id=recipes[title].id
        ).first():
            continue
        CommentModel(
            recipe_id=recipes[title].id,
            user_id=users[username].id,
            message=message,
        ).add_comment()


@app.cli.command("seed-db")
@click.option(
    "--clear",
    is_flag=True,
    help="Drop all tables and recreate them before seeding.",
)
def seed_db(clear):
    with app.app_context():
        if clear:
            click.echo("Dropping and recreating all tables...")
            db.drop_all()
            db.create_all()

        users = seed_users()
        recipes = seed_recipes(users)
        seed_socials(users, recipes)

        role_counts = {role.value: 0 for role in UserRole}
        for user in UserModel.query.all():
            role_counts[user.role.value] += 1

        click.echo("Seeding complete.")
        click.echo(f"  Users: {len(users)} -> {role_counts}")
        click.echo(f"  Recipes: {len(recipes)}")
        click.echo("  Sign in with username (password: " + SEED_PASSWORD + "):")
        for username, user in users.items():
            click.echo(f"    - {username} ({user.role.value})")