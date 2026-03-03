#!/usr/bin/env python3
"""Crawl UE5 documentation from dev.epicgames.com and save as markdown."""

import os
import re
import time
import hashlib
import json
from pathlib import Path
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

BASE_URL = "https://dev.epicgames.com/documentation/en-us/unreal-engine"
DOCS_DIR = Path(__file__).parent.parent / "docs" / "ue5-docs"
STATE_FILE = Path(__file__).parent.parent / ".crawl-state.json"
MAX_PAGES = 5000
RATE_LIMIT = 0.3  # seconds between requests
TIMEOUT = 30
WORKERS = 4

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (compatible; UE-Knowledge-Crawler/1.0; educational purpose)"
})


def url_to_filepath(url: str) -> Path:
    """Convert a URL to a local file path."""
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    # Remove the common prefix
    path = path.replace("documentation/en-us/unreal-engine", "").strip("/")
    if not path:
        path = "index"
    # Sanitize
    path = re.sub(r'[^\w/\-]', '_', path)
    return DOCS_DIR / f"{path}.md"


def extract_links(soup: BeautifulSoup, current_url: str) -> list[str]:
    """Extract UE5 doc links from a page."""
    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        full_url = urljoin(current_url, href)
        # Only follow UE5 docs links
        if "/documentation/en-us/unreal-engine" in full_url:
            # Remove anchors and query params
            full_url = full_url.split("#")[0].split("?")[0].rstrip("/")
            links.add(full_url)
    return list(links)


def extract_content(soup: BeautifulSoup, url: str) -> str | None:
    """Extract main content from a doc page and convert to markdown."""
    # Try common content selectors for Epic docs
    content = (
        soup.find("article")
        or soup.find("main")
        or soup.find("div", class_=re.compile(r"content|article|documentation", re.I))
        or soup.find("div", {"role": "main"})
    )
    if not content:
        return None

    # Remove nav, sidebar, footer, scripts
    for tag in content.find_all(["nav", "aside", "footer", "script", "style", "header"]):
        tag.decompose()

    # Convert to markdown
    markdown = md(str(content), heading_style="ATX", strip=["img"])

    # Clean up excessive whitespace
    markdown = re.sub(r'\n{4,}', '\n\n\n', markdown)
    markdown = markdown.strip()

    if len(markdown) < 50:
        return None

    # Add source URL header
    title = soup.find("title")
    title_text = title.get_text().strip() if title else "Untitled"
    header = f"# {title_text}\n\nSource: {url}\n\n---\n\n"

    return header + markdown


def fetch_page(url: str) -> tuple[str | None, list[str]]:
    """Fetch a page and return (content, links)."""
    try:
        resp = session.get(url, timeout=TIMEOUT)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        content = extract_content(soup, url)
        links = extract_links(soup, url)
        return content, links
    except Exception as e:
        print(f"  ERROR: {url}: {e}")
        return None, []


def load_state() -> dict:
    """Load crawl state for resumability."""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"visited": [], "queue": [BASE_URL]}


def save_state(visited: set, queue: list):
    """Save crawl state."""
    STATE_FILE.write_text(json.dumps({
        "visited": list(visited),
        "queue": queue
    }))


def crawl():
    """Main crawl loop."""
    state = load_state()
    visited = set(state["visited"])
    queue = list(state["queue"]) if state["queue"] else [BASE_URL]
    saved = 0
    errors = 0

    print(f"Starting crawl from {BASE_URL}")
    print(f"Resuming: {len(visited)} already visited, {len(queue)} in queue")
    print(f"Saving to: {DOCS_DIR}")
    print(f"Max pages: {MAX_PAGES}")
    print()

    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    try:
        while queue and len(visited) < MAX_PAGES:
            url = queue.pop(0)
            if url in visited:
                continue

            visited.add(url)
            filepath = url_to_filepath(url)

            # Skip if already saved
            if filepath.exists():
                print(f"  SKIP (exists): {filepath.name}")
                # Still need to get links from this page
                content, links = fetch_page(url)
                for link in links:
                    if link not in visited and link not in queue:
                        queue.append(link)
                time.sleep(RATE_LIMIT)
                continue

            print(f"[{len(visited)}/{MAX_PAGES}] {url}")
            content, links = fetch_page(url)

            if content:
                filepath.parent.mkdir(parents=True, exist_ok=True)
                filepath.write_text(content)
                saved += 1
                print(f"  SAVED: {filepath.relative_to(DOCS_DIR)} ({len(content)} chars)")
            else:
                errors += 1
                print(f"  SKIP (no content)")

            # Add new links to queue
            new_links = 0
            for link in links:
                if link not in visited and link not in queue:
                    queue.append(link)
                    new_links += 1

            if new_links:
                print(f"  Found {new_links} new links (queue: {len(queue)})")

            time.sleep(RATE_LIMIT)

            # Save state every 50 pages
            if len(visited) % 50 == 0:
                save_state(visited, queue)
                print(f"\n  --- Checkpoint: {saved} saved, {errors} errors, {len(queue)} queued ---\n")

    except KeyboardInterrupt:
        print("\n\nInterrupted! Saving state...")
    finally:
        save_state(visited, queue)

    print(f"\nDone!")
    print(f"  Pages visited: {len(visited)}")
    print(f"  Pages saved: {saved}")
    print(f"  Errors: {errors}")
    print(f"  Remaining in queue: {len(queue)}")


if __name__ == "__main__":
    crawl()
