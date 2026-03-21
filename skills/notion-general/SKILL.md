---
name: notion-general
description: "Notion General 공간 운영 — 개인·팀원용 프로젝트 내부 기록. Obsidian(raw)과 Portfolio Hub(공개) 사이의 정제된 내부 문서 레이어. 트리거: General 하위 페이지 작성/수정, 프로젝트 내부 기록 요청 시."
---

# Notion General — 내부 프로젝트 기록 레이어

## 역할 정의

General은 Obsidian과 Portfolio Hub 사이의 **내부 정제 레이어**다.

```
Obsidian          →  원본/raw 기록 (개인)
General (Notion)  →  내부 정제본 (팀 공유 가능, 과정 보존)
Portfolio Hub     →  공개 발행본 (포트폴리오)
```

- Obsidian보다 정제되어 있고
- Portfolio Hub보다 원문에 가깝다
- 팀원과 공유 가능한 수준으로 정리하되, 외부 공개 포장은 없음

---

## 공간 ID

- **General root**: `{general_root_id}`

현재 하위 프로젝트:
- {project_name}: `{page_id}`
- {project_name}: `{notion_page_id}`

> 전체 하위 ID → `{vault_path}/System/notion-ids.md`

---

## 페이지 구조 (프로젝트 단위)

새 프로젝트 추가 시 아래 구조를 기본으로 한다.

```
General
└── {프로젝트명}                ← 프로젝트 루트 (parent: General root)
    ├── Overview               ← 목표·배경·멤버·상태 요약 (1페이지)
    ├── Log/                   ← 날짜별 진행 기록
    │   ├── YYYY-MM-DD
    │   └── ...
    ├── Decisions/             ← 주요 결정 기록 (Why 중심)
    └── Artifacts/             ← 산출물 (SOP, KPI표, 기획서 등)
```

### 각 페이지 역할

**Overview**
- 한 눈에 파악 가능한 수준으로 작성
- 포함: 목표, 배경, 참여 멤버, 현재 상태, 주요 링크
- Obsidian의 MOC(Map of Content)에 대응

**Log/**
- 날짜 기준 진행 일지
- 형식 자유 — 회의록, 작업 메모, 인사이트 모두 가능
- Obsidian daily note보다 정제되어 있되 과정 전부 포함

**Decisions/**
- "왜 이 선택을 했는가" 중심
- 포함: 배경 / 선택지 / 결정 / 근거
- 나중에 Portfolio Hub Case Study 작성 시 핵심 소스

**Artifacts/**
- 실제 산출물 페이지 (SOP, 기획서, KPI표 등)
- 완성도 기준으로 관리 — 초안도 포함 가능

---

## 작성 원칙

1. **과정을 보존한다.** 실패, 변경, 우회도 기록. Portfolio Hub처럼 성공 서사로 편집하지 않음.
2. **팀원 가독성을 확보한다.** Obsidian 개인 메모보다 문장을 갖춰 쓴다.
3. **발행을 전제하지 않는다.** Portfolio Hub 발행은 별도 판단. General 기록이 자동으로 공개되지 않음.
4. **Obsidian과 중복을 허용한다.** 같은 내용이 양쪽에 있어도 됨. 목적이 다름.

---

## 쓰기 규칙

- 새 프로젝트 루트 페이지 생성: `notion_create_page_markdown(parent_id="{general_root_id}")`
- 하위 페이지 생성: `notion_create_page_markdown(parent_id="{프로젝트 루트 ID}")`
- 기존 페이지 수정: callout/toggle 있으면 `append_block_markdown` 또는 `insert_block_after`
- 텍스트만 있는 단순 페이지: `update_page_markdown` 가능
- write 전 반드시 `notion_validate_access`

### 금지
- General root 페이지 자체를 교체/삭제하지 않는다
- General 하위 페이지를 Portfolio Hub로 이동 시 → {user} 확인 필수
- 외부 공개 링크 생성 금지 (General은 비공개 공간)

---

## Portfolio Hub 발행 연계

General 기록 → Portfolio Hub 발행은 **knowledge-ops 스킬** 기준을 따른다.

연계 흐름:
1. General `Decisions/` + `Log/` → Portfolio Hub **Case Study** 소스
2. General `Overview` → Portfolio Hub **Project** 허브 소스
3. General `Artifacts/` → Portfolio Hub에 직접 첨부 또는 링크

발행 시 재구성 필수 (General 원문 그대로 옮기지 않음).

---

## 에러 대응

| 코드 | 원인 | 대응 |
|------|------|------|
| 403 | integration 미공유 | Notion UI → General 페이지 → Share → integration 초대 |
| 404 | ID 오류 | notion-ids.md 확인 |
| 429 | Rate limit | 대기 후 재시도 |
