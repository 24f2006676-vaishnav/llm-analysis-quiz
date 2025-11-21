import re

def extract_emails(text):
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return re.findall(pattern, text)

def extract_urls(text):
    pattern = r"https?://[^\s]+"
    return re.findall(pattern, text)

def extract_numbers(text):
    pattern = r"\b\d+\.?\d*\b"
    return re.findall(pattern, text)

def extract_phone_numbers(text):
    pattern = r"\b(?:\+?\d{1,3})?[-.\s]?(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})\b"
    return re.findall(pattern, text)

def word_count(text):
    words = re.findall(r"\w+", text.lower())
    return len(words)

def most_frequent_word(text):
    words = re.findall(r"\w+", text.lower())
    if not words:
        return None
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    return max(freq, key=freq.get)

def clean_text(text):
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text

def longest_sentence(text):
    sentences = re.split(r"[.!?]", text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return None
    return max(sentences, key=len)
