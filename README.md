# AI Trend Search — English edition

Weekly AI trends for marketers, published every Tuesday (KST).
Live site: https://hazajous-code.github.io/ai-newsletter-en/
Korean edition: https://hazajous-code.github.io/ai-newsletter-claude/trend/ (source repo: hazajous-code/ai-newsletter-claude)

## Structure
- `index.html` — current newsletter · `marketer.html` — current Marketer Kit
- `issues/<YYYY-MM-DD>.html`, `issues/<YYYY-MM-DD>-marketer.html` — permanent copies (links to shared pages use `../`; the pair link to each other)
- `news.html` — Today's AI News. Reads the Korean repo's curated data (`/ai-newsletter-claude/trend/data/news/`, same origin). Korean stories show only once `titleEn`/`summaryEn` exist in that repo's `trend/data/translations.json`.
- `archive.html` — past issues (entries added by `promote.py`)
- `style.css` — copied from the Korean edition (`trend/style.css`); keep in sync.

## Publishing
- Each issue is an English translation of the Korean issue of the same date: same structure, facts, sources and caveats. Don't add claims the Korean issue doesn't make; if a fact is corrected in one edition, correct both.
- Prepare the issue copies first, register them in `scheduled.json` (`{"id","date","title","promoted": false}`), and `promote.py` (run daily by `.github/workflows/daily.yml`, ~07:05 KST) moves them to the front page on the publish date.
- Glossary: footnote technical terms on first use per page, numbered in order of appearance, with a 1–2 sentence plain-language definition.
- Style: no filler sentences; start with a fact or a judgment. Mark hypothetical examples, editorial views and company claims as such.
