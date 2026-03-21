# Coder Workflow — 코딩 팀 오케스트레이션

> 이 문서는 openclaw 메인 세션이 참조하는 워크플로우다.
> 각 subagent는 자기 역할만 안다. 전체 흐름과 오케스트레이션은 openclaw이 한다.

---

## 계층 구조

```
설계 계층 (사고)     : architect → [spec-writer] → [designer] → planner
                                                                   ↓
실행 계층 (런타임)   :                                            ACP
                                                                   ↓
검증 계층 (사고)     :                                   reviewer / [integration-qa]
```

- ACP는 subagent가 아니라 **런타임**이다. tasks.md를 받아 실행하는 환경.
- `[]`는 확장형에서만 투입. 최소형에서는 생략.

---

## 운영 모드

### 최소 운영형 (기본)

```
[architect] → planner → ACP → reviewer
```

- architect: 시스템 설계 + 기능 명세 통합 (선택)
- planner: 구현 계획 (필수)
- ACP: Claude Code 런타임
- reviewer: diff 리뷰 + 스펙 검증

**subagent 수:** 2~3개. **문서:** architecture.md, decisions.md, tasks.md — 최대 3개.

### 확장 운영형 (Laplace급)

```
architect → [repo-scanner] → [spec-writer] → [designer] → planner → [plan review] → ACP → reviewer → [integration-qa]
```

**확장 순서 (필요 시에만 추가):**
1. 기본: architect + planner + ACP + reviewer
2. 기존 코드: + repo-scanner
3. 복잡 기능: + spec-writer (architect에서 분리)
4. UI 프로젝트: + designer
5. 대형 멀티모듈: + integration-qa
6. 극대형: + task-packager (planner에서 분리)

---

## 복잡도 판단

### architect 필요 여부

| 기준 | 필요 | 불필요 |
|---|---|---|
| 서브시스템 수 | 2개 이상 | 1개 |
| 기술 스택 결정 | 전체에 영향 | 명확/기존 스택 |
| 예상 파일 수 | 15+ | 10 이하 |

### designer 필요 여부

| 기준 | 필요 | 불필요 |
|---|---|---|
| UI 유무 | 웹/앱/대시보드 | CLI, API, 백엔드 |
| 화면 수 | 3개 이상 | 1~2개 |
| 인터랙션 | 복잡 | CRUD 수준 |

### spec-writer 분리 여부

| 기준 | 분리 | architect 통합 |
|---|---|---|
| 기능 수 | 10개 이상 | 10개 미만 |
| 동작 복잡도 | 엣지 케이스 많음 | 자명한 동작 |

---

## 단계별 상세

### Step 0: 요구사항 정리 (openclaw ↔ {user})

**이 단계는 subagent가 아니라 openclaw(나)이 직접 수행한다.**

architect를 spawn하기 전에, {user}와 대화하며 아래를 확정한다:

#### 확인 항목

1. **무엇을 만드는가** — 한 문장으로 정의 가능한가
2. **누가 쓰는가** — 사용자와 사용 맥락
3. **핵심 기능 3~5개** — "이것만 되면 MVP"
4. **안 만드는 것** — 범위 밖 명시 (scope creep 방지)
5. **기술 제약** — 언어, 프레임워크, 배포 환경 등 이미 결정된 것
6. **우선순위** — P0(필수) / P1(중요) / P2(나중)

#### 산출물: `requirements.md`

```markdown
# [프로젝트명] Requirements

> **rev:** 1 | **updated:** YYYY-MM-DD | **breaking:** no
> **합의:** {user} 확인 완료

## 개요
[한 문장 — 무엇을 만드는가]

## 사용자 / 맥락
[누가, 어디서, 왜 쓰는가]

## 핵심 기능

| ID | 기능 | 우선순위 | 설명 |
|---|---|---|---|
| R-001 | ... | P0 | ... |
| R-002 | ... | P1 | ... |

## 범위 밖 (Out of Scope)
- ...

## 기술 제약
- 언어: ...
- 프레임워크: ...
- 배포: ...

## 미결 사항
- [ ] ...
```

#### 진행 기준

