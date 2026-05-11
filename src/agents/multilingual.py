"""
Multilingual Support Module
Handles English ↔ Urdu translation and language detection for Pakistani Legal AI.
"""

import os
from pathlib import Path
from langchain_groq import ChatGroq
from dotenv import load_dotenv

_project_root = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=_project_root / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")


def get_llm():
    return ChatGroq(api_key=GROQ_API_KEY, model_name=LLM_MODEL, temperature=0.1, max_tokens=2000)


def detect_language(text: str) -> str:
    """Detect if text is Urdu, Roman Urdu, or English."""
    urdu_chars = set('ابتثجحخدذرزسشصضطظعغفقکگلمنوہیئاآ')
    urdu_count = sum(1 for c in text if c in urdu_chars)
    if urdu_count > len(text) * 0.2:
        return "urdu"

    roman_urdu_words = {
        'kya','hai','ka','ki','ke','mein','nahi','hota','karo',
        'ap','aap','hum','tum','woh','yeh','ye','jo','koi',
        'kuch','sab','bhi','sirf','lekin','aur','ya','agar',
        'qanoon','adalat','fir','bail','wakeel','judge','case',
        'Pakistan','Karachi','Lahore','Islamabad'
    }
    words = set(text.lower().split())
    if len(words & {w.lower() for w in roman_urdu_words}) >= 2:
        return "roman_urdu"

    return "english"


def translate_to_english(text: str) -> str:
    """Translate Urdu or Roman Urdu to English for processing."""
    lang = detect_language(text)
    if lang == "english":
        return text

    llm = get_llm()
    prompt = f"""Translate the following {'Urdu' if lang == 'urdu' else 'Roman Urdu'} legal question to English.
Keep legal terms accurate. Return ONLY the English translation, nothing else.

Text: {text}"""
    response = llm.invoke([{"role": "user", "content": prompt}])
    return response.content.strip()


def translate_to_urdu(text: str) -> str:
    """Translate English legal answer to Urdu."""
    llm = get_llm()
    prompt = f"""Translate this English legal answer to clear, simple Urdu.
- Keep legal terms in both Urdu and English (in brackets)
- Use simple Urdu that common people understand
- Preserve all section numbers and citations exactly
- Return ONLY the Urdu translation

Text: {text}"""
    response = llm.invoke([{"role": "user", "content": prompt}])
    return response.content.strip()


def translate_to_roman_urdu(text: str) -> str:
    """Translate English legal answer to Roman Urdu."""
    llm = get_llm()
    prompt = f"""Translate this English legal answer to Roman Urdu (Urdu written in English letters).
- Use simple everyday Roman Urdu
- Keep legal terms in English with Roman Urdu explanation
- Preserve all section numbers and citations
- Return ONLY the Roman Urdu translation

Text: {text}"""
    response = llm.invoke([{"role": "user", "content": prompt}])
    return response.content.strip()


def process_multilingual_query(query: str, output_lang: str = "auto") -> dict:
    """
    Full multilingual pipeline:
    1. Detect input language
    2. Translate to English if needed
    3. Return detected language and english query for RAG
    """
    detected = detect_language(query)
    english_query = translate_to_english(query) if detected != "english" else query

    return {
        "detected_language": detected,
        "english_query": english_query,
        "original_query": query,
        "output_lang": output_lang if output_lang != "auto" else detected,
    }


def translate_answer(answer: str, target_lang: str) -> str:
    """Translate a legal answer to the target language."""
    if target_lang == "english":
        return answer
    elif target_lang == "urdu":
        return translate_to_urdu(answer)
    elif target_lang == "roman_urdu":
        return translate_to_roman_urdu(answer)
    return answer
