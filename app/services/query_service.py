from app.services.rag_service import RAGService
from app.config import embeddings, llm, vector_store

from app.services.rag_user_service import RagUserService


def ask_llm(question: str) -> str:

    rag = RAGService(embeddings=embeddings, llm=llm, vector_store=vector_store)
    ans = rag.ask(question)

    return ans


def ask_llm_user(question: str, user_id: str) -> str:
    rag = RagUserService(
        llm=llm,
        vector_store=vector_store,
        embeddings=embeddings,
        user_id=user_id,
        top_k=5,
    )

    return rag.ask(question=question)
