
from agentic_profile_matching.adapters.db.db import Database
from agentic_profile_matching.adapters.db.models.embedding_1536 import Embedding1536Model
from agentic_profile_matching.app.utils.container import Container
from agentic_profile_matching.core.ports.vector_store import VectorStore
from sqlalchemy import select


class PGVectorStore(VectorStore[Embedding1536Model]):

    def __init__(self):
        self.database = Container.resolve(Database)

    def read(self, embedding: Embedding1536Model) -> list[Embedding1536Model]:
        stmt = (
            select(Embedding1536Model)
            .order_by(
                Embedding1536Model.embedding.cosine_distance(embedding.embedding) # type: ignore
            )
            .limit(50)
        )

        with self.database.get_session() as session:
            return list(session.execute(stmt).scalars().all())

    def insert(self, embeddings: list[Embedding1536Model]) -> bool:
        try:
            print("Embeddings to insert:", len(embeddings))

            with self.database.get_session() as session:
                session.add_all(embeddings)
                session.commit()

            return True

        except Exception as e:
            print("Insert failed:", e)
            raise