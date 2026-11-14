import json
import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
from validate_metrics import validate  # noqa: E402

SCRIPT = os.path.join(ROOT, 'scripts', 'validate_metrics.py')
SAMPLE = os.path.join(ROOT, 'assets', 'sample-fact-card.json')


def rec(**over):
    r = dict(institution='한전KPS', report_year=2025, baseline_year=2024,
             comparison_year=2025, program='육아휴직', population='전체',
             unit='명', baseline=127, actual=172, change_percent=35.4)
    r.update(over)
    return r


class ValidateTest(unittest.TestCase):
    def test_clean_record(self):
        out = validate([rec()])
        self.assertEqual((out['errors'], out['holds'], out['notes']), ([], [], []))

    def test_case_kps_percentages(self):
        pairs = [(127, 172, 35.4), (87, 115, 32.2), (140, 214, 52.9),
                 (196, 289, 47.4), (156, 205, 31.4)]
        rows = [rec(program=f'p{i}', baseline=a, actual=b, change_percent=c)
                for i, (a, b, c) in enumerate(pairs)]
        self.assertEqual(validate(rows)['errors'], [])

    def test_duplicate_citation_is_note_not_error(self):
        out = validate([rec(), rec()])
        self.assertEqual(out['errors'], [])
        self.assertEqual(out['unique_keys'], 1)
        self.assertEqual(len(out['notes']), 1)

    def test_conflicting_duplicate_is_error(self):
        out = validate([rec(), rec(actual=173, change_percent=None)])
        self.assertEqual(len(out['errors']), 1)

    def test_percentage_mismatch(self):
        self.assertEqual(len(validate([rec(change_percent=40)])['errors']), 1)

    def test_null_key_field_is_error(self):
        out = validate([rec(population=None)])
        self.assertIn('population', out['errors'][0])

    def test_zero_baseline_is_note(self):
        out = validate([rec(baseline=0, actual=12, change_percent=None)])
        self.assertEqual(out['errors'], [])
        self.assertEqual(len(out['notes']), 1)

    def test_zero_actual_is_valid_value(self):
        out = validate([rec(actual=0, change_percent=-100)])
        self.assertEqual((out['errors'], out['holds']), ([], []))

    def test_missing_value_is_hold_not_error(self):
        out = validate([rec(baseline=None, change_percent=None)])
        self.assertEqual(out['errors'], [])
        self.assertEqual(len(out['holds']), 1)

    def test_status_unavailable_and_not_applicable_differ(self):
        out = validate([rec(status='미확보', baseline=None, actual=None),
                        rec(program='x', status='비해당', baseline=None, actual=None)])
        self.assertEqual((len(out['holds']), len(out['notes'])), (1, 1))

    def test_non_numeric_is_error(self):
        self.assertEqual(len(validate([rec(baseline='많음')])['errors']), 1)

    def test_wrapped_records_accepted(self):
        self.assertEqual(validate({'records': [rec()]})['metric_rows'], 1)

    def test_bad_top_level_rejected(self):
        with self.assertRaises(ValueError):
            validate({'x': 1})


class CliTest(unittest.TestCase):
    def run_cli(self, path):
        return subprocess.run([sys.executable, SCRIPT, path],
                              capture_output=True, text=True)

    def test_sample_exits_zero_with_one_hold(self):
        p = self.run_cli(SAMPLE)
        self.assertEqual(p.returncode, 0, p.stderr)
        out = json.loads(p.stdout)
        self.assertEqual((out['unique_keys'], len(out['holds'])), (3, 1))

    def test_error_exits_one(self):
        path = os.path.join(os.path.dirname(__file__), '_bad.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump([rec(change_percent=99)], f, ensure_ascii=False)
        try:
            self.assertEqual(self.run_cli(path).returncode, 1)
        finally:
            os.remove(path)

    def test_missing_file_exits_two(self):
        self.assertEqual(self.run_cli('/nonexistent.json').returncode, 2)


if __name__ == '__main__':
    unittest.main()
