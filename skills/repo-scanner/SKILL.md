---
name: repo-scanner
description: "기존 코드베이스 구조 분석 — 디렉토리 매핑, 핵심 파일 식별, 의존성, 패턴 추출. subagent spawn 시 task에 포함. 트리거: 기존 프로젝트에 작업 시, Phase 2 착수 시, 외부 코드 분석 시."
---

# repo-scanner

## 역할

기존 코드베이스를 분석하여 구조 요약(`codebase-map.md`)을 생성한다.
**코드를 수정하지 않는다.** 읽기만 한다.

## 입력 계약

- 필수: 프로젝트 경로
- 선택: 관심 영역 (특정 모듈/디렉토리), 분석 깊이 (`overview` | `detailed`)

## 절차

1. `tree` + `find`로 디렉토리 구조 스캔
2. 진입점 식별 (main, index, app, server, __init__)
3. 핵심 파일 식별 (10개 이내) + 각 역할 태깅
4. import/require 분석 → 의존성 방향
5. 기존 패턴 추출 (네이밍, 에러 처리, 테스트 구조, 설정 방식)
6. 기술 스택 확인 (package.json, pyproject.toml, go.mod 등)
7. `codebase-map.md` 작성

## 산출물: `codebase-map.md`

```markdown
# [프로젝트명] Codebase Map

> **분석일:** YYYY-MM-DD
> **프로젝트 경로:** ~/projects/{project}/
> **분석 깊이:** overview / detailed

## 기술 스택
- 언어: {lang} {version}
- 프레임워크: {framework}
- 테스트: {test framework}
- 빌드: {build tool}

## 디렉토리 구조
(tree 출력, depth 2~3)

## 핵심 파일

| 파일 | 역할 | 중요도 |
|---|---|---|
| src/index.ts | 앱 진입점 | 높음 |
| src/core/store.ts | 데이터 저장소 | 높음 |
| ... | | |

## 의존성 방향
(모듈 간 import 관계, 간략 그래프)

## 기존 패턴

### 네이밍
- 파일: camelCase / kebab-case
- 함수: {규칙}
- 클래스: {규칙}

### 에러 처리
- {방식}

### 테스트 구조
- 테스트 위치: {__tests__/ | tests/ | 같은 디렉토리}
- 네이밍: {test_*.py | *.test.ts}

## 주의사항
- {planner가 알아야 할 특이 사항}
```

## 경로 권한

| 경로 | 권한 |
|---|---|
| `~/projects/{project}/` | **read-only** |
| `Designs/{project}/codebase-map.md` | **write** |
| 그 외 | 없음 |

exec: read-only (`find`, `grep`, `cat`, `wc`, `tree`, `head`, `git log`)
코드 수정: **금지**

## 완료 기준

- 디렉토리 트리 포함
- 핵심 파일 10개 이내 + 역할 설명
- 기존 패턴 3개 이상 추출
- planner가 읽고 기존 코드와 충돌 없는 plan 작성 가능

## 실패 반환

```yaml
status: partial
reason: "프로젝트가 너무 큼 — {N}개 파일. 관심 영역을 좁혀달라"
suggestion: "{디렉토리}에 집중 권장"
```

## 연계

- **후행:** planner — codebase-map.md 기반으로 기존 패턴 준수하며 plan 작성
- **병렬:** architect/spec-writer와 동시 실행 가능 (입력이 독립적)
- **전체 흐름:** `skills/coder-workflow.md` 참조

## spawn 예시

```
sessions_spawn:
  task: |
    너는 repo-scanner다. ~/.openclaw/workspace/skills/repo-scanner/SKILL.md를 읽고 따라라.
    
    프로젝트 경로: ~/projects/{project}/
    관심 영역: {있으면}
    분석 깊이: overview
    
    codebase-map.md를 작성하라. 코드를 수정하지 마라.
    저장 경로: {vault_path}/Designs/{project}/
  mode: run
  runtime: subagent
  model: sonnet
  runTimeoutSeconds: 300
```
