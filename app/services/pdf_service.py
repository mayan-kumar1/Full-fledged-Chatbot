from app.services.injester import Loader
from app.config import embeddings

import os


def process_pdf(pdf_file: str, file_name: str | None):

    print(f"Recieved file {file_name} at location {pdf_file}")

    loader = Loader(embedding=embeddings)
    pdf_docs = loader.load_pdf(pdf_file, file_name=file_name)
    loader.create_vector_db(pdf_docs)

    print("file added to database")
    os.remove(pdf_file)
