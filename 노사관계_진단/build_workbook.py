"""노사관계 진단·평가 구글시트(xlsx) 생성기.

노사발전재단 「일터혁신 실태조사」 2023·2024·2025 최종보고서의 일터혁신지수
노사관계 영역(100점)을 역산한 결과를 바탕으로, 설문 입력 → 문항 점수화 →
가중 합산 → 벤치마크 비교 → 등급·개선과제까지 수식만으로 자동 계산되는
통합문서를 만든다. 매크로·스크립트 없이 Excel/Google Sheets 공통 함수만 쓴다.

실행: python3 build_workbook.py  →  노사관계_진단평가_구글시트.xlsx
"""
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.utils import get_column_letter as CL
from openpyxl.worksheet.datavalidation import DataValidation

OUT = "노사관계_진단평가_구글시트.xlsx"
NRESP = 50                      # 응답자 열 수 (E열부터)
C0 = 5                          # 첫 응답자 열(E)
CLAST = CL(C0 + NRESP - 1)      # 마지막 응답자 열

# ---------------------------------------------------------------- 스타일
BRAND = "0B5FA5"
F_TITLE = Font(size=16, bold=True, color=BRAND)
F_H = Font(bold=True, color="FFFFFF")
F_B = Font(bold=True)
F_NOTE = Font(size=9, color="5B6878")
FILL_H = PatternFill("solid", fgColor=BRAND)
FILL_SEC = PatternFill("solid", fgColor="DCE8F5")
FILL_IN = PatternFill("solid", fgColor="FFF8DC")
FILL_OUT = PatternFill("solid", fgColor="EAF5EE")
FILL_GRAY = PatternFill("solid", fgColor="F1F3F6")
THIN = Side(style="thin", color="C9D1DB")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="center")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)


def hdr(ws, row, values, col=1):
    for i, v in enumerate(values):
        c = ws.cell(row=row, column=col + i, value=v)
        c.font, c.fill, c.alignment, c.border = F_H, FILL_H, CENTER, BOX


def put(ws, ref, value, font=None, fill=None, align=None, fmt=None, border=True):
    c = ws[ref]
    c.value = value
    if font: c.font = font
    if fill: c.fill = fill
    if align: c.alignment = align
    if fmt: c.number_format = fmt
    if border: c.border = BOX
    return c


def widths(ws, spec):
    for col, w in spec.items():
        ws.column_dimensions[col].width = w


# ---------------------------------------------------------------- 문항 정의
# 파트(소분류) : 공식 배점(2023~2025 동일, 2024 표 Ⅵ-3·Ⅵ-4 / 2025 표 Ⅵ-5)
PARTS = [
    ("P1", "노사관계 전반 인식", "노사관계분위기", 10),
    ("P2", "노조·근로자대표의 혁신 태도", "노사관계분위기", 10),
    ("P3", "노사협력 프로그램", "노사협력 및 갈등", 13),
    ("P4", "노사갈등(미발생)", "노사협력 및 갈등", 12),
    ("P5", "정보공유·의사소통", "정보공유와 의사소통", 25),
    ("P6", "고충처리", "고충처리", 15),
    ("P7", "노사협의회 활용성", "노사협의회", 15),
]
PART = {p[0]: p for p in PARTS}
MID = ["노사관계분위기", "노사협력 및 갈등", "정보공유와 의사소통", "고충처리", "노사협의회"]

Q16 = ["노사의 이해관계가 크게 다르지 않아 협조가 잘 이루어진다",
       "노사가 서로 상대방의 일에 대해 반대하지 않는다",
       "노사 모두가 회사를 더욱 일하기 좋은 곳으로 만들려고 노력한다",
       "그간 노사관계가 협력적이었다"]
Q17 = ["노사협력선언·노사공동결의대회", "노사공동기구·위원회를 통한 문제해결", "노사공동교육·워크숍",
       "직원단합대회(체육대회, 등반대회, 야유회 등)", "노사공동 사회봉사(일사일촌 등)"]
Q18 = ["파업(부분파업 포함) 발생", "노사문제로 인한 경제적 손실 발생",
       "노사문제로 인한 고소·고발 발생", "노사문제로 인한 해고자 발생"]
Q19 = ["근로자의 고충을 전달할 공식적인 통로를 충분히 제공하고 있다",
       "고충 제기 후 처리과정에서 노사 간 의사소통이 수시로 이루어진다",
       "근로자의 고충을 효과적으로 처리한다",
       "고충처리에 대해 근로자들은 만족하고 있다"]
Q21 = ["노사 간에는 공식·비공식의 의사소통 통로가 다양하게 존재한다",
       "경영진과 근로자와의 정기적인 간담회가 잘 이루어진다",
       "필요시 노사대표 간 핫라인이 잘 작동된다",
       "근로자들의 일상적인 문제들이 노사 간 의사소통을 통해서 잘 해결되고 있다",
       "개별 직원들이 최고책임자나 경영진에게 자신의 의견을 말할 수 있는 기회가 많다"]
Q22 = ["근로자들은 회사의 비전과 목표가 무엇인지 알고 있다",
       "근로자들은 회사의 각종 경영현황을 이해하고 있다",
       "회사는 각종 경영정보를 근로자와 공유하고 있다",
       "근로자는 회사가 제공하는 경영정보를 신뢰한다"]
Q23 = ["경영 계획과 실적에 대한 정보공유 창구로 활용된다",
       "인사노무제도 개선을 위한 논의 창구로 활용된다",
       "안전보건 및 작업환경 개선을 위한 논의 창구로 활용된다",
       "근로자 복지개선을 위한 협의 창구로 활용된다",
       "작업장 내 생산성 향상을 위한 논의 창구로 활용된다"]
Q24 = ["일터혁신과 관련된 인적자원개발(교육훈련 등) 활동을 지지한다",
       "일터혁신과 관련하여 고용안정을 위해 노력한다",
       "일터혁신과 관련된 작업장에서의 직원 참여활동을 지지한다",
       "일터혁신과 관련된 인적자원관리(보상, 평가 등) 활동을 지지한다",
       "일터혁신 전반에 대해 지지한다"]

# 점수 문항 36개(파트 순서로 정렬 — 파트별로 연속된 행이 되도록)
ITEMS = []
for i, t in enumerate(Q16, 1): ITEMS.append((f"Q16_{i}", "P1", t, "L"))
for i, t in enumerate(Q24, 1): ITEMS.append((f"Q24_{i}", "P2", t, "L"))
for i, t in enumerate(Q17, 1): ITEMS.append((f"Q17_{i}", "P3", t, "P"))
for i, t in enumerate(Q18, 1): ITEMS.append((f"Q18_{i}", "P4", t, "C"))
for i, t in enumerate(Q21, 1): ITEMS.append((f"Q21_{i}", "P5", t, "L"))
for i, t in enumerate(Q22, 1): ITEMS.append((f"Q22_{i}", "P5", t, "L"))
for i, t in enumerate(Q19, 1): ITEMS.append((f"Q19_{i}", "P6", t, "L"))
for i, t in enumerate(Q23, 1): ITEMS.append((f"Q23_{i}", "P7", t, "L"))
NPART = {p: sum(1 for it in ITEMS if it[1] == p) for p in PART}

# 설문지 순서(부록 설문지 문16→문24)
SURVEY = [("SEC", "문16. 노사관계 전반 — 우리 회사는 …", None)]
SURVEY += [("L", f"Q16_{i}", t) for i, t in enumerate(Q16, 1)]
SURVEY += [("SEC", "문17. 노사협력 프로그램·행사(최근 3년) — 시행여부, 시행했다면 활성화 정도(1 전혀 활용되지 않음 ~ 5 잘 활용됨)", None)]
for i, t in enumerate(Q17, 1):
    SURVEY += [("RUN", f"Q17_{i}", f"{t} — 시행여부"), ("ACT", f"Q17_{i}A", f"{t} — 활성화 정도(시행한 경우만)")]
SURVEY += [("SEC", "문18. 노사 간 갈등(최근 3년) — 발생 여부", None)]
SURVEY += [("CONF", f"Q18_{i}", t) for i, t in enumerate(Q18, 1)]
SURVEY += [("SEC", "문19. 근로자 고충처리 — 우리 회사는 …", None)]
SURVEY += [("L", f"Q19_{i}", t) for i, t in enumerate(Q19, 1)]
SURVEY += [("SEC", "문20. (참고·점수 미반영) 지난해 제기된 고충의 해결 정도", None)]
SURVEY += [("REF", "Q20", "1=30%미만 2=30~50% 3=50~70% 4=70~90% 5=90%이상")]
SURVEY += [("SEC", "문21. 근로자(대표)와의 의사소통 — 우리 회사는 …", None)]
SURVEY += [("L", f"Q21_{i}", t) for i, t in enumerate(Q21, 1)]
SURVEY += [("SEC", "문22. 경영정보 공유 — 근로자(또는 회사)는 …", None)]
SURVEY += [("L", f"Q22_{i}", t) for i, t in enumerate(Q22, 1)]
SURVEY += [("SEC", "문23. 노사협의회(또는 노사공동위원회) 운영 — 우리 노사협의회는 … (미설치면 비워두세요)", None)]
SURVEY += [("L", f"Q23_{i}", t) for i, t in enumerate(Q23, 1)]
SURVEY += [("SEC", "문24. 일터혁신에 대한 노동조합(없으면 노사협의회 근로자대표)의 태도와 역할 — 우리 노조(근로자대표)는 …", None)]
SURVEY += [("L", f"Q24_{i}", t) for i, t in enumerate(Q24, 1)]

