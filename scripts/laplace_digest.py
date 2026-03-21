#!/usr/bin/env python3
"""
Laplace Digest — AI-Native Note App 설계 단계 인풋
소스: Hacker News, GitHub Trending, arXiv cs.AI
출력: JSON (candidates 배열 + side_project_prompt) — cron 에이전트가 판단/포맷 후 Discord 전송
"""

import json
import urllib.request
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))

MAX_CANDIDATES = 15

LAPLACE_KEYWORDS = [
    r'\bknowledge graph\b', r'\bgraph.?rag\b', r'\bgraphrag\b',
    r'\bvector\b', r'\bembedding\b', r'\bsemantic search\b',
    r'\bpersonal knowledge\b', r'\bpkm\b', r'\bsecond brain\b',
    r'\bnote.?taking\b', r'\bknowledge management\b',
    r'\bai.?native\b', r'\blocal.?first\b', r'\boffline.?first\b',
    r'\bai editor\b', r'\bwriting assistant\b',
    r'\bcrdt\b', r'\bcollaborative editing\b',
    r'\bontology\b', r'\bknowledge base\b',
    r'\brag\b', r'\bretrieval\b', r'\bchunking\b',
    r'\bnotion\b', r'\bobsidian\b', r'\blogseq\b',
    r'\bmulti.?agent\b', r'\bagent\b',
]


def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'openclaw-digest/1.0'})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())


def fetch_html(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; openclaw-digest/1.0)'})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode('utf-8', errors='replace')


def matches_keywords(text):
    text_lower = text.lower()
    return any(re.search(p, text_lower) for p in LAPLACE_KEYWORDS)


def fetch_hn():
    items = []
    try:
        top_ids = fetch_json("https://hacker-news.firebaseio.com/v0/topstories.json")[:100]
        for item_id in top_ids:
            try:
                item = fetch_json(f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json")
                if not item or item.get('type') != 'story':
                    continue
                title = item.get('title', '')
                score = item.get('score', 0)
                url = item.get('url', f"https://news.ycombinator.com/item?id={item_id}")
                if matches_keywords(title):
                    items.append({'title': title, 'url': url, 'score': score, 'source': 'HN'})
            except Exception:
                continue
            if len(items) >= 10:
                break
    except Exception as e:
        print(f"# HN error: {e}", flush=True)
    return items


def fetch_github_trending():
    items = []
    try:
        html = fetch_html("https://github.com/trending?since=daily")
        repo_blocks = re.findall(r'<article[^>]*class="[^"]*Box-row[^"]*"[^>]*>(.*?)</article>', html, re.DOTALL)
        for block in repo_blocks[:30]:
            name_match = re.search(r'<h2[^>]*>\s*<a[^>]*href="/([^"]+)"[^>]*>', block, re.DOTALL)
            if not name_match:
                continue
            repo_path = re.sub(r'\s+', '', name_match.group(1).strip())
            desc_match = re.search(r'<p[^>]*class="[^"]*col-9[^"]*"[^>]*>\s*(.*?)\s*</p>', block, re.DOTALL)
            description = re.sub(r'<[^>]+>', '', desc_match.group(1)).strip() if desc_match else ''
            stars_match = re.search(r'href="/' + re.escape(repo_path) + r'/stargazers"[^>]*>\s*([0-9,]+)', block)
            stars = int(stars_match.group(1).replace(',', '')) if stars_match else 0
            title = f"{repo_path} — {description}" if description else repo_path
            if matches_keywords(title):
                items.append({'title': title, 'url': f"https://github.com/{repo_path}", 'score': stars, 'source': 'GitHub'})
    except Exception as e:
        print(f"# GitHub error: {e}", flush=True)
    return items


def fetch_arxiv():
    items = []
    try:
        req = urllib.request.Request("https://rss.arxiv.org/rss/cs.AI", headers={'User-Agent': 'openclaw-digest/1.0'})
        with urllib.request.urlopen(req, timeout=15) as r:
            xml_data = r.read()
        root = ET.fromstring(xml_data)
        channel = root.find('channel')
        if channel is None:
            return items
        for entry in channel.findall('item')[:20]:
            title_el = entry.find('title')
            link_el = entry.find('link')
            desc_el = entry.find('description')
            title = title_el.text.strip() if title_el is not None and title_el.text else ''
            url = link_el.text.strip() if link_el is not None and link_el.text else ''
            description = re.sub(r'<[^>]+>', '', desc_el.text).strip()[:200] if desc_el is not None and desc_el.text else ''
            if matches_keywords(f"{title} {description}"):
                items.append({'title': title, 'url': url, 'score': 10, 'source': 'arXiv'})
    except Exception as e:
        print(f"# arXiv error: {e}", flush=True)
    return items


def deduplicate(items):
    seen = set()
    unique = []
    for item in items:
        key = re.sub(r'https?://(www\.)?', '', item['url']).rstrip('/')
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique


def main():
    all_items = fetch_hn() + fetch_github_trending() + fetch_arxiv()
    all_items = deduplicate(all_items)
    all_items.sort(key=lambda x: x.get('score', 0), reverse=True)
    all_items = all_items[:MAX_CANDIDATES]

    if not all_items:
        print("NO_ITEMS")
        return

    output = {
        "candidates": all_items,
        "date": datetime.now(KST).strftime('%Y-%m-%d'),
        "side_project_context": (
            "Builder: Python + basic web dev, AI automation background. "
            "Interests: AI agents, knowledge graphs. "
            "Stage: pre-code, architecture design. "
            "Goal: AI-native note app where AI is first-class citizen — reads, writes, structures notes."
        )
    }
    print(json.dumps(output, ensure_ascii=False))


if __name__ == '__main__':
    main()
