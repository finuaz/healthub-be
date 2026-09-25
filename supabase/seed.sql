-- HealthHub seed data for Supabase (PostgreSQL)
-- Requires tables to exist first (run `flask db upgrade` via the app).
-- Safe to re-run: rows that already exist (unique/PK conflict) are skipped.

SET statement_timeout = 0;

-- ---------------------------------------------------------------
-- Users (one per role) - password for all: Healthub123!
-- ---------------------------------------------------------------
INSERT INTO "User"
  (id, username, first_name, last_name, email, password, image, role, bio, phone, location, view_count)
VALUES
  (1, 'chef_andre', 'Andre', 'Wijaya', 'chef@healthub.io',
   '$pbkdf2-sha512$25000$KkXo3dsbIyQkBEAoJWSM8Q$zPm0eNoY9WELiGb8UL77E1sa2YnnbUmhpk7jpeE2ggVwfKJgO0Z5Tjg8JOmHxFUSxaHGyd86cM0hde2qX5piCw',
   'https://placehold.co/200x200?text=Chef+Andre', 'CHEF'::userrole,
   'Professional chef crafting delicious yet healthy recipes.', '081234567801', 'Jakarta, ID', 0),
  (2, 'admin_healthub', 'Budi', 'Santoso', 'admin@healthub.io',
   '$pbkdf2-sha512$25000$KkXo3dsbIyQkBEAoJWSM8Q$zPm0eNoY9WELiGb8UL77E1sa2YnnbUmhpk7jpeE2ggVwfKJgO0Z5Tjg8JOmHxFUSxaHGyd86cM0hde2qX5piCw',
   'https://placehold.co/200x200?text=Admin', 'ADMIN'::userrole,
   'Platform admin keeping HealthHub running smoothly.', '081234567802', 'Surabaya, ID', 0),
  (3, 'expert_ria', 'Ria', 'Puspita', 'expert@healthub.io',
   '$pbkdf2-sha512$25000$KkXo3dsbIyQkBEAoJWSM8Q$zPm0eNoY9WELiGb8UL77E1sa2YnnbUmhpk7jpeE2ggVwfKJgO0Z5Tjg8JOmHxFUSxaHGyd86cM0hde2qX5piCw',
   'https://placehold.co/200x200?text=Ria', 'EXPERT'::userrole,
   'Registered dietitian and nutrition expert.', '081234567803', 'Bandung, ID', 0),
  (4, 'user_demo', 'Dewi', 'Lestari', 'user@healthub.io',
   '$pbkdf2-sha512$25000$KkXo3dsbIyQkBEAoJWSM8Q$zPm0eNoY9WELiGb8UL77E1sa2YnnbUmhpk7jpeE2ggVwfKJgO0Z5Tjg8JOmHxFUSxaHGyd86cM0hde2qX5piCw',
   'https://placehold.co/200x200?text=Dewi', 'USER'::userrole,
   'Foodie on a healthy journey.', '081234567804', 'Denpasar, ID', 0)
ON CONFLICT (username) DO NOTHING;

-- ---------------------------------------------------------------
-- Recipe domain lookups (unique names)
-- ---------------------------------------------------------------
INSERT INTO "Category" (id, category) VALUES
  (1, 'Main Dishes'), (2, 'Rice'), (3, 'Seafood'), (4, 'Breakfast'),
  (5, 'Vegetarian'), (6, 'Salads'), (7, 'Drinks'), (8, 'Soups')
ON CONFLICT (category) DO NOTHING;

INSERT INTO "Type" (id, type) VALUES
  (1, 'Dinner'), (2, 'Brunch'), (3, 'Lunch'), (4, 'Snack')
ON CONFLICT (type) DO NOTHING;

INSERT INTO "Origin" (id, origin) VALUES
  (1, 'Indonesia'), (2, 'Norway'), (3, 'United States'), (4, 'Peru'), (5, 'Japan'), (6, 'Thailand')
ON CONFLICT (origin) DO NOTHING;

INSERT INTO "Tag" (id, tagname) VALUES
  (1, 'rice'), (2, 'fried rice'), (3, 'umami'), (4, 'indonesian'),
  (5, 'salmon'), (6, 'omega-3'), (7, 'grilled'), (8, 'high protein'),
  (9, 'vegan'), (10, 'oats'), (11, 'berries'), (12, 'no cook'),
  (13, 'vegetarian'), (14, 'quinoa'), (15, 'bowl'), (16, 'meal prep'),
  (17, 'matcha'), (18, 'protein'), (19, 'smoothie'), (20, 'post workout'),
  (21, 'capcay'), (22, 'veggies'), (23, 'low calorie'), (24, 'soup'),
  (25, 'chicken'), (26, 'ginger'), (27, 'immunity'), (28, 'rendang'),
  (29, 'tempeh'), (30, 'tofu'), (31, 'peanut sauce'), (32, 'eggs'),
  (33, 'balado'), (34, 'spicy'), (35, 'pancakes'), (36, 'banana'),
  (37, 'fluffy'), (38, 'caesar'), (39, 'curry'), (40, 'thai'),
  (41, 'coconut milk'), (42, 'tuna'), (43, 'poke'), (44, 'avocado'),
  (45, 'antioxidant'), (46, 'smoothie bowl'), (47, 'breakfast'), (48, 'salad')
ON CONFLICT (tagname) DO NOTHING;

