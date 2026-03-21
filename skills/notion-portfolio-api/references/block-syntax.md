# Notion 블록 구문 레퍼런스 (Plugin v3, 실측 2026-03-15)

## 설계 원칙

- 표준 마크다운이 가능한 블록은 표준 구문을 기본값으로 사용
- Custom syntax `[[ ]]`는 Notion 전용 블록(callout, toggle, toc 등)에만 사용
- 읽기(Read) 시 항상 정규화된(canonical) 형태로 반환

## Standard Markdown → Notion Block

| 구문 | Notion 블록 | 비고 |
|------|------------|------|
| `# text` | heading_1 | |
| `## text` | heading_2 | |
| `### text` | heading_3 | |
| `- text` | bulleted_list_item | |
| `1. text` | numbered_list_item | |
| `- [ ] text` | to_do (unchecked) | |
| `- [x] text` | to_do (checked) | |
| `> text` | quote | callout이 필요하면 `[[ ]]` 사용 |
| `---` | divider | `***`는 불가 |
| `` ```lang ``` `` | code | 언어 태그 인식 |
| `![alt](url)` | image (external) | alt = caption |
| `$$expr$$` | equation (KaTeX) | 한 줄에 $$ 쌍 |
| `\| col \| col \|` | table + table_row | separator row 자동 감지 |

## Inline Annotations

| 구문 | 효과 |
|------|------|
| `**text**` | bold |
| `*text*` | italic |
| `~~text~~` | strikethrough |
| `` `text` `` | inline code |
| `[text](url)` | link |

## Custom Syntax → Notion Block

| 구문 | Notion 블록 | 비고 |
|------|------------|------|
| `[[ text ]]` | callout (💡, blue) | |
| `[[ 🔒 text ]]` | callout (emoji icon) | 첫 이모지 = 아이콘 |
| `[[! text ]]` | callout (⚠️, red) | 경고/에러용 |
| `[[> title ]]` | toggle (빈) | |
| `[[> title ]]{` ... `}]` | toggle + children | 재귀 파싱 |
| `[[@ page_id \| label ]]` | page mention | 블록 단독 및 인라인 모두 가능 |
| `[[@ page_id ]]` | page mention (자동 제목) | |
| `[[toc]]` | table_of_contents | |
| `[[breadcrumb]]` | breadcrumb | |
| `[[bookmark: url ]]` | bookmark | |
| `[[bookmark: url \| caption ]]` | bookmark + caption | |
| `[[embed: url ]]` | embed | YouTube 등 |
| `[[video: url ]]` | video (external) | |
| `[[audio: url ]]` | audio (external) | |
| `[[file: url ]]` | file (external) | |
| `[[file: url \| caption ]]` | file + caption | |
| `[[pdf: url ]]` | pdf (external) | |
| `[[equation: expr ]]` | equation | `$$expr$$` 별칭 |
| `[[image: url ]]` | image | `![](url)` 별칭 |
| `[[image: url \| caption ]]` | image + caption | |
| `[[link: page_id ]]` | link_to_page (page) | |
| `[[link: db_id \| database ]]` | link_to_page (database) | full-page DB만 가능 |
| `[[synced]]{` ... `}]` | synced_block (original) | 새 원본 생성 |
| `[[synced: block_id ]]` | synced_block (copy) | 기존 원본 참조 |
| `[[columns]]` ... `[[column]]` ... `[[/columns]]` | column_list + column | 다단 레이아웃 |

## 블록 사용 우선순위 (포트폴리오 작성 시)

1. **callout** — 상태, 요약, 강조
2. **toggle** — 펼쳐야 할 부가 정보
3. **heading** — 섹션 구분
4. **page mention** — Notion 내부 링크
5. **bullet / numbered list** — 열거, 단계
6. **to-do** — 체크리스트
7. **table** — 구조화된 비교
8. **quote** — 핵심 통찰
9. **divider** — 섹션 분리
10. **code** — 코드 예시
11. **bookmark** — 외부 링크 카드
12. **image / video / embed** — 미디어

## Notion API 제약

| 제약 | 설명 |
|------|------|
| image/video/audio/file/pdf | external URL만. Notion-hosted 파일은 UI에서만 업로드 |
| link_preview | 읽기 전용. URL 붙여넣기 시 Notion이 내부적으로 생성 |
| link_to_page (database) | full-page database만 가능. inline database 불가 |
| synced_block copy | 같은 워크스페이스의 원본 block_id 필요 |
| Max blocks per call | 100개. 초과 시 분할 필요 |
| Max nesting depth | 2단계 (block → child → grandchild까지) |
| template block | Notion이 deprecated. 비권장 |

## 사용 시 주의

- `> text`는 **quote**. callout이 필요하면 `[[ ]]` 사용
- toggle children은 `[[> title ]]{` ... `}]` 구문으로만 가능
- divider는 `---`만 사용 (`***` 불가)
- table separator row (`|---|---|`)는 자동 필터 → header 감지에 사용
- 읽기 시 image는 항상 `![caption](url)` 형태로 반환
- 읽기 시 equation은 항상 `$$expr$$` 형태로 반환
