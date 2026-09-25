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
            "1. Cook the brown rice according to the package and spread it on a tray to cool completely — cold rice makes the best fried rice.\n"
            "2. Mince the garlic and slice the carrot into thin half-moons.\n"
            "3. Cut the chicken breast into small bite-sized cubes and season with a pinch of salt.\n"
            "4. Heat a wok over high heat with a little oil and saute the garlic and carrot for 1 minute until fragrant.\n"
            "5. Add the chicken and stir-fry for 3-4 minutes until golden and cooked through.\n"
            "6. Push everything to one side, crack in the egg, scramble it, then mix it through the chicken.\n"
            "7. Add the cooled rice and toss over high heat for 2 minutes so every grain is coated.\n"
            "8. Season with sweet soy sauce, a splash of fish sauce and white pepper.\n"
            "9. Stir-fry for another minute, then serve with sliced cucumber and tomatoes."
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
        "attachment": "https://images.unsplash.com/photo-1512058564366-18510be2db19?w=600&h=600&fit=crop&crop=entropy&q=80",
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
            "1. Pat the salmon fillet dry and season both sides with salt, black pepper and a squeeze of lemon.\n"
            "2. Let it rest at room temperature for 10 minutes so it cooks evenly.\n"
            "3. Rinse the quinoa and cook it in twice its volume of water for about 15 minutes, then fluff with a fork.\n"
            "4. Cut the broccoli into small florets and steam it for 4-5 minutes until bright green and tender.\n"
            "5. Heat a grill pan over medium-high heat and lightly oil the surface.\n"
            "6. Grill the salmon skin-side down for 4 minutes without moving it.\n"
            "7. Flip and cook for 3 more minutes for a medium center; rest for 2 minutes.\n"
            "8. Mound the quinoa on a plate, top with the salmon and broccoli.\n"
            "9. Drizzle with olive oil and a final squeeze of lemon before serving."
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
        "attachment": "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=600&h=600&fit=crop&crop=entropy&q=80",
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
            "1. In a bowl, whisk together the rolled oats, almond milk, chia seeds and honey.\n"
            "2. Stir in half of the berries, crushing them lightly so their juices tint the mix.\n"
            "3. Divide the mixture evenly between two jars or glasses.\n"
            "4. Cover and refrigerate for at least 6 hours, preferably overnight.\n"
            "5. In the morning, give each jar a quick stir to loosen the pudding.\n"
            "6. If it looks too thick, loosen with a splash of almond milk.\n"
            "7. Top generously with the remaining fresh berries and a sprinkle of chia seeds.\n"
            "8. Serve cold straight from the fridge."
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
        "attachment": "https://images.unsplash.com/photo-1517673132405-a56a62b18caf?w=600&h=600&fit=crop&crop=entropy&q=80",
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
            "1. Rinse the quinoa well, then cook it in twice its volume of salted water for about 15 minutes.\n"
            "2. Let the quinoa cool slightly so it stays fluffy.\n"
            "3. Rinse and drain the chickpeas, patting them dry on a towel.\n"
            "4. Halve the cherry tomatoes and chop the greens coarsely.\n"
            "5. Cut the avocado in half, remove the pit and slice thinly.\n"
            "6. In a bowl, toss the chickpeas, tomatoes and greens with a squeeze of lemon and a pinch of salt.\n"
            "7. Divide the quinoa between two bowls and pile the veggie mix on top.\n"
            "8. Fan out the avocado slices on each bowl.\n"
            "9. Drizzle everything generously with the tahini dressing and finish with sesame seeds."
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
        "attachment": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600&h=600&fit=crop&crop=entropy&q=80",
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
            "1. Peel the banana and break it into chunks; freeze it briefly with the oat milk for a frostier drink.\n"
            "2. Add the frozen banana, oat milk, Greek yogurt, matcha powder and honey to a blender.\n"
            "3. Blend on high for 45-60 seconds until completely smooth and frothy.\n"
            "4. Pause, scrape down the sides and give it one more quick blitz.\n"
            "5. Taste and adjust the matcha, honey or milk to your preference.\n"
            "6. Pour into a tall glass over ice if you like it extra cold.\n"
            "7. Dust the top with a pinch of extra matcha.\n"
            "8. Enjoy immediately — it is best straight from the blender."
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
        "attachment": "https://images.unsplash.com/photo-1553530666-ba11a7da3888?w=600&h=600&fit=crop&crop=entropy&q=80",
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
    {
        "author": "chef_andre",
        "title": "Capcay Sayur",
        "description": "Crisp stir-fried vegetables in a light, savory garlic sauce — a quick and nutritious Indonesian favorite.",
        "nutriscore": 5,
        "cooktime": 20,
        "complexity": "Easy",
        "servings": 3,
        "budget": "$",
        "instruction": (
            "1. Wash and slice the bok choy, peel and slice the carrot into thin rounds, and break the cauliflower and broccoli into small florets.\n"
            "2. Mince the garlic and slice the onion thinly.\n"
            "3. Dissolve the cornstarch in 4 tablespoons of cold water and set aside.\n"
            "4. Heat a wok over high heat with a tablespoon of oil and saute the garlic and onion for 1 minute until fragrant.\n"
            "5. Add the carrot and cauliflower first, as they take longest to cook, and stir-fry for 3 minutes.\n"
            "6. Add the broccoli and bok choy and stir-fry for another 2 minutes until the leaves are just wilted but still crisp.\n"
            "7. Pour in the oyster sauce with half a cup of water and toss everything together.\n"
            "8. Stir in the cornstarch mix and cook for 1 minute until the sauce turns glossy and coats the vegetables.\n"
            "9. Season with salt and white pepper and serve immediately while the vegetables are still crunchy."
        ),
        "categories": ["Main Dishes", "Vegetarian"],
        "type": "Dinner",
        "origin": "Indonesia",
        "tags": ["capcay", "veggies", "low calorie", "vegetarian"],
        "ingredients": [
            ["Bok choy", "300 g"],
            ["Carrot", "1 pc"],
            ["Broccoli", "150 g"],
            ["Cauliflower", "150 g"],
            ["Garlic", "3 cloves"],
            ["Onion", "1 pc"],
            ["Oyster sauce", "2 tbsp"],
            ["Cornstarch", "1 tbsp"],
        ],
        "attachment": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600&h=600&fit=crop&crop=entropy&q=80",
        "nutrition": {
            "serving_per_container": 3,
            "serving_size": "3 plates",
            "calories": 180.00,
            "total_fat": 7.00,
            "total_carbohydrate": 24.00,
            "total_sugar": 6.00,
            "cholesterol": 0.00,
            "protein": 6.00,
            "vitamin_d": 0.00,
            "sodium": 520.00,
            "calcium": 110.00,
            "potassium": 480.00,
            "iron": 1.90,
        },
    },
    {
        "author": "expert_ria",
        "title": "Sup Ayam Jahe",
        "description": "A warm, aromatic Indonesian ginger chicken soup loaded with vegetables and herbs.",
        "nutriscore": 5,
        "cooktime": 40,
        "complexity": "Medium",
        "servings": 4,
        "budget": "$",
        "instruction": (
            "1. Peel and grate a 30 g piece of ginger and thinly slice the garlic.\n"
            "2. Cut the chicken breast into bite-sized chunks and season lightly with salt and pepper.\n"
            "3. Heat a pot over medium heat with a little oil and saute the ginger and garlic for 2 minutes until fragrant.\n"
            "4. Add the chicken and stir until it turns opaque on all sides.\n"
            "5. Pour in the chicken stock, bring to a boil, then lower the heat and simmer for 15 minutes, skimming off any foam.\n"
            "6. Slice the carrot into thin rounds and add them, cooking for another 5 minutes.\n"
            "7. Add the bok choy and cook for 3 more minutes until just tender.\n"
            "8. Season the broth with salt, pepper and a good squeeze of lime to balance the ginger heat.\n"
            "9. Ladle into bowls and finish with chopped scallions and cracked black pepper."
        ),
        "categories": ["Main Dishes", "Soups"],
        "type": "Dinner",
        "origin": "Indonesia",
        "tags": ["soup", "chicken", "ginger", "immunity"],
        "ingredients": [
            ["Chicken breast", "300 g"],
            ["Ginger", "30 g"],
            ["Garlic", "4 cloves"],
            ["Chicken stock", "1 L"],
            ["Carrot", "1 pc"],
            ["Bok choy", "200 g"],
            ["Lime", "1 pc"],
        ],
        "attachment": "https://images.unsplash.com/photo-1604152135912-04a022e23696?w=600&h=600&fit=crop&crop=entropy&q=80",
        "nutrition": {
            "serving_per_container": 4,
            "serving_size": "4 bowls",
            "calories": 210.00,
            "total_fat": 5.00,
            "total_carbohydrate": 18.00,
            "total_sugar": 4.00,
            "cholesterol": 55.00,
            "protein": 24.00,
            "vitamin_d": 0.30,
            "sodium": 610.00,
            "calcium": 60.00,
            "potassium": 520.00,
            "iron": 1.50,
        },
    },
    {
        "author": "chef_andre",
        "title": "Rendang Tahu Tempe",
        "description": "A rich, smoky vegan rendang with tofu and tempeh simmered in coconut milk and aromatic spices.",
        "nutriscore": 4,
        "cooktime": 60,
        "complexity": "Hard",
        "servings": 4,
        "budget": "$$",
        "instruction": (
            "1. Cut the tempeh and tofu into chunky cubes and pan-fry them in a little oil until golden on all sides, about 5 minutes, then set aside.\n"
            "2. Make the spice paste: blitz the shallots, garlic, red chilies and ginger in a food processor with a splash of water until smooth.\n"
            "3. Heat a tablespoon of oil in a heavy pot and cook the spice paste over medium heat for 5 minutes until it is fragrant and darkens.\n"
            "4. Add the fried tempeh and tofu and toss to coat them in the paste.\n"
            "5. Pour in the coconut milk and sweet soy sauce, then season with salt.\n"
            "6. Bring to a gentle simmer, then reduce the heat to low and cook uncovered for 35-40 minutes.\n"
            "7. Stir occasionally so the coconut milk does not stick to the bottom of the pot.\n"
            "8. As the sauce reduces it will turn thick, oily and deeply caramelized.\n"
            "9. Taste and adjust seasoning, then serve with steamed rice and pickled vegetables."
        ),
        "categories": ["Main Dishes", "Vegetarian"],
        "type": "Dinner",
        "origin": "Indonesia",
        "tags": ["rendang", "tempeh", "tofu", "vegan"],
        "ingredients": [
            ["Tempeh", "200 g"],
            ["Tofu", "200 g"],
            ["Coconut milk", "400 ml"],
            ["Red chili", "3 pcs"],
            ["Garlic", "4 cloves"],
            ["Onion", "2 pcs"],
            ["Ginger", "30 g"],
            ["Sweet soy sauce", "2 tbsp"],
        ],
        "attachment": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=600&h=600&fit=crop&crop=entropy&q=80",
        "nutrition": {
            "serving_per_container": 4,
            "serving_size": "4 plates",
            "calories": 380.00,
            "total_fat": 24.00,
            "total_carbohydrate": 30.00,
            "total_sugar": 8.00,
            "cholesterol": 0.00,
            "protein": 19.00,
            "vitamin_d": 0.00,
            "sodium": 430.00,
            "calcium": 150.00,
            "potassium": 470.00,
            "iron": 3.10,
        },
    },
    {
        "author": "expert_ria",
        "title": "Gado-Gado",
        "description": "A refreshing Indonesian salad of blanched vegetables, tofu and egg, drenched in creamy peanut sauce.",
        "nutriscore": 4,
        "cooktime": 25,
        "complexity": "Easy",
        "servings": 2,
        "budget": "$",
        "instruction": (
            "1. Boil the potatoes until fork-tender, about 15 minutes, then cool and slice thickly.\n"
            "2. Hard-boil the eggs for 9 minutes, cool in ice water, peel and quarter them.\n"
            "3. Cut the tofu into slabs and pan-fry until golden on both sides.\n"
            "4. Briefly blanch the cabbage, bean sprouts and carrot in boiling water for about a minute, then drain well.\n"
            "5. Make the sauce: whisk the peanut butter with warm water, sweet soy sauce, lime juice and a little chili into a pourable dressing.\n"
            "6. Arrange the vegetables, potatoes, tofu and eggs on a plate.\n"
            "7. Drizzle generously with the peanut sauce.\n"
            "8. Top with crispy fried shallots and serve at room temperature."
        ),
        "categories": ["Vegetarian", "Salads"],
        "type": "Lunch",
        "origin": "Indonesia",
        "tags": ["salad", "peanut sauce", "vegetarian", "indonesian"],
        "ingredients": [
            ["Potato", "2 pcs"],
            ["Egg", "2 pcs"],
            ["Tofu", "150 g"],
            ["Cabbage", "200 g"],
            ["Bean sprouts", "150 g"],
            ["Carrot", "1 pc"],
            ["Peanut butter", "3 tbsp"],
            ["Sweet soy sauce", "1 tbsp"],
            ["Lime", "1 pc"],
            ["Fried shallots", "1 tbsp"],
        ],
        "attachment": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=600&h=600&fit=crop&crop=entropy&q=80",
        "nutrition": {
            "serving_per_container": 2,
            "serving_size": "2 plates",
            "calories": 430.00,
            "total_fat": 20.00,
            "total_carbohydrate": 52.00,
            "total_sugar": 12.00,
            "cholesterol": 95.00,
            "protein": 18.00,
            "vitamin_d": 1.10,
            "sodium": 380.00,
            "calcium": 120.00,
            "potassium": 660.00,
            "iron": 2.40,
        },
    },
    {
        "author": "chef_andre",
        "title": "Telur Balado",
        "description": "Boiled eggs simmered in a fiery red chili and shallot sambal — a bold Minangkabau classic.",
        "nutriscore": 3,
        "cooktime": 30,
        "complexity": "Medium",
        "servings": 2,
        "budget": "$",
        "instruction": (
            "1. Boil the eggs for 10 minutes, transfer them to ice water, then peel them carefully.\n"
            "2. Lightly score the eggs and pan-fry them in a little oil until golden and crisp all over.\n"
            "3. Blitz the red chilies, garlic, shallots and tomato into a coarse sambal paste.\n"
            "4. Fry the paste in oil over medium heat for 5-7 minutes, stirring often, until it darkens and the oil starts to separate.\n"
            "5. Season the sambal with salt and a squeeze of lime.\n"
            "6. Add the fried eggs and toss gently so they are coated in the sambal.\n"
            "7. Stir in the sweet soy sauce, toss once more and simmer for 2 minutes.\n"
            "8. Serve hot with steamed rice and raw cucumber slices."
        ),
        "categories": ["Main Dishes", "Breakfast"],
        "type": "Dinner",
        "origin": "Indonesia",
        "tags": ["eggs", "balado", "spicy", "indonesian"],
        "ingredients": [
            ["Egg", "4 pcs"],
            ["Red chili", "4 pcs"],
            ["Garlic", "3 cloves"],
            ["Onion", "3 pcs"],
            ["Tomato", "1 pc"],
            ["Sweet soy sauce", "1 tbsp"],
            ["Lime", "1 pc"],
        ],
        "attachment": "https://images.unsplash.com/photo-1506976785307-8732e854ad03?w=600&h=600&fit=crop&crop=entropy&q=80",
        "nutrition": {
            "serving_per_container": 2,
            "serving_size": "2 plates",
            "calories": 320.00,
            "total_fat": 19.00,
            "total_carbohydrate": 16.00,
            "total_sugar": 7.00,
            "cholesterol": 370.00,
            "protein": 20.00,
            "vitamin_d": 2.20,
            "sodium": 410.00,
            "calcium": 80.00,
            "potassium": 340.00,
            "iron": 2.00,
        },
    },
    {
        "author": "expert_ria",
        "title": "Banana Oat Pancakes",
        "description": "Fluffy three-ingredient pancakes made from ripe banana, oats and egg — naturally sweet and gluten-free.",
        "nutriscore": 4,
        "cooktime": 15,
        "complexity": "Easy",
        "servings": 2,
        "budget": "$",
        "instruction": (
            "1. In a blender, combine the ripe bananas, rolled oats, eggs, baking powder and cinnamon.\n"
            "2. Blend until smooth, scraping down the sides once, then rest the batter for 5 minutes to thicken.\n"
            "3. Heat a non-stick pan over medium heat and lightly grease it.\n"
            "4. Pour 1/4 cup of batter per pancake.\n"
            "5. Cook for 2-3 minutes until the edges look set and bubbles appear on the surface.\n"
            "6. Flip and cook for another 1-2 minutes until golden brown.\n"
            "7. Keep the finished pancakes warm in a low oven while you cook the rest.\n"
            "8. Stack and top with sliced banana, a drizzle of honey and a dusting of cinnamon."
        ),
        "categories": ["Breakfast"],
        "type": "Brunch",
        "origin": "United States",
        "tags": ["pancakes", "banana", "oats", "fluffy"],
        "ingredients": [
            ["Ripe banana", "2 pcs"],
            ["Rolled oats", "1 cup"],
            ["Egg", "2 pcs"],
            ["Baking powder", "1 tsp"],
            ["Cinnamon", "1 tsp"],
            ["Honey", "1 tbsp"],
        ],
        "attachment": "https://images.unsplash.com/photo-1528207776546-365bb710ee93?w=600&h=600&fit=crop&crop=entropy&q=80",
        "nutrition": {
            "serving_per_container": 2,
            "serving_size": "2 portions",
            "calories": 350.00,
            "total_fat": 8.00,
            "total_carbohydrate": 58.00,
            "total_sugar": 22.00,
            "cholesterol": 165.00,
            "protein": 14.00,
            "vitamin_d": 1.00,
            "sodium": 220.00,
            "calcium": 90.00,
            "potassium": 480.00,
            "iron": 2.20,
        },
    },
    {
        "author": "chef_andre",
        "title": "Grilled Chicken Caesar Salad",
        "description": "Charred chicken breast over crisp romaine with parmesan, croutons and a light caesar dressing.",
        "nutriscore": 4,
        "cooktime": 25,
        "complexity": "Easy",
        "servings": 2,
        "budget": "$$",
        "instruction": (
            "1. Pound the chicken breast to an even thickness and season with salt, pepper and a drizzle of olive oil.\n"
            "2. Preheat a grill pan over high heat and grill the chicken for 4-5 minutes per side until charred and cooked through.\n"
            "3. Rest the chicken for 5 minutes, then slice it against the grain.\n"
            "4. Wash and dry the romaine, then tear it into bite-sized pieces.\n"
            "5. Toss the lettuce with the caesar dressing so every leaf is lightly coated.\n"
            "6. Add the croutons and most of the shaved parmesan, and toss once more.\n"
            "7. Lay the sliced chicken on top.\n"
            "8. Finish with the remaining parmesan, a squeeze of lemon and cracked black pepper."
        ),
        "categories": ["Salads", "Main Dishes"],
        "type": "Lunch",
        "origin": "United States",
        "tags": ["caesar", "chicken", "salad", "high protein"],
        "ingredients": [
            ["Chicken breast", "300 g"],
            ["Romaine lettuce", "1 pc"],
            ["Parmesan cheese", "40 g"],
            ["Croutons", "1 cup"],
            ["Caesar dressing", "3 tbsp"],
            ["Lemon", "1 pc"],
            ["Olive oil", "1 tbsp"],
        ],
        "attachment": "https://images.unsplash.com/photo-1550304943-4f24f54ddde9?w=600&h=600&fit=crop&crop=entropy&q=80",
        "nutrition": {
            "serving_per_container": 2,
            "serving_size": "2 plates",
            "calories": 390.00,
            "total_fat": 19.00,
            "total_carbohydrate": 16.00,
            "total_sugar": 4.00,
            "cholesterol": 105.00,
            "protein": 38.00,
            "vitamin_d": 0.50,
            "sodium": 620.00,
            "calcium": 190.00,
            "potassium": 560.00,
            "iron": 2.10,
        },
    },
    {
        "author": "chef_andre",
        "title": "Thai Green Veggie Curry",
        "description": "A fragrant coconut green curry brimming with crisp seasonal vegetables and tofu.",
        "nutriscore": 5,
        "cooktime": 30,
        "complexity": "Medium",
        "servings": 3,
        "budget": "$$",
        "instruction": (
            "1. Press and cube the tofu, then pan-fry it until golden on all sides and set aside.\n"
            "2. Warm the thick coconut cream in a pot over medium heat until the oil begins to separate.\n"
            "3. Add the green curry paste and fry for 2 minutes until intensely fragrant.\n"
            "4. Pour in the remaining coconut milk and bring to a gentle simmer.\n"
            "5. Add the green beans and bell pepper in large chunks and cook for 5 minutes.\n"
            "6. Stir in the fried tofu.\n"
            "7. Season with soy sauce, a pinch of sugar and kaffir lime leaves.\n"
            "8. Finish with a handful of basil leaves and remove from the heat.\n"
            "9. Serve over steamed jasmine rice with lime wedges."
        ),
        "categories": ["Main Dishes", "Vegetarian"],
        "type": "Dinner",
        "origin": "Thailand",
        "tags": ["curry", "thai", "coconut milk", "vegetarian"],
        "ingredients": [
            ["Green curry paste", "2 tbsp"],
            ["Coconut milk", "400 ml"],
            ["Tofu", "200 g"],
            ["Bell pepper", "1 pc"],
            ["Green beans", "150 g"],
            ["Basil", "20 g"],
            ["Soy sauce", "1 tbsp"],
        ],
        "attachment": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=600&h=600&fit=crop&crop=entropy&q=80",
        "nutrition": {
            "serving_per_container": 3,
            "serving_size": "3 bowls",
            "calories": 340.00,
            "total_fat": 23.00,
            "total_carbohydrate": 22.00,
            "total_sugar": 8.00,
            "cholesterol": 0.00,
            "protein": 12.00,
            "vitamin_d": 0.00,
            "sodium": 500.00,
            "calcium": 140.00,
            "potassium": 450.00,
            "iron": 2.60,
        },
    },
    {
        "author": "expert_ria",
        "title": "Tuna Avocado Rice Bowl",
        "description": "A colorful poke-style bowl with seared tuna, creamy avocado, crunchy veggies and sesame rice.",
        "nutriscore": 5,
        "cooktime": 20,
        "complexity": "Easy",
        "servings": 2,
        "budget": "$$$",
        "instruction": (
            "1. Cook the sushi rice, then fold in a splash of rice vinegar and a pinch of salt; keep it warm.\n"
            "2. Slice the tuna into thick strips and season with a little soy sauce and sesame.\n"
            "3. Sear the tuna in a very hot oiled pan for 45 seconds per side for a rare center, then slice thinly.\n"
            "4. Slice the avocado, cucumber and carrot into matchsticks.\n"
            "5. Build the bowls: a base of warm rice, then arrange the tuna, avocado, cucumber and carrot in sections.\n"
            "6. Drizzle generously with soy sauce.\n"
            "7. Scatter with toasted sesame seeds and a few scallions.\n"
            "8. Serve immediately."
        ),
        "categories": ["Main Dishes", "Seafood"],
        "type": "Lunch",
        "origin": "Japan",
        "tags": ["tuna", "poke", "avocado", "bowl"],
        "ingredients": [
            ["Tuna steak", "250 g"],
            ["Sushi rice", "1 cup"],
            ["Avocado", "1 pc"],
            ["Cucumber", "1 pc"],
            ["Carrot", "1 pc"],
            ["Soy sauce", "2 tbsp"],
            ["Sesame seeds", "1 tbsp"],
            ["Olive oil", "1 tbsp"],
        ],
        "attachment": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=600&h=600&fit=crop&crop=entropy&q=80",
        "nutrition": {
            "serving_per_container": 2,
            "serving_size": "2 bowls",
            "calories": 420.00,
            "total_fat": 14.00,
            "total_carbohydrate": 45.00,
            "total_sugar": 5.00,
            "cholesterol": 35.00,
            "protein": 31.00,
            "vitamin_d": 2.30,
            "sodium": 540.00,
            "calcium": 70.00,
            "potassium": 700.00,
            "iron": 2.30,
        },
    },
    {
        "author": "expert_ria",
        "title": "Berry Smoothie Bowl",
        "description": "A thick, spoonable smoothie bowl blended with frozen berries and yogurt, topped with granola and fresh fruit.",
        "nutriscore": 4,
        "cooktime": 10,
        "complexity": "Easy",
        "servings": 1,
        "budget": "$",
        "instruction": (
            "1. Add the frozen mixed berries, frozen banana, Greek yogurt and a splash of almond milk to a blender.\n"
            "2. Blend in short pulses, scraping down the sides, until the mixture is thick and spoonable.\n"
            "3. Do not over-blend — the base should hold a swirl.\n"
            "4. Pour the smoothie into a chilled bowl.\n"
            "5. Arrange the granola, sliced banana, extra berries and a drizzle of honey on top.\n"
            "6. Finish with a sprinkle of chia seeds.\n"
            "7. Serve immediately before it melts."
        ),
        "categories": ["Breakfast", "Drinks"],
        "type": "Brunch",
        "origin": "United States",
        "tags": ["smoothie bowl", "berries", "antioxidant", "breakfast"],
        "ingredients": [
            ["Frozen mixed berries", "200 g"],
            ["Frozen banana", "1 pc"],
            ["Greek yogurt", "150 g"],
            ["Almond milk", "0.5 cup"],
            ["Granola", "0.5 cup"],
            ["Honey", "1 tsp"],
        ],
        "attachment": "https://images.unsplash.com/photo-1511690743698-d9d85f2fbf38?w=600&h=600&fit=crop&crop=entropy&q=80",
        "nutrition": {
            "serving_per_container": 1,
            "serving_size": "1 bowl",
            "calories": 380.00,
            "total_fat": 8.00,
            "total_carbohydrate": 66.00,
            "total_sugar": 36.00,
            "cholesterol": 5.00,
            "protein": 15.00,
            "vitamin_d": 1.40,
            "sodium": 120.00,
            "calcium": 180.00,
            "potassium": 520.00,
            "iron": 2.10,
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