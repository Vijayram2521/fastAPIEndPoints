"""initial migration

Revision ID: 14b6f12d4996
Revises: d063289a2a88
Create Date: 2024-11-16 23:28:31.870734

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14b6f12d4996'
down_revision = 'd063289a2a88'
branch_labels = None
depends_on = None



def upgrade() -> None:
    # Check and drop indexes if they exist
    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'ix_symptom_symptom_name') THEN
                DROP INDEX ix_symptom_symptom_name;
            END IF;
        END $$;
    """)

    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'ix_symptom_symptom_code') THEN
                DROP INDEX ix_symptom_symptom_code;
            END IF;
        END $$;
    """)

    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'ix_business_business_name') THEN
                DROP INDEX ix_business_business_name;
            END IF;
        END $$;
    """)

    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'ix_business_business_id') THEN
                DROP INDEX ix_business_business_id;
            END IF;
        END $$;
    """)

    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'ix_diagnostic_business_id') THEN
                DROP INDEX ix_diagnostic_business_id;
            END IF;
        END $$;
    """)

    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'ix_diagnostic_symptom_code') THEN
                DROP INDEX ix_diagnostic_symptom_code;
            END IF;
        END $$;
    """)

    # Check and drop tables if they exist
    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'business') THEN
                DROP TABLE business;
            END IF;
        END $$;
    """)

    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'symptom') THEN
                DROP TABLE symptom;
            END IF;
        END $$;
    """)

    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'diagnostic') THEN
                DROP TABLE diagnostic;
            END IF;
        END $$;
    """)

    # Create the symptom table
    op.create_table(
        'symptom',
        sa.Column('symptom_code', sa.String(), nullable=False),
        sa.Column('symptom_name', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('symptom_code', name='symptom_pkey'),
        sa.UniqueConstraint('symptom_name', name='uq_symptom_name')
    )
    op.create_index('ix_symptom_symptom_name', 'symptom', ['symptom_name'])
    op.create_index('ix_symptom_symptom_code', 'symptom', ['symptom_code'])

    # Create the business table
    op.create_table(
        'business',
        sa.Column('business_id', sa.Integer(), nullable=False),
        sa.Column('business_name', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('business_id', name='business_pkey'),
        sa.UniqueConstraint('business_name', name='uq_business_name')
    )
    op.create_index('ix_business_business_name', 'business', ['business_name'])
    op.create_index('ix_business_business_id', 'business', ['business_id'])

    # Create the diagnostic table
    op.create_table(
        'diagnostic',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('business_id', sa.Integer(), nullable=True),
        sa.Column('symptom_code', sa.String(), nullable=True),
        sa.Column('diagnostic_value', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['business_id'], ['business.business_id'], name='fk_diagnostic_business'),
        sa.ForeignKeyConstraint(['symptom_code'], ['symptom.symptom_code'], name='fk_diagnostic_symptom'),
        sa.PrimaryKeyConstraint('id', name='diagnostic_pkey')
    )
    op.create_index('ix_diagnostic_business_id', 'diagnostic', ['business_id'])
    op.create_index('ix_diagnostic_symptom_code', 'diagnostic', ['symptom_code'])


def downgrade() -> None:
    # Drop the diagnostic table
    op.drop_table('diagnostic')

    # Drop the business table
    op.drop_table('business')

    # Drop the symptom table
    op.drop_table('symptom')

    # Drop the indexes if they exist
    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'ix_diagnostic_business_id') THEN
                DROP INDEX ix_diagnostic_business_id;
            END IF;
        END $$;
    """)

    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'ix_diagnostic_symptom_code') THEN
                DROP INDEX ix_diagnostic_symptom_code;
            END IF;
        END $$;
    """)

    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'ix_business_business_id') THEN
                DROP INDEX ix_business_business_id;
            END IF;
        END $$;
    """)

    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'ix_business_business_name') THEN
                DROP INDEX ix_business_business_name;
            END IF;
        END $$;
    """)

    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'ix_symptom_symptom_code') THEN
                DROP INDEX ix_symptom_symptom_code;
            END IF;
        END $$;
    """)

    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'ix_symptom_symptom_name') THEN
                DROP INDEX ix_symptom_symptom_name;
            END IF;
        END $$;
    """)

