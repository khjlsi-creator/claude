#!/usr/bin/env python3
"""layout_plan(JSON)의 칸 용량·어미·성과 띠 규칙 보조검사.

사용: python3 check_layout_plan.py plan.json [fact-card.json]
형식: references/layout-handoff.md 5절
종료코드: errors가 있으면 1, 없으면 0, 입력을 읽지 못하면 2.
지면의 형태(직각·색·좌표)는 검사하지 않는다.
"""
import json
import re
import sys

ARTIFACTS = ('경영평가', '친환경탄소중립', '시설개방', 'KORAD')

# (한 줄 글자 수, 최대 줄 수). None = 줄 수 제한 없음. references/layout-handoff.md 3절.
A4 = {
    'eval': (29, 2), 'title': (28, 1), 'subhead': (33, 1), 'rail': (4, 2),
    'tag': (8, 1), 'note': (42, 2), 'result': (36, 4),
    'body': {1: (42, None), 2: (20, None), 3: (13, None), 4: (9, None)},
}
CAPACITY = {
    '경영평가': A4,
    '시설개방': A4,
    '친환경탄소중립': dict(A4, subhead=(35, 1), result=(41, 4), tag=(6, 1),
                      body={1: (42, None), 2: (17, None), 3: (12, None)}),
    'KORAD': {
        'title': (43, 1), 'subhead': (12, 1), 'rail': (4, 2), 'tag': (8, 1),
        'note': (45, 1), 'result': (45, 4), 'eval': (43, 2),
        'body': {1: (45, 6), 2: (17, None), 3: (15, 15), 4: (11, 10)},
    },
}
CAUSAL = ('덕분', '로 인해', '로 인하여', '으로 인한', '에 힘입어', '효과로', '에 기여',
          '기여하', '을 견인', '를 견인', '입증', '초래', '에 따라 증가', '결과로')
PROSE_VERB = re.compile(r'(였다|했다|한다|이다|있다|었다|았다|됐다|된다|습니다|입니다|했음|였음)[.。]?\s*$')
OK_RESULT = {'SUPPORTED', 'CONDITIONAL'}
NUM = re.compile(r'\d[\d,]*\.?\d*')
BULLET = re.compile(r'^\s*[•\-\*★✔]\s*')


def _lines(text):
    return [BULLET.sub('', ln).strip() for ln in str(text).split('\n') if ln.strip()]


def _cap(artifact, slot):
    if 'max_chars' in slot:
        return slot['max_chars'], slot.get('max_lines')
    table = CAPACITY[artifact]
    kind = slot.get('kind', 'body')
    if kind == 'body':
        cols = table['body']
        return cols.get(slot.get('columns', 1), cols[max(cols)])
    return table.get(kind, table['body'][1])


def _card_numbers(card):
    if isinstance(card, dict):
        card = card.get('records', [])
    out = set()
    for r in card:
        if not isinstance(r, dict):
            continue
        for k in ('baseline', 'actual', 'change_percent', 'baseline_year',
                  'comparison_year', 'report_year'):
            v = r.get(k)
            if v is None or isinstance(v, bool):
                continue
            s = str(v)
            out.add(s)
            try:
                f = float(s)
                out.add(str(int(f)) if f == int(f) else s)
                if k.endswith('year'):
                    out.add(str(int(f))[-2:])
            except ValueError:
                pass
    return out


def check(plan, card=None):
    errors, warnings, slots_total = [], [], 0
    artifact = plan.get('artifact')
    if artifact not in ARTIFACTS:
        raise ValueError(f'artifact는 {"/".join(ARTIFACTS)} 중 하나여야 한다')
    claims = plan.get('claims', {})
    numbers = _card_numbers(card) if card is not None else None

    for pi, para in enumerate(plan.get('paragraphs', [])):
        where = f'단락{pi}({para.get("layout", "?")})'
        if not re.fullmatch(r'L\d{2,3}', str(para.get('layout', ''))):
            errors.append(f'{where}: 레이아웃 번호(Lxx)가 없음')
        slots = para.get('slots', [])
        if not slots:
            errors.append(f'{where}: 칸이 없음')
            continue
        if slots[-1].get('kind') != 'result' and not para.get('supplement'):
            errors.append(f'{where}: 성과 띠로 끝나지 않음(보충이면 supplement: true)')
        if para.get('supplement'):
            warnings.append(f'{where}: 보충 레이아웃 → 단계 상한 CONDITIONAL')

        for si, slot in enumerate(slots):
            slots_total += 1
            at = f'{where} 칸{slot.get("area", si)}'
            kind = slot.get('kind', 'body')
            lines = _lines(slot.get('text', ''))
            if not lines:
                errors.append(f'{at}: 글이 비어 있음(채울 자료가 없으면 칸이 적은 레이아웃으로)')
                continue
            per_line, max_lines = _cap(artifact, slot)
            for ln in lines:
                if len(ln) > per_line:
                    errors.append(f'{at}: OVER {len(ln)}자 > {per_line}자 "{ln[:20]}…"')
            if max_lines and len(lines) > max_lines:
                errors.append(f'{at}: OVER {len(lines)}줄 > {max_lines}줄')
            if kind in ('body', 'result', 'note'):
                for ln in lines:
                    if PROSE_VERB.search(ln):
                        errors.append(f'{at}: 서술형 종결 "{ln[-12:]}" → 명사형으로')
            ids = slot.get('claim_ids', [])
            for cid in ids:
                if claims and cid not in claims:
                    errors.append(f'{at}: claim "{cid}"가 claims에 없음')
            text = ' '.join(lines)
            if kind == 'result':
                hit = [w for w in CAUSAL if w in text]
                if hit:
                    errors.append(f'{at}: BLOCKED 성과 띠에 인과 표현 {hit}')
                if not ids:
                    errors.append(f'{at}: BLOCKED 성과 띠에 claim_ids가 없음')
                for cid in ids:
                    v = claims.get(cid)
                    if v and v not in OK_RESULT:
                        errors.append(f'{at}: BLOCKED 성과 띠에 {v} 주장 "{cid}"')
            elif kind in ('body', 'note') and NUM.search(text) and not ids:
                warnings.append(f'{at}: 수치가 있는데 claim_ids가 없음')
            if numbers is not None and kind in ('body', 'result', 'note'):
                for n in NUM.findall(text):
                    n = n.replace(',', '').rstrip('.')
                    if n and n not in numbers and len(n) > 1:
                        errors.append(f'{at}: 수치 {n}이(가) 사실카드에 없음')

    return {
        'artifact': artifact,
        'paragraphs': len(plan.get('paragraphs', [])),
        'slots': slots_total,
        'errors': errors,
        'warnings': warnings,
        'scope': '용량·어미·성과 띠·수치 대조만 검사. 견본 글 잔존과 지면 형태는 사람이 확인한다.',
    }


def main(argv):
    if len(argv) not in (2, 3):
        print('사용: check_layout_plan.py plan.json [fact-card.json]', file=sys.stderr)
        return 2
    try:
        with open(argv[1], encoding='utf-8') as f:
            plan = json.load(f)
        card = None
        if len(argv) == 3:
            with open(argv[2], encoding='utf-8') as f:
                card = json.load(f)
        result = check(plan, card)
    except (OSError, ValueError) as e:
        print(f'입력 오류: {e}', file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result['errors'] else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