아래 모두 충족 시 다음 단계(architect 또는 planner) 진행:
- [ ] {user}가 기능 목록을 확인했다
- [ ] 범위 밖이 명시되었다
- [ ] 우선순위가 결정되었다
- [ ] 미결 사항이 없거나, 있어도 다음 단계 진행에 지장 없다

**저장:** `{vault_path}/Designs/{project}/requirements.md`

---

### Step 1: architect (선택)

```
sessions_spawn:
  runtime: subagent
  model: opus
  task: |
    ~/.openclaw/workspace/skills/coder-architect/SKILL.md 읽고 따라라.
    프로젝트: {name}
    요구사항: {vault_path}/Designs/{project}/requirements.md
    기술 리서치 (있으면): {dev-research 결과 경로}
    저장 경로: {vault_path}/Designs/{project}/
```

**산출물:** `architecture.md` (기능 명세 포함), `decisions.md`

### Step 1.5: spec-writer (확장형, 선택)

architect에서 분리 필요 시에만.
**산출물:** `spec.md` 또는 `spec-{module}.md`

### Step 2: designer (확장형, UI 프로젝트만)

```
sessions_spawn:
  runtime: subagent
  model: sonnet
  task: |
    ~/.openclaw/workspace/skills/coder-designer/SKILL.md 읽고 따라라.
    프로젝트: {name}
    아키텍처: {architecture.md 경로}
    기능 명세: {spec.md 경로} (있으면)
    저장 경로: {vault_path}/Designs/{project}/
```

**산출물:** `ui-spec.md`

### Step 3: planner (필수)

**입력:**
- architecture.md (기능 명세 포함, 있으면)
- spec.md (확장형, 있으면)
- ui-spec.md (있으면)
- codebase-map.md (있으면)

```
sessions_spawn:
  runtime: subagent
  model: opus
  task: |
    ~/.openclaw/workspace/skills/coder-planner/SKILL.md 읽고 따라라.
    프로젝트: {name}
    설계 문서: {vault_path}/Designs/{project}/
    저장 경로: {vault_path}/Designs/{project}/
```

**산출물:** `tasks.md` 또는 `tasks-{module}.md`

> Iterative planning: 대형 프로젝트에서 planner는 한 모듈씩 계획한다.
> Module 1 구현 완료 → Module 2 계획 → ... 이전 모듈 결과가 다음 계획에 반영된다.

### Step 3.5: plan review (확장형, architect 겸임)

대형 프로젝트에서만. architect에게 reviewer 역할로 spawn:
- architecture.md vs tasks.md 정합성 5개 항목 검토
- 승인 / 수정 요청

### Step 4: ACP (Claude Code 런타임)

ACP는 subagent가 아니라 **실행 환경**이다.

```
sessions_spawn:
  runtime: acp
  task: |
    아래 설계 문서를 읽고 tasks.md를 순차 구현하라.
    설계 문서: {vault_path}/Designs/{project}/
    프로젝트 경로: ~/projects/{project}/
  attachments:
    - name: tasks.md
      content: (tasks.md 내용)
  cwd: ~/projects/{project}
```

**세션 전략:**

| 규모 | 모드 | 전략 |
|---|---|---|
| 단순 (태스크 10 이하) | `mode: run` | tasks.md 통째로 |
| 중형 (10~25) | `mode: session`, `thread: true` | {user} 개입 가능 |
| 대형 (25+, 모듈 분리) | `mode: session`, `thread: true` | 모듈별 순차 |

**ACP 규칙:**
- Designs/ 문서를 수정하지 않는다
- 프로젝트 코드만 소유
- tasks.md의 품질이 곧 output 품질 — ACP가 추측하면 tasks.md 탓

### Step 5: reviewer (필수)

```
sessions_spawn:
  runtime: subagent
  model: sonnet
  task: |
    ~/.openclaw/workspace/skills/coder-developer/SKILL.md 읽고 따라라.
    역할: 리뷰어
    프로젝트: {name}
    프로젝트 경로: ~/projects/{project}/
    설계 문서: {vault_path}/Designs/{project}/
    검토 대상: {변경 파일 또는 커밋 범위}
    코드를 수정하지 마라. 이슈를 리포트하라.
```

