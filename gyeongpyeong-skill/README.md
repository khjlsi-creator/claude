# 경평스킬 설치 패키지 (v1.4)

ZIP 최상단의 `SKILL.md`를 인식하는 스킬 설치 화면에 ZIP을 업로드한다. 설치 화면에서 ZIP 업로드를 지원하지 않는 경우 압축을 해제해 스킬 디렉터리로 추가한다. 플랫폼별 설치 방식은 다를 수 있다.

포함 범위는 1단계 Mind, 2단계 Writing, 3단계 Layout(아티팩트 지면 배치안)이다. 지면 렌더링은 하지 않는다. KORAD 경영평가·친환경탄소중립 지표·시설개방 지표·KORAD(16:9) 디자인 시스템 아티팩트와 함께 쓴다(`references/artifact-map.md`). 연구용 통합본이며 공식 Master PASS 인증본이 아니다. 예약·반복 실행을 만들지 않는다. Google Drive 선별 근거를 참고해 새로 작성했으며 전체 원본 데이터 백업은 아니다.

## 점검
```
python3 -m unittest discover -s tests
python3 scripts/validate_metrics.py assets/sample-fact-card.json
python3 scripts/check_layout_plan.py assets/sample-layout-plan.json assets/sample-fact-card.json
```

## v1.4 변경
- 3단계 Layout 추가: 아티팩트 레이아웃 선택, 지면 어법, 칸 용량, `layout_plan` 형식, 게이트 G5
- 스킬과 아티팩트가 부딪히는 10곳의 조정 규칙(추진성과 띠에는 관측 수치만, 견본 글 금지 등)
- `check_layout_plan.py` 추가: 용량 초과, 서술형 종결, 성과 띠의 인과 표현·HOLD 주장, 카드에 없는 수치 검출
- 사실카드: 모르는 식별키는 `null` + HOLD, `label_as_printed`·`hold`·`activities` 추가, 같은 값쌍·다른 지표명 자동 검출
- 단계 판정을 단계별 표로 분리, 대조 판정에 AUTHOR·EXCLUDED 추가

## v1.3 변경
- 판정 체계를 항목(HOLD) / 주장 / 문장 대조 / 단계 네 층으로 분리하고 단계 환산 규칙을 명시
- 단계 PASS는 "연구용, 공식 아님"으로 표기. G4(독립 반복검증)는 단계 판정 요건에서 분리
- 상위 체계의 "Quality Gate 3"과 이 패키지의 G3이 다른 절차임을 명시
- 사실카드 없이 원문만 받은 경우의 처리(잠정 사실카드, 상한 CONDITIONAL) 추가
- 용어집, JSON 사실카드 형식, 예시 입력, 출력 키 ↔ 템플릿 대응 추가
- 금지패턴 점검(D) 절차를 구체화하고 '해석 한계' 금지 문구의 뜻을 바로잡음
- 한전KPS 사례의 출처 집계를 충돌 기록과 맞춤(7건 → 9건, 패키지 내 재집계)
- `validate_metrics.py`: null 식별키 미검출 수정, 정상 중복 인용·원값 0·미확보를 오류와 분리, 종료코드 추가, 테스트 추가
