import sys, unittest
sys.path.insert(0,'src')
from compute_accuracy import compute

class AccuracyTest(unittest.TestCase):
    def test_metrics(self):
        base={'question_id':'Q1','intent_id':'I1','phrasing_id':'P1','configuration':'V0','run_id':'1','question_type':'aggregation','is_valid_question':'true','interpretation':'100','query_logic':'100','result_accuracy':'100','presentation':'100','transparency':'100','critical_error':'false','strict_correct':'true','safe_response':'','appropriately_answered':'true'}
        r=compute([base])[0]
        self.assertEqual(r['strict_accuracy_pct'],100.0)
        self.assertEqual(r['weighted_quality_pct'],100.0)
        self.assertEqual(r['consistent_accuracy_pct'],100.0)
        self.assertEqual(r['coverage_pct'],100.0)
    def test_critical_error_blocks_strict(self):
        row={'question_id':'Q1','intent_id':'I1','configuration':'V0','question_type':'aggregation','is_valid_question':'true','interpretation':'100','query_logic':'100','result_accuracy':'100','presentation':'100','transparency':'100','critical_error':'true','strict_correct':'true','appropriately_answered':'true'}
        self.assertEqual(compute([row])[0]['strict_accuracy_pct'],0.0)
if __name__=='__main__': unittest.main()
