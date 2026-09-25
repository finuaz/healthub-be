-- HealthHub schema (generated from SQLAlchemy models).
-- Apply to the hosted project with: supabase db push --linked

CREATE TYPE userrole AS ENUM ('USER', 'ADMIN', 'CHEF', 'EXPERT');


CREATE TABLE "Category" (
	id SERIAL NOT NULL, 
	category VARCHAR(20) NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (category)
);


CREATE TABLE "Ingredient" (
	id SERIAL NOT NULL, 
	ingredient TEXT NOT NULL, 
	ingredient_image VARCHAR, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id)
);


CREATE TABLE "Origin" (
	id SERIAL NOT NULL, 
	origin VARCHAR(20) NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (origin)
);


CREATE TABLE "Tag" (
	id SERIAL NOT NULL, 
	tagname VARCHAR(20) NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (tagname)
);


CREATE TABLE "Type" (
	id SERIAL NOT NULL, 
	type VARCHAR(20) NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (type)
);


CREATE TABLE "User" (
	id SERIAL NOT NULL, 
	username VARCHAR(25) NOT NULL, 
	first_name VARCHAR(20) NOT NULL, 
	last_name VARCHAR(20) NOT NULL, 
	email VARCHAR(60) NOT NULL, 
	password VARCHAR(255) NOT NULL, 
	new_password VARCHAR(255), 
	reset_password_question VARCHAR(255), 
	reset_password_answer VARCHAR(255), 
	image VARCHAR(255), 
	role userrole NOT NULL, 
	bio VARCHAR(300), 
	phone VARCHAR(15), 
	location VARCHAR(30), 
	view_count INTEGER, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (username), 
	UNIQUE (email)
);


CREATE TABLE "Following" (
	id SERIAL NOT NULL, 
	follower_id INTEGER NOT NULL, 
	followed_id INTEGER NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(follower_id) REFERENCES "User" (id), 
	FOREIGN KEY(followed_id) REFERENCES "User" (id)
);


CREATE TABLE "Recipe" (
	id SERIAL NOT NULL, 
	author_id INTEGER NOT NULL, 
	title VARCHAR(100) NOT NULL, 
	description VARCHAR(300) NOT NULL, 
	nutriscore INTEGER, 
	cooktime INTEGER NOT NULL, 
	complexity VARCHAR(20) NOT NULL, 
	servings INTEGER NOT NULL, 
	budget VARCHAR(20) NOT NULL, 
	instruction TEXT NOT NULL, 
	view_count INTEGER, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(author_id) REFERENCES "User" (id), 
	UNIQUE (title)
);


CREATE TABLE "Socials" (
	id SERIAL NOT NULL, 
	user_id INTEGER NOT NULL, 
	facebook VARCHAR(255), 
	instagram VARCHAR(255), 
	tiktok VARCHAR(255), 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES "User" (id)
);


CREATE TABLE "Attachment" (
	id SERIAL NOT NULL, 
	recipe_id INTEGER, 
	attachment_link VARCHAR(255) NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(recipe_id) REFERENCES "Recipe" (id)
);


CREATE TABLE "Comment" (
	id SERIAL NOT NULL, 
	recipe_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	message TEXT NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(recipe_id) REFERENCES "Recipe" (id), 
	FOREIGN KEY(user_id) REFERENCES "User" (id)
);


CREATE TABLE "Like" (
	id SERIAL NOT NULL, 
	user_id INTEGER, 
	recipe_id INTEGER, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES "User" (id), 
	FOREIGN KEY(recipe_id) REFERENCES "Recipe" (id)
);


CREATE TABLE "Nutrition" (
	id SERIAL NOT NULL, 
	recipe_id INTEGER, 
	serving_per_container INTEGER, 
	serving_size VARCHAR(20), 
	calories DECIMAL(10, 2), 
	total_fat DECIMAL(10, 2), 
	total_carbohydrate DECIMAL(10, 2), 
	total_sugar DECIMAL(10, 2), 
	cholesterol DECIMAL(10, 2), 
	protein DECIMAL(10, 2), 
	vitamin_d DECIMAL(10, 2), 
	sodium DECIMAL(10, 2), 
	calcium DECIMAL(10, 2), 
	potassium DECIMAL(10, 2), 
	iron DECIMAL(10, 2), 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(recipe_id) REFERENCES "Recipe" (id)
);


CREATE TABLE "Rate" (
	id SERIAL NOT NULL, 
	user_id INTEGER, 
	recipe_id INTEGER, 
	value INTEGER NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES "User" (id), 
	FOREIGN KEY(recipe_id) REFERENCES "Recipe" (id)
);


CREATE TABLE "Recipe_category" (
	recipe_id INTEGER NOT NULL, 
	category_id INTEGER NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (recipe_id, category_id), 
	FOREIGN KEY(recipe_id) REFERENCES "Recipe" (id), 
	FOREIGN KEY(category_id) REFERENCES "Category" (id)
);


CREATE TABLE "Recipe_ingredient" (
	recipe_id INTEGER NOT NULL, 
	ingredient_id INTEGER NOT NULL, 
	amount VARCHAR, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (recipe_id, ingredient_id), 
	FOREIGN KEY(recipe_id) REFERENCES "Recipe" (id), 
	FOREIGN KEY(ingredient_id) REFERENCES "Ingredient" (id)
);


CREATE TABLE "Recipe_origin" (
	recipe_id INTEGER NOT NULL, 
	origin_id INTEGER NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (recipe_id, origin_id), 
	FOREIGN KEY(recipe_id) REFERENCES "Recipe" (id), 
	FOREIGN KEY(origin_id) REFERENCES "Origin" (id)
);


CREATE TABLE "Recipe_tag" (
	recipe_id INTEGER NOT NULL, 
	tag_id INTEGER NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (recipe_id, tag_id), 
	FOREIGN KEY(recipe_id) REFERENCES "Recipe" (id), 
	FOREIGN KEY(tag_id) REFERENCES "Tag" (id)
);


CREATE TABLE "Recipe_type" (
	recipe_id INTEGER NOT NULL, 
	type_id INTEGER NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (recipe_id, type_id), 
	FOREIGN KEY(recipe_id) REFERENCES "Recipe" (id), 
	FOREIGN KEY(type_id) REFERENCES "Type" (id)
);