RESP_HELP = {"L": "1~5 (1 전혀 그렇지 않다 · 3 보통 · 5 매우 그렇다)", "RUN": "시행 / 미시행",
             "ACT": "1~5 (시행한 경우만)", "CONF": "발생 / 미발생", "REF": "1~5"}

# ---------------------------------------------------------------- 공식 벤치마크
# 파트별 표준화값(0~1) : 2023 표 Ⅴ-8, 2024 표 Ⅵ-8, 2025 표 Ⅵ-9
STD = {
    ("2023", "수혜"): [7.356/10, 7.334/10, 4.9634/13, 11.7432/12, 18.335/25, 10.6845/15, 10.3725/15],
    ("2023", "일반"): [7.010/10, 6.705/10, 4.5695/13, 11.724/12, 16.7375/25, 10.3575/15, 9.909/15],
    ("2024", "수혜"): [.7455, .7434, .3813, .6619, .6930, .7072, .6903],
    ("2024", "일반"): [.7210, .6862, .3011, .5087, .6721, .6973, .6670],
    ("2025", "수혜"): [.6779, .6887, .3836, .9790, .6302, .6788, .6280],
    ("2025", "일반"): [.6340, .5918, .2845, .9808, .5866, .6084, .5724],
}
# 2024(보정): 갈등(P4)만 공표 발생률로 다시 계산(1-평균발생률). 나머지는 2024 공식값
STD[("2024(보정)", "수혜")] = STD[("2024", "수혜")][:3] + [1 - (1.3+1.6+3.3+2.2)/400] + STD[("2024", "수혜")][4:]
STD[("2024(보정)", "일반")] = STD[("2024", "일반")][:3] + [1 - (2.3+3.2+3.2+1.5)/400] + STD[("2024", "일반")][4:]
STD_NOTE = {
    ("2024", "수혜"): "갈등 0.6619는 공표 발생률(평균 2.1%)과 맞지 않는 이상치",
    ("2024", "일반"): "갈등 0.5087은 공표 발생률(평균 2.6%)과 맞지 않는 이상치",
    ("2025", "수혜"): "표 Ⅵ-9 수혜 세부값 5개가 2024값과 동일하게 기재(표준화값은 신규)",
    ("2024(보정)", "수혜"): "갈등만 1-평균발생률로 대체",
    ("2024(보정)", "일반"): "갈등만 1-평균발생률로 대체",
}
# 노사관계 영역 공표 총점(0~100): 전체·규모·업종·노조유무
TOT = {
    "2023": {"수혜": {"전체": 70.79, "50인 미만": 69.58, "50~100인 미만": 68.71, "100~300인 미만": 70.79, "300인 이상": 72.46,
                     "제조업": 69.15, "일반서비스": 70.12, "공공행정서비스": 74.19, "금융서비스": 71.19, "기타서비스": 68.53,
                     "노조 있음": 71.79, "노조 없음": 69.57},
             "일반": {"전체": 67.01, "50인 미만": 66.51, "50~100인 미만": 67.10, "100~300인 미만": 66.75, "300인 이상": 69.84,
                     "제조업": 65.68, "일반서비스": 68.42, "공공행정서비스": 73.18, "금융서비스": 66.07, "기타서비스": 69.23,
                     "노조 있음": 70.29, "노조 없음": 66.25}},
    "2024": {"수혜": {"전체": 66.08, "50인 미만": 64.26, "50~100인 미만": 67.17, "100~300인 미만": 65.91, "300인 이상": 72.65,
                     "제조업": 66.04, "일반서비스": 65.21, "공공행정서비스": 70.73, "금융서비스": 65.89, "기타서비스": 55.51,
                     "노조 있음": 70.72, "노조 없음": 65.48},
             "일반": {"전체": 61.36, "50인 미만": 58.48, "50~100인 미만": 61.02, "100~300인 미만": 64.44, "300인 이상": 68.79,
                     "제조업": 60.60, "일반서비스": 61.26, "공공행정서비스": 65.84, "금융서비스": 60.19, "기타서비스": 69.51,
                     "노조 있음": 63.33, "노조 없음": 60.95}},
    "2025": {"수혜": {"전체": 65.16, "50인 미만": 64.27, "50~100인 미만": 66.60, "100~300인 미만": 64.84, "300인 이상": 65.75,
                     "제조업": 65.12, "일반서비스": 63.92, "공공행정서비스": 69.12, "금융서비스": 72.70, "기타서비스": 68.48,
                     "노조 있음": 64.53, "노조 없음": 65.20},
             "일반": {"전체": 60.10, "50인 미만": 58.02, "50~100인 미만": 59.76, "100~300인 미만": 62.52, "300인 이상": 73.01,
                     "제조업": 59.06, "일반서비스": 60.26, "공공행정서비스": 65.40, "금융서비스": 69.76, "기타서비스": 68.86,
                     "노조 있음": 65.95, "노조 없음": 59.21}},
}
# 2024(보정): 갈등 블록 차이만큼 가산(하위집단은 집단 전체 보정폭을 동일 적용한 근사)
ADJ = {g: round(12 * (STD[("2024(보정)", g)][3] - STD[("2024", g)][3]), 4) for g in ("수혜", "일반")}
TOT["2024(보정)"] = {g: {k: round(v + ADJ[g], 2) for k, v in TOT["2024"][g].items()} for g in ("수혜", "일반")}

# 문항별 공표 평균(1~5). 2024는 전 문항, 2023·2025는 문16만 원문 확보
IM = {
    ("2024", "수혜"): {"Q16": [3.57, 3.58, 3.93, 3.83], "Q24": [3.70, 3.79, 3.72, 3.65, 3.73],
                      "Q21": [3.64, 3.41, 3.46, 3.57, 3.37], "Q22": [3.55, 3.31, 3.43, 3.44],
                      "Q19": [3.62, 3.60, 3.56, 3.36], "Q23": [3.27, 3.40, 3.57, 3.65, 3.35]},
    ("2024", "일반"): {"Q16": [3.49, 3.48, 3.76, 3.69], "Q24": [3.39, 3.53, 3.45, 3.38, 3.40],
                      "Q21": [3.48, 3.27, 3.34, 3.45, 3.24], "Q22": [3.48, 3.26, 3.31, 3.41],
                      "Q19": [3.55, 3.54, 3.48, 3.38], "Q23": [3.18, 3.24, 3.46, 3.49, 3.30]},
    ("2023", "수혜"): {"Q16": [3.54, 3.56, 3.84, 3.77]}, ("2023", "일반"): {"Q16": [3.39, 3.40, 3.65, 3.58]},
    ("2025", "수혜"): {"Q16": [3.56, 3.61, 3.88, 3.80]}, ("2025", "일반"): {"Q16": [3.42, 3.46, 3.64, 3.62]},
}
# 문17 시행률·활성화 평균, 문18 발생률(%)
Q17RATE = {("2023", "수혜"): ([.154, .485, .39, .592, .136], [3.52, 3.51, 3.53, 3.71, 3.59]),
           ("2023", "일반"): ([.158, .396, .311, .531, .109], [3.27, 3.5, 3.5, 3.6, 3.55]),
           ("2024", "수혜"): ([.173, .589, .456, .698, .145], [3.38, 3.57, 3.68, 3.72, 3.89]),
           ("2024", "일반"): ([.147, .47, .329, .588, .102], [3.22, 3.39, 3.43, 3.65, 3.65]),
           ("2025", "수혜"): ([.148, .506, .428, .643, .126], [3.29, 3.49, 3.69, 3.74, 3.57]),
           ("2025", "일반"): ([.088, .371, .294, .568, .102], [3.13, 3.43, 3.57, 3.61, 3.65])}
Q18RATE = {("2023", "수혜"): [2.0, 3.3, 4.0, 1.5], ("2023", "일반"): [2.3, 2.9, 4.7, 1.6],
           ("2024", "수혜"): [1.3, 1.6, 3.3, 2.2], ("2024", "일반"): [2.3, 3.2, 3.2, 1.5],
           ("2025", "수혜"): [0.2, 2.0, 3.1, 0.9], ("2025", "일반"): [0.9, 1.9, 1.9, 1.1]}

ADVICE = {
    "P1": "노사 신뢰의 기본기. 정기 노사간담회와 현안 사전공유 규칙(‘반대 전에 먼저 협의’)을 운영하세요.",
    "P2": "노조·근로자대표가 교육·고용안정·참여·평가보상 혁신에 함께하도록 사전설명회와 노사공동 TF를 꾸리세요.",
    "P3": "시행하지 않는 협력 프로그램(공동교육·공동결의 등)부터 연 1회 도입하고, 시행 중인 것은 실질 의제를 넣어 활성화하세요.",
    "P4": "갈등 발생 항목이 있습니다. 쟁점·이력 분석과 재발방지 협의체(분쟁 조기경보)를 가동하세요.",
    "P5": "분기 경영설명회·사내 게시로 경영정보를 정기 공유하고, 경영진 현장간담회와 노사대표 핫라인을 정비하세요.",
    "P6": "공식 고충창구(고충처리위원·온라인)를 알리고 처리기한·결과 피드백 규칙을 만들어 만족도를 높이세요.",
    "P7": "노사협의회 안건을 경영실적·인사노무·안전보건·복지·생산성 5개 축으로 고르게 상정하고 회의결과를 전 직원에 공개하세요.",
}

