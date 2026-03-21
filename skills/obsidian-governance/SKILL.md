---
name: obsidian-governance
description: >
  Obsidian vault 내부 운영 규칙. 폴더 배치, 노트 타입, 프론트매터, 작성 가이드.
  시스템 간 관계와 발행 흐름은 knowledge-ops 스킬을 참조.
  트리거: vault 내 파일 배치, 노트 타입 결정, 프론트매터 작성 시.
---

# Obsidian Governance

Vault root: `{obsidian_vault}`

## 역할

이 스킬은 Obsidian vault 내부의 운영 규칙만 다룬다.
Obsidian과 Notion 사이의 관계, 발행 흐름, 작성 루트는
**knowledge-ops 스킬**에 정의되어 있다.

## 폴더 구조 (PARA)

- **Projects/** — 마감 또는 산출물이 있는 활성 작업
- **Areas/** — 종료 없이 지속되는 관심 영역
- **Resources/** — 재사용 가능한 참고 자료
  - `Resources/Research/` — 리서치 파이프라인 산출물
    - `Markets/` — 시장·거시경제 리서치 (finance-researcher)
    - `Product/` — 제품·시장 분석 (dev-research 등)
    - `Notes/` — 리서치 메모·인사이트
  - `Resources/Finance/` — 금융 학습·참고 자료
    - `Lectures/` — 강의 노트
    - `Notes/` — 금융 메모
    - `Prompts/` — 분석 프롬프트
  - `Resources/Daily digests/` — 일일 브리핑 (Intel Pipeline)
    - `AI/`, `Finance/KR/`, `Finance/US/`, `Schedule/`
- **Archive/** — 비활성/완료된 것
- **_Atlas/** — 내비게이션 허브. Home.md = 메인 진입점
- **_System/** — 운영 문서, 거버넌스, 로그, 템플릿
- **_Trash/** — 소프트 삭제

**배치 판단:** 마감+산출물 → Projects/ · 지속 영역 → Areas/ · 재사용 참고 → Resources/ · 내비 → _Atlas/ · 운영 → _System/

## 폴더 생성 원칙

**{user}는 "폴더가 컨테이너, 파일은 끝단에만" 구조를 선호한다.**

- 같은 폴더 안에 파일이 **2개 이상** 생기면 적절한 서브폴더로 묶는다
- 폴더와 파일이 같은 레벨에 공존하는 것을 최소화한다
- 폴더 생성 기준이 애매할 때는 **적극적으로 만드는 쪽**을 선택한다
- 인덱스용 파일(폴더와 같은 이름의 .md)은 허용 — 탐색 편의를 위해 openclaw가 생성할 수 있음

## 노트 타입

- project-note — 활성 이니셔티브
- concept-note — 영역 지식
- research-note — 분석, 독서 요약
- resource-note — 재사용 참고/프레임워크/프롬프트
- operational-note — 거버넌스, 로그, 워크플로우
- fragment — 미완성 초안
- archive-candidate — 활동 낮음, 리뷰 대기

불확실하면 → fragment 또는 archive-candidate 선호.

## 프론트매터

필요한 것만 사용. 핵심 필드:

```yaml
title:
type:                # 위 노트 타입
status:              # active | draft | reference | archived | fragment
area:                # 관련 Area
project:             # 관련 Project
last_updated:
related:             # [[링크 노트]]
```

권장 필드 (Notion 연동 추적용):

```yaml
publish_candidate: false   # true = Notion 발행 후보
notion_status: none        # none | published | outdated
notion_page_id:            # 발행된 Notion 페이지 ID
```

## 서술 원칙

- 프로젝트, 경험, 회고 노트: 1인칭 기본 ("나는 ~했다")
- 개념, 리서치, 레퍼런스, 강의 요약: 중립 서술 허용

## 핵심 규칙

1. **만들기 전에 확인** — 기존 노트를 보강하거나 링크. 중복 생성 금지
2. **삭제 전에 아카이브** — 명시적 삭제 요청 없으면 _Trash/ 사용
3. **구조 먼저, 다듬기 나중** — 배치 → 역할 → 헤딩 → 프론트매터 → 링크 → 산문
4. **작은 단위로** — 기본적으로 한 프로젝트/영역/클러스터씩 작업. {user}가 명시적으로 전체 재구조화를 요청하면 전체 볼트 작업 가능
5. **의미 보존** — 재작성 시 내용을 임의로 재해석하지 않음

## 작성 가이드

- 실질적인 노트는 2~5줄 요약으로 시작
- fragment 이상의 노트에는 헤딩 사용
- 개념이 독립적으로 재사용될 때만 노트 분리

## 참고 문서

- 마이그레이션 작업 → references/migration.md
- 상세 작성 가이드 → references/writing.md
