#!/usr/bin/env python3
"""
discord_forum_post.py — Digest 포맷 + Discord forum 포스팅 유틸

사용법:
  # 판단 완료된 JSON을 stdin으로 받아 포스팅
  echo '[{"title":"...","url":"...","source":"HN","score":300,"summary_ko":"요약","hn_url":"..."}]' \
    | python3 discord_forum_post.py dev

  echo '{"articles":[...], "projects":[...]}' \
    | python3 discord_forum_post.py laplace

  # --dry-run: 포스팅 없이 포맷 출력만
  echo '[...]' | python3 discord_forum_post.py dev --dry-run

입력 형식:
  dev:     JSON 배열 — [{title, url, source, score, summary_ko, hn_url?}, ...]
  laplace: JSON 객체 — {
             "articles": [{title, url, source, summary_ko}, ...],
             "projects": [{title, why, tech, deliverable, difficulty}, ...]
           }
"""

import json
import pathlib
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
FORUM_CHANNEL_ID = os.environ.get("FORUM_CHANNEL_ID", "YOUR_CHANNEL_ID")
TAG_AI = os.environ.get("TAG_AI", "YOUR_TAG_ID")
TAG_PRODUCTIVITY = os.environ.get("TAG_PRODUCTIVITY", "YOUR_TAG_ID")


def load_discord_token():
    cfg_path = pathlib.Path.home() / ".openclaw" / "openclaw.json"
    with open(cfg_path) as f:
        cfg = json.load(f)
    return cfg["channels"]["discord"]["token"]


def discord_headers(token):
    return {
        "Authorization": f"Bot {token}",
        "User-Agent": "DiscordBot (https://openclaw.ai, 1.0)",
        "Content-Type": "application/json",
    }


def post_forum(token, name, content, tags):
    payload = json.dumps({
        "name": name,
        "message": {"content": content},
        "applied_tags": tags,
    }).encode()
    req = urllib.request.Request(
        f"https://discord.com/api/v10/channels/{FORUM_CHANNEL_ID}/threads",
        data=payload,
        headers=discord_headers(token),
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def format_dev(items, date_str):
    if not items:
        return None
    lines = [f"# 🗞️ Dev Digest — {date_str}\n", f"AI/LLM · 생산성 도구 | {len(items)}건\n"]
    for i, item in enumerate(items, 1):
        summary = item.get("summary_ko", "")
        title_line = f"**{i}. {item['title']}**"
        if summary:
            title_line += f"\n   > {summary}"
        lines.append(title_line)
        score_str = f"  ⬆{item['score']}" if item.get("score") else ""
        lines.append(f"   <{item['url']}>{score_str}")
        if item.get("hn_url") and item["url"] != item.get("hn_url"):
            lines.append(f"   [HN 댓글](<{item['hn_url']}>)")
        lines.append("")
    content = "\n".join(lines)
    return content[:1990] + "\n..." if len(content) > 1990 else content


def format_laplace(articles, projects, date_str):
    if not articles:
        return None
    lines = [
        f"# 🔬 Laplace Digest — {date_str}\n",
        "설계 단계 인풋 | 읽을거리 3 + 사이드프로젝트 제안 3\n",
        "## 📚 오늘의 읽을거리\n",
    ]
    for i, item in enumerate(articles[:3], 1):
        summary = item.get("summary_ko", "")
        title_line = f"**{i}. {item['title']}**"
        if summary:
            title_line += f"\n   > {summary}"
        lines.append(title_line)
        lines.append(f"   <{item['url']}>")
        lines.append("")

    if projects:
        lines += ["\n---\n", "## 🛠️ 오늘의 사이드프로젝트 제안\n"]
        for i, proj in enumerate(projects[:3], 1):
            diff = proj.get("difficulty", "medium")
            lines.append(f"**{i}. {proj.get('title', '?')}** `{diff}`")
            lines.append(f"   > {proj.get('why', '')}")
            lines.append(f"   - 만들 것: {proj.get('deliverable', '')}")
            lines.append(f"   - 기술: {', '.join(proj.get('tech', []))}")
            lines.append("")

    content = "\n".join(lines)
    return content[:1800] + "\n..." if len(content) > 1800 else content


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "dev"
    dry_run = "--dry-run" in sys.argv
    date_str = datetime.now(KST).strftime("%Y-%m-%d")

    raw_input = sys.stdin.read().strip()
    if not raw_input:
        print("NO_INPUT"); sys.exit(1)

    data = json.loads(raw_input)

    if mode == "dev":
        items = data if isinstance(data, list) else data.get("items", [])
        content = format_dev(items, date_str)
        if not content:
            print("NO_ITEMS"); return
        if dry_run:
            print(content); return
        token = load_discord_token()
        res = post_forum(token, f"Dev Digest {date_str}", content, [TAG_AI, TAG_PRODUCTIVITY])
        print(f"[✅] Dev Digest posted — thread_id: {res.get('id')}")

    elif mode == "laplace":
        articles = data.get("articles", [])
        projects = data.get("projects", [])
        content = format_laplace(articles, projects, date_str)
        if not content:
            print("NO_ITEMS"); return
        if dry_run:
            print(content); return
        token = load_discord_token()
        res = post_forum(token, f"Laplace {date_str}", content, [TAG_AI])
        print(f"[✅] Laplace Digest posted — thread_id: {res.get('id')}")

    else:
        print(f"Unknown mode: {mode}"); sys.exit(1)


if __name__ == "__main__":
    main()
