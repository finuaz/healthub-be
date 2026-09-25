"""add profile detail indexes

Revision ID: f8b0116e8db7
Revises: 7f4cb4a716b7
Create Date: 2026-09-25 12:00:00.000000

Backs the aggregate counts and social lookup used by the public profile-detail
endpoints (GET /users/<id>, GET /users/<username>) and the follower/followed
collection lists. Without these the correlated COUNT subqueries and the
selectinload on Socials user_id are sequential scans.
"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "f8b0116e8db7"
down_revision = "7f4cb4a716b7"
branch_labels = None
depends_on = None


INDEXES = (
    ("ix_following_follower", "Following", ["follower_id"]),
    ("ix_following_followed", "Following", ["followed_id"]),
    ("ix_socials_user", "Socials", ["user_id"]),
    ("ix_recipe_author", "Recipe", ["author_id"]),
)


def upgrade():
    for index_name, table_name, columns in INDEXES:
        op.create_index(
            index_name,
            table_name,
            columns,
            unique=False,
            if_not_exists=True,
        )


def downgrade():
    for index_name, table_name, _columns in reversed(INDEXES):
        op.drop_index(index_name, table_name=table_name, if_exists=True)