OPT_IND = ["제조업", "일반서비스", "공공행정서비스", "금융서비스", "기타서비스"]
OPT_SIZE = ["50인 미만", "50~100인 미만", "100~300인 미만", "300인 이상"]

wb = Workbook()

# ================================================================ 1. 안내
ws = wb.active
ws.title = "안내"
widths(ws, {"A": 3, "B": 110})
lines = [
    ("노사관계 진단·평가 도구 (구글시트용)", F_TITLE),
    ("근거: 노사발전재단 「일터혁신 실태조사」 2023·2024·2025 최종보고서 — 일터혁신지수 ‘노사관계’ 영역(100점)", F_NOTE),
    ("", None),
    ("■ 이 파일은 무엇인가요?", F_B),
    ("설문에 답하면 노사발전재단이 매년 발표하는 일터혁신지수 ‘노사관계’ 점수(100점 만점)와 같은 방식으로 자동 채점하고,", None),
    ("같은 해·같은 조건(규모·업종·노조유무) 사업장 평균과 비교해 등급과 우선 개선과제를 보여줍니다. 매크로 없이 수식만으로 동작합니다.", None),
    ("쉽게 말하면 — 5과목(분위기·협력/갈등·정보공유·고충처리·노사협의회) 성적표를 만들고 ‘전국 평균 대비 몇 점 위/아래인지’ 알려주는 도구입니다.", Font(color=BRAND, bold=True)),
    ("", None),
    ("■ 사용 순서", F_B),
    ("① [설문] 시트 위쪽 노란 칸에 기관 기본정보(업종·규모·노조·노사협의회·컨설팅 수혜)를 고릅니다.", None),
    ("② [설문] 시트에서 응답자 1명이 한 열(E열=응답자1, F열=응답자2 …, 최대 50명)을 맡아 드롭다운으로 답합니다.", None),
    ("    · 14행 ‘응답자 유형’을 꼭 고르세요(사업주·담당자 / 근로자). 유형을 고르지 않은 열은 집계에서 빠집니다.", None),
    ("    · 여러 사람이 동시에 답하려면 구글시트 공유(편집자)로 링크를 보내 각자 자기 열에 입력하면 됩니다.", None),
    ("③ [결과] 시트에서 응답자 유형·비교연도·비교집단을 고르면 종합점수·등급·벤치마크 비교·우선 개선과제·문항별 강약점이 자동 계산됩니다.", None),
    ("④ (선택) [가중치] 시트에서 문항별 배점을 바꿔 ‘우리 기관 중요도’ 시나리오를 볼 수 있습니다. 벤치마크 비교는 기본 배점일 때만 정확합니다.", None),
    ("", None),
    ("■ 시트 구성", F_B),
    ("안내 · 설문(입력) · 결과(자동) · 가중치(문항별 배점) · 벤치마크(공식 비교값) · 역산검증(공식 산식 재현 근거) · 모형설계(평가모형 설명서) · 점수_응답자(계산용, 수정 금지)", None),
    ("", None),
    ("■ 꼭 알아두세요", F_B),
    ("· 사업주·담당자 응답(재단 실태조사와 같은 응답주체)과 근로자 응답은 서로 다른 시각이므로 합산하지 않고 따로 봅니다. 벤치마크는 사업주·담당자 기준입니다.", None),
    ("· 재단은 2025년에 계산식을 바꿨습니다(5점 응답을 0~1로 바꾸는 방식 ÷5 → (−1)÷4). 그래서 2025 비교는 2025식, 2023·2024 비교는 2023·24식으로 자동 계산합니다.", None),
    ("· 노란 칸만 입력하세요. 초록·회색 칸은 수식입니다. [점수_응답자] 시트는 지우거나 고치지 마세요.", None),
    ("· 등급(S~D)은 재단 공식 등급이 아니라 이 도구가 정한 ‘벤치마크 대비 차이’ 기준입니다. 자세한 근거는 [모형설계]·[역산검증] 시트에 있습니다.", None),
]
for i, (t, f) in enumerate(lines, 1):
    c = ws.cell(row=i, column=2, value=t)
    c.alignment = Alignment(wrap_text=True, vertical="center")
    if f: c.font = f

# ================================================================ 2. 설문
sv = wb.create_sheet("설문")
widths(sv, {"A": 9, "B": 16, "C": 58, "D": 22})
for j in range(NRESP):
    sv.column_dimensions[CL(C0 + j)].width = 9
put(sv, "A1", "노사관계 진단 설문", F_TITLE, border=False)
put(sv, "A2", "노란 칸만 입력 · 응답자 1명 = 1열(E열부터 최대 50명) · 드롭다운으로 선택", F_NOTE, border=False)
info = [("기관/사업장명", "", None, "자유 입력"),
        ("업종", "공공행정서비스", OPT_IND, "재단 실태조사 업종 분류"),
        ("규모(상시근로자)", "300인 이상", OPT_SIZE, "벤치마크 규모 구간"),
        ("노동조합", "있음", ["있음", "없음"], ""),
        ("노사협의회", "설치", ["설치", "미설치"], "미설치·50인 미만·무노조면 노사협의회 영역 제외 후 100점 환산"),
        ("일터혁신 컨설팅(최근 3년)", "받지 않음(일반)", ["받음(수혜)", "받지 않음(일반)"], "벤치마크 비교집단 자동 선택에 사용")]
INFO_ROW = {}
for k, (lab, default, opts, help_) in enumerate(info):
    r = 4 + k
    INFO_ROW[lab] = r
    put(sv, f"B{r}", lab, F_B, FILL_GRAY)
    put(sv, f"C{r}", default, fill=FILL_IN)
    put(sv, f"D{r}", help_, F_NOTE, align=WRAP)
    if opts:
        dv = DataValidation(type="list", formula1='"' + ",".join(opts) + '"', allow_blank=True)
        sv.add_data_validation(dv); dv.add(f"C{r}")
R_IND, R_SIZE, R_UNION, R_COUNCIL, R_GRP = (INFO_ROW[x] for x in ["업종", "규모(상시근로자)", "노동조합", "노사협의회", "일터혁신 컨설팅(최근 3년)"])

HR = 12                         # 표 머리글 행
hdr(sv, HR, ["문항ID", "구분", "문항", "응답 방법"] + [f"응답자{j+1}" for j in range(NRESP)])
R_TYPE, R_MEMO = HR + 1, HR + 2
put(sv, f"A{R_TYPE}", "TYPE", F_B, FILL_GRAY); put(sv, f"C{R_TYPE}", "응답자 유형 (반드시 선택)", F_B, FILL_GRAY)
put(sv, f"D{R_TYPE}", "사업주·담당자 / 근로자", F_NOTE)
put(sv, f"A{R_MEMO}", "MEMO", F_B, FILL_GRAY); put(sv, f"C{R_MEMO}", "소속·비고(선택)", fill=FILL_GRAY); put(sv, f"D{R_MEMO}", "자유 입력", F_NOTE)
dv_type = DataValidation(type="list", formula1='"사업주·담당자,근로자"', allow_blank=True)
dv_l = DataValidation(type="list", formula1='"1,2,3,4,5"', allow_blank=True)
dv_run = DataValidation(type="list", formula1='"시행,미시행"', allow_blank=True)
dv_conf = DataValidation(type="list", formula1='"발생,미발생"', allow_blank=True)
for d in (dv_type, dv_l, dv_run, dv_conf): sv.add_data_validation(d)
dv_type.add(f"{CL(C0)}{R_TYPE}:{CLAST}{R_TYPE}")
for j in range(NRESP):
    sv.cell(row=R_TYPE, column=C0 + j).fill = FILL_IN
    sv.cell(row=R_MEMO, column=C0 + j).fill = FILL_IN

SROW = {}                       # 설문 변수ID → 행
r = R_MEMO + 1
for kind, a, b in SURVEY:
    if kind == "SEC":
        sv.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
        put(sv, f"A{r}", a, F_B, FILL_SEC, WRAP)
    else:
        SROW[a] = r
        mid = PART[next(it[1] for it in ITEMS if it[0] == a.rstrip("A"))][2] if kind != "REF" else "참고"
        put(sv, f"A{r}", a); put(sv, f"B{r}", mid, F_NOTE, align=WRAP); put(sv, f"C{r}", b, align=WRAP)
        put(sv, f"D{r}", RESP_HELP[kind], F_NOTE, align=WRAP)
        rng = f"{CL(C0)}{r}:{CLAST}{r}"
        {"L": dv_l, "ACT": dv_l, "REF": dv_l, "RUN": dv_run, "CONF": dv_conf}[kind].add(rng)
        for j in range(NRESP):
            c = sv.cell(row=r, column=C0 + j); c.fill = FILL_IN; c.border = BOX; c.alignment = CENTER
    sv.row_dimensions[r].height = 30
    r += 1
sv.freeze_panes = sv[f"{CL(C0)}{R_MEMO + 1}"]