**결과 처리:**
- ✅ 승인 → 완료 (또는 다음 모듈)
- ❌ must-fix → ACP에 수정 태스크 재위임 (Step 4 재실행)

### Step 5.5: integration-qa (확장형)

모듈 2개 이상 완료 후, Phase 전환 전.
전체 테스트 + 모듈 간 인터페이스 + 회귀 체크.

---

## Iterative Planning (대형 프로젝트)

```
architect: 전체 구조 + 모듈 순서 결정
  → Module 1: planner → [review] → ACP → reviewer ✅
  → Module 2: planner → [review] → ACP → reviewer ✅
  → Module 3: planner → [review] → ACP → reviewer ✅
  → Integration: planner → ACP → reviewer + [integration-qa] ✅
```

- 전체를 한 번에 계획하지 않는다
- 이전 모듈 구현 결과가 다음 모듈 계획에 반영된다
- tasks-integration.md는 항상 마지막

---

## 설계 변경 관리

```
변경 발생
    │
    ▼
[1] 영향 범위 판단
    ├── 단일 모듈 내 → planner가 tasks.md 수정
    ├── 모듈 간 인터페이스 → architect가 architecture.md 업데이트
    └── 근본적 방향 전환 → {user} 확인 → architect 재설계

[2] decisions.md에 기록 (항상)

[3] 영향받는 문서/코드 수정
```

---

## 문서 버전 연동

### 왜 필요한가

spec을 수정했는데 tasks.md에 옛 기준이 남아있으면 → ACP가 옛 테스트를 통과시키려 구현 → 잘못된 구현.
문서 간 정합성이 깨지는 순간 전체 파이프라인이 무의미해진다.

### 버전 헤더 규칙

모든 설계 문서에 버전 헤더를 포함한다:

```markdown
> **rev:** 2 | **updated:** 2026-03-20 | **breaking:** yes
```

- `rev`: 순차 정수. 내용 변경 시마다 +1
- `updated`: 최종 수정일
- `breaking`: 하류 문서에 영향을 주는 변경이면 `yes`

### 하류 문서 의존성 선언

tasks.md 헤더에 의존하는 상류 문서의 버전을 선언:

```markdown
> **depends-on:**
> - architecture.md rev 3
> - spec.md rev 2 (확장형)
> - ui-spec.md rev 1 (있으면)
```

### 정합성 검증 규칙

1. **상류 문서가 breaking 변경되면** → 하류 문서는 무효
   - architecture.md breaking → spec, tasks, ui-spec 모두 재검토
   - spec.md breaking → tasks.md 재검토
   - ui-spec.md breaking → tasks.md의 UI 태스크만 재검토

2. **openclaw이 변경 전파를 관리한다:**
   ```
   상류 문서 변경 (breaking: yes)
       ↓
   openclaw: "tasks.md가 spec rev 2 기반인데, spec이 rev 3으로 변경됐다"
       ↓
   planner에게 tasks.md 업데이트 요청 (변경 사항 명시)
   ```

3. **reviewer가 버전 불일치를 잡는다:**
   - 리뷰 시 tasks.md의 `depends-on` vs 실제 상류 문서 rev를 대조
   - 불일치 시 → must-fix 이슈로 리포트

### non-breaking 변경

오타 수정, 문구 개선, 추가 설명 등 하류에 영향 없는 변경:
- rev는 올리되 `breaking: no`
- 하류 문서 재검토 불필요

---

## 문서 관리

### 설계 문서 (Designs/{project}/)

| 문서 | 생성자 | 최소형 | 확장형 |
|---|---|---|---|
| requirements.md | openclaw ({user} 합의) | ✅ | ✅ |
| architecture.md | architect (또는 planner) | ✅ (기능 명세 포함) | ✅ |
| decisions.md | architect | ✅ | ✅ |
| spec.md | spec-writer | ❌ | 선택 |
| ui-spec.md | designer | ❌ | 선택 |
| tasks*.md | planner | ✅ | ✅ |
| codebase-map.md | repo-scanner | ❌ | 선택 |

### 프로젝트 코드 문서

