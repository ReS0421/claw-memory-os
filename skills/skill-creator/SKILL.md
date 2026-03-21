---
name: skill-creator
description: "OpenClaw 로컬 스킬 작성 및 감사 전문. subagent spawn 시 task에 포함. 트리거: 새 스킬 만들어줘, 스킬 감사/개선, skill-creator 요청 시."
---

# Skill Creator

OpenClaw 로컬 스킬(`~/.openclaw/workspace/skills/`)을 작성하거나 감사·개선한다.

## 스킬 경로
- 로컬 스킬: `~/.openclaw/workspace/skills/{skill-name}/`
- 시스템 스킬(읽기 전용): `~/.npm-global/lib/node_modules/openclaw/skills/`

## SKILL.md 필수 구조

```
---
name: skill-name
description: "역할 설명. 트리거 조건 포함. subagent 스킬이면 'subagent spawn 시 task에 포함' 명시."
---

# 제목
(본문)
```

**규칙:**
- frontmatter: `name` + `description` 두 필드만. `version`, `trigger`, `read_when` 등 비표준 필드 금지.
- description: 트리거 조건 반드시 포함. 충분히 구체적으로.
- body: 500줄 이하. 핵심 워크플로우만. 상세 내용은 `references/`로 분리.
- 불필요 파일 금지: README.md, CHANGELOG, INSTALLATION.md 등.

## 디렉토리 구조

```
skill-name/
├── SKILL.md          # 필수
├── references/       # 상세 레퍼런스 (선택)
├── scripts/          # 실행 스크립트 (선택)
└── assets/           # 출력용 파일 (선택)
```

references/는 SKILL.md에서 언제 읽을지 명시해서 링크.

## 새 스킬 작성 절차

1. **목적 파악** — 어떤 상황에서 트리거되는지, 반복되는 작업이 무엇인지
2. **구조 결정** — references/scripts/assets 필요 여부
3. **SKILL.md 작성** — frontmatter → 핵심 워크플로우 순서로
4. **references 작성** — 상세 스키마, API 문서, 예시 등
5. **git 커밋** — `bash ~/.openclaw/workspace/scripts/git-autocommit.sh "skill: {name} 추가"`

## 스킬 감사 절차

1. 각 스킬 SKILL.md 읽기
2. 체크:
   - [ ] frontmatter 비표준 필드 없음
   - [ ] description에 트리거 조건 포함
   - [ ] body 500줄 이하
   - [ ] 불필요 파일 없음
   - [ ] references 분리 적절
3. 문제 있으면 직접 수정
4. 완료 후 스킬별 변경 요약 출력
5. git 커밋

## 우리 시스템 스킬 타입

**메인 세션 스킬** (내가 직접 사용):
`knowledge-ops`, `obsidian-governance`, `notion-portfolio-api`, `notion-general`, `intel-x-post`, `skill-creator`

**Subagent 스킬 — 파이프라인형** (stage/GATE/checkpoint 구조):
`dev-research` (8-stage), `finance-researcher` (6-stage), `finance-analyst` (7-stage)

**Subagent 스킬 — 태스크형** (단발 실행):
`coder-architect`, `coder-planner`, `coder-developer`(reviewer), `openclaw-secretary`, `second-brain-operator`

**확장형 전용:** `coder-spec`, `coder-designer`, `repo-scanner`, `integration-qa`(미생성)

**Deprecated:** `researcher` (→ finance-researcher), `analyst` (→ finance-analyst)

Subagent 스킬은 description에 반드시 "subagent spawn 시 task에 포함" 명시.

## 파이프라인 스킬 작성 가이드

stage 기반 파이프라인 스킬은 아래 요소를 포함해야 한다:

1. **Stage 정의** — 번호, 이름, 목적, 산출물
2. **GATE** — 어느 stage에서 {user} 승인이 필요한지 + GATE 메시지 형식
3. **체크포인트** — `{run_dir}/checkpoint.json` 형식, 재시작 지원
4. **롤백 규칙** — GATE 거부 시 어느 stage로 돌아가는지
5. **저장 경로** — 최종 산출물 + 중간 데이터 각각 명시

참고 예시: `skills/dev-research/SKILL.md`

## 참고
- Anthropic spec 상세: `references/spec.md`
- 기존 스킬 예시: `references/examples.md`
