import unittest

from peg_monitor import assess, deviation_pct, monitor


class TestPeg(unittest.TestCase):
    def test_deviation(self):
        self.assertAlmostEqual(deviation_pct(0.99), -1.0)
        self.assertAlmostEqual(deviation_pct(1.02), 2.0)

    def test_assess(self):
        self.assertEqual(assess(1.0), "OK")
        self.assertEqual(assess(1.01), "WATCH")
        self.assertEqual(assess(0.95), "ALERT")

    def test_monitor(self):
        rows = monitor({"USDT": 1.0, "DAI": 0.95})
        by_symbol = {r["symbol"]: r for r in rows}
        self.assertEqual(by_symbol["USDT"]["status"], "OK")
        self.assertEqual(by_symbol["DAI"]["status"], "ALERT")


if __name__ == "__main__":
    unittest.main()
