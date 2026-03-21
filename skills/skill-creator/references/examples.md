# Skill Creator — 우리 시스템 스킬 예시

## 좋은 예: intel-x-post

```yaml
---
name: intel-x-post
description: "Intel Pipeline 보고서(KR/US Pre-Open)를 X 단일 포스트로 변환하는 전용 스킬. 저작권 안전 처리, 팩트 라인 형식, 출처 표기 규칙 포함. 트리거: Intel Pipeline 보고서를 X에 올려줘, intel 보고서 X 포스트 작성 요청 시."
---
```
✅ 역할 명확, 트리거 구체적, references 분리 사용

## 좋은 예: subagent 스킬 (analyst)

```yaml
---
name: analyst
description: "투자 분석 전문 — 펀더멘털 기반 바이사이드 리서치, 종목 분석, 밸류에이션. subagent spawn 시 task에 포함. 트리거: 종목/섹터 분석, 밸류에이션, 투자 리서치 요청 시."
---
```
✅ "subagent spawn 시 task에 포함" 명시, 트리거 상황 구체적

## 안티패턴

```yaml
---
name: analyst
version: "1.0"          # ❌ 비표준 필드
trigger: subagent spawn  # ❌ 비표준 필드
description: "투자 분석"  # ❌ 트리거 조건 없음
---
```

## 새 스킬 SKILL.md 템플릿

```markdown
---
name: {skill-name}
description: "{역할 설명}. {subagent면: subagent spawn 시 task에 포함.} 트리거: {트리거 상황}."
---

# {제목}

## 역할
{한 줄 요약}

## 핵심 워크플로우
1. ...
2. ...

## 참고
- 상세 레퍼런스: `references/xxx.md` (읽을 시점: ...)
```