# ================================================================ 3. 가중치
wt = wb.create_sheet("가중치")
widths(wt, {"A": 9, "B": 16, "C": 24, "D": 58, "E": 13, "F": 13, "G": 46})
put(wt, "A1", "문항별 가중치(배점) — 역산 결과", F_TITLE, border=False)
put(wt, "A2", "E열=2023~2025 공식 지수에서 역산한 배점(블록 배점 ÷ 문항 수, 블록 안 동일가중 검증). F열(노란 칸)을 바꾸면 결과에 바로 반영. 되돌리려면 E열 값을 F열에 복사.", F_NOTE, border=False)
hdr(wt, 4, ["문항ID", "중분류", "소분류(파트)", "문항", "공식 역산 배점", "적용 배점", "근거·신뢰도"])
WROW = {}
CONF_TXT = {"L": "A 검증: 2023·2024·2025 표준화값을 문항평균으로 재현(14/14 블록)",
            "P": "B/C: 2023식 재현, 2024·2025 공표값 미재현(공개 집계 한계)",
            "C": "B: 1-평균발생률과 ±0.006 일치(2023·2025), 2024 공표값은 이상치"}
for k, (iid, p, t, typ) in enumerate(ITEMS):
    rr = 5 + k
    WROW[iid] = rr
    pts = PART[p][3] / NPART[p]
    vals = [iid, PART[p][2], PART[p][1], t, pts, pts, CONF_TXT[typ]]
    for j, v in enumerate(vals):
        c = wt.cell(row=rr, column=1 + j, value=v); c.border = BOX; c.alignment = WRAP
    wt.cell(row=rr, column=5).number_format = "0.000"
    wt.cell(row=rr, column=6).number_format = "0.000"
    wt.cell(row=rr, column=6).fill = FILL_IN
W_LAST = 5 + len(ITEMS) - 1
rr = W_LAST + 2
put(wt, f"A{rr}", "합계", F_B, FILL_GRAY); put(wt, f"E{rr}", f"=SUM(E5:E{W_LAST})", F_B, fmt="0.00"); put(wt, f"F{rr}", f"=SUM(F5:F{W_LAST})", F_B, fmt="0.00")
rr += 2
hdr(wt, rr, ["파트", "중분류", "소분류", "문항 수", "공식 배점", "적용 배점"])
for k, (pid, pn, mid, pts) in enumerate(PARTS):
    q = rr + 1 + k
    for j, v in enumerate([pid, mid, pn, NPART[pid], f'=SUMIF($C$5:$C${W_LAST},C{q},$E$5:$E${W_LAST})',
                           f'=SUMIF($C$5:$C${W_LAST},C{q},$F$5:$F${W_LAST})']):
        c = wt.cell(row=q, column=1 + j, value=v); c.border = BOX
    wt.cell(row=q, column=5).number_format = "0.00"; wt.cell(row=q, column=6).number_format = "0.00"
wt.freeze_panes = "E5"

# ================================================================ 4. 점수_응답자 (계산 전용)
sc = wb.create_sheet("점수_응답자")
widths(sc, {"A": 10, "B": 26, "C": 10, "D": 30})
for j in range(NRESP):
    sc.column_dimensions[CL(C0 + j)].width = 9
put(sc, "A1", "응답자별 계산 시트 — 수정하지 마세요", F_TITLE, border=False)
put(sc, "A2", "노사협의회 제외", F_B); put(sc, "C2", f'=AND(설문!$C${R_COUNCIL}="미설치",설문!$C${R_SIZE}="50인 미만",설문!$C${R_UNION}="없음")')
put(sc, "D2", "노사협의회 0점 처리"); put(sc, "E2", f'=AND(설문!$C${R_COUNCIL}="미설치",NOT($C$2))')
hdr(sc, 3, ["ID", "구분", "배점", "설명"] + [f"=설문!{CL(C0+j)}{HR}" for j in range(NRESP)])
R_ST, R_VALID = 4, 5
put(sc, f"A{R_ST}", "TYPE"); put(sc, f"B{R_ST}", "응답자 유형")
put(sc, f"A{R_VALID}", "VALID"); put(sc, f"B{R_VALID}", "유효 응답(1=집계)")
row = 7
put(sc, f"A{row}", "① RAW: 설문 응답을 숫자로 변환", F_B, FILL_SEC, border=False)
row += 1
RAW = {}
RAW_ORDER = [x for x in SURVEY if x[0] != "SEC"]
raw_first = row
for kind, vid, text in RAW_ORDER:
    RAW[vid] = row
    put(sc, f"A{row}", vid); put(sc, f"B{row}", {"L": "5점척도", "RUN": "시행=1", "ACT": "활성화 1~5", "CONF": "발생=1", "REF": "참고 1~5"}[kind])
    for j in range(NRESP):
        col = CL(C0 + j); s = f"설문!{col}{SROW[vid]}"
        if kind in ("L", "ACT", "REF"):
            f = f'=IF({s}="","",IFERROR(VALUE({s}),""))'
        elif kind == "RUN":
            f = f'=IF({s}="","",IF({s}="시행",1,0))'
        else:
            f = f'=IF({s}="","",IF({s}="발생",1,0))'
        sc.cell(row=row, column=C0 + j, value=f)
    row += 1
raw_last = row - 1
for j in range(NRESP):
    col = CL(C0 + j)
    sc.cell(row=R_ST, column=C0 + j, value=f'=IF(설문!{col}{R_TYPE}="","",설문!{col}{R_TYPE})')
    sc.cell(row=R_VALID, column=C0 + j, value=f'=IF(AND({col}{R_ST}<>"",COUNT({col}{raw_first}:{col}{raw_last})>0),1,0)')


def norm_section(title, method):
    """문항 36개를 0~1로 변환하는 구역. method='25'(2025식) 또는 '24'(2023·24식)."""
    global row
    row += 1
    put(sc, f"A{row}", title, F_B, FILL_SEC, border=False)
    row += 1
    rows = {}
    for iid, p, t, typ in ITEMS:
        rows[iid] = row
        put(sc, f"A{row}", iid); put(sc, f"B{row}", PART[p][1]); put(sc, f"C{row}", f"=가중치!$F${WROW[iid]}", fmt="0.000")
        for j in range(NRESP):
            col = CL(C0 + j)
            if typ == "L":
                x = f"{col}{RAW[iid]}"
                f = f'=IF({x}="","",({x}-1)/4)' if method == "25" else f'=IF({x}="","",{x}/5)'
            elif typ == "P":
                run, act = f"{col}{RAW[iid]}", f"{col}{RAW[iid + 'A']}"
                f = (f'=IF({run}="","",{run})' if method == "25"
                     else f'=IF({run}="","",IF({run}=0,0.2,IF({act}="","",{act}/5)))')
            else:
                x = f"{col}{RAW[iid]}"
                f = f'=IF({x}="","",1-{x})'
            sc.cell(row=row, column=C0 + j, value=f)
        row += 1
    return rows


N25 = norm_section("② 2025식 변환: 5점척도 (x−1)/4 · 문17 시행=1/미시행=0 · 문18 미발생=1", "25")
N24 = norm_section("③ 2023·24식 변환: 5점척도 x/5 · 문17 (미시행=1, 시행=활성화)/5 · 문18 미발생=1", "24")


def part_section(title, nrows):
    global row
    row += 1
    put(sc, f"A{row}", title, F_B, FILL_SEC, border=False)
    row += 1
    prow = {}
    for pid, pn, mid, pts in PARTS:
        ids = [it[0] for it in ITEMS if it[1] == pid]
        a, b = nrows[ids[0]], nrows[ids[-1]]
        prow[pid] = row
        put(sc, f"A{row}", pid); put(sc, f"B{row}", pn); put(sc, f"C{row}", f"=SUM($C${a}:$C${b})", fmt="0.00")
        for j in range(NRESP):
            col = CL(C0 + j)
            den = f"SUMPRODUCT($C${a}:$C${b},--({col}{a}:{col}{b}<>\"\"))"
            core = f"IF({den}=0,\"\",SUMPRODUCT($C${a}:$C${b},{col}{a}:{col}{b})/{den}*$C{row})"
            if pid == "P7":
                f = f'=IF({col}${R_VALID}<>1,"",IF($C$2,"",IF($E$2,0,{core})))'
            else:
                f = f'=IF({col}${R_VALID}<>1,"",{core})'
            sc.cell(row=row, column=C0 + j, value=f)
        row += 1
    tot = row
    p1, p7 = prow["P1"], prow["P7"]
    put(sc, f"A{row}", "TOTAL", F_B); put(sc, f"B{row}", "노사관계 종합(100점 환산)", F_B)
    for j in range(NRESP):
        col = CL(C0 + j)
        sc.cell(row=row, column=C0 + j,
                value=f'=IF({col}${R_VALID}<>1,"",IFERROR(SUM({col}{p1}:{col}{p7})/SUMPRODUCT($C${p1}:$C${p7},--({col}{p1}:{col}{p7}<>""))*100,""))')
    row += 1
    return prow, tot


P25, T25 = part_section("④ 파트 점수 — 2025식", N25)
P24, T24 = part_section("⑤ 파트 점수 — 2023·24식", N24)
sc.freeze_panes = sc[f"{CL(C0)}6"]

