from alembic import op
import sqlalchemy as sa
revision = '0001_baseline'
down_revision = None
branch_labels = None
depends_on = None
def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(255), unique=True, index=True),
        sa.Column('role', sa.String(32)),
        sa.Column('active', sa.Boolean, default=True),
        sa.Column('password_hash', sa.String(255), default=''),
    )
    op.create_table('templates',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('key', sa.String(128), unique=True, index=True),
        sa.Column('name', sa.String(255)),
        sa.Column('storage_key', sa.String(1024)),
        sa.Column('metadata_json', sa.JSON),
        sa.Column('created_at', sa.DateTime(timezone=True)),
    )
def downgrade():
    op.drop_table('templates')
    op.drop_table('users')
