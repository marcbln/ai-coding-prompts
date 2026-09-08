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
4. **Deliver** to the user's preferred location (e.g. `/home/marc/Syncthing/notes/angebote/`)

File naming: `YYMMDD__angebot-<topic-slug>.md`

## Usage / Correct Patterns

### Angebot Structure Template

````markdown
# <Feature-Titel>

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

### File Delivery

After writing the Angebot, ask the user where to save it. Common locations:
- `/home/marc/Syncthing/notes/angebote/` (default)
- Project-local `_ai/backlog/proposals/`

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
````
