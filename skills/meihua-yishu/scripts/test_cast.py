import unittest
from cast import calculate, cast_numbers, cast_lunar, relation, TRIGRAMS

class CastingTests(unittest.TestCase):
    def test_observing_plum_classical_example(self):
        r = cast_lunar(5, 12, 17, 9)
        self.assertEqual((r["main"]["name"], r["moving_line"], r["changed"]["name"]),
                         ("泽火革", 1, "泽山咸"))
        self.assertEqual((r["mutual"]["upper"]["name"], r["mutual"]["lower"]["name"]), ("乾", "巽"))
        self.assertEqual((r["ti"]["name"], r["relation"], r["changed_relation"]), ("兑", "用克体", "用生体"))

    def test_peony_classical_example(self):
        r = cast_lunar(6, 3, 16, 4)
        self.assertEqual((r["main"]["name"], r["moving_line"], r["changed"]["name"], r["mutual"]["name"]),
                         ("天风姤", 5, "火风鼎", "乾为天"))

    def test_exhaustive_structural_invariants(self):
        names = set()
        for u in range(1, 9):
            for l in range(1, 9):
                for m in range(1, 7):
                    r = calculate(u, l, m, "website")
                    names.add(r["main"]["name"])
                    self.assertEqual(sum(a != b for a, b in zip(r["main"]["lines"], r["changed"]["lines"])), 1)
                    self.assertNotEqual(r["main"]["lines"][m-1], r["changed"]["lines"][m-1])
                    self.assertEqual(r["main"]["lines"][1:4], r["mutual"]["lower"]["lines"])
                    self.assertEqual(r["main"]["lines"][2:5], r["mutual"]["upper"]["lines"])
                    self.assertEqual(r["ti"]["id"], u if m <= 3 else l)
                    self.assertEqual(r["ti"]["lines"], (r["changed"]["upper"] if m <= 3 else r["changed"]["lower"])["lines"])
        self.assertEqual(len(names), 64)

    def test_pure_hexagram_conventions(self):
        self.assertEqual(calculate(1, 1, 3, "website")["mutual"]["name"], "乾为天")
        self.assertEqual(calculate(1, 1, 3, "book")["mutual"]["name"], "风火家人")
        self.assertEqual(calculate(8, 8, 4, "book")["mutual"]["name"], "水山蹇")

    def test_zero_remainders(self):
        r = cast_numbers(8, 16, 6)
        self.assertEqual((r["main"]["name"], r["moving_line"]), ("坤为地", 6))

    def test_all_five_element_relations(self):
        elements = "金木水火土"
        for ti in elements:
            self.assertEqual({relation(ti, yong) for yong in elements},
                             {"比和", "用生体", "体克用", "体生用", "用克体"})

    def test_invalid_inputs(self):
        for inputs in [(0, 1, 1), (-1, 2, 3), (True, 2, 3), (1.5, 2, 3)]:
            with self.assertRaises(ValueError):
                cast_numbers(*inputs)
        for moving in (0, 7):
            with self.assertRaises(ValueError):
                calculate(1, 1, moving)
        with self.assertRaises(ValueError):
            cast_lunar(5, 13, 1, 1)
        with self.assertRaises(ValueError):
            cast_lunar(5, 2, 1, 1, leap=True)

if __name__ == "__main__":
    unittest.main()
