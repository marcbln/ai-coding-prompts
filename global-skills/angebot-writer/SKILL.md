---
name: angebot-writer
description: >
  Creates technical proposals (Angebote) with multiple implementation options
  and effort/pricing for shop owners. Use when asked to "write an Angebot",
  "erstelle ein Angebot", or when a feature needs a multi-option offer.
---

# Angebot Writer

An "Angebot" (proposal/offer) is a structured document presenting a shop owner with multiple implementation options for a feature request. Each option describes what they get, how it works technically, and the estimated effort. The shop owner then picks which option(s) they want.

The standard flow is:
1. **Brainstorm** the feature (technical research, alternatives, decisions)
2. **Ask** the user whether to price in PersonDays/PersonHours or monetary amounts (CHF/EUR)
3. **Write** the Angebot as a clean German-language markdown document
4. **Deliver** to the user's preferred location (e.g. `/home/marc/Syncthing/focusshop-other/offers/`)
5. **Convert** to PDF/ODT/DOCX with `sb ... --no-view` and verify the artifacts

File naming: `YYMMDD__angebot-<topic-slug>.md`

## Usage / Correct Patterns

### Angebot Structure Template

````markdown
# <Feature-Titel>

**Kunde:** <Betreiber / Firma>
**Datum:** <JJJJ-MM-TT>
**Gültig bis:** <JJJJ-MM-TT>
**Angebotsnummer:** <optional>

---

## Ausgangslage

<2-3 Sätze: Was ist aktuell der Stand, was will der Shop-Betreiber?>

<Technischer Fund / Kontext: Was gibt es in der Datenbank / im System?>

---

## Optionen

### Option A: <Kurzbeschreibung>

<Was sehen Sie / Was bekommen Sie?>

- **Interaktion:** <Wie verhält sich das Feature?>
- **Aufwand:** ca. **X Tage** / **X Personenstunden**

---

### Option B: <Kurzbeschreibung>

...

---

## Vergleich

| Option | Beschreibung | Aufwand |
|--------|-------------|---------|
| **A** | <Kurzbeschreibung> | **X Tage** |
| **B** | <Kurzbeschreibung> | **X Tage** |

---

## Weiteres

- <Zusätzliche Infos: Technische Details, Abhängigkeiten, Konfiguration>

---

## Offene Fragen

1. <Frage an den Shop-Betreiber>
2. <Frage>
````

### Pricing Mode Decision

Before writing the Angebot, **ask the user** which pricing format to use:

- **PersonDays/PersonHours** — effort only, no monetary amounts. Good when the shop owner handles internal billing.
- **Monetary (CHF/EUR)** — fixed price per option. Good for external clients or fixed-budget projects.
- **Both** — show PersonDays AND a calculated price.

### Effort Estimation — derive it from evidence, never guess

An Angebot is an invoice basis. Every PT number must point at something you can show.

**First: how much did this actually take?** If the work exists, that figure is known and it
outranks every heuristic below — commit counts, file counts and test counts measure *produced
code*, not *effort*, and with agent-assisted development the two diverge by a large factor.
A 14-commit, 40-file feature can be well under a person-day. Ask, or read it off the
delivered work, before estimating. Only fall back to the table when it is genuinely new work.

Then, for new work, derive rather than guess:

| Evidence | What it tells you | Usual weight |
|---|---|---|
| `_ai/backlog/reports/*IMPLEMENTATION_REPORT*.md` | files touched, deviations, verification matrix | best single source — read it fully |
| `git log --stat -- <paths>` | commit count and blast radius per commit | medium |
| New migration classes | schema change, irreversible data movement | 0,5–1 PT each |
| New test files, test count | how much behaviour got pinned down | ~0,25 PT per 10 tests |
| New admin page (module + Vue/Twig + snippets × N locales) | a full UI slice incl. i18n | 1–2 PT |
| New orchestration service | the hard part: transactions, retries, state machine | 1–2 PT each |
| CLI command | thin wrapper over an existing service | 0,25–0,5 PT |
| ADR / plan / README / knowledge doc | write-up time | 0 — already inside the above, never double-count |

**Worked example** (Shopware plugin ↔ TradeGuard customer conversion, Sept 2026). Actual effort
was **4 PT** — roughly 2 PT to build both sides plus 2 PT of live testing and finetuning on the
Shopware and ERP clones, which is where the two real defects surfaced. The heuristic table
applied to the same 14 commits suggests well over 15 PT, i.e. it over-estimates by ~4x. Use it
for genuinely new work only.

Tiering of that 4 PT into what the customer is offered:

- **Option A — 1,5 PT** — the shop-side conversion on its own: transfer of orders, retention
  of the customer's login data, address de-duplication, audit trail, manual trigger via admin
  mask or CLI.
