from chromadb import PersistentClient
from search.llm import query_openrouter
from sentence_transformers import SentenceTransformer
from settings import CHROMA_DB_DIR, COLLECTION_NAME, EMBEDDING_MODEL


client_chroma = PersistentClient(path=CHROMA_DB_DIR)
collection = client_chroma.get_or_create_collection(COLLECTION_NAME)
embedding_model = SentenceTransformer(EMBEDDING_MODEL)


def search_relevant_context(query: str, n_results: int = 5) -> list[str]:
    query_emb = embedding_model.encode([query]).tolist()[0]
    results = collection.query(query_embeddings=[query_emb], n_results=n_results)
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    combined = [
        f"{meta.get('framework', '')} ({meta.get('language', '')}): {doc}"
        for doc, meta in zip(documents, metadatas, strict=True)
    ]
    return combined


def get_framework_recommendation(task_description: str) -> str:
    if not task_description.strip():
        return "Описание задачи пустое"
    contexts = search_relevant_context(task_description, n_results=5)
    context_text = "\n\n".join(contexts)

    prompt = f"""
    Вот контекст из локальной базы знаний (из ChromaDB):
    {context_text}
    Теперь ответь на вопрос пользователя, опираясь на этот контекст:
    {task_description}
    """

    return str(query_openrouter(prompt))
