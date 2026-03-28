from sqlalchemy import Column, Text, TIMESTAMP, func, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from pgvector.sqlalchemy import Vector  # type: ignore

from agentic_profile_matching.adapters.db.models.base import Base

class Embedding1536Model(Base):
    __tablename__ = "embedding_1536"

    id = Column(UUID(as_uuid=True), primary_key=True,
                server_default=text("gen_random_uuid()"))

    content = Column(Text)

    embedding = Column(Vector(1536)) # type: ignore

    metadata_ = Column("metadata", JSONB)

    created_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp()
    )