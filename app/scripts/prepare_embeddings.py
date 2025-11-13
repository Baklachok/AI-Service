import json
import logging
import re

from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer
from settings import CHROMA_DB_DIR, DATA_PATH


model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

client_chroma = PersistentClient(path=str(CHROMA_DB_DIR))
collection = client_chroma.get_or_create_collection("frameworks")


def clean_text(text: str) -> str:
    """Очистка текста от лишних символов"""
    return re.sub(r"\s+", " ", text).strip()


def chunk_text(text: str, max_words: int = 500) -> list[str]:
    """Разбиваем текст на чанки по количеству слов"""
    words = text.split()
    return [" ".join(words[i : i + max_words]) for i in range(0, len(words), max_words)]


def embed_text(texts: list[str]) -> list[list[float]]:
    """Создание эмбеддингов через SentenceTransformer"""
    logging.info("Создаём локальные эмбеддинги для %s чанков...", len(texts))
    return model.encode(texts, show_progress_bar=True).tolist()


def safe_str(value):
    """Преобразует None → '' и всё остальное → str"""
    return str(value) if value is not None else ""


def main():
    if not DATA_PATH.exists():
        logging.error("%s не найден", DATA_PATH)
        return

    ids, texts, metadatas = [], [], []

    with open(DATA_PATH, encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            text_clean = clean_text(record["text"])
            chunks = chunk_text(text_clean, max_words=500)
            for idx, chunk in enumerate(chunks):
                ids.append(f"{record['id']}_{idx}")
                texts.append(chunk)
                metadatas.append(
                    {
                        "framework": safe_str(record["framework"]),
                        "language": safe_str(record.get("language", "Python")),
                        "source_github": safe_str(record.get("github")),
                        "source_habr": safe_str(record.get("habr")),
                        "source_stackoverflow": safe_str(record.get("stackoverflow")),
                        "source_website": safe_str(record.get("website")),
                    }
                )

    embeddings = embed_text(texts)

    logging.info("Сохраняем в ChromaDB (%s)...", CHROMA_DB_DIR)
    collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=texts)
    logging.info("Готово! Данные можно искать семантически.")


if __name__ == "__main__":
    main()
