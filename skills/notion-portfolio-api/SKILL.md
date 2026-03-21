---
name: notion-portfolio-api
description: "Notion 도구 사용법, DB 스키마 레퍼런스, 블록 구문 레퍼런스. 시스템 간 관계와 발행 흐름은 knowledge-ops 스킬을 참조. 트리거: notion_* 도구 사용 시, Notion DB 스키마/property/ID 확인 시, 블록 구문 확인 시."
---

# Notion API — 도구 레퍼런스

## 역할

Notion 도구의 사용법, DB 구조, 블록 구문 레퍼런스를 다룬다.
Obsidian과의 관계, 발행 기준, 작성 루트는 **knowledge-ops 스킬**에 정의되어 있다.

**상세 ID 레퍼런스** → `{vault_path}/System/notion-ids.md`

---

## 인증

- 토큰 우선순위: NOTION_API_KEY (preferred) → NOTION_TOKEN
- 토큰 값 절대 출력 금지
- write 작업 전 반드시 `notion_validate_access` 실행
- 401 → NOTION_API_KEY 확인, gateway 재시작
- 403 → Notion UI에서 해당 페이지/DB를 integration에 공유

---

## Notion 공간 구조

```
General (최상위 — 개인·팀원용 공간, 비공개)
├── Improving cleaning company work efficiency
└── {project_name}

{user} · Portfolio (포트폴리오 메인 페이지)
└── OpenClaw로 AI 운영 시스템 구축하기

Portfolio Home DB (포트폴리오 내비게이션 허브)
├── Domains        → Domains DB
├── Projects       → Projects DB
├── Research/Notes → Research/Notes DB
├── Case Studies   → Case Studies DB
└── Portfolio Home (허브 페이지)

Portfolio Hub Free Tier (Notion 마켓 무료 공개용)
```

### 핵심 ID (자주 쓰는 것)

| 공간 | root ID |
|---|---|
| General | `{general_root_id}` |
| Portfolio Home DB | `{portfolio_home_db_id}` |
| Portfolio Hub Free Tier | `{portfolio_hub_free_id}` |

| DB | ID |
|---|---|
| Projects (Portfolio Home) | `{projects_db_id}` |
| Case Studies (Portfolio Home) | `{case_studies_db_id}` |
| Research / Notes (Portfolio Home) | `{research_notes_db_id}` |
| Domains (Portfolio Home) | `{domains_db_id}` |

> 전체 ID 목록 → `notion-ids.md` 참조

---

## General 공간 운영 규칙

- **용도**: 개인 공간 + 팀원 공유 문서. 포트폴리오와 분리.
- **쓰기 주의**: General 하위에 새 페이지 생성 시 parent_id = `{general_root_id}`
- **공개 여부**: 비공개 (포트폴리오 공개 대상 아님)
- General 하위 문서를 포트폴리오용으로 이동 시 {user} 확인 필수

---

## DB 스키마

### Relation Chain (Portfolio Hub)
```
Domain → Project (Hub) → Case Study (Narrative)
                       → Research / Notes (Reference)
```

### Domain Taxonomy (8개)
AI · Coding · Finance · Productivity · SNS Operations · Systems/Workflow · Soft Skills & Leadership · Career

### Visibility 체계
Internal → Curated → Public → Featured

### Property 핵심
- **Projects**: Name, Summary, Status, Visibility, Domain(s), Tags, Start Date
- **Case Studies**: Name, Project [relation], Status, Visibility, Domain(s), Tags
- **Research/Notes**: Name, Summary, Domain(s), Related Project(s), Content Type, Status, Visibility, Tags

---

## 도구 사용 가이드

### Read (안전)
| 도구 | 용도 |
|------|------|
| notion_validate_access | write 세션 시작 시 |
| notion_search | 중복 확인, ID 조회 |
| notion_get_page_meta | 구조 확인 |
| notion_get_page_markdown | 내용 읽기 |
| notion_list_child_pages | 하위 목록 |
| notion_query_data_source | DB 쿼리 |
| notion_get_block_ids | 블록 ID 조회 (insert_after용) |

### Write (validated access 필요)
| 도구 | 용도 | 주의 |
|------|------|------|
| notion_create_page_markdown | 새 페이지 | 중복 확인 후 |
| notion_update_page_markdown | 전체 교체 | 텍스트만 있는 페이지에만 |
| notion_update_page_properties | 메타데이터만 | 내용 미변경 |
| notion_archive_page | Soft-delete | |
| notion_append_block_markdown | 끝에 추가 | 기존 블록 보존 |
| notion_insert_block_after | 특정 블록 뒤에 삽입 | get_block_ids 먼저 |

