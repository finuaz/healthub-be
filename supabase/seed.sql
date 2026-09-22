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
  (5, 'Vegetarian'), (6, 'Salads'), (7, 'Drinks')
ON CONFLICT (category) DO NOTHING;

INSERT INTO "Type" (id, type) VALUES
  (1, 'Dinner'), (2, 'Brunch'), (3, 'Lunch'), (4, 'Snack')
ON CONFLICT (type) DO NOTHING;

INSERT INTO "Origin" (id, origin) VALUES
  (1, 'Indonesia'), (2, 'Norway'), (3, 'United States'), (4, 'Peru'), (5, 'Japan')
ON CONFLICT (origin) DO NOTHING;

INSERT INTO "Tag" (id, tagname) VALUES
  (1, 'rice'), (2, 'fried rice'), (3, 'umami'), (4, 'indonesian'),
  (5, 'salmon'), (6, 'omega-3'), (7, 'grilled'), (8, 'high protein'),
  (9, 'vegan'), (10, 'oats'), (11, 'berries'), (12, 'no cook'),
  (13, 'vegetarian'), (14, 'quinoa'), (15, 'bowl'), (16, 'meal prep'),
  (17, 'matcha'), (18, 'protein'), (19, 'smoothie'), (20, 'post workout')
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
  (25, 'Oat milk', 'https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-indian-cuisine-spice-mix-curry-powder-food-age-reversing-nutrition-ayurveda-creating-radi-5b7ba6e00461f8.418255421534830304018.png')
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
   E'1. Cook the brown rice and let it cool.\n2. Saute garlic and carrot in a little oil until fragrant.\n3. Add chicken breast and cook until golden.\n4. Push to the side, scramble the egg, then mix in the rice.\n5. Season with sweet soy sauce, stir-fry for 2 minutes and serve.', 0),
  (2, 1, 'Grilled Salmon with Quinoa',
   'Perfectly grilled salmon fillet served over fluffy quinoa with steamed broccoli.',
   5, 30, 'Easy', 1, '$$',
   E'1. Season the salmon with salt, pepper and a squeeze of lemon.\n2. Grill skin-side down for 4 minutes, then flip and cook 3 more.\n3. Meanwhile cook quinoa per package instructions.\n4. Steam broccoli until bright green.\n5. Plate quinoa, top with salmon and broccoli, drizzle olive oil.', 0),
  (3, 3, 'Berry Overnight Oats',
   'No-cook overnight oats layered with chia seeds and fresh berries. Perfect meal prep.',
   4, 10, 'Easy', 2, '$',
   E'1. Mix rolled oats, almond milk and chia seeds in a jar.\n2. Stir in honey and half the berries.\n3. Cover and refrigerate overnight.\n4. Top with the remaining berries before serving.', 0),
  (4, 2, 'Quinoa Power Bowl',
   'A colorful vegetarian bowl with quinoa, chickpeas, avocado and tahini dressing.',
   5, 20, 'Easy', 2, '$$',
   E'1. Cook quinoa and let it cool slightly.\n2. Toss chickpeas, cherry tomatoes and greens together.\n3. Divide quinoa into two bowls and top with the veggie mix.\n4. Add sliced avocado and drizzle with tahini dressing.', 0),
  (5, 4, 'Matcha Protein Smoothie',
   'Energizing green smoothie with matcha, banana and Greek yogurt for a post-workout boost.',
   4, 5, 'Easy', 1, '$',
   E'1. Add all ingredients to a blender.\n2. Blend until completely smooth.\n3. Pour into a glass and enjoy immediately.', 0)
ON CONFLICT (title) DO NOTHING;

-- ---------------------------------------------------------------
-- Recipe relations (categories, type, origin, tags, ingredients)
-- ---------------------------------------------------------------
INSERT INTO "Recipe_category" (recipe_id, category_id) VALUES
  (1, 1), (1, 2), (2, 3), (2, 1), (3, 4), (4, 5), (4, 6), (5, 7)
ON CONFLICT DO NOTHING;

INSERT INTO "Recipe_type" (recipe_id, type_id) VALUES
  (1, 1), (2, 1), (3, 2), (4, 3), (5, 4)
ON CONFLICT DO NOTHING;

INSERT INTO "Recipe_origin" (recipe_id, origin_id) VALUES
  (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)
ON CONFLICT DO NOTHING;

INSERT INTO "Recipe_tag" (recipe_id, tag_id) VALUES
  (1, 1), (1, 2), (1, 3), (1, 4),
  (2, 5), (2, 6), (2, 7), (2, 8),
  (3, 9), (3, 10), (3, 11), (3, 12),
  (4, 13), (4, 14), (4, 15), (4, 16),
  (5, 17), (5, 18), (5, 19), (5, 20)
ON CONFLICT DO NOTHING;

INSERT INTO "Recipe_ingredient" (recipe_id, ingredient_id, amount) VALUES
  (1, 1, '2 cups'), (1, 2, '1 pc'), (1, 3, '150 g'), (1, 4, '1 pc'), (1, 5, '2 cloves'), (1, 6, '2 tbsp'),
  (2, 7, '200 g'), (2, 8, '1 cup'), (2, 9, '150 g'), (2, 10, '1 tbsp'), (2, 11, '1 pc'),
  (3, 12, '1 cup'), (3, 13, '1 cup'), (3, 14, '1 tbsp'), (3, 15, '150 g'), (3, 16, '1 tsp'),
  (4, 8, '1 cup'), (4, 17, '150 g'), (4, 18, '1 pc'), (4, 19, '100 g'), (4, 20, '2 cups'), (4, 21, '2 tbsp'),
  (5, 22, '1 tsp'), (5, 23, '1 pc'), (5, 24, '150 g'), (5, 25, '1 cup'), (5, 16, '1 tsp')
ON CONFLICT DO NOTHING;

-- ---------------------------------------------------------------
-- Attachments & Nutrition per recipe
-- ---------------------------------------------------------------
INSERT INTO "Attachment" (id, recipe_id, attachment_link) VALUES
  (1, 1, 'https://placehold.co/600x400?text=Nasi+Goreng+Sehat'),
  (2, 2, 'https://placehold.co/600x400?text=Grilled+Salmon'),
  (3, 3, 'https://placehold.co/600x400?text=Overnight+Oats'),
  (4, 4, 'https://placehold.co/600x400?text=Quinoa+Power+Bowl'),
  (5, 5, 'https://placehold.co/600x400?text=Matcha+Smoothie')
ON CONFLICT DO NOTHING;

INSERT INTO "Nutrition"
  (id, recipe_id, serving_per_container, serving_size, calories, total_fat, total_carbohydrate, total_sugar, cholesterol, protein, vitamin_d, sodium, calcium, potassium, iron)
VALUES
  (1, 1, 2, '2 bowls', 420.50, 12.00, 58.00, 9.00, 90.00, 22.00, 0.50, 480.00, 45.00, 320.00, 2.50),
  (2, 2, 1, '1 plate', 550.00, 25.00, 40.00, 6.00, 85.00, 42.00, 16.00, 240.00, 60.00, 890.00, 2.80),
  (3, 3, 2, '2 jars', 310.00, 9.00, 48.00, 14.00, 0.00, 11.00, 1.20, 70.00, 180.00, 240.00, 1.90),
  (4, 4, 2, '2 bowls', 480.00, 18.00, 62.00, 11.00, 0.00, 17.00, 0.00, 310.00, 90.00, 640.00, 3.20),
  (5, 5, 1, '1 glass', 290.00, 4.00, 40.00, 20.00, 5.00, 24.00, 2.00, 90.00, 200.00, 420.00, 1.10)
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