- **Option B — 4 PT** (A + 2,5) — everything that was actually built: A plus the ERP queue,
  automatic retry with backoff, per-case pre-check, dry run, result write-back, web view and
  the operating documentation.
- **Option C — 2 PT** additional — only work that is **not** done yet: automatic case pickup
  from the ERP, settling the login-credential behaviour, improved failure reporting, and
  commissioning. Never fold unshipped work into an option labelled as delivered.

**Traps**

- Tiers that don't add up to the total. If A + (B − A) ≠ the effort, you have either
  double-counted or under-sold. State explicitly which tiers overlap instead.
- **Commit count as effort.** It is the single most common error here. See the warning above.
- Counting a documentation pass on top of the commit that produced the code.
- Billing an option as delivered when the feature exists but is **not active in production**.
  Either say so in `Ausgangslage`, or ship the activation as its own option.
- Padding a retroactive Angebot. When the work is already delivered and the customer feels the
  value anyway, precision beats a rounder number.
- Letting the *method* of delivery leak into the document. How the work was produced —
  in-house, with contractor support, with tooling — is not the customer's concern and does not
  belong in the Angebot. Only the result, the scope and the effort.

### File Delivery

Ask the user where to save it. Verified locations, newest first:

- `/home/marc/Syncthing/focusshop-other/offers/` — **default.** Holds every existing Focus
  Angebot as `.md` + `.odt` + `.pdf` triplets with a shared basename
  (e.g. `260823__angebot-ki-cross-selling-empfehlungen`). Keep the `YYMMDD__angebot-<slug>`
  basename identical across all generated formats.
- Project-local `_ai/backlog/proposals/`

Do not create a new offers directory — consolidate into the existing one.

### QA Checklist — run on the markdown before converting

Never hand the source file straight to the converter. Walk the list:

- [ ] **Language** — German throughout; no English heading or leftover placeholder text
- [ ] **Spelling** — house style applied consistently. Swiss shops expect `ss` not `ß`
      (`ausschliesslich`, `dass`, `grösser`). Zero `ß` and zero mixed variants, and
      watch for doubled consonants (`ausschl<ss>sslich`). Grep both variants and compare counts.
- [ ] **No monetary amounts** unless the user chose monetary pricing
- [ ] **Every PT figure** is a concrete integer or one decimal — never "ca. 1 Woche"
- [ ] **Tiers add up** to the evidence sum (see Effort Estimation)
- [ ] **Tables render** — pipes balanced, header separator row present
- [ ] **No internal jargon** in the client-facing body: no table names, class names, HTTP
      status codes, commit hashes, file paths, or internal service names
- [ ] **No third-party customer names** other than the recipient
- [ ] **`## Offene Fragen`** holds at least 3 questions the shop owner can actually answer
- [ ] **`## Weiteres`** names at least one explicit non-inclusion (Abgrenzung)
- [ ] **Filename** matches `YYMMDD__angebot-<topic-slug>.md` and the date is today

### Document Conversion

An Angebot is almost always needed as PDF (and ODT/DOCX for the shop owner to edit), not just
markdown. Convert with `sb`, which uses pandoc and Gotenberg:

```bash
sb markdown pdf  <file>.md <file>.pdf  --no-view   # Gotenberg, `--theme github` default
sb markdown odt  <file>.md <file>.odt  --no-view   # pandoc
sb markdown docx <file>.md <file>.docx --no-view   # pandoc
```

**Always pass `--no-view`.** Without it every conversion opens a GUI viewer (Evince /
LibreOffice) that pops up over the terminal and blocks the session. The flag is supported on
all three subcommands. `sb markdown pdf` also offers `--theme`, `--no-toc`, `--no-outline`,
`--url`, and `--jobs`; ODT/DOCX offer `--toc`, `--font`, `--reference-doc`, `--jobs`.

Verify each artifact rather than trusting the exit code: `file` for the container type,
`pdftotext <out>.pdf - | grep '<expected string>'` for content, and for ODT/DOCX read
`content.xml` / `word/document.xml` out of the zip to confirm umlauts and tables survived.

## Anti-patterns (DO NOT USE)

````markdown
# ❌ English-language Angebot for a German shop owner

# ❌ Single option — an Angebot must always present multiple choices

# ❌ Pricing without asking — always ask PersonDays vs. monetary first

# ❌ Vague effort like "ca. 1 Woche" — use concrete numbers (0,5 Tage / 4h)

# ❌ Missing "Ausgangslage" — always describe the current state first

# ❌ Technical implementation details in the Angebot — keep it client-facing,
#    put technical notes in a separate brainstorm/proposal doc

# ❌ Forgetting "Offene Fragen" — always end with questions for the shop owner

# ❌ Running sb markdown pdf|odt|docx WITHOUT --no-view — a GUI viewer opens over
#    the terminal and blocks the session
````
