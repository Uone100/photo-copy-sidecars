"""Create two byte-identical PNGs with different XMP descriptions."""
import argparse
from pathlib import Path
import struct
import zlib

def pixel():
    def chunk(kind, payload):
        return (struct.pack(">I", len(payload)) + kind + payload
                + struct.pack(">I", zlib.crc32(kind + payload)))
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">2I5B", 1, 1, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(b"\0\x20\x75\xca"))
            + chunk(b"IEND", b""))

def build(root):
    root.mkdir()
    for folder, name, label in (("original","photo","Unedited"),("backup","renamed","Print crop")):
        target=root/folder
        target.mkdir()
        (target/(name+".png")).write_bytes(pixel())
        (target/(name+".png.xmp")).write_text(
            '<x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">'
            '<rdf:Description xmlns:xmp="http://ns.adobe.com/xap/1.0/" rdf:about="" xmp:Label="'
            +label+'"/></rdf:RDF></x:xmpmeta>',encoding="utf-8")

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    build(parser.parse_args().directory)