# ================================================================ 5. 벤치마크
bm = wb.create_sheet("벤치마크")
widths(bm, {"A": 26, "B": 10, "C": 8, "D": 16, "E": 12, "F": 12, "G": 60})
put(bm, "A1", "공식 벤치마크 — 노사발전재단 일터혁신 실태조사(사업주·인사노무 담당자 응답)", F_TITLE, border=False)
put(bm, "A2", "2023 표 Ⅴ-8·Ⅴ-10 / 2024 표 Ⅵ-8·Ⅵ-10·Ⅳ-2.1~2.11 / 2025 표 Ⅵ-9·Ⅵ-11·Ⅲ-2.1~2.4. 2024(보정)=갈등 블록만 공표 발생률로 재계산.", F_NOTE, border=False)
r = 4
put(bm, f"A{r}", "① 파트별 표준화값(0~1)", F_B, FILL_SEC, border=False); r += 1
hdr(bm, r, ["키", "연도", "집단", "파트", "표준화값", "×공식배점", "비고"]); r += 1
BM_STD_A = r
for (y, g), vals in STD.items():
    for (pid, pn, mid, pts), v in zip(PARTS, vals):
        note = STD_NOTE.get((y, g), "") if (pid == "P4" or (y, g) == ("2025", "수혜")) else ""
        for j, x in enumerate([f"{y}|{g}|{pid}", y, g, pid, round(v, 6), f"=E{r}*{pts}", note]):
            c = bm.cell(row=r, column=1 + j, value=x); c.border = BOX
        bm.cell(row=r, column=5).number_format = "0.0000"; bm.cell(row=r, column=6).number_format = "0.00"
        r += 1
BM_STD_B = r - 1
r += 1
put(bm, f"A{r}", "② 노사관계 영역 공표 총점(100점)", F_B, FILL_SEC, border=False); r += 1
hdr(bm, r, ["키", "연도", "집단", "구분", "총점", "", "비고"]); r += 1
BM_TOT_A = r
for y, gd in TOT.items():
    for g, d in gd.items():
        for k, v in d.items():
            note = "갈등 블록 근사 보정(+%.2f)" % ADJ[g] if y == "2024(보정)" else ("표본 10개 미만, 참고만" if k in ("금융서비스", "기타서비스") else "")
            for j, x in enumerate([f"{y}|{g}|{k}", y, g, k, v, "", note]):
                c = bm.cell(row=r, column=1 + j, value=x); c.border = BOX
            r += 1
BM_TOT_B = r - 1
r += 1
put(bm, f"A{r}", "③ 문항별 공표 평균(1~5) · 문17 시행률/활성화 · 문18 발생률", F_B, FILL_SEC, border=False); r += 1
hdr(bm, r, ["키", "연도", "집단", "문항ID", "값", "단위", "비고"]); r += 1
BM_ITEM_A = r
for (y, g), d in IM.items():
    for q, vals in d.items():
        for i, v in enumerate(vals, 1):
            for j, x in enumerate([f"{y}|{g}|{q}_{i}", y, g, f"{q}_{i}", v, "평균(1~5)", ""]):
                c = bm.cell(row=r, column=1 + j, value=x); c.border = BOX
            r += 1
for (y, g), (p, a) in Q17RATE.items():
    for i in range(5):
        for iid, v, u in ((f"Q17_{i+1}", p[i], "시행률"), (f"Q17_{i+1}A", a[i], "활성화(1~5)")):
            for j, x in enumerate([f"{y}|{g}|{iid}", y, g, iid, v, u, "2025 활성화 N 일부 전년값 잔존 이슈" if y == "2025" and u != "시행률" else ""]):
                c = bm.cell(row=r, column=1 + j, value=x); c.border = BOX
            r += 1
for (y, g), rates in Q18RATE.items():
    for i, v in enumerate(rates, 1):
        for j, x in enumerate([f"{y}|{g}|Q18_{i}", y, g, f"Q18_{i}", v / 100, "발생률", ""]):
            c = bm.cell(row=r, column=1 + j, value=x); c.border = BOX
        r += 1
BM_ITEM_B = r - 1
r += 1
put(bm, f"A{r}", "④ 파트별 개선 처방", F_B, FILL_SEC, border=False); r += 1
BM_ADV_A = r
for pid, txt in ADVICE.items():
    put(bm, f"A{r}", pid); bm.merge_cells(f"B{r}:G{r}"); put(bm, f"B{r}", txt, align=WRAP)
    r += 1
BM_ADV_B = r - 1
bm.freeze_panes = "A4"

# ================================================================ 6. 결과
rs = wb.create_sheet("결과", 1)
widths(rs, {"A": 2, "B": 28, "C": 16, "D": 11, "E": 11, "F": 11, "G": 11, "H": 11, "I": 11, "J": 24, "K": 12})
put(rs, "B1", "노사관계 진단 결과", F_TITLE, border=False)
put(rs, "B2", "노란 칸에서 조건을 고르면 자동 계산됩니다. 점수는 재단 일터혁신지수 노사관계 영역과 같은 구조(100점)입니다.", F_NOTE, border=False)
ctrl = [("응답자 유형", "사업주·담당자", "사업주·담당자,근로자", "벤치마크는 사업주·담당자 응답 기준"),
        ("비교 연도", "2025", "2025,2024(보정),2024,2023", "2025=최신(2025식 계산), 2024(보정)=갈등 이상치 보정"),
        ("비교 집단", "자동", "자동,수혜,일반", "자동=설문 기본정보의 컨설팅 수혜 여부를 따름")]
for k, (lab, d, opts, h) in enumerate(ctrl):
    rr = 4 + k
    put(rs, f"B{rr}", lab, F_B, FILL_GRAY); put(rs, f"C{rr}", d, fill=FILL_IN, align=CENTER)
    rs.merge_cells(f"D{rr}:J{rr}"); put(rs, f"D{rr}", h, F_NOTE)
    dv = DataValidation(type="list", formula1=f'"{opts}"', allow_blank=False)
    rs.add_data_validation(dv); dv.add(f"C{rr}")
put(rs, "B7", "적용 계산식", F_B, FILL_GRAY); put(rs, "C7", '=IF(C5&""="2025","2025식","2023·24식")', fill=FILL_OUT, align=CENTER)
put(rs, "B8", "적용 비교집단", F_B, FILL_GRAY)
put(rs, "C8", f'=IF(C6="자동",IF(설문!$C${R_GRP}="받음(수혜)","수혜","일반"),C6)', fill=FILL_OUT, align=CENTER)
put(rs, "B9", "문항 비교 기준연도", F_B, FILL_GRAY); put(rs, "C9", '=IF(C5&""="2024(보정)","2024",C5&"")', fill=FILL_OUT, align=CENTER)
rs.merge_cells("D7:J9")
put(rs, "D7", f'="기관: "&IF(설문!$C$4="","(미입력)",설문!$C$4)&" · "&설문!$C${R_IND}&" · "&설문!$C${R_SIZE}&" · 노조 "&설문!$C${R_UNION}&" · 노사협의회 "&설문!$C${R_COUNCIL}', align=WRAP)

TYPE_RNG = f"점수_응답자!${CL(C0)}${R_ST}:${CLAST}${R_ST}"
VALID_RNG = f"점수_응답자!${CL(C0)}${R_VALID}:${CLAST}${R_VALID}"


def avg_row(sheet_row):
    rng = f"점수_응답자!${CL(C0)}${sheet_row}:${CLAST}${sheet_row}"
    return f'IFERROR(AVERAGEIFS({rng},{TYPE_RNG},$C$4,{VALID_RNG},1),"")'


def bm_std(pid):
    return (f'IFERROR(INDEX(벤치마크!$E${BM_STD_A}:$E${BM_STD_B},MATCH($C$5&"|"&$C$8&"|"&"{pid}",'
            f'벤치마크!$A${BM_STD_A}:$A${BM_STD_B},0)),"")')


def bm_tot(key_expr):
    return (f'IFERROR(INDEX(벤치마크!$E${BM_TOT_A}:$E${BM_TOT_B},MATCH($C$5&"|"&$C$8&"|"&{key_expr},'
            f'벤치마크!$A${BM_TOT_A}:$A${BM_TOT_B},0)),"")')


