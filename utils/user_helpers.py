from sqlalchemy import func

from models import FollowingModel, RecipeModel, UserModel, SocialModel
from schemas import UserPublicProfileSchema


def serialize_user_list(users):
    if not users:
        return []

    user_ids = [user.id for user in users]
    following_counts = dict(
        FollowingModel.query.with_entities(
            FollowingModel.follower_id, func.count(FollowingModel.id)
        )
        .group_by(FollowingModel.follower_id)
        .all()
    )
    follower_counts = dict(
        FollowingModel.query.with_entities(
            FollowingModel.followed_id, func.count(FollowingModel.id)
        )
        .group_by(FollowingModel.followed_id)
        .all()
    )
    socials = {}
    for social in SocialModel.query.filter(SocialModel.user_id.in_(user_ids)).all():
        socials.setdefault(social.user_id, social)

    for user in users:
        user.total_following = following_counts.get(user.id, 0)
        user.total_follower = follower_counts.get(user.id, 0)
        social = socials.get(user.id)
        user.social_facebook = social.facebook if social else None
        user.social_instagram = social.instagram if social else None
        user.social_tiktok = social.tiktok if social else None

    return UserPublicProfileSchema(many=True).dump(users)


def count_following(user_id):
    total_following = FollowingModel.query.filter_by(follower_id=user_id).count()
    return total_following


def count_follower(user_id):
    total_follower = FollowingModel.query.filter_by(followed_id=user_id).count()
    return total_follower


def get_author_facebook(recipe_id):
    recipe = RecipeModel.query.filter_by(id=recipe_id).first()
    author = UserModel.query.filter_by(id=recipe.author_id).first()
    social = SocialModel.query.filter_by(user_id=author.id).first()
    if not social:
        return None

    return social.facebook if social.facebook else None


def get_author_instagram(recipe_id):
    recipe = RecipeModel.query.filter_by(id=recipe_id).first()
    author = UserModel.query.filter_by(id=recipe.author_id).first()
    social = SocialModel.query.filter_by(user_id=author.id).first()
    if not social:
        return None

    return social.instagram if social.instagram else None


def get_author_tiktok(recipe_id):
    recipe = RecipeModel.query.filter_by(id=recipe_id).first()
    author = UserModel.query.filter_by(id=recipe.author_id).first()
    social = SocialModel.query.filter_by(user_id=author.id).first()
    if not social:
        return None

    return social.tiktok if social.tiktok else None


def get_social_facebook(user_id):
    social = SocialModel.query.filter_by(user_id=user_id).first()
    if not social:
        return None

    return social.facebook


def get_social_instagram(user_id):
    social = SocialModel.query.filter_by(user_id=user_id).first()
    if not social:
        return None

    return social.instagram


def get_social_tiktok(user_id):
    social = SocialModel.query.filter_by(user_id=user_id).first()
    if not social:
        return None

    return social.tiktok