| 문서 | 위치 | ACP가 관리 |
|---|---|---|
| README.md | ~/projects/{project}/ | Task 0 + 모듈마다 |
| CHANGELOG.md | ~/projects/{project}/ | 모듈마다 |

### decisions.md 누적 규칙

설계 ~ 구현 전 과정에서 누적:
- architect: 설계 결정
- openclaw: 구현 중 설계 변경 (ACP/reviewer 보고 기반)

---

## Handoff 규칙

모든 agent 간 인계는 **파일**로 한다. 메시지 전달 없음.

```
agent A → 파일 (Designs/{project}/) → agent B
```

- 파일이 없으면 해당 단계를 건너뛴 것 — 다음 agent는 없는 파일을 요구하지 않음
- 파일 이름이 계약 (architecture.md, spec.md, tasks.md, ui-spec.md)

---

## 권한 매트릭스

### 설계 계층 vs 실행 계층 vs 검증 계층

| agent | ~/projects/ | Designs/ | exec | 원칙 |
|---|---|---|---|---|
| architect | read | **write** (arch, decisions) | read-only | 구조를 정하지만 코드를 만들지 않는다 |
| spec-writer | read | **write** (spec) | read-only | 동작을 정하지만 구현하지 않는다 |
| designer | read | **write** (ui-spec) | read-only | 화면을 정하지만 만들지 않는다 |
| planner | read | **write** (tasks) | read-only | 계획을 세우지만 실행하지 않는다 |
| **ACP** | **write** | read | **full** | 유일한 코드 생성자 |
| **reviewer** | **read-only** | **read-only** | **test-run only** | 판단만. 수정 금지 |
| **integration-qa** | **read-only** | **read-only** | **full** (test) | 실행만. 수정 금지 |
| repo-scanner | read-only | write (map) | read-only | 분석만. 수정 금지 |

### 핵심 제약

**검증 계층(reviewer, integration-qa)은 코드/문서를 수정하지 않는다.**

이 제약은 "규칙"이 아니라 **구조적 안전장치**다:
- reviewer가 코드를 고치면 → 자기 수정을 자기가 리뷰하는 셈 → 리뷰 독립성 상실
- 수정이 필요하면 → 이슈 리포트 → openclaw이 ACP에 재위임
- 이 루프가 비효율적으로 보여도, 검증 독립성이 더 중요하다

**설계 계층은 코드를 생성하지 않는다.**

- architect/spec/designer/planner는 문서만 작성
- 코드를 직접 만들면 → planner가 자기 plan을 자기가 구현하는 셈 → plan 품질 검증 불가

**ACP는 설계 문서를 수정하지 않는다.**

- ACP가 architecture.md를 수정하면 → 설계 변경이 추적 불가
- 설계 변경은 반드시 설계 계층을 거쳐야 한다

### spawn 시 권한 전달

reviewer/qa spawn 시 task에 명시적으로 제약을 포함:

```
코드를 수정하지 마라. 이슈를 리포트하라.
Designs/ 문서를 수정하지 마라.
```

> 현재 subagent에 기술적 write 제한을 거는 방법은 없다 (exec 접근은 동일).
> 따라서 **skill 내 규칙 + spawn task 내 명시적 제약**으로 통제한다.
> 추후 OpenClaw에 subagent sandbox 기능이 추가되면 환경 수준 제한으로 전환.

---

## 비용 참고

| 역할 | 모델 | 비용 |
|---|---|---|
| architect | opus | 높음 |
| spec-writer | opus | 높음 (확장형만) |
| planner | opus | 높음 |
| designer | sonnet | 보통 (확장형만) |
| ACP | ACP 기본 | 가변 |
| reviewer | sonnet | 보통 |
| repo-scanner | sonnet | 보통 (확장형만) |
| integration-qa | sonnet | 보통 (확장형만) |

최소형: opus 1~2회 + sonnet 1회 + ACP
확장형: opus 2~3회 + sonnet 2~4회 + ACP

---

## dev-research 연계

기술 스택 결정에 리서치 필요 시:
```
dev-research → architect → ...
```
dev-research 결과 경로를 architect spawn에 포함.