# 요약
put(rs, "B11", "■ 종합", F_B, border=False)
PT_HDR = 22                      # 파트 표 머리글 행
PT_A, PT_B = PT_HDR + 1, PT_HDR + 7
PT_SUM = PT_B + 1
summary = [
    ("응답자 수(유효)", f'=COUNTIFS({TYPE_RNG},$C$4,{VALID_RNG},1)', "0"),
    ("종합점수(100점)", f'=IFERROR(SUM(E{PT_A}:E{PT_B})/SUMPRODUCT(D{PT_A}:D{PT_B},--(E{PT_A}:E{PT_B}<>""))*100,"")', "0.0"),
    ("벤치마크(배점 반영)", f'=IFERROR(SUMPRODUCT(D{PT_A}:D{PT_B},G{PT_A}:G{PT_B},--(E{PT_A}:E{PT_B}<>""))/SUMPRODUCT(D{PT_A}:D{PT_B},--(E{PT_A}:E{PT_B}<>""))*100,"")', "0.0"),
    ("공식 공표 총점(참고)", "=" + bm_tot('"전체"'), "0.00"),
    ("벤치마크 대비 차이", '=IF(OR(C13="",C14=""),"",C13-C14)', "+0.0;-0.0;0.0"),
    ("진단 등급", '=IF(C16="","",IF(C16>=10,"S 매우 우수",IF(C16>=3,"A 우수",IF(C16>-3,"B 평균 수준",IF(C16>-10,"C 미흡","D 매우 미흡")))))', None),
    ("한 줄 해석", '=IF(C16="","응답을 입력하면 해석이 표시됩니다.","같은 해 "&$C$8&"사업장 평균보다 "&TEXT(ABS(C16),"0.0")&"점 "&IF(C16>=0,"높습니다.","낮습니다.")&" 가장 큰 개선 여지는 ‘"&C47&"’입니다.")', None),
]
for k, (lab, f, fmt) in enumerate(summary):
    rr = 12 + k
    put(rs, f"B{rr}", lab, F_B, FILL_GRAY)
    put(rs, f"C{rr}", f, F_B if k in (1, 5) else None, FILL_OUT, CENTER, fmt)
    if k == 6:
        rs.merge_cells(f"C{rr}:J{rr}")
        rs[f"C{rr}"].alignment = WRAP
        rs.row_dimensions[rr].height = 32
put(rs, "D13", '=IF(C13="","",REPT("■",ROUND(C13/5,0))&REPT("□",20-ROUND(C13/5,0)))', border=False)
rs.merge_cells("D13:J13")
put(rs, "D14", '=IF(C14="","",REPT("■",ROUND(C14/5,0))&REPT("□",20-ROUND(C14/5,0)))', border=False)
rs.merge_cells("D14:J14")
put(rs, "B20", "■ 소분류(파트)별 점수 — 막대: ■=우리 달성률, 숫자=벤치마크 달성률", F_B, border=False)
hdr(rs, PT_HDR, ["파트", "중분류", "배점", "우리 점수", "우리 달성률", "벤치 달성률", "벤치 점수", "차이(점)", "막대(우리 달성률)", "판정"], col=2)
for k, (pid, pn, mid, pts) in enumerate(PARTS):
    rr = PT_A + k
    vals = [f"{pid} {pn}", mid, f"=가중치!$F${W_LAST + 5 + k}",
            f'=IF($C$7="2025식",{avg_row(P25[pid])},{avg_row(P24[pid])})',
            f'=IF(E{rr}="","",E{rr}/D{rr})',
            "=" + bm_std(pid),
            f'=IF(G{rr}="","",G{rr}*D{rr})',
            f'=IF(OR(E{rr}="",H{rr}=""),"",E{rr}-H{rr})',
            f'=IF(F{rr}="","",REPT("■",ROUND(F{rr}*10,0))&REPT("□",10-ROUND(F{rr}*10,0)))',
            f'=IF(I{rr}="","",IF(I{rr}>=0.5,"강점",IF(I{rr}<=-0.5,"약점","보통")))']
    for j, v in enumerate(vals):
        c = rs.cell(row=rr, column=2 + j, value=v); c.border = BOX; c.alignment = CENTER if j else WRAP
    for colx, fm in (("D", "0.00"), ("E", "0.00"), ("F", "0%"), ("G", "0%"), ("H", "0.00"), ("I", "+0.00;-0.00;0.00")):
        rs[f"{colx}{rr}"].number_format = fm
put(rs, f"B{PT_SUM}", "합계", F_B, FILL_GRAY)
for colx, f, fm in (("D", f"=SUM(D{PT_A}:D{PT_B})", "0.00"), ("E", f"=IF(COUNT(E{PT_A}:E{PT_B})=0,\"\",SUM(E{PT_A}:E{PT_B}))", "0.00"),
                    ("H", f"=SUM(H{PT_A}:H{PT_B})", "0.00")):
    put(rs, f"{colx}{PT_SUM}", f, F_B, FILL_GRAY, CENTER, fm)
put(rs, f"B{PT_SUM+1}", "※ 노사협의회 미설치·50인 미만·무노조이면 노사협의회 파트를 빼고 100점으로 환산합니다(그 밖의 미설치는 0점).", F_NOTE, border=False)

# 중분류 5개
MR = PT_SUM + 3
put(rs, f"B{MR}", "■ 중분류(공식 5개 하위부문)", F_B, border=False)
hdr(rs, MR + 1, ["중분류", "배점", "우리 점수", "달성률", "벤치 점수", "차이(점)"], col=2)
for k, mid in enumerate(MID):
    rr = MR + 2 + k
    vals = [mid, f'=SUMIF($C${PT_A}:$C${PT_B},B{rr},$D${PT_A}:$D${PT_B})',
            f'=IF(COUNTIFS($C${PT_A}:$C${PT_B},B{rr},$E${PT_A}:$E${PT_B},">=0")=0,"",SUMIF($C${PT_A}:$C${PT_B},B{rr},$E${PT_A}:$E${PT_B}))',
            f'=IF(D{rr}="","",D{rr}/C{rr})',
            f'=SUMIF($C${PT_A}:$C${PT_B},B{rr},$H${PT_A}:$H${PT_B})',
            f'=IF(D{rr}="","",D{rr}-F{rr})']
    for j, v in enumerate(vals):
        c = rs.cell(row=rr, column=2 + j, value=v); c.border = BOX; c.alignment = CENTER if j else WRAP
    for colx, fm in (("C", "0.00"), ("D", "0.00"), ("E", "0%"), ("F", "0.00"), ("G", "+0.00;-0.00;0.00")):
        rs[f"{colx}{rr}"].number_format = fm

# 우선 개선과제
PR = MR + 8
put(rs, f"B{PR}", "■ 우선 개선과제 TOP 3 — ‘잃은 점수’(배점−우리 점수)가 큰 순", F_B, border=False)
hdr(rs, PR + 1, ["순위", "파트", "잃은 점수", "벤치 대비", "처방"], col=2)
# 보조열 L: 잃은 점수(+동점 방지용 아주 작은 값)
for k in range(7):
    rr = PT_A + k
    rs[f"L{rr}"] = f'=IF(E{rr}="",-1,D{rr}-E{rr}+ROW()/1000000)'
rs.column_dimensions["L"].hidden = True
for k in range(3):
    rr = PR + 2 + k
    m = f"MATCH(LARGE($L${PT_A}:$L${PT_B},{k+1}),$L${PT_A}:$L${PT_B},0)"
    vals = [k + 1,
            f'=IF(LARGE($L${PT_A}:$L${PT_B},{k+1})<0,"",INDEX($B${PT_A}:$B${PT_B},{m}))',
            f'=IF(C{rr}="","",INDEX($D${PT_A}:$D${PT_B},{m})-INDEX($E${PT_A}:$E${PT_B},{m}))',
            f'=IF(C{rr}="","",INDEX($I${PT_A}:$I${PT_B},{m}))',
            f'=IF(C{rr}="","",INDEX(벤치마크!$B${BM_ADV_A}:$B${BM_ADV_B},MATCH(LEFT(C{rr},2),벤치마크!$A${BM_ADV_A}:$A${BM_ADV_B},0)))']
    for j, v in enumerate(vals):
        c = rs.cell(row=rr, column=2 + j, value=v); c.border = BOX; c.alignment = WRAP if j in (1, 4) else CENTER
    rs.merge_cells(f"F{rr}:J{rr}")
    rs[f"D{rr}"].number_format = "0.00"; rs[f"E{rr}"].number_format = "+0.00;-0.00;0.00"
    rs.row_dimensions[rr].height = 44
# 한 줄 해석이 참조하는 1순위 파트 셀(C47) 위치 보정
first_pr = PR + 2
rs["C18"] = (f'=IF(C16="","응답을 입력하면 해석이 표시됩니다.","같은 해 "&$C$8&"사업장 평균보다 "&TEXT(ABS(C16),"0.0")&"점 "'
             f'&IF(C16>=0,"높습니다.","낮습니다.")&IF(C{first_pr}="",""," 가장 큰 개선 여지는 ‘"&C{first_pr}&"’입니다."))')

# 벤치마크 총점 비교(규모·업종·노조)
BR = PR + 6
put(rs, f"B{BR}", "■ 같은 조건 사업장과 비교(공식 공표 총점)", F_B, border=False)
hdr(rs, BR + 1, ["비교 대상", "공표 총점", "우리 점수", "차이"], col=2)
cmp_rows = [('"전체 평균"', '"전체"'), (f'"규모: "&설문!$C${R_SIZE}', f"설문!$C${R_SIZE}"),
            (f'"업종: "&설문!$C${R_IND}', f"설문!$C${R_IND}"), (f'"노조 "&설문!$C${R_UNION}', f'"노조 "&설문!$C${R_UNION}')]
for k, (lab, key) in enumerate(cmp_rows):
    rr = BR + 2 + k
    vals = ["=" + lab, "=" + bm_tot(key), "=C13", f'=IF(OR(C{rr}="",D{rr}=""),"",D{rr}-C{rr})']
    for j, v in enumerate(vals):
        c = rs.cell(row=rr, column=2 + j, value=v); c.border = BOX; c.alignment = CENTER if j else WRAP
    rs[f"C{rr}"].number_format = "0.00"; rs[f"D{rr}"].number_format = "0.0"; rs[f"E{rr}"].number_format = "+0.0;-0.0;0.0"
