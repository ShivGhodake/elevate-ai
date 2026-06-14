import os
import re
from dataclasses import dataclass


@dataclass
class SimpleDocument:
    page_content: str


class SimpleRetriever:
    def __init__(self, chunks):
        self.chunks = chunks

    def invoke(self, query: str):
        query_tokens = set(_tokenize(query))
        if not query_tokens:
            return self.chunks[:3]

        scored = []
        for chunk in self.chunks:
            content_lower = chunk.page_content.lower()
            chunk_tokens = set(_tokenize(chunk.page_content))
            overlap = len(query_tokens & chunk_tokens)

            # Small bonus for exact phrase hits so obvious matches rise first.
            phrase_bonus = 2 if query.lower() in content_lower else 0
            score = overlap + phrase_bonus

            if score > 0:
                scored.append((score, chunk))

        if not scored:
            return self.chunks[:3]

        scored.sort(key=lambda item: item[0], reverse=True)
        return [chunk for _, chunk in scored[:3]]


def _tokenize(text: str):
    return re.findall(r"[a-zA-Z0-9]+", text.lower())


def _split_text(text: str, chunk_size: int = 1200, overlap: int = 200):
    chunks = []
    start = 0

    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(SimpleDocument(page_content=chunk))

        if end >= len(text):
            break

        start = max(end - overlap, start + 1)

    return chunks


def _load_chunks():
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, "..", "data")
    chunks = []

    for file_name in ("textbook.txt", "pyq.txt"):
        file_path = os.path.join(data_dir, file_name)
        if not os.path.exists(file_path):
            continue

        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        chunks.extend(_split_text(text))

    if not chunks:
        chunks.append(
            SimpleDocument(
                page_content="No local study material was found for retrieval."
            )
        )

    return chunks


_RETRIEVER = SimpleRetriever(_load_chunks())


def get_retriever():
    return _RETRIEVER
