from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils import EmailType

revision = __revid__
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user_credentials',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(255), nullable=False),
        sa.Column('email', EmailType, nullable=False),
        sa.Column('password', sa.LargeBinary, nullable = False)
    )

def downgrade():
    op.drop_table('user_credentials')