put(rs, f"B{BR+6}", "※ 공표 총점은 기본 배점 기준입니다. 가중치를 바꿨다면 위 ‘벤치마크(배점 반영)’을 보세요. 2025 수혜 표는 일부 세부값 정합성 이슈가 있어 참고용입니다.", F_NOTE, border=False)

# 문항별 비교
IR = BR + 8
put(rs, f"B{IR}", "■ 문항별 강·약점(우리 평균 vs 공표 평균) — 2023·2025는 문16·17·18만 공개되어 나머지는 2024 평균 사용", F_B, border=False)
hdr(rs, IR + 1, ["문항ID", "문항", "우리 평균", "벤치마크", "차이", "기준연도", "판정"], col=2)
item_rows = [(k, v, t) for (k, v, t) in RAW_ORDER if k in ("L", "RUN", "ACT", "CONF")]
for k, (kind, vid, text) in enumerate(item_rows):
    rr = IR + 2 + k
    key_y = f'$C$9&"|"&$C$8&"|"&"{vid}"'
    key_24 = f'"2024|"&$C$8&"|"&"{vid}"'
    lk = f"벤치마크!$A${BM_ITEM_A}:$A${BM_ITEM_B}"
    lv = f"벤치마크!$E${BM_ITEM_A}:$E${BM_ITEM_B}"
    bench = f'IFERROR(INDEX({lv},MATCH({key_y},{lk},0)),IFERROR(INDEX({lv},MATCH({key_24},{lk},0)),""))'
    byear = f'IFERROR(MATCH({key_y},{lk},0)*0+$C$9,IFERROR(MATCH({key_24},{lk},0)*0+2024,""))'
    label = {"L": text, "RUN": text.replace(" — 시행여부", " — 시행률"), "ACT": text, "CONF": text + " — 발생률"}[kind]
    if kind == "L" or kind == "ACT":
        judge = f'=IF(OR(F{rr}=""),"",IF(F{rr}>=0.3,"강점",IF(F{rr}<=-0.3,"약점","보통")))'
        fm = "0.00"
    elif kind == "RUN":
        judge = f'=IF(F{rr}="","",IF(F{rr}>=0.15,"강점",IF(F{rr}<=-0.15,"약점","보통")))'
        fm = "0%"
    else:
        judge = f'=IF(D{rr}="","",IF(D{rr}>0,"발생(주의)","미발생"))'
        fm = "0%"
    vals = [vid, label, "=" + avg_row(RAW[vid]), "=" + bench, f'=IF(OR(D{rr}="",E{rr}=""),"",D{rr}-E{rr})', "=" + byear, judge]
    for j, v in enumerate(vals):
        c = rs.cell(row=rr, column=2 + j, value=v); c.border = BOX; c.alignment = WRAP if j == 1 else CENTER
    rs[f"D{rr}"].number_format = fm; rs[f"E{rr}"].number_format = fm
    rs[f"F{rr}"].number_format = "+0.00;-0.00;0.00" if fm == "0.00" else "+0%;-0%;0%"
IR_END = IR + 1 + len(item_rows)
rr = IR_END + 1
put(rs, f"B{rr}", "참고: 지난해 고충 해결 정도(문20) 평균 코드", F_B, FILL_GRAY)
put(rs, f"C{rr}", "=" + avg_row(RAW["Q20"]), fill=FILL_OUT, align=CENTER, fmt="0.0")
put(rs, f"D{rr}", "1=30%미만 … 5=90%이상 (점수 미반영)", F_NOTE, border=False)

# 조건부 서식
red, green = Font(color="C0392B", bold=True), Font(color="1B8A5A", bold=True)
for rng in (f"I{PT_A}:I{PT_B}", f"G{MR+2}:G{MR+6}", f"E{BR+2}:E{BR+5}", f"F{IR+2}:F{IR_END}", "C16"):
    rs.conditional_formatting.add(rng, CellIsRule(operator="lessThan", formula=["0"], font=red))
    rs.conditional_formatting.add(rng, CellIsRule(operator="greaterThan", formula=["0"], font=green))
for rng in (f"K{PT_A}:K{PT_B}", f"H{IR+2}:H{IR_END}"):
    rs.conditional_formatting.add(rng, FormulaRule(formula=[f'LEFT({rng.split(":")[0]},2)="약점"'], fill=PatternFill("solid", fgColor="FDE2DF")))
    rs.conditional_formatting.add(rng, FormulaRule(formula=[f'LEFT({rng.split(":")[0]},2)="강점"'], fill=PatternFill("solid", fgColor="DFF3E7")))
    rs.conditional_formatting.add(rng, FormulaRule(formula=[f'LEFT({rng.split(":")[0]},2)="발생"'], fill=PatternFill("solid", fgColor="FDE2DF")))
rs.freeze_panes = "A11"

# ================================================================ 7. 역산검증
rv = wb.create_sheet("역산검증")
widths(rv, {"A": 8, "B": 8, "C": 10})
for colx in "DEFGHIJKLMNOPQRS":
    rv.column_dimensions[colx].width = 9
rv.column_dimensions["P"].width = 11; rv.column_dimensions["Q"].width = 11; rv.column_dimensions["R"].width = 11
put(rv, "A1", "역산검증 — 공표 문항평균으로 공식 표준화값을 재현(수식이 실시간 계산)", F_TITLE, border=False)
put(rv, "A2", "판정 허용오차: 문항평균은 소수 둘째 자리 반올림(±0.005)이므로 x/5는 ±0.00105, (x−1)/4는 ±0.0013 이내면 ‘일치’.", F_NOTE, border=False)
hdr(rv, 4, ["연도", "집단", "블록", "평균1", "평균2", "평균3", "평균4", "평균5", "평균6", "평균7", "평균8", "평균9",
            "블록평균", "x/5", "(x−1)/4", "공식값", "x/5 판정", "(x−1)/4 판정"])
blocks = []
for (y, g), d in IM.items():
    for q, vals in d.items():
        if q == "Q21":
            vals = vals + IM[(y, g)]["Q22"]; q = "Q21+22"
        if q == "Q22":
            continue
        pidx = {"Q16": 0, "Q24": 1, "Q21+22": 4, "Q19": 5, "Q23": 6}[q]
        blocks.append((y, g, q, vals, STD[(y, g)][pidx]))
blocks.sort(key=lambda b: (b[0], b[2], b[1]))
r = 5
for y, g, q, vals, off in blocks:
    rv.cell(row=r, column=1, value=y); rv.cell(row=r, column=2, value=g); rv.cell(row=r, column=3, value=q)
    for i, v in enumerate(vals):
        rv.cell(row=r, column=4 + i, value=v)
    rv[f"M{r}"] = f"=AVERAGE(D{r}:L{r})"
    rv[f"N{r}"] = f"=M{r}/5"
    rv[f"O{r}"] = f"=(M{r}-1)/4"
    rv[f"P{r}"] = round(off, 4)
    rv[f"Q{r}"] = f'=IF(ABS(N{r}-P{r})<=0.00105,"일치","불일치")'
    rv[f"R{r}"] = f'=IF(ABS(O{r}-P{r})<=0.0013,"일치","불일치")'
    for colx in "MNOP":
        rv[f"{colx}{r}"].number_format = "0.0000"
    for cc in range(1, 19):
        rv.cell(row=r, column=cc).border = BOX
    r += 1
LV_END = r - 1
for rng in (f"Q5:R{LV_END}",):
    rv.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"일치"'], fill=PatternFill("solid", fgColor="DFF3E7")))
    rv.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"불일치"'], fill=PatternFill("solid", fgColor="FDE2DF")))
r += 1
put(rv, f"A{r}", "결론: 2023·2024년은 ‘평균÷5’, 2025년은 ‘(평균−1)÷4’로 5점척도를 0~1로 바꾼 뒤 블록 배점을 곱함. 블록 안 문항은 동일가중(단순평균).", F_B, border=False)
r += 2
put(rv, f"A{r}", "문17 노사협력 프로그램(13점) — 후보식 비교", F_B, FILL_SEC, border=False); r += 1
hdr(rv, r, ["연도", "집단", "", "시행률1", "시행률2", "시행률3", "시행률4", "시행률5", "활성1", "활성2", "활성3", "활성4", "활성5",
            "(미시행1·시행a)/5", "시행률평균", "공식값", "후보1 판정", "후보2 판정"]); r += 1
Q17_A = r
for (y, g), (p, a) in Q17RATE.items():
    rv.cell(row=r, column=1, value=y); rv.cell(row=r, column=2, value=g)
    for i in range(5):
        rv.cell(row=r, column=4 + i, value=p[i]); rv.cell(row=r, column=9 + i, value=a[i])
    rv[f"N{r}"] = f"=SUMPRODUCT(1-D{r}:H{r}+D{r}:H{r}*I{r}:M{r})/25"
    rv[f"O{r}"] = f"=AVERAGE(D{r}:H{r})"
    rv[f"P{r}"] = STD[(y, g)][2]
    rv[f"Q{r}"] = f'=IF(ABS(N{r}-P{r})<=0.0007,"일치","불일치")'
    rv[f"R{r}"] = f'=IF(ABS(O{r}-P{r})<=0.0007,"일치","불일치")'
    for colx in "NOP":
        rv[f"{colx}{r}"].number_format = "0.0000"
    for cc in range(1, 19):
        rv.cell(row=r, column=cc).border = BOX
    r += 1
