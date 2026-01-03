import re

def remove_urls(text: str) -> str:
    text = re.sub(r'https?://\S+\b', '', text)
    text = re.sub(r'www\.\S+\b', '', text)
    return text.strip()

def split_into_sentences(text: str):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip(), flags=re.UNICODE)
    return [s.strip() for s in sentences if s.strip()]

def sanitize_response(response: str, remove_n: int = 1) -> str:
    if not response:
        return response

    text = remove_urls(response)
    text = text.strip()
    sentences = split_into_sentences(text)
    if len(sentences) <= remove_n:
        return " ".join(sentences[:-remove_n]) if sentences else ""
    kept = sentences[:-remove_n]
    cleaned = " ".join(kept).strip()
    cleaned = re.sub(r'\s+\n\s+', '\n', cleaned)
    cleaned = re.sub(r'\s{2,}', ' ', cleaned)

    return cleaned