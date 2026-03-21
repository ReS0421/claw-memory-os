#!/usr/bin/env python3
"""
fetch_invest_signal.py — #invest-signals 채널에서 오늘 날짜 .txt 첨부파일을 읽어
지정 경로에 저장한다.

사용법:
    python3 fetch_invest_signal.py
    python3 fetch_invest_signal.py --date 2026-03-21  # 특정 날짜 지정

출력:
    성공 시: 저장된 파일 경로를 stdout에 출력
    파일 없음: NO_SIGNAL 출력 후 종료
    에러: 에러 메시지 후 exit(1)
"""

import json
import pathlib
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
CHANNEL_ID = os.environ.get("INVEST_SIGNALS_CHANNEL_ID", "YOUR_CHANNEL_ID")  # #invest-signals
SAVE_DIR = pathlib.Path(os.environ.get("INVEST_SIGNALS_DIR", "signals"))

def load_token():
    cfg_path = pathlib.Path.home() / ".openclaw" / "openclaw.json"
    with open(cfg_path) as f:
        cfg = json.load(f)
    return cfg["channels"]["discord"]["token"]

def discord_headers(token):
    return {
        "Authorization": f"Bot {token}",
        "User-Agent": "DiscordBot (https://openclaw.ai, 1.0)",
        "Content-Type": "application/json"
    }

def get_messages(token, limit=20):
    url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages?limit={limit}"
    req = urllib.request.Request(url, headers=discord_headers(token))
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

def download_text(url, token):
    req = urllib.request.Request(url, headers=discord_headers(token))
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode("utf-8")

def main():
    # 날짜 결정
    target_date = None
    for i, arg in enumerate(sys.argv[1:]):
        if arg == "--date" and i + 1 < len(sys.argv) - 1:
            target_date = sys.argv[i + 2]
            break
    
    if target_date is None:
        target_date = datetime.now(KST).strftime("%Y-%m-%d")
    
    # 저장 경로 확인
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    save_path = SAVE_DIR / f"signal-{target_date}.txt"
    
    # 이미 존재하면 그대로 반환
    if save_path.exists():
        print(str(save_path))
        return
    
    token = load_token()
    
    try:
        messages = get_messages(token)
    except urllib.error.HTTPError as e:
        print(f"ERROR: Discord API {e.code}: {e.read().decode()[:200]}", file=sys.stderr)
        sys.exit(1)
    
    # 오늘 날짜 메시지 중 .txt 첨부파일 찾기
    for msg in messages:
        msg_date = msg.get("timestamp", "")[:10]
        if msg_date != target_date:
            continue
        for att in msg.get("attachments", []):
            fname = att.get("filename", "")
            ctype = att.get("content_type", "")
            if fname.endswith(".txt") or "text/plain" in ctype:
                # 다운로드
                try:
                    content = download_text(att["url"], token)
                    save_path.write_text(content, encoding="utf-8")
                    print(str(save_path))
                    return
                except Exception as e:
                    print(f"ERROR: download failed: {e}", file=sys.stderr)
                    sys.exit(1)
    
    print("NO_SIGNAL")

if __name__ == "__main__":
    main()
