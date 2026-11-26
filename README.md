# Photo Copy Sidecars

Find every byte-identical copy of a chosen photograph under one local folder, including renamed files. See which copies have different adjacent XMP edits before organizing the originals.

[Download v0.1.0 ZIP](https://github.com/Uone100/photo-copy-sidecars/releases/download/v0.1.0/photo-copy-sidecars-0.1.0.zip)

Install in a Codex project with Node.js 22.20 or newer:

```sh
npx skills add Uone100/photo-copy-sidecars -a codex
```

## English quickstart

**[Follow the step-by-step tutorial](TUTORIAL.md)**

Download the named ZIP under **Assets** on the [release page](https://github.com/Uone100/photo-copy-sidecars/releases/latest). Extract it and open a terminal in the folder that contains `SKILL.md`.

Python 3.9 or later. The helper uses the standard library.

```sh
python examples/make_demo.py demo
python scripts/locate.py demo/original/photo.png demo
```

Two paths match the same photo. The backup has different XMP bytes.

## Use as an Agent Skill

Extract the ZIP contents into `.agents/skills/photo-copy-sidecars/` in a Codex project or `.claude/skills/photo-copy-sidecars/` in a Claude Code project. Confirm that `SKILL.md` sits directly inside that folder, then start a new session. The tutorial includes an example request and the inputs to supply. You can also use the commands directly.

## Where the request came from

PhotoPrism users describe duplicate photos hidden from view and ask for their file paths. This helper works directly on exported or original files. [Duplicate photo request](https://github.com/photoprism/photoprism/issues/1308) · [User discussion](https://github.com/photoprism/photoprism/discussions/3450)
