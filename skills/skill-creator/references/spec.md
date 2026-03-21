# Skill Creator — Anthropic Spec 요약

출처: Anthropic skill-creator (github.com/anthropics/skills)

## Progressive Disclosure 3단계

1. **Metadata** (name + description) — 항상 컨텍스트에 있음 (~100 words)
2. **SKILL.md body** — 스킬 트리거 시 로드 (<5k words)
3. **Bundled resources** — 필요할 때만 로드 (용량 무제한)

## 자유도 설정

| 자유도 | 사용 시점 | 형태 |
|---|---|---|
| 높음 | 여러 접근법이 유효할 때 | 텍스트 지시 |
| 중간 | 선호 패턴은 있지만 변형 허용 | 슈도코드/파라미터화 스크립트 |
| 낮음 | 순서가 중요하고 오류 가능성 높을 때 | 구체적 스크립트 |

## References 파일 설계

- 100줄 초과 시 파일 상단에 목차 포함
- SKILL.md에서 "언제 읽을지" 명시 후 링크
- 중복 금지: 내용은 SKILL.md 또는 references 중 한 곳에만
- 도메인별 분리: `references/finance.md`, `references/sales.md` 등

## Description 작성 기준

좋은 예:
```
"Intel Pipeline 보고서(KR/US Pre-Open)를 X 단일 포스트로 변환. 
저작권 안전 처리, 팩트 라인 형식, 출처 표기 규칙 포함. 
트리거: Intel 보고서를 X에 올려줘, intel 보고서 X 포스트 작성 요청 시."
```

나쁜 예:
```
"X post writer skill"  # 너무 짧음, 트리거 없음
```

## 네이밍 규칙
- 소문자 + 하이픈만 (`skill-creator`, `gh-issues`)
- 64자 이하
- 동사 주도 선호 (`pdf-rotate` > `pdf-rotator`)
- 도구 네임스페이스 활용 (`gh-address-comments`)
