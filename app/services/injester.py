from app.config import settings
from langchain_community.document_loaders import (
    PyPDFLoader,
    DirectoryLoader,
    UnstructuredPDFLoader,
)
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.utils import filter_complex_metadata

from app.utils.web_scrapper import WebScrapper
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
import os
import shutil
from uuid import UUID


class Loader:

    def __init__(self, embedding) -> None:

        self.chunk_size = settings.text_splitter.chunk_size
        self.chunk_overlap = settings.text_splitter.chunk_overlap
        self.separators = settings.text_splitter.separators
        self.embeddings_model = settings.embeddings.model_name

        self.embedding = embedding

    def load_pdf_dir(self, dir: str):
        loader = DirectoryLoader(dir, glob="./*.pdf", loader_cls=PyPDFLoader)  # type: ignore

        pdf_docs = loader.load()
        pdf_docsFiltered = filter_complex_metadata(pdf_docs)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )
        pdf_chunks = splitter.split_documents(pdf_docsFiltered)

        for doc in pdf_chunks:
            doc.metadata["source_type"] = "pdf_text"

        return pdf_chunks

    def load_pdf(self, pdf: str, file_name: str | None = None):
        loader = PyPDFLoader(pdf)  # type: ignore

        pdf_docs = loader.load()
        pdf_docsFiltered = filter_complex_metadata(pdf_docs)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )
        pdf_chunks = splitter.split_documents(pdf_docsFiltered)

        if file_name:
            for doc in pdf_chunks:
                doc.metadata["file_name"] = file_name

        return pdf_chunks

    def load_pdf_user_id(
        self, pdf: str, user_id: str | None, file_name: str | None = None
    ):
        loader = PyPDFLoader(pdf)  # type: ignore

        pdf_docs = loader.load()
        pdf_docsFiltered = filter_complex_metadata(pdf_docs)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )
        pdf_chunks = splitter.split_documents(pdf_docsFiltered)

        for doc in pdf_chunks:
            doc.metadata["user_id"] = user_id

            if file_name:
                doc.metadata["file_name"] = file_name

        return pdf_chunks

    def load_web(self, urls: list[str]):
        webScrapper = WebScrapper(urls=urls)
        allData = webScrapper.scrape_all_urls()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )

        web_chunks = splitter.create_documents(allData)

        return web_chunks

    def create_vector_db(self, docs) -> None:
        # embeddings = OllamaEmbeddings(model=self.embeddings_model)

        db = Chroma.from_documents(
            docs,
            self.embedding,
            collection_name="mixed_data_rag",
            persist_directory=settings.chroma_settings.persist_directory,
        )

    def update_db(self, pdf_dir, urls: list[str]) -> None:

        pdf_docs = self.load_pdf_dir(pdf_dir)
        print("PDFs loaded")
        web_docs = self.load_web(urls)
        print("Web data loaded")
        combined_docs = pdf_docs + web_docs
        print("creating db")
        self.create_vector_db(docs=combined_docs)
        print("db updated")

    @staticmethod
    def delete_db():
        if os.path.exists(settings.chroma_settings.persist_directory):
            shutil.rmtree(settings.chroma_settings.persist_directory)
            print("database deleted")


if __name__ == "__main__":
    print(settings.text_splitter.chunk_size)
    embeddings = OllamaEmbeddings(model=settings.embeddings.model_name)

    loader = Loader(embedding=embeddings)
    urls = [
        "https://www.tatamotors.com/careers/faqs",
        "https://www.tatamotors.com/corporate-responsibility/planet-resilience/",
        "https://www.tatamotors.com/careers/life-at-tml/",
        "https://www.tatamotors.com/newsroom/thought-leadership",
        "https://www.tatamotors.com/careers",
        "https://www.tatamotors.com/careers/kaushalya-earn-learn-program/",
        "https://www.tatamotors.com/corporate-responsibility/planet-resilience",
        "https://www.tatamotors.com/corporate-responsibility/governance/",
        "https://www.tatamotors.com/careers/openings/",
        "https://www.tatamotors.com/open-source-license-disclosure",
        "https://www.tatamotors.com/blog/a-smarter-vision-for-safer-roads-decoding-advanced-driver-assistance-systems-3/",
        "https://www.tatamotors.com/blog/new-era-for-indias-cv-landscape/",
        "https://www.tatamotors.com/corporate-responsibility",
        "https://www.tatamotors.com/legal-disclaimer",
        "https://www.tatamotors.com/newsroom",
        "https://www.tatamotors.com/careers/life-at-tml",
        "https://www.tatamotors.com/blog/defining-new-mobility-for-india/",
        "https://www.tatamotors.com/blog/2021-recovery-ahead/",
        "https://www.tatamotors.com/organisation/our-history/",
        "https://www.tatamotors.com/csr-archive",
        "https://www.tatamotors.com",
        "https://www.tatamotors.com/corporate-responsibility/governance",
        "https://www.tatamotors.com/contact-us",
        "https://www.tatamotors.com/blog/developing-software-on-wheels-seamless-technologies-for-the-vehicles-of-tomorrow-2/",
        "https://www.tatamotors.com/corporate-responsibility/",
        "https://www.tatamotors.com/blog/ownership-in-logistics-newer-opportunities-for-india-in-a-post-covid-world/",
        "https://www.tatamotors.com/future-of-mobility/",
        "https://www.tatamotors.com/future-of-mobility",
        "https://www.tatamotors.com/careers/",
        "https://www.tatamotors.com/corporate-responsibility/working-with-communities",
        "https://www.tatamotors.com/careers/kaushalya-earn-learn-program",
        "https://www.tatamotors.com/careers/openings",
        "https://www.tatamotors.com/corporate-responsibility/working-with-communities/",
    ]
    loader.update_db(pdf_dir=r"Data", urls=urls)
