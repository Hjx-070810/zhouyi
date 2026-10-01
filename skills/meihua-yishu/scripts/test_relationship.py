import unittest
from relationship_evidence import prepare, state

class RelationshipTests(unittest.TestCase):
    def test_three_readings_are_distinct(self):
        inputs = [(5, 9, 4), (39, 82, 41), (58, 37, 21)]
        expected = [
            ["体克用", "比和", "用克体", "体生用"],
            ["用生体", "体克用", "用生体", "用生体"],
            ["体克用", "比和", "比和", "用生体"],
        ]
        for numbers, relations in zip(inputs, expected):
            e = prepare(*numbers)
            self.assertEqual([x["relation_to_original_ti"] for x in e["phases"]], relations)
            self.assertIsNone(e["season"])
            self.assertEqual(e["moving_line_text"]["position"], e["casting"]["moving_line"])
        e = prepare(58, 37, 21)
        self.assertEqual(e["phases"][0]["marriage_rule"], "可成但成迟")
        self.assertIn("枯楊生稊", e["moving_line_text"]["text"])

    def test_season_does_not_recast(self):
        a, b = prepare(58, 37, 21), prepare(58, 37, 21, "autumn")
        self.assertEqual(a["casting"], b["casting"])
        self.assertEqual(b["season"]["ti"], "旺")
        self.assertEqual(b["season"]["phases"]["本用"], "死")
        self.assertEqual(b["season"]["phases"]["变用"], "休")

    def test_element_strength_table(self):
        self.assertEqual([state(x, "木") for x in "木火水金土"], ["旺", "相", "休", "囚", "死"])
        for dominant in "木火土金水":
            self.assertEqual({state(x, dominant) for x in "木火土金水"}, {"旺", "相", "休", "囚", "死"})

if __name__ == "__main__":
    unittest.main()
