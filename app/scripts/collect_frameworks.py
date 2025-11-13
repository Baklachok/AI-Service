import json
import logging
import re
import time
import uuid
from typing import Any, Optional

import requests
from bs4 import BeautifulSoup
from settings import DATA_PATH, HEADERS, SOURCES_PATH


def fetch_html(url: str) -> Optional[str]:
    """Получает html, возвращает текст страницы"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logging.warning("Не удалось загрузить %s: %s", url, e)


def extract_text_from_html(html: str, max_len: int = 5000) -> str:
    """Извлекает чистый текст из HTML"""
    if not html or not isinstance(html, str):
        return ""
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    text = re.sub(r"\s+", " ", text, flags=re.UNICODE).strip()
    return text[:max_len]


def parse_github(url: str) -> str:
    """Пробуем взять README или описание репозитория"""
    html = fetch_html(url)
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")

    readme_section = soup.find("article", attrs={"class": "markdown-body"})
    if readme_section:
        text = readme_section.get_text(separator=" ", strip=True)
        text = re.sub(r"\s+", " ", text, flags=re.UNICODE).strip()
        return text[:5000]

    desc = soup.find("meta", {"property": "og:description"})
    if desc and desc.get("content"):
        return desc["content"]
    return ""


def parse_habr(url: str, max_articles: int = 2) -> str:
    """Парсим первые статьи с Habr по поиску"""
    html = fetch_html(url)
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")

    articles = soup.select("article")[:max_articles]
    texts = []
    for art in articles:
        title = art.find("h2")
        summary = art.get_text(separator=" ", strip=True)
        summary = re.sub(r"\s+", " ", summary, flags=re.UNICODE).strip()
        if title:
            texts.append(title.get_text(strip=True))
        if summary:
            texts.append(summary)
    return " ".join(texts)[:5000]


def parse_stackoverflow(url: str, max_questions: int = 3) -> str:
    """Парсим описание из StackOverflow теговой страницы"""
    html = fetch_html(url)
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")

    desc = soup.find("div", {"class": "s-prose"})
    if desc:
        return desc.get_text(separator=" ", strip=True)[:3000]

    # запасной вариант: взять заголовки вопросов
    questions = soup.select("a.s-link")[:max_questions]
    q_texts = [q.get_text(strip=True) for q in questions]
    return " ".join(q_texts)


def collect_data(source: dict[str, Any]) -> dict[str, Any]:
    """Собирает данные по одному фреймворку"""
    name = source["name"]
    logging.info("Парсим %s...", name)

    text_parts = []

    github_text = parse_github(source["github"])
    if github_text:
        text_parts.append(f"[GitHub] {github_text}")

    habr_text = parse_habr(source["habr"])
    if habr_text:
        text_parts.append(f"[Habr] {habr_text}")

    stackoverflow_text = parse_stackoverflow(source["stackoverflow"])
    if stackoverflow_text:
        text_parts.append(f"[StackOverflow] {stackoverflow_text}")

    html = fetch_html(source["website"])
    if html:
        website_text = extract_text_from_html(html)
        text_parts.append(f"[Website] {website_text}")

    combined_text = "\n\n".join(text_parts)

    return {
        "id": str(uuid.uuid4()),
        "framework": name,
        "language": source.get("lang", "Python"),
        "text": combined_text,
        "source_github": source.get("github"),
        "source_stackoverflow": source.get("stackoverflow"),
        "source_habr": source.get("habr"),
        "source_website": source.get("website"),
    }


def main():
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(SOURCES_PATH, encoding="utf-8") as f:
        sources: list[dict[str, Any]] = json.load(f)

    with open(DATA_PATH, "w", encoding="utf-8") as out:
        for s in sources:
            record = collect_data(s)
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
            time.sleep(1)  # немного, чтобы не банили за частые запросы

    logging.info("Данные сохранены в %s", DATA_PATH)


if __name__ == "__main__":
    main()
