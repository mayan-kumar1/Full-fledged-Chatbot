from app.services.injester import Loader
from app.services.rag_service import RAGService
from app.config import embeddings, llm, vector_store


def is_db_exists() -> bool:
    return False


def create_db() -> None:
    loader = Loader(embedding=embeddings)
    docs = loader.load_pdf(r"app\data\Resume.pdf")
    loader.create_vector_db(docs=docs)
    print("db created")


def main() -> None:

    if not is_db_exists():
        create_db()

    rag = RAGService(embeddings=embeddings, llm=llm, vector_store=vector_store)

    ans = rag.ask("What languages does this persons knows ?")
    print(f"ans = {ans}")


if __name__ == "__main__":
    main()
