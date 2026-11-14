#!/usr/bin/env python3
"""JSON 사실카드의 산술·식별키·중복 보조검사. 원문 사실성 판정기는 아니다.

사용: python3 validate_metrics.py fact-card.json
형식: references/fact-card-schema.md
종료코드: errors가 있으면 1, 없으면 0, 입력을 읽지 못하면 2.
"""
import json
import sys
from decimal import Decimal, InvalidOperation

KEY_FIELDS = ('institution', 'report_year', 'baseline_year', 'comparison_year',
              'program', 'population', 'unit')
TOLERANCE = Decimal('0.11')
STATUSES = ('확보', '미확보', '비해당')


def _blank(v):
    return v is None or (isinstance(v, str) and not v.strip())


def _num(v):
    if _blank(v) or isinstance(v, bool):
        raise InvalidOperation
    d = Decimal(str(v))
    if not d.is_finite():
        raise InvalidOperation
    return d


def validate(records):
    if isinstance(records, dict) and isinstance(records.get('records'), list):
        records = records['records']
    if not isinstance(records, list):
        raise ValueError('최상위는 레코드 배열이어야 한다')

    errors, holds, notes, seen, pairs = [], [], [], {}, {}
    for i, r in enumerate(records):
        if not isinstance(r, dict):
            errors.append(f'{i}: 레코드가 객체가 아님')
            continue

        missing = [k for k in KEY_FIELDS if _blank(r.get(k))]
        if missing:
            holds.append(f'{i}: 식별키 미확정 {missing} → MISSING_FIELD_HOLD')
        key = None if missing else tuple(str(r[k]).strip() for k in KEY_FIELDS)
        for code in r.get('hold') or []:
            holds.append(f'{i}: {code}')

        status = r.get('status', '확보')
        if status not in STATUSES:
            errors.append(f'{i}: status는 {"/".join(STATUSES)} 중 하나여야 함')
            continue
        if status == '비해당':
            notes.append(f'{i}: 비해당')
            continue
        if status == '미확보':
            holds.append(f'{i}: 미확보 → MISSING_FIELD_HOLD')
            continue

        raw = (r.get('baseline'), r.get('actual'))
        if any(_blank(v) for v in raw):
            holds.append(f'{i}: 값이 비어 있음 → MISSING_FIELD_HOLD (0과 다름)')
            continue
        try:
            a, b = _num(raw[0]), _num(raw[1])
        except (InvalidOperation, ValueError):
            errors.append(f'{i}: baseline/actual이 숫자가 아님')
            continue

        if a == 0:
            notes.append(f'{i}: 원값 0, 증가율 산출 불가(신설 제도 가능)')
            if not _blank(r.get('change_percent')):
                errors.append(f'{i}: 원값이 0인데 change_percent가 기재됨')
        elif not _blank(r.get('change_percent')):
            try:
                stated = _num(r['change_percent'])
                calc = (b - a) / a * 100
                if abs(calc - stated) > TOLERANCE:
                    errors.append(f'{i}: 증감률 불일치 (표기 {stated}, 재계산 {calc:.1f})')
            except (InvalidOperation, ValueError):
                errors.append(f'{i}: change_percent가 숫자가 아님')

        pair = (str(r.get('institution')), str(r.get('baseline_year')),
                str(r.get('comparison_year')), str(r.get('unit')), a, b)
        label = (str(r.get('program')), str(r.get('population')))
        if pair in pairs and label not in pairs[pair]:
            j = pairs[pair][0]
            holds.append(f'{i}: {j}번과 값쌍이 같고 지표명이 다름 → LABEL_CONFLICT_HOLD 후보')
        pairs.setdefault(pair, [])
        if not pairs[pair]:
            pairs[pair].append(i)
        pairs[pair].append(label)

        if key is None:
            continue
        if key in seen:
            j, pa, pb = seen[key]
            if (a, b) != (pa, pb):
                errors.append(f'{i}: {j}번과 같은 지표키인데 값이 다름')
            else:
                notes.append(f'{i}: {j}번과 중복 인용, 1회만 집계')
        else:
            seen[key] = (i, a, b)

    return {
        'metric_rows': len(records),
        'unique_keys': len(seen),
        'errors': errors,
        'holds': holds,
        'notes': notes,
        'scope': '산술·식별키 검사만 수행. 원문 사실성과 의미는 사람이 확인한다.',
    }


def main(argv):
    if len(argv) != 2:
        print('사용: validate_metrics.py fact-card.json', file=sys.stderr)
        return 2
    try:
        with open(argv[1], encoding='utf-8') as f:
            result = validate(json.load(f))
    except (OSError, ValueError) as e:
        print(f'입력 오류: {e}', file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result['errors'] else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
