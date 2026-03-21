---
name: knowledge-ops
description: >
  Obsidian + Notion 이중 운영 체계의 상위 규칙.
  Obsidian이 중심이고 Notion은 취사선택 발행 레이어.
  트리거: 콘텐츠 작성/정리/발행/업데이트 요청 시, Obsidian↔Notion 운영 판단이 필요할 때 이 스킬을 먼저 로드.
---

# Knowledge Ops — 이중 운영 체계

## 핵심 원칙

1. **Obsidian이 중심이다.** 모든 콘텐츠의 원본은 Obsidian에 존재한다.
2. **Notion은 발행 레이어다.** Obsidian의 콘텐츠 중 선별하여 Notion에 재구성한다.
3. **발행은 지시 시에만.** {user}가 Notion에 올리라고 할 때만 발행한다.
4. **재구성이지 복사가 아니다.** Notion에 올릴 때 Obsidian 원문을 그대로 옮기지 않는다. Notion의 구조와 목적에 맞게 재구성한다. Obsidian보다 더 길어질 수도 있다.

---

## 시스템 역할 정의

```
Obsidian          →  원본/raw 기록 (개인)
General (Notion)  →  내부 정제본 (팀 공유 가능, 과정 보존)
Portfolio Hub     →  공개 발행본 (포트폴리오)
```

### Obsidian (중심) — {obsidian_vault}

나의 모든 콘텐츠의 원본. PARA 구조.