### 안전 규칙
1. validate before write
2. read before write
3. archive > delete
4. 중복 생성 금지 (search 먼저)
5. Portfolio Main 메인 페이지 → **전체 교체 절대 금지**
6. General 하위 변경 시 → 비공개 공간임을 인지하고 작업

---

## 쓰기 안전 규칙

- callout/toggle/page mention이 있는 기존 페이지 → `update_page_markdown` 금지
- 텍스트만 있는 단순 페이지 → `update_page_markdown` 사용 가능
- 기존 페이지에 추가 → `append_block_markdown`
- 위치 지정 삽입 → `insert_block_after` (get_block_ids로 ID 먼저 조회)

---

## 블록 구문 요약

Plugin v3 기준. **상세 구문 레퍼런스 → `references/block-syntax.md`**

### Standard Markdown → Notion
`#/##/###` heading · `- ` bullet · `1. ` numbered · `- [ ]` to_do · `> ` quote · `---` divider · `` ```lang ``` `` code · `![alt](url)` image · `$$expr$$` equation · `| | |` table

### Custom Syntax `[[ ]]` → Notion 전용 블록

**Callout / Toggle**
- `[[ text ]]` — callout (💡, blue_background)
- `[[ 🔒 text ]]` — callout (커스텀 이모지 아이콘)
- `[[! text ]]` — callout 경고 (⚠️, red_background)
- `[[> title ]]` — toggle (빈)
- `[[> title ]]{` ... `}]` — toggle + children (recursive)

**Page Mention / Link**
- `[[@ page_id | label ]]` — page/database mention (인라인/블록 모두 지원. 단독 줄이면 paragraph 블록으로, 문장 안이면 mention rich_text로 파싱됨)
- `[[@ page_id ]]` — page mention (auto title)
- `[[link: page_id ]]` — link_to_page
- `[[link: page_id | database ]]` — link_to_page (database)

**Navigation**
- `[[toc]]` — table_of_contents
- `[[breadcrumb]]` — breadcrumb

**Media / Embed**
- `[[bookmark: url ]]` — bookmark
- `[[bookmark: url | caption ]]` — bookmark with caption
- `[[embed: url ]]` — embed
- `[[image: url ]]` — image (= `![image](url)`)
- `[[image: url | caption ]]` — image with caption
- `[[video: url ]]` — video (external)
- `[[audio: url ]]` — audio (external)
- `[[file: url ]]` — file (external)
- `[[file: url | caption ]]` — file with caption
- `[[pdf: url ]]` — pdf (external)

**Math**
- `$$expr$$` — equation (standard)
- `[[equation: expr ]]` — equation (alias)

**Layout**
- `[[columns]]` ... `[[column]]` ... `[[/columns]]` — 다단 레이아웃

**Synced Block**
- `[[synced]]{` ... `}]` — synced_block 원본 (original)
- `[[synced: block_id ]]` — synced_block 복사본 (copy, 기존 block_id 참조)

### API 제약
- image/video/audio/file/pdf: external URL만 (Notion-hosted는 UI 전용)
- `link_preview`: read-only. Notion이 URL 붙여넣기 시 자동 생성 — API로 쓰기 불가
- Max blocks per call: 100개
- Max nesting depth: 2단계
- column_list는 반드시 column 자식 ≥1개 포함
- table은 반드시 table_row 자식 ≥1개 포함

---

## 에러 대응

| 코드 | 원인 | 대응 |
|------|------|------|
| 401 | 토큰 무효 | NOTION_API_KEY 확인, gateway 재시작 |
| 403 | 권한 없음 | Notion UI → Share → integration 초대 |
| 404 | ID 오류/미공유 | ID 확인, 공유 상태 확인 |
| 429 | Rate limit | 대기 후 재시도, 루프 금지 |

---

## 작성 기준

- 밀도 우선: 최소 1줄 요약 + 본문 핵심 5~8문장
- Project: What / Status / Scope / Links / Why (허브, 상태 파악용)
- Case Study: Context / My Role / Key Decisions / Contributions / Learned / Next Step (서사)
- Project/Case Study: 1인칭 기본. Research/Notes: 중립 서술 허용.

## Notion API 버전 참고
- `archived` → `in_trash`로 대체 (2022-06-28 기준)
- plugin client.js: NOTION_VERSION = "2022-06-28" (2026-03-21 수정)
