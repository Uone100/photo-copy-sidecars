# Find copies of one photo and check their edits

You have an original folder and a backup. Both contain the same image under different names. Before deciding what to keep, you want to see whether their editing sidecars differ.

## Set up

Download the named ZIP under **Assets** on the [release page](https://github.com/Uone100/photo-copy-sidecars/releases/latest). Extract it and open a terminal in the folder that contains `SKILL.md`.

Python 3.9 or later. The helper uses the standard library.

## Read the example report

Run the two quickstart commands below.

```sh
python examples/make_demo.py demo
python scripts/locate.py demo/original/photo.png demo
```

 The first creates a new example directory. The second reads it and prints JSON. Look under `matches`:

| Path | same_roles_and_bytes | Meaning |
| --- | --- | --- |
| backup/renamed.png | false | The photo bytes match, but its full-name XMP differs from the reference. |
| original/photo.png | true | Both the photo and its adjacent sidecar match the reference. |

Compare the names and hashes in `adjacent_xmp` with `reference_xmp`. A different hash means the file bytes differ. Open the sidecars in your editor to understand the actual change. If neither image has a recognized sidecar the flag is true for the two empty sets.

## Scan your own collection

Run `python scripts/locate.py "path/to/reference.jpg" "path/to/collection"`. Leave both paths readable and stable during the scan. For a large result redirect the output to a new JSON file outside the collection. The command only reads the images and XMPs. Missing or inaccessible paths appear in `scan_errors` and produce exit code 1 for a partial scan. A bad reference or root gives code 2. Re-run with a fresh demo directory if the example already exists.

The comparison recognizes adjacent full-name XMPs, stem-only XMPs and numbered darktable variants. It skips linked files and directories. Cropped, re-encoded and visually similar photos need a different search method. A stem-only XMP can be shared by multiple files with the same stem.

## Ask an agent

“Find exact copies of this photo in my backup, list their paths and tell me which sidecars need manual review.” Provide the reference path and the search folder.
