# 통합 결과 템플릿

결과는 아래 한글 제목 구조의 마크다운으로 낸다. 사용자가 JSON을 요청하면 같은 키를 최상위 키로 쓴다. 맨 위에 한 줄로 `공식 Master PASS 아님 · 연구용`을 적는다.

| 출력 키 | 담는 절 |
|---|---|
| `fact_card` | 0. 사실카드 |
| `source_links` | 1. 입력 및 출처 |
| `mind_analysis` | 2. Mind |
| `stage1_status` | 2. Mind의 마지막 줄 |
| `source_conflicts` | 3. 출처 충돌과 HOLD |
| `writing_draft` | 4. Writing |
| `stage2_status` | 4. Writing의 마지막 줄 |
| `claim_evidence_matrix` | 5. 주장-증거 매트릭스 |
| `layout_plan` | 6. 지면 배치안 |
| `stage3_status` | 6. 지면 배치안의 마지막 줄 |
| `validation_scope` | 7. 검증 기록 |
| `risks` | 8. 잔여 리스크 |
| `next_experiment` | 9. 다음 실험 |

## 0. 사실카드 (`fact_card`)
봉인한 카드 JSON 전체와 `card_version`. 잠정 카드면 "잠정(미검증)"이라고 적고, 사용자가 확인해 줄 항목을 목록으로 붙인다. 사용자가 거절한 주장(예: 인과 서술 요청)이 있으면 여기서 먼저 알린다.

## 1. 입력 및 출처 (`source_links`)
기관 / 실적연도 / 보고서 / 페이지 / 원본 URL / 작성일 / 대상 지표와 아티팩트

## 2. Mind (`mind_analysis`, `stage1_status`)
- 핵심 평가주장 및 평가요건
- 정책활동 → 관측산출 → 관측성과의 연결 (검증된 인과만 표시)
- 지표 정의·정규화 키·분모·중복 출처
- 대안 설명, 외생요인, 미확보 근거
- 1단계 판정: PASS(연구용, 공식 아님) / CONDITIONAL / FAIL / 미실행 + 사유 한 줄

## 3. 출처 충돌과 HOLD (`source_conflicts`)
항목 | HOLD 사유코드 | 충돌 내용 | 해소에 필요한 확인

## 4. Writing (`writing_draft`, `stage2_status`)
- 평가보고서 문안 (문장별 출처 주석)
- 유보 문구
- 2단계 판정 + 사유 한 줄

## 5. 주장-증거 매트릭스 (`claim_evidence_matrix`)
`writing-rules.md`의 대조표(C) 필드 그대로. Mind 판정과 대조 판정을 각각 적는다.

## 6. 지면 배치안 (`layout_plan`, `stage3_status`)
- 읽은 아티팩트와 파일(읽지 못했으면 그 사실과 "3단계 미실행")
- 단락 | 레이아웃 Lxx | 고른 이유 | 쪽 비중 | 보충 여부
- 단락별 칸 표: 영역 번호 | 블록 | 지면 문구 | 글자 수/용량 | claim_id | FIT·OVER·BLOCKED
- `layout_plan` JSON(`layout-handoff.md` 5절 형식)
- 16:9 장표면 Source Slide Mapping 표
- 3단계 판정 + 사유 한 줄

## 7. 검증 기록 (`validation_scope`)
- A 봉인(`card_version`), B 작성, C 대조, D 금지패턴 점검 결과
- 구조 검사: `validate_metrics.py`와 `check_layout_plan.py`의 출력 요약(각각 errors/holds/warnings 건수)
- 자연어 의미검토 결과(스크립트 통과와 별개)
- 작업 정의를 쓴 점검 항목(`glossary.md`)은 "작업 정의 기준"으로 표시
- 독립 반복검증(G4): 수행 기록 또는 "미실행"
- 지면 형태 검수(아티팩트 `quality-gate.md`): 이 스킬은 렌더링하지 않으므로 "미실행"
- 공식 Master PASS 아님

## 8. 잔여 리스크 (`risks`)

## 9. 다음 실험 (`next_experiment`)
