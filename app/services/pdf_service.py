from app.services.injester import Loader
from app.config import embeddings
from app.models.users import User
import os


def process_pdf(pdf_file: str, file_name: str | None, curernt_user_id: str | None):

    print(f"Recieved file {file_name} at location {pdf_file}")
    print(f"user id of user: {curernt_user_id}")

    loader = Loader(embedding=embeddings)
    # pdf_docs = loader.load_pdf(pdf_file, file_name=file_name)
    pdf_docs = loader.load_pdf_user_id(
        pdf_file, file_name=file_name, user_id=curernt_user_id
    )
    loader.create_vector_db(pdf_docs)

    print("file added to database")
    os.remove(pdf_file)