- **Projects/** — 마감 또는 산출물이 있는 활성 작업. 진행 중인 프로젝트, 달성할 목표가 있는 것
- **Areas/** — 종료 없이 지속되는 관심 영역. AI, Coding, Finance, Productivity, 건강, 일상 기록 등
- **Resources/** — 재사용 가능한 참고 자료. 프레임워크, 템플릿, 도구 노트, 외부 자료 정리
- **Archive/** — 비활성/완료된 것. 더 이상 발전시키지 않지만 보존할 가치가 있는 것
- **_Atlas/** — 내비게이션 허브. Home.md = 메인 진입점
- **_System/** — 운영 문서, 거버넌스, 로그
- **_Assets/** — 첨부 파일
- **_Trash/** — 소프트 삭제

### Notion General (내부 정제 레이어)

Obsidian보다 정제되어 있고 Portfolio Hub보다 원문에 가까운 **내부 공유 공간**.

- **General root** (`{general_root_id}`)
- 프로젝트별 페이지 구조: Overview / Log / Decisions / Artifacts
- 비공개 — 팀원 공유 가능하나 외부 공개 아님
- 상세 운영 규칙 → `skills/notion-general/SKILL.md`

### Notion Portfolio (공개 발행 레이어)

Obsidian에서 취사선택한 콘텐츠를 재구성하여 발행하는 곳.

- **{user} · Portfolio** (`{portfolio_root_id}`) — 포트폴리오 루트 페이지
- **Portfolio Home DB** (`{portfolio_home_db_id}`) — 내비게이션 허브
  - Domains DB (`{domains_db_id}`) — 8개 지식 영역 분류 (taxonomy)
  - Projects DB (`{projects_db_id}`) — 이니셔티브 허브. 개요·상태·마일스톤 중심
  - Case Studies DB (`{case_studies_db_id}`) — 서사·의사결정·회고 중심. Project에 링크
  - Research / Notes DB (`{research_notes_db_id}`) — 학습 로그, 리서치, 아이디어
  - Portfolio Home (허브 페이지) (`{portfolio_home_page_id}`) — 탐색 진입점
- **Portfolio Hub Free Tier** (`{portfolio_hub_free_id}`) — Notion 공식 마켓 무료 공개용

### Archive 차이

- **Obsidian**: 완료된 프로젝트는 Archive/ 폴더로 이동. PARA 체계의 일부.
- **Notion**: 완료 프로젝트도 DB 안에 유지하고 Status로 구분. `notion_archive_page`는 soft-delete(trash)용.
- "archive 해줘" 요청 시 → 문맥으로 구분.

### Areas vs Domains 비대칭

Obsidian Areas와 Notion Domains는 1:1 대응이 아니다.
Obsidian은 개인 운영 중심이라 더 넓고 생활 밀착적일 수 있고 (Lifestyle, Daily Notes 등),
Notion은 포트폴리오/탐색 중심이라 압축된 taxonomy를 사용한다 (7개 Domains).
Obsidian의 모든 Area가 Notion Domain에 대응하지 않으며, 그래야 할 이유도 없다.

---

## 작업 흐름: 의사결정 트리

### 새 콘텐츠 작성 요청

```
요청이 들어왔다
├── 개인 메모, 강의 노트, 일상 기록, 투자 분석, 학습 노트
│   → Obsidian에만 작성. 끝.
│
├── 팀 공유 또는 내부 정제 문서 (SOP, 기획서, 프로젝트 기록)
│   → General (Notion) 에 작성
│   → 필요 시 Obsidian에도 원본 유지
│
└── 포트폴리오, 공개 발행, 외부 공유 목적
    → Obsidian에 먼저 작성
    → {user}가 "올려줘" 지시 → Portfolio Hub에 재구성하여 발행
```

### 기존 콘텐츠 업데이트 요청

```
업데이트 대상이 어디에 있는가?
├── Obsidian에만 있음
│   → Obsidian 업데이트. 끝.
│
├── General에 있음
│   → General 업데이트
│   → Obsidian 원본도 있으면 함께 확인
│
├── Portfolio Hub에만 있음
│   → Obsidian에 원본 먼저 생성 or 확인
│   → 그 다음 Portfolio Hub 업데이트
│
└── 여러 곳에 있음
    → Obsidian 원본 먼저 확인/업데이트
    → 그 다음 Notion 반영 ({user} 지시 시)
```

### Notion 발행 흐름 (Portfolio Hub)

```
{user}가 "Notion에 올려줘" 지시
│
├── 1. Obsidian 원본 확인 (최신 상태인지)
├── 2. Portfolio Hub에 이미 존재하는지 확인 (notion_search)
│   ├── 존재 → 기존 페이지 업데이트
│   └── 미존재 → Portfolio Home DB 아래 해당 DB에 새 페이지 생성
├── 3. Notion에 맞게 재구성하여 작성
├── 4. DB property 설정 (Domain, Status, Visibility 등)
└── 5. Portfolio Home 페이지에 노출 (block insert)
```

---

## Notion 발행 기준

### General (내부 정제본)에 가야 하는 콘텐츠
- 팀원과 공유할 프로젝트 기록, SOP, 기획서
- 과정·맥락을 보존해야 하는 내부 문서
- Portfolio Hub보다 원문에 가깝게 유지하고 싶은 것

### Portfolio Hub (공개 발행본)에 가야 하는 콘텐츠
- 포트폴리오에 포함할 프로젝트, 케이스 스터디
- 외부 공유가 필요한 정리된 문서
- {user}가 "올려줘"라고 지시한 것

### Obsidian에만 있으면 되는 콘텐츠
- 개인 메모, 일상 기록
- 강의 노트, 학습 노트
- 투자 분석, 기업 리서치
- 회의록, raw 자료
- 아직 정리되지 않은 초안/fragment
- **리서치 파이프라인 산출물** — 아래 경로에 자동 저장됨:
  - 시장·거시경제 리서치 → `Resources/Research/Markets/`
  - 제품·시장 분석 → `Resources/Research/Product/`
  - 리서치 메모 → `Resources/Research/Notes/`
  - 일일 브리핑 (Intel Pipeline) → `Resources/Daily digests/`

### 판단이 애매할 때
- {user}에게 물어본다: "General에 정리할까요, Portfolio Hub에 올릴까요?"

---

## Notion 도구 제약

Notion 블록 생성 능력의 상세는 notion-portfolio-api 스킬을 참조.
plugin v3 기준 대부분의 블록 타입을 네이티브 지원한다.
column_list/column, synced_block, breadcrumb 포함.

### Notion API 버전 참고 (2022-06-28 기준)
- `archived` 필드 → `in_trash`로 대체 (현행)
- 아카이브 요청: `{ in_trash: true }`
- plugin NOTION_VERSION: "2022-06-28" (2026-03-21 수정 — "2026-03-11"은 query POST 오류 유발)

---

## 쓰기 안전 규칙

- callout/toggle/page mention이 있는 기존 페이지 → `update_page_markdown` 전체 교체 금지
- 텍스트만 있는 단순 페이지 → `update_page_markdown` 사용 가능
- Portfolio Home 페이지 → 전체 교체 절대 금지. `append_block_markdown` 사용
- 새 페이지 → `create_page_markdown` 자유 사용
- 기존 페이지에 추가 → `append_block_markdown` (끝에 추가)
- validate before write / read before write / archive > delete

---

## 서술 원칙

### 1인칭 기본 (포트폴리오 / 프로젝트 / 경험 / 케이스 스터디)
- "나는 이 프로젝트를 리딩했다" (O)
- "{user}는 이 프로젝트를 리딩했다" (X)

### 중립 서술 허용 (개념 / 리서치 / 레퍼런스 / 거버넌스 / 강의 요약)
- 내용의 성격에 맞게 중립 서술 가능
- 예: "PARA 체계는 ~로 구성된다" (O)

---

## 하위 스킬 참조 규칙

이 스킬(knowledge-ops)을 로드한 상태에서:

- **Obsidian 내부 작업** (폴더 배치, 프론트매터, 노트 타입 판단)
  → `skills/obsidian-governance/SKILL.md` 참조
- **Notion General 작업** (내부 프로젝트 기록, 팀 공유 문서)
  → `skills/notion-general/SKILL.md` 참조
- **Notion Portfolio Hub 작업** (DB 스키마, property 설정, ID, 블록 구문)
  → `skills/notion-portfolio-api/SKILL.md` 참조
- **리서치 결과 저장 위치 판단** (기술 리서치 / 금융 리서치 / 투자 분석)
  → 각 리서치 스킬이 자체 저장 경로를 가짐. Notion 발행 시에만 knowledge-ops 규칙 적용
- 참조가 필요하면 해당 스킬 파일을 그때 읽는다

---

## Portfolio Home 페이지 운영

- ID: `{portfolio_home_page_id}`
- 역할: 탐색 진입점
- **전체 교체 금지**

### 새 항목 노출 절차
1. Portfolio Home DB 아래에 페이지 생성
2. {user} 확인
3. `notion_get_block_ids`로 메인 페이지 블록 조회
4. `notion_append_block_markdown`으로 끝에 추가 후 Notion UI에서 원하는 위치로 드래그
5. 토글은 내용이 채워진 상태로 삽입
