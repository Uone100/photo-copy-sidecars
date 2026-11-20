---
name: photo-copy-sidecars
description: Locate every byte-identical copy of a specific photo across an originals or backup folder, including renamed copies, and compare adjacent XMP edit histories before advising a photographer about duplicates hidden by PhotoPrism.
---
Ask for one reference image and the folder to inspect. Run locally; paths and XMP stay on that machine.

Run `python scripts/locate.py REFERENCE SEARCH_FOLDER`. Review the relative paths of matches, their sidecar roles and shortened or full hashes. Distinguish identical media bytes from identical adjacent XMP sets. A differing XMP hash can reflect any metadata change; inspect relevant fields locally before attributing it to a different edit. Stem-only XMP can be shared by several local originals. Treat it as a candidate association.

When the originals folder belongs to PhotoPrism, explain why search results may show only one copy. For separate sidecar directories, sidecars in other formats, PhotoPrism database-only state or unavailable folders, list what was outside the scan. The report is read-only; use the user's normal photo manager for any later cleanup.