rv.conditional_formatting.add(f"Q{Q17_A}:R{r-1}", CellIsRule(operator="equal", formula=['"일치"'], fill=PatternFill("solid", fgColor="DFF3E7")))
put(rv, f"A{r}", "→ 2023은 (미시행=1, 시행=활성화)/5 식이 수혜·일반 모두 재현. 2025 일반은 시행률 평균과 일치. 2024 두 집단과 2025 수혜는 어떤 단순식으로도 재현 안 됨(원자료·결측처리 미공개).", F_NOTE, border=False)
r += 2
put(rv, f"A{r}", "문18 노사갈등(12점) — 1−평균발생률", F_B, FILL_SEC, border=False); r += 1
hdr(rv, r, ["연도", "집단", "", "파업%", "손실%", "고소%", "해고%", "", "", "", "", "", "", "1−평균발생률", "", "공식값", "차이", "판정"]); r += 1
Q18_A = r
for (y, g), rates in Q18RATE.items():
    rv.cell(row=r, column=1, value=y); rv.cell(row=r, column=2, value=g)
    for i, v in enumerate(rates):
        rv.cell(row=r, column=4 + i, value=v)
    rv[f"N{r}"] = f"=1-AVERAGE(D{r}:G{r})/100"
    rv[f"P{r}"] = STD[(y, g)][3]
    rv[f"Q{r}"] = f"=P{r}-N{r}"
    rv[f"R{r}"] = f'=IF(ABS(Q{r})<=0.01,"근접(±0.01)","이상치")'
    for colx in "NPQ":
        rv[f"{colx}{r}"].number_format = "0.0000"
    for cc in range(1, 19):
        rv.cell(row=r, column=cc).border = BOX
    r += 1
put(rv, f"A{r}", "→ 2023 산정방식(p.242): 미발생 0·발생 −1로 재코딩 후 0~1 변환. 2023·2025는 ±0.006 근접(결측 분모 차이 추정), 2024 공표값만 크게 벗어남 → 2024(보정) 벤치마크 제공.", F_NOTE, border=False)

# ================================================================ 8. 모형설계
md = wb.create_sheet("모형설계")
widths(md, {"A": 3, "B": 120})
doc = [
    ("노사관계 진단 평가모형 설계서", F_TITLE),
    ("", None),
    ("1. 목적과 원칙", F_B),
    ("· 노사발전재단 일터혁신지수 ‘노사관계’ 영역(100점)과 같은 문항·배점·변환식으로 채점해, 공식 벤치마크와 같은 잣대로 비교한다.", None),
    ("· 공개 자료로 재현이 확인된 규칙(A)만 그대로 쓰고, 재현되지 않은 부분(B·C)은 근거를 밝히고 가장 근접한 대안을 쓴다.", None),
    ("· 사업주·담당자 응답(재단 조사와 같은 응답주체)만 벤치마크와 비교하고, 근로자 응답은 따로 집계해 인식 차이를 본다.", None),
    ("", None),
    ("2. 구조(36문항 → 7개 소분류 → 5개 중분류 → 100점)", F_B),
    ("· 노사관계분위기 20 = 전반 인식(문16, 4문항) 10 + 노조·근로자대표 혁신 태도(문24, 5문항) 10", None),
    ("· 노사협력 및 갈등 25 = 협력 프로그램(문17, 5종) 13 + 노사갈등(문18, 4종) 12", None),
    ("· 정보공유와 의사소통 25 = 의사소통(문21, 5문항) + 경영정보 공유(문22, 4문항)", None),
    ("· 고충처리 15 = 문19(4문항) · 노사협의회 15 = 문23(5문항)", None),
    ("· 문항별 가중치(역산): 블록 안 동일가중 → 문16 2.50, 문24 2.00, 문17 2.60, 문18 3.00, 문21·22 2.78, 문19 3.75, 문23 3.00점/문항", None),
    ("", None),
    ("3. 점수 변환식(역산 결과)", F_B),
    ("· 5점척도 — 2023·2024: 평균÷5 (1점=0.2, 5점=1.0) / 2025: (평균−1)÷4 (1점=0, 5점=1). 14개 블록 모두 반올림 오차 안에서 일치 [신뢰도 A]", None),
    ("  쉽게 말하면: 2024년까지는 ‘전혀 그렇지 않다’도 기본점수 20%를 줬지만, 2025년부터는 0점에서 시작합니다. 그래서 2025년 점수가 낮아 보입니다.", Font(color=BRAND)),
    ("· 문17 협력 프로그램 — 2023·24식: 프로그램별 (미시행=1, 시행=활성화 1~5)÷5의 평균(2023 재현) / 2025식: 시행률(시행=1, 미시행=0)의 평균(2025 일반 재현) [신뢰도 B~C]", None),
    ("· 문18 노사갈등 — 미발생=1, 발생=0의 평균(=1−발생 항목 비율). 2023·2025 공표값과 ±0.006 [신뢰도 B]. 2024 공표값(0.66/0.51)은 이상치라 ‘2024(보정)’을 따로 둠", None),
    ("· 소분류 점수 = Σ(문항 배점×변환값)÷Σ(응답한 문항 배점)×소분류 배점 — 일부 문항 미응답 시 응답한 문항으로 비례 환산", None),
    ("· 종합 = Σ소분류 점수 ÷ Σ(산출된 소분류 배점) × 100", None),
    ("· 노사협의회 미설치: 50인 미만·무노조면 해당 소분류 제외 후 100점 환산, 그 외는 0점(30인 이상 설치 의무 반영)", None),
    ("", None),
    ("4. 비교·등급", F_B),
    ("· 비교연도 2025 → 2025식, 2023·2024 → 2023·24식으로 자동 계산(같은 잣대 비교). 비교집단은 컨설팅 수혜/일반.", None),
    ("· 벤치마크(배점 반영) = Σ(공식 소분류 표준화값 × 적용 배점). 기본 배점이면 공식 공표 총점과 같다.", None),
    ("· 등급(도구 자체 기준): 벤치마크 대비 +10점 이상 S, +3~+10 A, −3~+3 B, −10~−3 C, −10 미만 D", None),
    ("  근거: 2023~2025 규모·업종별 공표 총점의 집단 간 차이가 대체로 ±3~10점 범위여서, ±3점은 ‘평균 수준’, ±10점은 ‘뚜렷한 차이’로 둠.", None),
    ("· 우선 개선과제 = 잃은 점수(배점−우리 점수)가 큰 소분류 순. 문항별 판정은 공표 평균 대비 ±0.3점(시행률 ±15%p).", None),
    ("", None),
    ("5. 3개년 분석에서 확인된 사실", F_B),
    ("· 문항·척도·배점은 2023~2025 동일(36문항). 문17·18의 조사기간만 매년 1년씩 이동.", None),
    ("· 2024→2025 노사관계 점수 하락(수혜 66.08→65.16, 일반 61.36→60.10)은 상당 부분 변환식 변경 효과. 예) 문16 수혜 평균은 3.73→3.71로 거의 같지만 표준화값은 0.7455→0.6779로 떨어짐.", None),
    ("· 2024 갈등 표준화값(0.66/0.51)은 발생률 2%대와 맞지 않아, 보정 시 2024 노사관계 총점은 수혜 약 69.9, 일반 약 67.0으로 2023(70.79/67.01)과 비슷해짐.", None),
    ("· 2025 수혜 세부표(Ⅵ-9)는 5개 세부값이 2024값과 동일하게 기재되는 등 정합성 이슈가 있어 세부 비교는 참고용.", None),
    ("· 규모가 클수록, 노조가 있을수록, 공공행정서비스일수록 노사관계 점수가 대체로 높다(2023·2024 일관, 2025 수혜는 예외 존재).", None),
    ("", None),
    ("6. 한계와 업데이트", F_B),
    ("· 재단은 원자료·코드북·산출 프로그램을 공개하지 않아 문17(2024·2025)과 결측 처리 규칙은 정확히 복제할 수 없다. 공식 점수와 소수점 단위 차이가 날 수 있다.", None),
    ("· 표준편차가 공개되지 않아 백분위·Z점수는 산출하지 않는다(등급은 점수 차이 기준).", None),
    ("· 2026 「일터혁신 상생컨설팅 진단·평가 지표 개선방안 연구」 결과가 공개되면 문항·배점을 다시 검토해 [가중치]·[벤치마크] 시트만 갱신하면 된다.", None),
]
for i, (t, f) in enumerate(doc, 1):
    c = md.cell(row=i, column=2, value=t)
    c.alignment = Alignment(wrap_text=True, vertical="center")
    if f: c.font = f

# 시트 순서: 안내, 결과, 설문, 가중치, 벤치마크, 역산검증, 모형설계, 점수_응답자
order = ["안내", "설문", "결과", "가중치", "벤치마크", "역산검증", "모형설계", "점수_응답자"]
wb._sheets = [wb[n] for n in order]
wb.active = 1
for w in wb.worksheets:
    w.sheet_view.showGridLines = w.title in ("점수_응답자",)
wb.save(OUT)
print("saved", OUT, "| 설문 rows", min(SROW.values()), "-", max(SROW.values()), "| 점수 total rows", T25, T24)
