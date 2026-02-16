from app.services.rag_service import RAGService
from app.config import embeddings, llm, vector_store


def ask_llm(question: str) -> str:

    rag = RAGService(embeddings=embeddings, llm=llm, vector_store=vector_store)
    ans = rag.ask(question)

    return ans
