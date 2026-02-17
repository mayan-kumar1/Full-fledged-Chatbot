from app.config import llm, vector_store, embeddings
from langchain_core.messages import SystemMessage, HumanMessage


class RagUserService:

    def __init__(self, llm, vector_store, embeddings, user_id, top_k=5) -> None:
        self.llm = llm
        self.vector_store = vector_store
        self.embeddings = embeddings

        self.retriever = vector_store.as_retriever(
            search_kwargs={"filter": {"user_id": user_id}, "k": top_k}
        )

        self.SYSTEM_PROMPT_TEMPLATE = """
        You are a knowledgeable, friendly assistant.
Answer the user's question based on the context provided below.

Important guidelines:
- Only use information from the provided context
- If the context doesn't contain relevant information, clearly state that
- Be concise and specific
- If you're uncertain, acknowledge it

Context:
{context}
        """

    def ask(self, question: str):
        docs = self.retriever.invoke(question)
        context = "\n\n".join(doc.page_content for doc in docs)
        system_prompt = self.SYSTEM_PROMPT_TEMPLATE.format(context=context)
        response = self.llm.invoke(
            [SystemMessage(content=system_prompt), HumanMessage(content=question)]
        )
        return response.content


if __name__ == "__main__":
    rag_user_service = RagUserService(
        llm=llm,
        embeddings=embeddings,
        vector_store=vector_store,
        user_id="58eff0a5-c29a-4020-9a40-06b0ad08c173",
        top_k=5,
    )
    ans = rag_user_service.ask(question="What technical skills are listed here ?")
    print(ans)
