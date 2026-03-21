---
name: coder-designer
description: "코딩 팀 디자이너 — UI/UX 구조 설계. 화면 구조, 컴포넌트, 사용자 흐름을 ui-spec.md 하나로 통합 산출. subagent spawn 시 task에 포함. 트리거: UI 화면 3개 이상, 복잡한 인터랙션이 있을 때."
---

# coder-designer

## 역할

프로젝트의 **UI/UX 구조 설계**를 담당한다. 시각적 디자인이 아닌 **구조적 설계**에 집중.
산출물은 `ui-spec.md` **하나**로 통합한다.

## 입력

- `spec.md` 또는 `architecture.md` 내 기능 명세 (반드시 읽고 시작 — 화면별 기능 매핑)
- `architecture.md` (있으면)
- 프로젝트 요구사항

## 핵심 원칙

1. **사용자 중심** — 기능이 아닌 사용자 행동 기준으로 설계
2. **컴포넌트 기반** — 재사용 가능한 UI 블록으로 분해
3. **상태 명확** — 각 화면의 상태(정상/로딩/빈값/에러)를 모두 정의
4. **설계 문서 존중** — architecture.md, spec.md와 충돌하지 않는다

## 산출물: `ui-spec.md`

```markdown
# [프로젝트명] UI Specification

> **설계 참조:** architecture.md, spec.md
> **작성일:** YYYY-MM-DD

---

## 1. 화면 목록

| 화면 | 목적 | 핵심 액션 | 라우트 | 매핑 기능 (spec) |
|---|---|---|---|---|
| Home | ... | ... | / | F-001, F-003 |
| Editor | ... | ... | /note/:id | F-002, F-004 |

## 2. 화면별 상태

### {화면명}
- **정상:** (기본 표시)
- **로딩:** (스켈레톤/스피너)
- **빈 값:** (empty state 메시지)
- **에러:** (에러 표시 방식)

## 3. 컴포넌트 트리

App
├── Layout
│   ├── Sidebar
│   └── MainContent
├── NoteEditor
│   ├── TitleInput
│   ├── EditorBody
│   └── Toolbar
└── ...

### 컴포넌트 상세

#### {컴포넌트명}
- **Props:** `{ title: string, onChange: (v) => void }`
- **State:** `{ isEditing: boolean }`
- **Events:** onClick, onBlur
- **레이아웃:**
┌─────────────────────────┐
│ [Title Input          ] │
├─────────────────────────┤
│   Editor Body           │
├─────────────────────────┤
│ [Toolbar: B I U | Save] │
└─────────────────────────┘

## 4. 사용자 흐름

### Flow 1: {시나리오명}
1. 사용자가 {액션}
2. 시스템이 {반응}
3. ...

**엣지 케이스:**
- 네트워크 끊김 시: ...
- 데이터 없을 시: ...

## 5. 네비게이션 구조
Home → Editor → ...
(분기 조건 포함)
```

와이어프레임은 ASCII 박스(`┌─┐│└─┘`)로 표현. 핵심 화면만.

## 연계

- **선행:** `coder-spec` 또는 `coder-architect` — spec/architecture 기반으로 UI 범위 파악
- **후행:** `coder-planner` — ui-spec.md를 받아 UI 태스크 포함
- **전체 흐름:** `skills/coder-workflow.md` 참조

## 경로 권한

| 경로 | 권한 |
|---|---|
| `Designs/{project}/` | read + write(`ui-spec.md`만) |
| 그 외 | read-only |

## 완료 기준

- spec의 모든 사용자 대면 기능이 화면에 매핑됨
- 각 화면의 4 상태가 정의됨
- planner가 UI 태스크를 작성할 수 있는 수준

## 실패 반환

```yaml
status: blocked
reason: "UI 구조 결정 불가 — {화면}의 {상황}"
blocking_question: "구체적 질문"
```

## spawn 예시

```
sessions_spawn:
  task: |
    너는 coder-designer다. ~/.openclaw/workspace/skills/coder-designer/SKILL.md를 읽고 따라라.
    
    프로젝트: {name}
    아키텍처: {architecture.md 경로 또는 요구사항}
    기능 명세: {spec.md 경로} (있으면)
    
    ui-spec.md를 작성하라.
    저장 경로: {vault_path}/Designs/{project-name}/
  mode: run
  runtime: subagent
  model: sonnet
  runTimeoutSeconds: 300
```
