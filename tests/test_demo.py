import copy
import json
from pathlib import Path
import unittest
from main import run


class DemoTests(unittest.TestCase):
    def test_business_result(self):
        data = json.loads(Path('sample.json').read_text())
        original = copy.deepcopy(data)
        result = run(data)
        self.assertFalse(result['compatible'])
        self.assertEqual(result['issues'],[{'field':'amount','issue':'type_changed'}])
        self.assertEqual(data, original, 'Input should not be mutated')

    def test_boundary_and_failure_behavior(self):
        data = json.loads(Path('sample.json').read_text())
        data['new'] = copy.deepcopy(data['old'])
        data['new']['note'] = {'type':'string','required':False}
        self.assertTrue(run(data)['compatible'])
        data['new']['note']['required'] = True
        self.assertEqual(run(data)['issues'], [{'field':'note','issue':'new_required_field'}])


if __name__ == '__main__':
    unittest.main()
