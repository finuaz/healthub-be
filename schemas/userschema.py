from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from models.user import UserRole


class UserRegisterSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
    reset_password_question = fields.String(required=True)
    reset_password_answer = fields.String(required=True)
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class UserLoginSchema(Schema):
    id = fields.Integer(dump_only=True)
    username_or_email = fields.String(required=True)
    first_name = fields.String(required=False)
    last_name = fields.String(required=False)
    email = fields.String(required=False)
    password = fields.String(required=True, load_only=True)


class UserPublicProfileSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    image = fields.String()
    role = EnumField(UserRole, by_value=True)
    bio = fields.String()
    location = fields.String()
    total_following = fields.Integer()
    total_follower = fields.Integer()
    view_count = fields.Integer()
    social_facebook = fields.String()
    social_instagram = fields.String()
    social_tiktok = fields.String()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class UserGetProfileSchema(UserPublicProfileSchema):
    email = fields.String(required=True)
    phone = fields.String()


class UserProfileDetailSchema(UserPublicProfileSchema):
    total_recipe_count = fields.Integer()


class UserListSchema(UserPublicProfileSchema):
    pass


class UserGetFollowingFollower(Schema):
    following = fields.Integer()
    follower = fields.Integer()


class UserUpdateInfoSchema(Schema):
    id = fields.Integer(dump_only=True)
    first_name = fields.String()
    last_name = fields.String()
    bio = fields.String()
    phone = fields.String()
    location = fields.String()
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class UserUpdateImageSchema(Schema):
    id = fields.Integer(dump_only=True)
    image = fields.String()
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class UserResetPasswordSchema(Schema):
    id = fields.Integer(dump_only=True)
    password = fields.String(required=True, load_only=True)
    # reset_password_question = fields.String()
    reset_password_answer = fields.String()
    new_password = fields.String(required=True, load_only=True)
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class GetResetPasswordPackage(Schema):
    id = fields.Integer(dump_only=True)
    reset_password_question = fields.String()


class UserDeletionSchema(Schema):
    id = fields.Integer(dump_only=True)
    password = fields.String(required=True)


class UserFollowingSchema(Schema):
    id = fields.Integer(dump_only=True)
    follower_id = fields.Integer(required=True)
    followed_id = fields.Integer(required=True)
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
