# YouTube and social video experiment skills

A local improvement of [Jakeschincariol/chatgpt-youtube-agent-skill](https://github.com/Jakeschincariol/chatgpt-youtube-agent-skill), preserving its MIT licence.

Fourteen Codex skills for planning, analysing and repurposing videos. They produce research,
edit briefs, scripts and experiment records; they do not publish posts or render restyles.

## Improvements

- Fairer comparisons within each platform/profile, with age, length and format matching.
  Small groups fall back to labelled looser comparisons instead of returning nothing.
- New-opening-first selection, visual restyle assessment and themed mashup briefs.
  Mostly reused footage with little new substance receives an editorial risk flag, not a
  guaranteed prediction of platform reach or monetisation.
- Optional first-frame brightness, approximate shot boundaries, frame change per shot and
  frontal-face detection; visual results need editorial review.
- Explicit retention time units and columns, invalid-row reporting, overlapping-cut merging,
  and suppression of false repeat cuts in YouTube rolling captions.
- Story/visual hook modes that omit direct-address and threat-word scoring; all scores state
  applicability and limits. Scores are heuristics, not future performance predictions.
- Originals and one-change variants tracked at 24h, 72h and 7d, including platform, profile,
  credits, actual observation ages, manual numbers and screenshot provenance/uncertainty.

## Skills

`yt-script`, `yt-package`, `yt-viral`, `yt-retention`, `yt-edit`, `yt-plan`, `yt-comment`,
`yt-seo`, `yt-chapters`, `yt-shorts`, `yt-audit`, `yt-repurpose`, `yt-frames`, `yt-experiments`.

## Use and installation

Copy each `skills/yt-*` folder into your Codex skills directory (normally `~/.codex/skills`).
Keep all fourteen together because some helpers reference sibling skills. New skills become
available on the next turn. A voice profile template is available in `templates/voice.md`.

Open `analytics-entry.html` for quick manual entry. Installed users also have the same page
inside `yt-experiments/assets/analytics-entry.html`. Export regular backups; if downloads are
unavailable, the page exposes copyable backup JSON. Private experiment stores are ignored by
Git. Do not commit your analytics, screenshots, videos, credentials or installed dependencies.

Text/analytics helpers use Python's standard library. Frame inspection optionally requires
OpenCV 4.x and NumPy. Install with:

```text
python -m pip install --target skills/yt-frames/vendor -r skills/yt-frames/requirements.txt
```

For an installed copy, use the corresponding installed `yt-frames` path instead.
See [USAGE.md](USAGE.md) for input schemas, example commands and limitations.

## Validation

```text
python -m unittest discover -s tests -v
```

Regression fixtures include synthetic overlapping captions and a public YouTube rolling
caption fixture with provenance and its MIT licence in `tests/fixtures`. Frame measurements
were separately checked on synthetic footage and a public OpenCV face sample. No private
user analytics or footage is bundled.
