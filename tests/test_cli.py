import tempfile
import unittest
from pathlib import Path

from lunchbox.cli import load, render

CSV = """person,item,price,tags
Ada,Falafel wrap,7.50,vegan
Grace,Chicken katsu,9.95,
Ada,Lemonade,2.20,vegan;gf
"""


class CliTest(unittest.TestCase):
    def test_render_shows_each_person_and_total(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "order.csv"
            path.write_text(CSV)
            out = render(load(path))
        self.assertIn("Ada", out)
        self.assertIn("9.70", out)
        self.assertIn("TOTAL", out)
        self.assertTrue(out.strip().endswith("19.65"))

    def test_render_split_evenly_total_matches_rows(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "order.csv"
            path.write_text("person,item,price\nAnn,a,10.00\nBob,b,0.00\nCy,c,0.00\n")
            out = render(load(path), even=True)
        lines = out.splitlines()
        self.assertEqual([l.split() for l in lines[1:]], [["Ann", "3.34"], ["Bob", "3.33"], ["Cy", "3.33"], ["TOTAL", "10.00"]])

    def test_main_split_evenly_flag(self):
        import io
        from contextlib import redirect_stdout
        from lunchbox.cli import main
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "order.csv"
            path.write_text(CSV)
            buf = io.StringIO()
            with redirect_stdout(buf):
                self.assertEqual(main([str(path), "--split-evenly"]), 0)
        self.assertIn("9.83", buf.getvalue())
        self.assertTrue(buf.getvalue().strip().endswith("19.65"))


if __name__ == "__main__":
    unittest.main()
