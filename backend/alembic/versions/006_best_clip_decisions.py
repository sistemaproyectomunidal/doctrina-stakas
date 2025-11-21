"""Add BestClipDecisionModel

Revision ID: 006_best_clip_decisions
Revises: 005_publishing_engine
Create Date: 2025-11-21 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '006_best_clip_decisions'
down_revision = '005_publishing_engine'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create best_clip_decisions table
    op.create_table('best_clip_decisions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('video_asset_id', sa.UUID(), nullable=False),
        sa.Column('platform', sa.String(length=50), nullable=False),
        sa.Column('selected_clip_id', sa.Integer(), nullable=True),
        sa.Column('decision_data', sa.JSON(), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['selected_clip_id'], ['clips.id'], ),
        sa.ForeignKeyConstraint(['video_asset_id'], ['video_assets.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_best_clip_decisions_id'), 'best_clip_decisions', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_best_clip_decisions_id'), table_name='best_clip_decisions')
    op.drop_table('best_clip_decisions')
