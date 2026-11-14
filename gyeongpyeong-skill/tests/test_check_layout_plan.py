import copy
import json
import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
from check_layout_plan import check  # noqa: E402

PLAN = os.path.join(ROOT, 'assets', 'sample-layout-plan.json')
CARD = os.path.join(ROOT, 'assets', 'sample-fact-card.json')
SCRIPT = os.path.join(ROOT, 'scripts', 'check_layout_plan.py')


def load(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


class LayoutPlanTest(unittest.TestCase):
    def setUp(self):
        self.plan = load(PLAN)
        self.result = self.plan['paragraphs'][0]['slots'][-1]

    def test_sample_passes_with_card(self):
        out = check(self.plan, load(CARD))
        self.assertEqual(out['errors'], [])

    def test_causal_wording_in_result_is_blocked(self):
        self.result['text'] = '• 제도개선 덕분에 사용자 127 → 172명'
        self.assertTrue(any('인과' in e for e in check(self.plan)['errors']))

    def test_hold_claim_in_result_is_blocked(self):
        self.plan['claims']['c1'] = 'CONFLICT'
        self.assertTrue(any('CONFLICT' in e for e in check(self.plan)['errors']))

    def test_result_without_claims_is_blocked(self):
        self.result['claim_ids'] = []
        self.assertTrue(any('claim_ids' in e for e in check(self.plan)['errors']))

    def test_over_capacity(self):
        self.plan['paragraphs'][0]['slots'][0]['text'] = '가' * 29
        self.assertTrue(any('OVER' in e for e in check(self.plan)['errors']))

    def test_slot_max_chars_overrides_default(self):
        s = self.plan['paragraphs'][0]['slots'][0]
        s['text'] = '가' * 29
        s['max_chars'] = 30
        self.assertEqual(check(self.plan)['errors'], [])

    def test_prose_ending_is_error(self):
        self.plan['paragraphs'][0]['slots'][2]['text'] = '• 사용자가 127명에서 172명으로 늘었다'
        self.assertTrue(any('서술형' in e for e in check(self.plan)['errors']))

    def test_paragraph_must_end_with_result(self):
        self.plan['paragraphs'][0]['slots'].pop()
        self.assertTrue(any('성과 띠' in e for e in check(self.plan)['errors']))

    def test_supplement_paragraph_allowed_with_warning(self):
        self.plan['paragraphs'][0]['slots'].pop()
        self.plan['paragraphs'][0]['supplement'] = True
        out = check(self.plan)
        self.assertEqual(out['errors'], [])
        self.assertTrue(out['warnings'])

    def test_number_not_in_card(self):
        self.result['text'] = '• 육아휴직 사용자 127 → 173명'
        self.assertTrue(any('173' in e for e in check(self.plan, load(CARD))['errors']))

    def test_rail_label_limit(self):
        self.plan['paragraphs'][0]['slots'][1]['text'] = '추진실적현황'
        self.assertTrue(any('OVER' in e for e in check(self.plan)['errors']))

    def test_unknown_artifact_rejected(self):
        p = copy.deepcopy(self.plan)
        p['artifact'] = '기타'
        with self.assertRaises(ValueError):
            check(p)

    def test_cli_exit_codes(self):
        ok = subprocess.run([sys.executable, SCRIPT, PLAN, CARD], capture_output=True, text=True)
        self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)
        self.assertEqual(subprocess.run([sys.executable, SCRIPT, '/none.json'], capture_output=True).returncode, 2)


if __name__ == '__main__':
    unittest.main()
