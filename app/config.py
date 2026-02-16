from pydantic import BaseModel
import yaml
from pathlib import Path
from typing import List
from langchain_ollama import OllamaEmbeddings
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv(override=True)


class EmbeddingSettings(BaseModel):
    model_name: str
    dimensions: int


class SplitterSettings(BaseModel):
    chunk_size: int
    chunk_overlap: int
    separators: List[str]


class LLMSettings(BaseModel):
    model_name: str
    temperature: float
    max_tokens: int


class ChromaSettings(BaseModel):
    persist_directory: str


class Config(BaseModel):
    embeddings: EmbeddingSettings
    text_splitter: SplitterSettings
    llm: LLMSettings
    chroma_settings: ChromaSettings


CONFIG_PATH = Path(__file__).parent / "config.yaml"


def load_config() -> Config:
    with open(CONFIG_PATH, "r") as f:
        raw_config = yaml.safe_load(f)
    return Config(**raw_config)


settings = load_config()

embeddings = OllamaEmbeddings(model="nomic-embed-text")

llm = ChatGroq(
    model=settings.llm.model_name,
    temperature=settings.llm.temperature,
    max_tokens=settings.llm.max_tokens,
)
vector_store = Chroma(
    persist_directory="./Chroma_db",
    embedding_function=embeddings,
    collection_name="mixed_data_rag",
)

if __name__ == "__main__":
    print(f"Model: {settings.llm.model_name}")
    print(f"Chunk Size: {settings.text_splitter.chunk_size}")
    print(f"chroma path: {settings.chroma_settings.persist_directory}")
