from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


class RAGService:
    def __init__(self, llm, embeddings, vector_store):

        self.embeddigns = embeddings
        self.llm = llm
        self.vector_store = vector_store

        # 2. Setup the Chain
        self.retriever = self.vector_store.as_retriever(
            search_kwargs={"k": 5}
        )  # Added threshold to filter irrelevant docs
        self.chain = self._build_chain()

    def _format_docs(self, docs):
        return "\n\n".join([d.page_content for d in docs])

    def _build_chain(self):
        template = """You are a helpful assistant assisting with document analysis.

        INSTRUCTIONS:
        1. Answer the question based on the following context. If the context is relevant but doesn't have a direct answer, provide the most related information and note that it's based on available data.
        2. If the answer is found in the context, be DETAILED and ELABORATIVE. Explain the "why" and "how" if the text supports it, but not too long.
        3. If the context has NO relevant information at all, respond with exactly: "I Don't Know".

        CONTEXT:
        {context}

        QUESTION:
        {question}
        """
        prompt = ChatPromptTemplate.from_template(template)

        return (
            {
                "context": self.retriever | self._format_docs,
                "question": RunnablePassthrough(),
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )

    def ask(self, query: str):
        if not query:
            return "Please provide a query."

        ans = self.chain.invoke(query)

        # if "i don't know" in ans.lower():
        #     return ""

        return ans


if __name__ == "__main__":
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    llm = ChatOllama(model="llama3.2", temperature=0.3)
    vector_store = Chroma(
        persist_directory="./Chroma_db",
        embedding_function=embeddings,
        collection_name="mixed_data_rag",
    )

    rag = RAGService(embeddings=embeddings, llm=llm, vector_store=vector_store)
    ans = rag.ask("Does tata motors produce commercial vehicles ?")
    print(f"ans = {ans}")