-- ---------------------------------------------------------------
-- Ingredients
-- ---------------------------------------------------------------
INSERT INTO "Ingredient" (id, ingredient, ingredient_image) VALUES
  (1, 'Brown rice', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-indian-cuisine-spice-mix-curry-powder-food-age-reversing-nutrition-ayurveda-creating-radi-5b7ba6e00461f8.418255421534830304018.png'),
  (2, 'Egg', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-herbalism-therapy-herbal-tonic-medicine-spice-5abb76950594b8.6884587515222350290229.png'),
  (3, 'Chicken breast', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-organic-food-vegetable-carrot-5ae2b63ea38993.9311661015248072306699.png'),
  (4, 'Carrot', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-spice-masala-indian-cuisine-nutmeg-turmeric-spices-5b17857fbed319.5587043615282681597816.png'),
  (5, 'Garlic', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-vegetable-portable-network-graphics-fruit-clip-art-baking-needs-5cbf3c93326f43.1363482015560367552066.png'),
  (6, 'Sweet soy sauce', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-allspice-herb-food-spice-mix-spices-5abd2b9718b375.3009980215223469031012.png'),
  (7, 'Salmon fillet', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-indian-cuisine-spice-mix-curry-powder-food-age-reversing-nutrition-ayurveda-creating-radi-5b7ba6e00461f8.418255421534830304018.png'),
  (8, 'Quinoa', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-herbalism-therapy-herbal-tonic-medicine-spice-5abb76950594b8.6884587515222350290229.png'),
  (9, 'Broccoli', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-organic-food-vegetable-carrot-5ae2b63ea38993.9311661015248072306699.png'),
  (10, 'Olive oil', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-spice-masala-indian-cuisine-nutmeg-turmeric-spices-5b17857fbed319.5587043615282681597816.png'),
  (11, 'Lemon', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-vegetable-portable-network-graphics-fruit-clip-art-baking-needs-5cbf3c93326f43.1363482015560367552066.png'),
  (12, 'Rolled oats', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-allspice-herb-food-spice-mix-spices-5abd2b9718b375.3009980215223469031012.png'),
  (13, 'Almond milk', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-indian-cuisine-spice-mix-curry-powder-food-age-reversing-nutrition-ayurveda-creating-radi-5b7ba6e00461f8.418255421534830304018.png'),
  (14, 'Chia seeds', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-herbalism-therapy-herbal-tonic-medicine-spice-5abb76950594b8.6884587515222350290229.png'),
  (15, 'Mixed berries', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-organic-food-vegetable-carrot-5ae2b63ea38993.9311661015248072306699.png'),
  (16, 'Honey', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-spice-masala-indian-cuisine-nutmeg-turmeric-spices-5b17857fbed319.5587043615282681597816.png'),
  (17, 'Chickpeas', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-vegetable-portable-network-graphics-fruit-clip-art-baking-needs-5cbf3c93326f43.1363482015560367552066.png'),
  (18, 'Avocado', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-allspice-herb-food-spice-mix-spices-5abd2b9718b375.3009980215223469031012.png'),
  (19, 'Cherry tomatoes', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-indian-cuisine-spice-mix-curry-powder-food-age-reversing-nutrition-ayurveda-creating-radi-5b7ba6e00461f8.418255421534830304018.png'),
  (20, 'Mixed greens', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-herbalism-therapy-herbal-tonic-medicine-spice-5abb76950594b8.6884587515222350290229.png'),
  (21, 'Tahini dressing', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-organic-food-vegetable-carrot-5ae2b63ea38993.9311661015248072306699.png'),
  (22, 'Matcha powder', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-spice-masala-indian-cuisine-nutmeg-turmeric-spices-5b17857fbed319.5587043615282681597816.png'),
  (23, 'Banana', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-vegetable-portable-network-graphics-fruit-clip-art-baking-needs-5cbf3c93326f43.1363482015560367552066.png'),
  (24, 'Greek yogurt', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-allspice-herb-food-spice-mix-spices-5abd2b9718b375.3009980215223469031012.png'),
  (25, 'Oat milk', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-indian-cuisine-spice-mix-curry-powder-food-age-reversing-nutrition-ayurveda-creating-radi-5b7ba6e00461f8.418255421534830304018.png'),
  (26, 'Bok choy', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-herbalism-therapy-herbal-tonic-medicine-spice-5abb76950594b8.6884587515222350290229.png'),
  (27, 'Cauliflower', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-organic-food-vegetable-carrot-5ae2b63ea38993.9311661015248072306699.png'),
  (28, 'Onion', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-spice-masala-indian-cuisine-nutmeg-turmeric-spices-5b17857fbed319.5587043615282681597816.png'),
  (29, 'Oyster sauce', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-vegetable-portable-network-graphics-fruit-clip-art-baking-needs-5cbf3c93326f43.1363482015560367552066.png'),
  (30, 'Cornstarch', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-allspice-herb-food-spice-mix-spices-5abd2b9718b375.3009980215223469031012.png'),
  (31, 'Ginger', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-indian-cuisine-spice-mix-curry-powder-food-age-reversing-nutrition-ayurveda-creating-radi-5b7ba6e00461f8.418255421534830304018.png'),
  (32, 'Chicken stock', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-herbalism-therapy-herbal-tonic-medicine-spice-5abb76950594b8.6884587515222350290229.png'),
  (33, 'Lime', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-organic-food-vegetable-carrot-5ae2b63ea38993.9311661015248072306699.png'),
  (34, 'Tempeh', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-spice-masala-indian-cuisine-nutmeg-turmeric-spices-5b17857fbed319.5587043615282681597816.png'),
  (35, 'Tofu', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-vegetable-portable-network-graphics-fruit-clip-art-baking-needs-5cbf3c93326f43.1363482015560367552066.png'),
  (36, 'Coconut milk', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-allspice-herb-food-spice-mix-spices-5abd2b9718b375.3009980215223469031012.png'),
  (37, 'Red chili', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-indian-cuisine-spice-mix-curry-powder-food-age-reversing-nutrition-ayurveda-creating-radi-5b7ba6e00461f8.418255421534830304018.png'),
  (38, 'Potato', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-herbalism-therapy-herbal-tonic-medicine-spice-5abb76950594b8.6884587515222350290229.png'),
  (39, 'Cabbage', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-organic-food-vegetable-carrot-5ae2b63ea38993.9311661015248072306699.png'),
  (40, 'Bean sprouts', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-spice-masala-indian-cuisine-nutmeg-turmeric-spices-5b17857fbed319.5587043615282681597816.png'),
  (41, 'Peanut butter', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-vegetable-portable-network-graphics-fruit-clip-art-baking-needs-5cbf3c93326f43.1363482015560367552066.png'),
  (42, 'Fried shallots', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-allspice-herb-food-spice-mix-spices-5abd2b9718b375.3009980215223469031012.png'),
  (43, 'Tomato', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-indian-cuisine-spice-mix-curry-powder-food-age-reversing-nutrition-ayurveda-creating-radi-5b7ba6e00461f8.418255421534830304018.png'),
  (44, 'Ripe banana', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-herbalism-therapy-herbal-tonic-medicine-spice-5abb76950594b8.6884587515222350290229.png'),
  (45, 'Baking powder', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-organic-food-vegetable-carrot-5ae2b63ea38993.9311661015248072306699.png'),
  (46, 'Cinnamon', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-spice-masala-indian-cuisine-nutmeg-turmeric-spices-5b17857fbed319.5587043615282681597816.png'),
  (47, 'Romaine lettuce', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-vegetable-portable-network-graphics-fruit-clip-art-baking-needs-5cbf3c93326f43.1363482015560367552066.png'),
  (48, 'Parmesan cheese', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-allspice-herb-food-spice-mix-spices-5abd2b9718b375.3009980215223469031012.png'),
  (49, 'Croutons', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-indian-cuisine-spice-mix-curry-powder-food-age-reversing-nutrition-ayurveda-creating-radi-5b7ba6e00461f8.418255421534830304018.png'),
  (50, 'Caesar dressing', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-herbalism-therapy-herbal-tonic-medicine-spice-5abb76950594b8.6884587515222350290229.png'),
  (51, 'Green curry paste', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-organic-food-vegetable-carrot-5ae2b63ea38993.9311661015248072306699.png'),
  (52, 'Bell pepper', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-spice-masala-indian-cuisine-nutmeg-turmeric-spices-5b17857fbed319.5587043615282681597816.png'),
  (53, 'Green beans', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-vegetable-portable-network-graphics-fruit-clip-art-baking-needs-5cbf3c93326f43.1363482015560367552066.png'),
  (54, 'Basil', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-allspice-herb-food-spice-mix-spices-5abd2b9718b375.3009980215223469031012.png'),
  (55, 'Tuna steak', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-indian-cuisine-spice-mix-curry-powder-food-age-reversing-nutrition-ayurveda-creating-radi-5b7ba6e00461f8.418255421534830304018.png'),
  (56, 'Sushi rice', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-herbalism-therapy-herbal-tonic-medicine-spice-5abb76950594b8.6884587515222350290229.png'),
  (57, 'Cucumber', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-organic-food-vegetable-carrot-5ae2b63ea38993.9311661015248072306699.png'),
  (58, 'Soy sauce', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-spice-masala-indian-cuisine-nutmeg-turmeric-spices-5b17857fbed319.5587043615282681597816.png'),
  (59, 'Sesame seeds', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-vegetable-portable-network-graphics-fruit-clip-art-baking-needs-5cbf3c93326f43.1363482015560367552066.png'),
  (60, 'Frozen mixed berries', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-allspice-herb-food-spice-mix-spices-5abd2b9718b375.3009980215223469031012.png'),
  (61, 'Frozen banana', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-indian-cuisine-spice-mix-curry-powder-food-age-reversing-nutrition-ayurveda-creating-radi-5b7ba6e00461f8.418255421534830304018.png'),
  (62, 'Granola', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-herbalism-therapy-herbal-tonic-medicine-spice-5abb76950594b8.6884587515222350290229.png')
ON CONFLICT DO NOTHING;

-- ---------------------------------------------------------------
-- Recipes
-- ---------------------------------------------------------------
INSERT INTO "Recipe"
  (id, author_id, title, description, nutriscore, cooktime, complexity, servings, budget, instruction, view_count)
VALUES
  (1, 1, 'Nasi Goreng Sehat',
   'A healthier take on the classic Indonesian fried rice, packed with vegetables and lean protein.',
   4, 25, 'Medium', 2, '$',
   E'1. Cook the brown rice according to the package and spread it on a tray to cool completely — cold rice makes the best fried rice.\n2. Mince the garlic and slice the carrot into thin half-moons.\n3. Cut the chicken breast into small bite-sized cubes and season with a pinch of salt.\n4. Heat a wok over high heat with a little oil and saute the garlic and carrot for 1 minute until fragrant.\n5. Add the chicken and stir-fry for 3-4 minutes until golden and cooked through.\n6. Push everything to one side, crack in the egg, scramble it, then mix it through the chicken.\n7. Add the cooled rice and toss over high heat for 2 minutes so every grain is coated.\n8. Season with sweet soy sauce, a splash of fish sauce and white pepper.\n9. Stir-fry for another minute, then serve with sliced cucumber and tomatoes.', 0),
  (2, 1, 'Grilled Salmon with Quinoa',
   'Perfectly grilled salmon fillet served over fluffy quinoa with steamed broccoli.',
   5, 30, 'Easy', 1, '$$',
   E'1. Pat the salmon fillet dry and season both sides with salt, black pepper and a squeeze of lemon.\n2. Let it rest at room temperature for 10 minutes so it cooks evenly.\n3. Rinse the quinoa and cook it in twice its volume of water for about 15 minutes, then fluff with a fork.\n4. Cut the broccoli into small florets and steam it for 4-5 minutes until bright green and tender.\n5. Heat a grill pan over medium-high heat and lightly oil the surface.\n6. Grill the salmon skin-side down for 4 minutes without moving it.\n7. Flip and cook for 3 more minutes for a medium center; rest for 2 minutes.\n8. Mound the quinoa on a plate, top with the salmon and broccoli.\n9. Drizzle with olive oil and a final squeeze of lemon before serving.', 0),
  (3, 3, 'Berry Overnight Oats',
   'No-cook overnight oats layered with chia seeds and fresh berries. Perfect meal prep.',
   4, 10, 'Easy', 2, '$',
   E'1. In a bowl, whisk together the rolled oats, almond milk, chia seeds and honey.\n2. Stir in half of the berries, crushing them lightly so their juices tint the mix.\n3. Divide the mixture evenly between two jars or glasses.\n4. Cover and refrigerate for at least 6 hours, preferably overnight.\n5. In the morning, give each jar a quick stir to loosen the pudding.\n6. If it looks too thick, loosen with a splash of almond milk.\n7. Top generously with the remaining fresh berries and a sprinkle of chia seeds.\n8. Serve cold straight from the fridge.', 0),
  (4, 2, 'Quinoa Power Bowl',
   'A colorful vegetarian bowl with quinoa, chickpeas, avocado and tahini dressing.',
   5, 20, 'Easy', 2, '$$',
   E'1. Rinse the quinoa well, then cook it in twice its volume of salted water for about 15 minutes.\n2. Let the quinoa cool slightly so it stays fluffy.\n3. Rinse and drain the chickpeas, patting them dry on a towel.\n4. Halve the cherry tomatoes and chop the greens coarsely.\n5. Cut the avocado in half, remove the pit and slice thinly.\n6. In a bowl, toss the chickpeas, tomatoes and greens with a squeeze of lemon and a pinch of salt.\n7. Divide the quinoa between two bowls and pile the veggie mix on top.\n8. Fan out the avocado slices on each bowl.\n9. Drizzle everything generously with the tahini dressing and finish with sesame seeds.', 0),
  (5, 4, 'Matcha Protein Smoothie',
   'Energizing green smoothie with matcha, banana and Greek yogurt for a post-workout boost.',
   4, 5, 'Easy', 1, '$',
   E'1. Peel the banana and break it into chunks; freeze it briefly with the oat milk for a frostier drink.\n2. Add the frozen banana, oat milk, Greek yogurt, matcha powder and honey to a blender.\n3. Blend on high for 45-60 seconds until completely smooth and frothy.\n4. Pause, scrape down the sides and give it one more quick blitz.\n5. Taste and adjust the matcha, honey or milk to your preference.\n6. Pour into a tall glass over ice if you like it extra cold.\n7. Dust the top with a pinch of extra matcha.\n8. Enjoy immediately — it is best straight from the blender.', 0),
  (6, 1, 'Capcay Sayur',
   'Crisp stir-fried vegetables in a light, savory garlic sauce — a quick and nutritious Indonesian favorite.',
   5, 20, 'Easy', 3, '$',
   E'1. Wash and slice the bok choy, peel and slice the carrot into thin rounds, and break the cauliflower and broccoli into small florets.\n2. Mince the garlic and slice the onion thinly.\n3. Dissolve the cornstarch in 4 tablespoons of cold water and set aside.\n4. Heat a wok over high heat with a tablespoon of oil and saute the garlic and onion for 1 minute until fragrant.\n5. Add the carrot and cauliflower first, as they take longest to cook, and stir-fry for 3 minutes.\n6. Add the broccoli and bok choy and stir-fry for another 2 minutes until the leaves are just wilted but still crisp.\n7. Pour in the oyster sauce with half a cup of water and toss everything together.\n8. Stir in the cornstarch mix and cook for 1 minute until the sauce turns glossy and coats the vegetables.\n9. Season with salt and white pepper and serve immediately while the vegetables are still crunchy.', 0),
  (7, 3, 'Sup Ayam Jahe',
   'A warm, aromatic Indonesian ginger chicken soup loaded with vegetables and herbs.',
   5, 40, 'Medium', 4, '$',
   E'1. Peel and grate a 30 g piece of ginger and thinly slice the garlic.\n2. Cut the chicken breast into bite-sized chunks and season lightly with salt and pepper.\n3. Heat a pot over medium heat with a little oil and saute the ginger and garlic for 2 minutes until fragrant.\n4. Add the chicken and stir until it turns opaque on all sides.\n5. Pour in the chicken stock, bring to a boil, then lower the heat and simmer for 15 minutes, skimming off any foam.\n6. Slice the carrot into thin rounds and add them, cooking for another 5 minutes.\n7. Add the bok choy and cook for 3 more minutes until just tender.\n8. Season the broth with salt, pepper and a good squeeze of lime to balance the ginger heat.\n9. Ladle into bowls and finish with chopped scallions and cracked black pepper.', 0),
  (8, 1, 'Rendang Tahu Tempe',
   'A rich, smoky vegan rendang with tofu and tempeh simmered in coconut milk and aromatic spices.',
   4, 60, 'Hard', 4, '$$',
   E'1. Cut the tempeh and tofu into chunky cubes and pan-fry them in a little oil until golden on all sides, about 5 minutes, then set aside.\n2. Make the spice paste: blitz the shallots, garlic, red chilies and ginger in a food processor with a splash of water until smooth.\n3. Heat a tablespoon of oil in a heavy pot and cook the spice paste over medium heat for 5 minutes until it is fragrant and darkens.\n4. Add the fried tempeh and tofu and toss to coat them in the paste.\n5. Pour in the coconut milk and sweet soy sauce, then season with salt.\n6. Bring to a gentle simmer, then reduce the heat to low and cook uncovered for 35-40 minutes.\n7. Stir occasionally so the coconut milk does not stick to the bottom of the pot.\n8. As the sauce reduces it will turn thick, oily and deeply caramelized.\n9. Taste and adjust seasoning, then serve with steamed rice and pickled vegetables.', 0),
  (9, 3, 'Gado-Gado',
   'A refreshing Indonesian salad of blanched vegetables, tofu and egg, drenched in creamy peanut sauce.',
   4, 25, 'Easy', 2, '$',
   E'1. Boil the potatoes until fork-tender, about 15 minutes, then cool and slice thickly.\n2. Hard-boil the eggs for 9 minutes, cool in ice water, peel and quarter them.\n3. Cut the tofu into slabs and pan-fry until golden on both sides.\n4. Briefly blanch the cabbage, bean sprouts and carrot in boiling water for about a minute, then drain well.\n5. Make the sauce: whisk the peanut butter with warm water, sweet soy sauce, lime juice and a little chili into a pourable dressing.\n6. Arrange the vegetables, potatoes, tofu and eggs on a plate.\n7. Drizzle generously with the peanut sauce.\n8. Top with crispy fried shallots and serve at room temperature.', 0),
  (10, 1, 'Telur Balado',
   'Boiled eggs simmered in a fiery red chili and shallot sambal — a bold Minangkabau classic.',
   3, 30, 'Medium', 2, '$',
   E'1. Boil the eggs for 10 minutes, transfer them to ice water, then peel them carefully.\n2. Lightly score the eggs and pan-fry them in a little oil until golden and crisp all over.\n3. Blitz the red chilies, garlic, shallots and tomato into a coarse sambal paste.\n4. Fry the paste in oil over medium heat for 5-7 minutes, stirring often, until it darkens and the oil starts to separate.\n5. Season the sambal with salt and a squeeze of lime.\n6. Add the fried eggs and toss gently so they are coated in the sambal.\n7. Stir in the sweet soy sauce, toss once more and simmer for 2 minutes.\n8. Serve hot with steamed rice and raw cucumber slices.', 0),
  (11, 3, 'Banana Oat Pancakes',
   'Fluffy three-ingredient pancakes made from ripe banana, oats and egg — naturally sweet and gluten-free.',
   4, 15, 'Easy', 2, '$',
   E'1. In a blender, combine the ripe bananas, rolled oats, eggs, baking powder and cinnamon.\n2. Blend until smooth, scraping down the sides once, then rest the batter for 5 minutes to thicken.\n3. Heat a non-stick pan over medium heat and lightly grease it.\n4. Pour 1/4 cup of batter per pancake.\n5. Cook for 2-3 minutes until the edges look set and bubbles appear on the surface.\n6. Flip and cook for another 1-2 minutes until golden brown.\n7. Keep the finished pancakes warm in a low oven while you cook the rest.\n8. Stack and top with sliced banana, a drizzle of honey and a dusting of cinnamon.', 0),
  (12, 1, 'Grilled Chicken Caesar Salad',
   'Charred chicken breast over crisp romaine with parmesan, croutons and a light caesar dressing.',
   4, 25, 'Easy', 2, '$$',
   E'1. Pound the chicken breast to an even thickness and season with salt, pepper and a drizzle of olive oil.\n2. Preheat a grill pan over high heat and grill the chicken for 4-5 minutes per side until charred and cooked through.\n3. Rest the chicken for 5 minutes, then slice it against the grain.\n4. Wash and dry the romaine, then tear it into bite-sized pieces.\n5. Toss the lettuce with the caesar dressing so every leaf is lightly coated.\n6. Add the croutons and most of the shaved parmesan, and toss once more.\n7. Lay the sliced chicken on top.\n8. Finish with the remaining parmesan, a squeeze of lemon and cracked black pepper.', 0),
  (13, 1, 'Thai Green Veggie Curry',
   'A fragrant coconut green curry brimming with crisp seasonal vegetables and tofu.',
   5, 30, 'Medium', 3, '$$',
   E'1. Press and cube the tofu, then pan-fry it until golden on all sides and set aside.\n2. Warm the thick coconut cream in a pot over medium heat until the oil begins to separate.\n3. Add the green curry paste and fry for 2 minutes until intensely fragrant.\n4. Pour in the remaining coconut milk and bring to a gentle simmer.\n5. Add the green beans and bell pepper in large chunks and cook for 5 minutes.\n6. Stir in the fried tofu.\n7. Season with soy sauce, a pinch of sugar and kaffir lime leaves.\n8. Finish with a handful of basil leaves and remove from the heat.\n9. Serve over steamed jasmine rice with lime wedges.', 0),
  (14, 3, 'Tuna Avocado Rice Bowl',
   'A colorful poke-style bowl with seared tuna, creamy avocado, crunchy veggies and sesame rice.',
   5, 20, 'Easy', 2, '$$$',
   E'1. Cook the sushi rice, then fold in a splash of rice vinegar and a pinch of salt; keep it warm.\n2. Slice the tuna into thick strips and season with a little soy sauce and sesame.\n3. Sear the tuna in a very hot oiled pan for 45 seconds per side for a rare center, then slice thinly.\n4. Slice the avocado, cucumber and carrot into matchsticks.\n5. Build the bowls: a base of warm rice, then arrange the tuna, avocado, cucumber and carrot in sections.\n6. Drizzle generously with soy sauce.\n7. Scatter with toasted sesame seeds and a few scallions.\n8. Serve immediately.', 0),
  (15, 3, 'Berry Smoothie Bowl',
   'A thick, spoonable smoothie bowl blended with frozen berries and yogurt, topped with granola and fresh fruit.',
   4, 10, 'Easy', 1, '$',
   E'1. Add the frozen mixed berries, frozen banana, Greek yogurt and a splash of almond milk to a blender.\n2. Blend in short pulses, scraping down the sides, until the mixture is thick and spoonable.\n3. Do not over-blend — the base should hold a swirl.\n4. Pour the smoothie into a chilled bowl.\n5. Arrange the granola, sliced banana, extra berries and a drizzle of honey on top.\n6. Finish with a sprinkle of chia seeds.\n7. Serve immediately before it melts.', 0)
ON CONFLICT (title) DO NOTHING;

-- ---------------------------------------------------------------
-- Recipe relations (categories, type, origin, tags, ingredients)
-- ---------------------------------------------------------------
INSERT INTO "Recipe_category" (recipe_id, category_id) VALUES
  (1, 1), (1, 2), (2, 3), (2, 1), (3, 4), (4, 5), (4, 6), (5, 7),
  (6, 1), (6, 5), (7, 1), (7, 8), (8, 1), (8, 5), (9, 5), (9, 6),
  (10, 1), (10, 4), (11, 4), (12, 6), (12, 1), (13, 1), (13, 5),
  (14, 1), (14, 3), (15, 4), (15, 7)
ON CONFLICT DO NOTHING;

INSERT INTO "Recipe_type" (recipe_id, type_id) VALUES
  (1, 1), (2, 1), (3, 2), (4, 3), (5, 4),
  (6, 1), (7, 1), (8, 1), (9, 3), (10, 1), (11, 2), (12, 3), (13, 1), (14, 3), (15, 2)
ON CONFLICT DO NOTHING;

INSERT INTO "Recipe_origin" (recipe_id, origin_id) VALUES
  (1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
  (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 3), (12, 3), (13, 6), (14, 5), (15, 3)
ON CONFLICT DO NOTHING;

INSERT INTO "Recipe_tag" (recipe_id, tag_id) VALUES
  (1, 1), (1, 2), (1, 3), (1, 4),
  (2, 5), (2, 6), (2, 7), (2, 8),
  (3, 9), (3, 10), (3, 11), (3, 12),
  (4, 13), (4, 14), (4, 15), (4, 16),
  (5, 17), (5, 18), (5, 19), (5, 20),
  (6, 21), (6, 22), (6, 23), (6, 13),
  (7, 24), (7, 25), (7, 26), (7, 27),
  (8, 28), (8, 29), (8, 30), (8, 9),
  (9, 48), (9, 31), (9, 13), (9, 4),
  (10, 32), (10, 33), (10, 34), (10, 4),
  (11, 35), (11, 36), (11, 10), (11, 37),
  (12, 38), (12, 25), (12, 48), (12, 8),
  (13, 39), (13, 40), (13, 41), (13, 13),
  (14, 42), (14, 43), (14, 44), (14, 15),
  (15, 46), (15, 11), (15, 45), (15, 47)
ON CONFLICT DO NOTHING;

INSERT INTO "Recipe_ingredient" (recipe_id, ingredient_id, amount) VALUES
  (1, 1, '2 cups'), (1, 2, '1 pc'), (1, 3, '150 g'), (1, 4, '1 pc'), (1, 5, '2 cloves'), (1, 6, '2 tbsp'),
  (2, 7, '200 g'), (2, 8, '1 cup'), (2, 9, '150 g'), (2, 10, '1 tbsp'), (2, 11, '1 pc'),
  (3, 12, '1 cup'), (3, 13, '1 cup'), (3, 14, '1 tbsp'), (3, 15, '150 g'), (3, 16, '1 tsp'),
  (4, 8, '1 cup'), (4, 17, '150 g'), (4, 18, '1 pc'), (4, 19, '100 g'), (4, 20, '2 cups'), (4, 21, '2 tbsp'),
  (5, 22, '1 tsp'), (5, 23, '1 pc'), (5, 24, '150 g'), (5, 25, '1 cup'), (5, 16, '1 tsp'),
  (6, 26, '300 g'), (6, 4, '1 pc'), (6, 9, '150 g'), (6, 27, '150 g'), (6, 5, '3 cloves'),
  (6, 28, '1 pc'), (6, 29, '2 tbsp'), (6, 30, '1 tbsp'),
  (7, 3, '300 g'), (7, 31, '30 g'), (7, 5, '4 cloves'), (7, 32, '1 L'), (7, 4, '1 pc'),
  (7, 26, '200 g'), (7, 33, '1 pc'),
  (8, 34, '200 g'), (8, 35, '200 g'), (8, 36, '400 ml'), (8, 37, '3 pcs'), (8, 5, '4 cloves'),
  (8, 28, '2 pcs'), (8, 31, '30 g'), (8, 6, '2 tbsp'),
  (9, 38, '2 pcs'), (9, 2, '2 pcs'), (9, 35, '150 g'), (9, 39, '200 g'), (9, 40, '150 g'),
  (9, 4, '1 pc'), (9, 41, '3 tbsp'), (9, 6, '1 tbsp'), (9, 33, '1 pc'), (9, 42, '1 tbsp'),
  (10, 2, '4 pcs'), (10, 37, '4 pcs'), (10, 5, '3 cloves'), (10, 28, '3 pcs'), (10, 43, '1 pc'),
  (10, 6, '1 tbsp'), (10, 33, '1 pc'),
  (11, 44, '2 pcs'), (11, 12, '1 cup'), (11, 2, '2 pcs'), (11, 45, '1 tsp'), (11, 46, '1 tsp'),
  (11, 16, '1 tbsp'),
  (12, 3, '300 g'), (12, 47, '1 pc'), (12, 48, '40 g'), (12, 49, '1 cup'), (12, 50, '3 tbsp'),
  (12, 11, '1 pc'), (12, 10, '1 tbsp'),
  (13, 51, '2 tbsp'), (13, 36, '400 ml'), (13, 35, '200 g'), (13, 52, '1 pc'), (13, 53, '150 g'),
  (13, 54, '20 g'), (13, 58, '1 tbsp'),
  (14, 55, '250 g'), (14, 56, '1 cup'), (14, 18, '1 pc'), (14, 57, '1 pc'), (14, 4, '1 pc'),
  (14, 58, '2 tbsp'), (14, 59, '1 tbsp'), (14, 10, '1 tbsp'),
  (15, 60, '200 g'), (15, 61, '1 pc'), (15, 24, '150 g'), (15, 13, '0.5 cup'), (15, 62, '0.5 cup'),
  (15, 16, '1 tsp')
ON CONFLICT DO NOTHING;

-- ---------------------------------------------------------------
-- Attachments & Nutrition per recipe
-- ---------------------------------------------------------------
INSERT INTO "Attachment" (id, recipe_id, attachment_link) VALUES
  (1, 1, 'https://images.unsplash.com/photo-1512058564366-18510be2db19?w=600&h=600&fit=crop&crop=entropy&q=80'),
  (2, 2, 'https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=600&h=600&fit=crop&crop=entropy&q=80'),
  (3, 3, 'https://images.unsplash.com/photo-1517673132405-a56a62b18caf?w=600&h=600&fit=crop&crop=entropy&q=80'),
  (4, 4, 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600&h=600&fit=crop&crop=entropy&q=80'),
  (5, 5, 'https://images.unsplash.com/photo-1553530666-ba11a7da3888?w=600&h=600&fit=crop&crop=entropy&q=80'),
  (6, 6, 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600&h=600&fit=crop&crop=entropy&q=80'),
  (7, 7, 'https://images.unsplash.com/photo-1604152135912-04a022e23696?w=600&h=600&fit=crop&crop=entropy&q=80'),
  (8, 8, 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=600&h=600&fit=crop&crop=entropy&q=80'),
  (9, 9, 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=600&h=600&fit=crop&crop=entropy&q=80'),
  (10, 10, 'https://images.unsplash.com/photo-1506976785307-8732e854ad03?w=600&h=600&fit=crop&crop=entropy&q=80'),
  (11, 11, 'https://images.unsplash.com/photo-1528207776546-365bb710ee93?w=600&h=600&fit=crop&crop=entropy&q=80'),
  (12, 12, 'https://images.unsplash.com/photo-1550304943-4f24f54ddde9?w=600&h=600&fit=crop&crop=entropy&q=80'),
  (13, 13, 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=600&h=600&fit=crop&crop=entropy&q=80'),
  (14, 14, 'https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=600&h=600&fit=crop&crop=entropy&q=80'),
  (15, 15, 'https://images.unsplash.com/photo-1511690743698-d9d85f2fbf38?w=600&h=600&fit=crop&crop=entropy&q=80')
ON CONFLICT DO NOTHING;

INSERT INTO "Nutrition"
  (id, recipe_id, serving_per_container, serving_size, calories, total_fat, total_carbohydrate, total_sugar, cholesterol, protein, vitamin_d, sodium, calcium, potassium, iron)
VALUES
  (1, 1, 2, '2 bowls', 420.50, 12.00, 58.00, 9.00, 90.00, 22.00, 0.50, 480.00, 45.00, 320.00, 2.50),
  (2, 2, 1, '1 plate', 550.00, 25.00, 40.00, 6.00, 85.00, 42.00, 16.00, 240.00, 60.00, 890.00, 2.80),
  (3, 3, 2, '2 jars', 310.00, 9.00, 48.00, 14.00, 0.00, 11.00, 1.20, 70.00, 180.00, 240.00, 1.90),
  (4, 4, 2, '2 bowls', 480.00, 18.00, 62.00, 11.00, 0.00, 17.00, 0.00, 310.00, 90.00, 640.00, 3.20),
  (5, 5, 1, '1 glass', 290.00, 4.00, 40.00, 20.00, 5.00, 24.00, 2.00, 90.00, 200.00, 420.00, 1.10),
  (6, 6, 3, '3 plates', 180.00, 7.00, 24.00, 6.00, 0.00, 6.00, 0.00, 520.00, 110.00, 480.00, 1.90),
  (7, 7, 4, '4 bowls', 210.00, 5.00, 18.00, 4.00, 55.00, 24.00, 0.30, 610.00, 60.00, 520.00, 1.50),
  (8, 8, 4, '4 plates', 380.00, 24.00, 30.00, 8.00, 0.00, 19.00, 0.00, 430.00, 150.00, 470.00, 3.10),
  (9, 9, 2, '2 plates', 430.00, 20.00, 52.00, 12.00, 95.00, 18.00, 1.10, 380.00, 120.00, 660.00, 2.40),
  (10, 10, 2, '2 plates', 320.00, 19.00, 16.00, 7.00, 370.00, 20.00, 2.20, 410.00, 80.00, 340.00, 2.00),
  (11, 11, 2, '2 portions', 350.00, 8.00, 58.00, 22.00, 165.00, 14.00, 1.00, 220.00, 90.00, 480.00, 2.20),
  (12, 12, 2, '2 plates', 390.00, 19.00, 16.00, 4.00, 105.00, 38.00, 0.50, 620.00, 190.00, 560.00, 2.10),
  (13, 13, 3, '3 bowls', 340.00, 23.00, 22.00, 8.00, 0.00, 12.00, 0.00, 500.00, 140.00, 450.00, 2.60),
  (14, 14, 2, '2 bowls', 420.00, 14.00, 45.00, 5.00, 35.00, 31.00, 2.30, 540.00, 70.00, 700.00, 2.30),
  (15, 15, 1, '1 bowl', 380.00, 8.00, 66.00, 36.00, 5.00, 15.00, 1.40, 120.00, 180.00, 520.00, 2.10)
ON CONFLICT DO NOTHING;

-- ---------------------------------------------------------------
-- Socials, follows, likes, rates, comments
-- ---------------------------------------------------------------
INSERT INTO "Socials" (id, user_id, facebook, instagram, tiktok) VALUES
  (1, 1, 'https://facebook.com/andre.wijaya', 'https://instagram.com/chef.andre', NULL),
  (2, 3, NULL, 'https://instagram.com/ria.nutrition', 'https://tiktok.com/@ria.nutrition'),
  (3, 4, NULL, 'https://instagram.com/dewi.eats', NULL)
ON CONFLICT DO NOTHING;

INSERT INTO "Following" (id, follower_id, followed_id) VALUES
  (1, 4, 1), (2, 4, 3), (3, 4, 2), (4, 3, 1), (5, 2, 1), (6, 2, 3)
ON CONFLICT DO NOTHING;

INSERT INTO "Like" (id, user_id, recipe_id) VALUES
  (1, 4, 1), (2, 4, 2), (3, 4, 3), (4, 4, 5),
  (5, 1, 3), (6, 1, 5), (7, 3, 1), (8, 3, 2), (9, 2, 4)
ON CONFLICT DO NOTHING;

INSERT INTO "Rate" (id, user_id, recipe_id, value) VALUES
  (1, 4, 1, 4), (2, 4, 2, 5), (3, 4, 3, 5), (4, 4, 4, 4),
  (5, 3, 1, 5), (6, 3, 2, 5), (7, 3, 3, 4), (8, 3, 4, 5),
  (9, 2, 1, 4), (10, 2, 5, 4)
ON CONFLICT DO NOTHING;

INSERT INTO "Comment" (id, recipe_id, user_id, message) VALUES
  (1, 1, 4, 'Enyak dan sehat, wajib coba!'),
  (2, 2, 3, 'Perfect balance of protein and omega-3.'),
  (3, 3, 2, 'Staple for my meal prep every week.'),
  (4, 4, 4, 'Loved the tahini dressing.'),
  (5, 5, 1, 'Great post-workout pick-me-up.'),
  (6, 2, 4, 'Cooked this twice this week already.')
ON CONFLICT DO NOTHING;

-- ---------------------------------------------------------------
-- Advance SERIAL sequences so app-created rows never collide
-- ---------------------------------------------------------------
SELECT setval(pg_get_serial_sequence('"User"', 'id'), COALESCE(MAX(id), 1)) FROM "User";
SELECT setval(pg_get_serial_sequence('"Category"', 'id'), COALESCE(MAX(id), 1)) FROM "Category";
SELECT setval(pg_get_serial_sequence('"Type"', 'id'), COALESCE(MAX(id), 1)) FROM "Type";
SELECT setval(pg_get_serial_sequence('"Origin"', 'id'), COALESCE(MAX(id), 1)) FROM "Origin";
SELECT setval(pg_get_serial_sequence('"Tag"', 'id'), COALESCE(MAX(id), 1)) FROM "Tag";
SELECT setval(pg_get_serial_sequence('"Ingredient"', 'id'), COALESCE(MAX(id), 1)) FROM "Ingredient";
SELECT setval(pg_get_serial_sequence('"Recipe"', 'id'), COALESCE(MAX(id), 1)) FROM "Recipe";
SELECT setval(pg_get_serial_sequence('"Nutrition"', 'id'), COALESCE(MAX(id), 1)) FROM "Nutrition";
SELECT setval(pg_get_serial_sequence('"Attachment"', 'id'), COALESCE(MAX(id), 1)) FROM "Attachment";
SELECT setval(pg_get_serial_sequence('"Socials"', 'id'), COALESCE(MAX(id), 1)) FROM "Socials";
SELECT setval(pg_get_serial_sequence('"Following"', 'id'), COALESCE(MAX(id), 1)) FROM "Following";
SELECT setval(pg_get_serial_sequence('"Like"', 'id'), COALESCE(MAX(id), 1)) FROM "Like";
SELECT setval(pg_get_serial_sequence('"Rate"', 'id'), COALESCE(MAX(id), 1)) FROM "Rate";
SELECT setval(pg_get_serial_sequence('"Comment"', 'id'), COALESCE(MAX(id), 1)) FROM "Comment";