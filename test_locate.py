import base64
import tempfile
import unittest
from pathlib import Path
from scripts.locate import locate

PIXEL=base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+j1XkAAAAASUVORK5CYII=")
class Copies(unittest.TestCase):
    def test_renamed_and_different_edits(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); (root/"backup").mkdir()
            original=root/"a.png"; other=root/"backup"/"b.png"
            original.write_bytes(PIXEL); other.write_bytes(PIXEL)
            (root/"not-a-match.png").write_bytes(b"x"*len(PIXEL))
            (root/"a_01.png.xmp").write_text("<edit>one</edit>")
            (other.parent/"b_01.png.xmp").write_text("<edit>two</edit>")
            r=locate(original,root)
            self.assertEqual([m["path"] for m in r["matches"]],["a.png","backup/b.png"])
            self.assertEqual([m["same_roles_and_bytes"] for m in r["matches"]],[True,False])
            self.assertEqual(r["matches"][1]["adjacent_xmp"][0]["role"],"darktable-version-01")
            self.assertEqual(other.read_bytes(),PIXEL)
