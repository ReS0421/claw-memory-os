#!/usr/bin/env python3
"""
Dev Digest — 생산성 · Second Brain · AI 도구 뉴스 큐레이션
소스: Hacker News, Lobsters, GitHub Trending, Reddit
출력: JSON 배열 (cron 에이전트가 판단/포맷 후 Discord 전송)
"""

import json
import urllib.request
import re
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))

MAX_CANDIDATES = 30
MIN_SCORE_HN = 30        # 생산성 관련은 HN 스코어가 낮아도 포함
MIN_SCORE_LOBSTERS = 8
MIN_UPVOTES_REDDIT = 30  # PKM 서브는 업보트가 적어도 의미 있음

# ── 키워드 ───────────────────────────────────────────────────────────────────
# 생산성 · Second Brain · PKM (높은 우선순위)
PRODUCTIVITY_KEYWORDS = [
    r'\bproductivity\b', r'\bsecond brain\b', r'\bpkm\b',
    r'\bpersonal knowledge\b', r'\bknowledge management\b',
    r'\bzettelkasten\b', r'\bmente.map\b', r'\bmind map\b',
    r'\bnote.?taking\b', r'\bnote.?app\b',
    r'\bobsidian\b', r'\bnotion\b', r'\blogseq\b', r'\broam\b',
    r'\bappflowy\b', r'\banytype\b', r'\bcrafts app\b', r'\bbear app\b',
    r'\bworkflow\b', r'\bautomation\b', r'\btask management\b',
    r'\bgtd\b', r'\bdeep work\b', r'\btime blocking\b',
    r'\bfocus\b', r'\bpomodoro\b', r'\bbuilding a second brain\b',
    r'\bknowledge graph\b', r'\bsemantic search\b', r'\bvector\b',
    r'\bembedding\b', r'\brag\b', r'\bretrieval\b',
    r'\blocal.?first\b', r'\boffline.?first\b', r'\bself.?hosted\b',
    r'\bopen.?source\b', r'\bplaintext\b', r'\bmarkdown\b',
]

# AI 도구 (실용적인 것만, 기술 뉴스 아닌 것)
AI_TOOL_KEYWORDS = [
    r'\bai tool\b', r'\bai assistant\b', r'\bai editor\b',
    r'\bai notes\b', r'\bai writing\b', r'\bai search\b',
    r'\bcoding assistant\b', r'\bcopilot\b', r'\bcursor\b',
    r'\bllm\b', r'\blocal llm\b', r'\bollama\b', r'\bopen.?source ai\b',
    r'\bmcp\b', r'\bmodel context\b',
    r'\bagent\b', r'\bagentic\b', r'\bautomation\b',
]

# 개발자 도구 (실용)
DEV_TOOL_KEYWORDS = [
    r'\bdev tool\b', r'\bcli tool\b', r'\bdeveloper tool\b',
    r'\bneovim\b', r'\bvscode\b', r'\bterminal\b',
    r'\bopen.?source\b', r'\bself.?hosted\b',
]

ALL_KEYWORDS = PRODUCTIVITY_KEYWORDS + AI_TOOL_KEYWORDS + DEV_TOOL_KEYWORDS

LOBSTER_TAGS_RELEVANT = {'productivity', 'ai', 'ml', 'tools', 'show', 'release', 'programming'}

REDDIT_SUBS = [
    'PKMS',           # Personal Knowledge Management Systems
    'ObsidianMD',     # Obsidian 커뮤니티
    'Zettelkasten',   # 제텔카스텐
    'productivity',   # 일반 생산성
    'LocalLLaMA',     # 로컬 AI 도구
    'MachineLearning',
]


def fetch_json(url, headers=None):
    default_headers = {'User-Agent': 'openclaw-digest/1.0'}
    if headers:
        default_headers.update(headers)
    req = urllib.request.Request(url, headers=default_headers)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())


def fetch_html(url):
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (compatible; openclaw-digest/1.0)'}
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode('utf-8', errors='replace')


def matches_keywords(text):
    text_lower = text.lower()
    return any(re.search(p, text_lower) for p in ALL_KEYWORDS)


def fetch_hn():
    items = []
    try:
        top_ids = fetch_json("https://hacker-news.firebaseio.com/v0/topstories.json")[:150]
        for item_id in top_ids:
            try:
                item = fetch_json(f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json")
                if not item or item.get('type') != 'story':
                    continue
                title = item.get('title', '')
                score = item.get('score', 0)
                url = item.get('url', f"https://news.ycombinator.com/item?id={item_id}")
                if score >= MIN_SCORE_HN and matches_keywords(title):
                    items.append({
                        'title': title, 'url': url, 'score': score,
                        'comments': item.get('descendants', 0),
                        'hn_url': f"https://news.ycombinator.com/item?id={item_id}",
                        'source': 'HN',
                    })
            except Exception:
                continue
            if len(items) >= 20:
                break
    except Exception as e:
        print(f"# HN error: {e}", flush=True)
    return items


def fetch_lobsters():
    items = []
    try:
        data = fetch_json("https://lobste.rs/hottest.json")
        for item in data:
            title = item.get('title', '')
            score = item.get('score', 0)
            tags = set(item.get('tags', []))
            url = item.get('url') or item.get('comments_url', '')
            tag_match = bool(tags & LOBSTER_TAGS_RELEVANT)
            kw_match = matches_keywords(title)
            if score >= MIN_SCORE_LOBSTERS and (kw_match or tag_match):
                items.append({
                    'title': title, 'url': url, 'score': score,
                    'comments': item.get('comment_count', 0),
                    'source': 'Lobsters', 'tags': list(tags),
                })
    except Exception as e:
        print(f"# Lobsters error: {e}", flush=True)
    return items


def fetch_github_trending():
    items = []
    try:
        html = fetch_html("https://github.com/trending?since=daily")
        repo_blocks = re.findall(
            r'<article[^>]*class="[^"]*Box-row[^"]*"[^>]*>(.*?)</article>',
            html, re.DOTALL
        )
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
            url = f"https://github.com/{repo_path}"
            if matches_keywords(title):
                items.append({'title': title, 'url': url, 'score': stars, 'source': 'GitHub'})
    except Exception as e:
        print(f"# GitHub Trending error: {e}", flush=True)
    return items


def fetch_reddit():
    items = []
    for sub in REDDIT_SUBS:
        try:
            data = fetch_json(f"https://www.reddit.com/r/{sub}/hot.json?limit=25")
            for post in data.get('data', {}).get('children', []):
                p = post.get('data', {})
                title = p.get('title', '')
                upvotes = p.get('ups', 0)
                permalink = p.get('permalink', '')
                post_url = f"https://www.reddit.com{permalink}" if permalink else p.get('url', '')
                if upvotes >= MIN_UPVOTES_REDDIT and matches_keywords(title):
                    items.append({
                        'title': title, 'url': post_url, 'score': upvotes,
                        'comments': p.get('num_comments', 0), 'source': f'r/{sub}',
                    })
        except Exception as e:
            print(f"# Reddit r/{sub} error: {e}", flush=True)
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
    all_items = fetch_hn() + fetch_lobsters() + fetch_github_trending() + fetch_reddit()
    all_items = deduplicate(all_items)
    all_items.sort(key=lambda x: x.get('score', 0), reverse=True)
    all_items = all_items[:MAX_CANDIDATES]

    if not all_items:
        print("NO_ITEMS")
        return

    print(json.dumps(all_items, ensure_ascii=False))


if __name__ == '__main__':
    main()
