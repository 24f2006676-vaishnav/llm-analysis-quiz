import pandas as pd
import pdfplumber
import requests
from io import BytesIO
import matplotlib.pyplot as plt
import base64
import re
import os
from server.utils.text_utils import (
    extract_emails,
    extract_urls,
    extract_numbers,
    extract_phone_numbers,
    word_count,
    most_frequent_word,
    clean_text,
    longest_sentence
)


def download_file(url):
    """Download file from URL and return bytes + extension."""
    response = requests.get(url)
    filename = url.split("/")[-1]
    ext = os.path.splitext(filename)[1].lower()
    return response.content, ext

def read_table(file_bytes, ext):
    """Read a table from PDF, CSV, or Excel and return DataFrame."""
    # ------------ PDF ------------
    if ext == ".pdf":
        try:
            with pdfplumber.open(BytesIO(file_bytes)) as pdf:
                page = pdf.pages[0]
                table = page.extract_table()
                df = pd.DataFrame(table[1:], columns=table[0])
                return df
        except:
            return None

    # ------------ CSV ------------
    if ext == ".csv":
        try:
            df = pd.read_csv(BytesIO(file_bytes))
            return df
        except:
            return None

    # ------------ Excel ------------
    if ext in [".xlsx", ".xls"]:
        try:
            df = pd.read_excel(BytesIO(file_bytes))
            return df
        except:
            return None

    return None

def solve_task(parsed_page):
    text = parsed_page["text"].lower()
    links = parsed_page["links"]
    base64_blocks = parsed_page["base64_data"]
    original_text = parsed_page["text"]

    if "extract email" in text or "emails" in text:
        return extract_emails(original_text)

    if "extract url" in text or "extract link" in text:
        return extract_urls(original_text)

    if "extract number" in text or "numbers" in text:
        return extract_numbers(original_text)

    if "phone" in text or "contact" in text:
        return extract_phone_numbers(original_text)

    if "word count" in text:
        return word_count(original_text)

    if "most frequent" in text:
        return most_frequent_word(original_text)

    if "clean text" in text:
        return clean_text(original_text)

    if "longest sentence" in text:
        return longest_sentence(original_text)


    if not links:
        return "No links detected to read files."

    # Download the first file
    file_bytes, ext = download_file(links[0])
    df = read_table(file_bytes, ext)

    if df is None:
        return f"Could not read the file type: {ext}"

    # Convert all numeric columns automatically
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass

    # --------------------------
    # DETECT SUM QUESTION
    # --------------------------
    if "sum" in text:
        # find numeric columns
        numeric_cols = df.select_dtypes(include="number").columns
        if len(numeric_cols) == 0:
            return "No numeric columns found for sum."
        return df[numeric_cols[0]].sum()

    # --------------------------
    # DETECT COUNT QUESTION
    # --------------------------
    if "count" in text or "how many" in text:
        return len(df)

    # --------------------------
    # DEFAULT
    # --------------------------
    return {
        "detected_text": text[:300],
        "message": "No known question pattern detected yet.",
        "columns": list(df.columns)
    }
