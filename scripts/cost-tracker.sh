#!/usr/bin/env bash
# cost-tracker.sh — 세션 jsonl에서 토큰 사용량/비용 집계
# 사용: bash cost-tracker.sh [today|week|all|YYYY-MM-DD]

set -euo pipefail
SESSIONS_DIR="$HOME/.openclaw/agents/research/sessions"
PERIOD="${1:-today}"

python3 << PYEOF
import json, os, glob
from datetime import datetime, timedelta

sessions_dir = "$SESSIONS_DIR"
period = "$PERIOD"

now = datetime.now()
if period == "today":
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    label = f"오늘 ({now.strftime('%Y-%m-%d')})"
elif period == "week":
    start = (now - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
    label = f"최근 7일 ({start.strftime('%Y-%m-%d')} ~ {now.strftime('%Y-%m-%d')})"
elif period == "all":
    start = datetime(2020, 1, 1)
    label = "전체"
else:
    start = datetime.strptime(period, "%Y-%m-%d")
    label = period

# 모든 jsonl 파일 스캔 (활성 + 리셋 + 삭제 포함)
files = glob.glob(os.path.join(sessions_dir, "*.jsonl*"))
files = [f for f in files if not f.endswith('.lock')]

total_cost = 0.0
total_input = 0
total_output = 0
total_cache_read = 0
total_cache_write = 0
total_requests = 0
model_costs = {}

for fpath in files:
    try:
        with open(fpath) as f:
            for line in f:
                try:
                    d = json.loads(line)
                    msg = d.get('message', {})
                    usage = msg.get('usage', {})
                    cost_data = usage.get('cost', {})
                    
                    if not cost_data:
                        continue
                    
                    # 시간 필터
                    ts = d.get('timestamp', d.get('ts', ''))
                    if ts:
                        try:
                            dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                            dt = dt.replace(tzinfo=None)
                        except:
                            dt = now
                    else:
                        dt = now
                    
                    if dt < start:
                        continue
                    
                    cost = cost_data.get('total', 0)
                    total_cost += cost
                    total_input += usage.get('input', 0)
                    total_output += usage.get('output', 0)
                    total_cache_read += usage.get('cacheRead', 0)
                    total_cache_write += usage.get('cacheWrite', 0)
                    total_requests += 1
                    
                    model = msg.get('model', d.get('model', 'unknown'))
                    if model not in model_costs:
                        model_costs[model] = {'cost': 0, 'requests': 0}
                    model_costs[model]['cost'] += cost
                    model_costs[model]['requests'] += 1
                    
                except (json.JSONDecodeError, KeyError):
                    continue
    except:
        continue

print(f"📊 Cost Report — {label}")
print(f"{'='*50}")
print(f"총 비용:        \${total_cost:.4f}")
print(f"총 요청:        {total_requests}회")
print(f"입력 토큰:      {total_input:,}")
print(f"출력 토큰:      {total_output:,}")
print(f"캐시 읽기:      {total_cache_read:,}")
print(f"캐시 쓰기:      {total_cache_write:,}")
print()
print("모델별:")
for model, data in sorted(model_costs.items(), key=lambda x: -x[1]['cost']):
    print(f"  {model}: \${data['cost']:.4f} ({data['requests']}회)")

if total_cost > 0:
    cache_ratio = total_cache_read / max(total_input + total_cache_read + total_cache_write, 1) * 100
    print(f"\n캐시 적중률:    {cache_ratio:.1f}%")
    print(f"요청당 평균:    \${total_cost/total_requests:.4f}")
PYEOF
