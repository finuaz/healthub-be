from models import FollowingModel, RecipeModel, UserModel, SocialModel


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
