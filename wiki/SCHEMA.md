---
name: SCHEMA
description: Maintenance schema for the JamuKG wiki — the keystone document
type: schema
last_updated: 2026-05-07
---

# JamuKG Wiki — Schema

> "The exact directory structure, the schema conventions, the page formats —
> all of that will depend on your domain, your preferences, and your LLM of
> choice." — Karpathy, LLM Wiki gist

This document tells Claude how to operate the wiki. It is the single
configuration file that keeps the wiki disciplined across sessions. It is
co-evolved with the user.

## 1. Architecture

Three layers, in order of upstream-ness:

| Layer | Location | Mutable by | Purpose |
|---|---|---|---|
| **Raw sources** | `data/raw/{duke_csv, knapsack, farmakope_pdf, pubmed}` | Harvest scripts only — never edited by hand | Source of truth. KG and wiki derive from here. |
| **Derived data** | `data/kg/*.json`, `data/processed/` | Analysis scripts in `src/` | Built artifacts. Reproducible from raw + scripts. |
| **The wiki** | `wiki/` | Claude (this assistant) | Synthesis, entity pages, concept pages, log. The wiki you are now reading. |
| **Canonical docs** | Project root: `HANDOFF.md`, `MANIFESTO_FARMAKOPE_NUSANTARA.md`, `MANUSCRIPT.md`, `TRIAGE.md`, `PAPER_DRAFT.md`, `NOTES_*.md`, `data_audit_*.md`, `literature_review_*.md` | Co-edited by user and Claude with deliberation | First-class documents that pre-date the wiki. The wiki references them, never replaces. |

**The wiki does not subsume canonical docs.** When a canonical doc and a wiki
page disagree, the canonical doc wins; flag the contradiction and resolve
through deliberation.

## 2. Page Types and Templates

### 2.1 Concept page (`wiki/concepts/<concept>.md`)

For recurring methodological or conceptual ideas (validation_gap,
forbidden_pairs, bridge_herb, consensus_louvain, ontology_split, jamu_grammar_roles).

```markdown
---
type: concept
status: validated | hypothesized | contested | retired
manifesto_layer: L1 | L2 | L3 | L4 | cross
last_updated: YYYY-MM-DD
---

# <Concept Name>

**One-line definition.**

## What it means

Plain prose definition. Indonesian narrative ok.

## Provenance

- `[script:<file.py>]` what computed it
- `[source:<dataset>]` what raw data it derives from
- `[null-tested:<statistic>]` robustness validation
- `[manuscript:§N.N]` where in MANUSCRIPT.md it appears

## Numbers and findings

Bullet points with explicit provenance per claim.

## Open questions / contradictions

If any. **Do not delete contradictions when newer data arrives — strikethrough
the old number, keep it visible, append the new with a date.**

## See also

[[wikilink]] to related pages.
```

### 2.2 Entity page (`wiki/entities/<class>/<name>.md`)

For named individuals: a herb species, a mazhab, a disease category.

```markdown
---
type: entity
class: herb | mazhab | disease_category | bridge | source
canonical_name: "Zingiber officinale Rosc"   # or mazhab id S0, etc.
manifesto_layer: L2
last_updated: YYYY-MM-DD
---

# <Canonical Name>

**Role / classification (one line).**

## Identity

- Scientific name / id
- Common names (Indonesian, regional)
- Family / parent

## Position in JamuKG

- Mazhab assignment (if herb): S0, role, n_partners, total_formulas
- Members (if mazhab): list with degrees
- Top therapeutic effects with provenance

## Findings about this entity

Per-claim bullets with provenance tags.

## Cross-mazhab relationships (if relevant)

Forbidden pairs, bridge connections, signature partnerships.

## Open questions

What we don't know yet about this entity.

## See also
```

### 2.3 Source page (`wiki/sources/<source>.md`)

For each raw dataset.

```markdown
---
type: source
location: data/raw/<path>
size_mb: N
n_records: N
license: <if known>
last_harvested: YYYY-MM-DD
---

# <Source Name>

**One-line description.**

## What it is

Origin, format, scope.

## How we use it

Which scripts read it, which derived artifacts depend on it.

## Quality and caveats

Known issues, biases, gaps. Flagged contradictions with other sources.

## Coverage in the wiki

Pages that derive content from this source.
```

### 2.4 Synthesis page (`wiki/syntheses/<topic>.md`)

For multi-source comparisons and analyses that emerged from queries.

```markdown
---
type: synthesis
question: "<original question that triggered this>"
sources_consulted: [<list of wiki page paths>]
last_updated: YYYY-MM-DD
---

# <Synthesis Title>

The question. The answer. The reasoning. With citations to wiki pages.

This is the most "wiki-grows-from-queries" page type. Karpathy: *good answers
can be filed back into the wiki as new pages*.
```

## 3. Conventions

### 3.1 Frontmatter

YAML frontmatter on every page. Tools (Obsidian Dataview, our own scripts)
parse it. Required keys depend on `type` (see templates above). Always include
`last_updated`.

### 3.2 Wikilinks

Use `[[wiki/path/to/page.md|display]]` for internal links. Use full path so
links work in plain markdown viewers and in Obsidian. Avoid bare titles.

External links to canonical docs: `[HANDOFF.md](../HANDOFF.md)` (relative).

### 3.3 Claim-provenance tags

**Every quantitative claim must carry a provenance tag.** This is the most
important convention in the wiki. Five tag types:

| Tag | Meaning |
|---|---|
| `[source:<name>]` | Directly observed in raw data (e.g. `[source:knapsack]`) |
| `[script:<file.py>]` | Computed by an analysis script |
| `[null-tested:<statistic>]` | Survived a robustness test (`Z=37.97`, `99.5% across 60 configs`) |
| `[hypothesis]` | Proposed but not yet tested |
| `[contradicted-by:<page>]` | Has a known counter-claim — link to where |

A page that is mostly `[hypothesis]` is fine but flag it as `status:
hypothesized` in frontmatter. Do not let a hypothesis migrate to "fact" without
a robustness test.

### 3.4 Bilingual rule

| Language | Used for |
|---|---|
| **Bahasa Indonesia** | Narrative prose, deliberation, motivation, "why we did this" |
| **English** | Species names (`Zingiber officinale Rosc`), taxonomy, statistics, file paths, code, ICD-10 / disease ontology, technical terms (mazhab is fine — it's a borrowed term used internally) |

Don't translate scientific names. Don't write narrative paragraphs in English
unless quoting a source.

### 3.5 Manifesto layer tag

Every page declares which Manifesto layer it relates to:

- **L1**: Historical text mining (Serat Centhini, Usada Bali) — the real frontier
- **L2**: Contemporary digital (KNApSAcK, Duke) — well-developed
- **L3**: Cross-temporal alignment — needs L1 first
- **L4**: Validation bridge (PubMed evidence) — well-developed
- **cross**: Methodological pages spanning layers

This makes layer-coverage visible. We currently know L4 and L2 are deep, L1 and
L3 are sparse. Lint should surface this asymmetry.

### 3.6 Tense and voice

- "We" for collective work (user + Claude)
- Past tense for completed analyses, present tense for current state
- No marketing language ("powerful", "comprehensive", "groundbreaking"). Plain
  description.

## 4. Operations

### 4.1 Ingest (when user adds a new source or finding)

When the user drops a paper, dataset, or insight:

1. Read the source. If a PDF, summarize the relevant section.
2. Discuss with the user: what is novel, what corroborates existing pages, what
   contradicts.
3. Write a `wiki/sources/<name>.md` page if it's a new dataset.
4. Update or create entity pages it touches.
5. Update or create concept pages whose definitions it sharpens.
6. **Append an entry to `wiki/log.md`** with the standard prefix.
7. Add new entry to `wiki/index.md` if a new page was created.

A single ingest may touch 5–15 wiki pages. That is correct.

### 4.2 Query (when user asks a question)

1. Read `wiki/index.md` to find candidate pages.
2. Read those pages, plus any canonical doc referenced.
3. Read raw data or run a script if needed.
4. Answer.
5. **If the answer is non-trivial synthesis** — file it as
   `wiki/syntheses/<topic>.md` and append to log. Do not let the synthesis die
   in chat history. Karpathy's compounding rule.

### 4.3 Lint (per session, opportunistically)

Once per session, run a lint pass. Items to check:

- **Orphans**: pages with no inbound links (`grep -L "filename"` on `wiki/`).
- **Stale claims**: pages where `last_updated` is more than 90 days old AND
  underlying script has changed since.
- **Contradictions**: pages whose numbers disagree with `data/kg/*.json`.
- **Missing pages**: concepts/entities cited 3+ times across the wiki but
  without their own page.
- **Layer asymmetry**: which Manifesto layers are under-developed.

**Lint reports a list. It does not auto-fix.** All fixes go through
deliberation with the user.

## 5. Guardrails (override conventions)

These rules trump all of §2–§4. They come from accumulated user feedback.

### G1. Do not edit `MANUSCRIPT.md` without prior deliberation

Wiki edits are cheap; manuscript edits are not. Discuss before editing.

### G2. Do not introduce new analysis without a robustness test

Every new claim that wants `status: validated` must have at least one of:
null-model test, parameter sweep, sensitivity analysis, or independent-axis
convergence. If the test cannot be specified, the analysis is not ready —
file as `status: hypothesized`.

### G3. Do not stay narrow for 3+ sessions

After two consecutive narrow sessions on the same sub-topic, the next session
must include a zoom-out audit: what avoided directions are now stale? What
manifesto layer is under-served? Lint counts as a zoom-out.

### G4. Do not smooth contradictions

When a new finding disagrees with an old page:

- **Wrong**: silently overwrite the old number with the new one.
- **Right**: strike through the old number, keep it visible, append the new
  number with date and reason. The contradiction is itself a finding.

Example: the 88.5% gap hypothesis from TRIAGE-asli vs the 85.56% we measured
at v08. Both numbers stay in the wiki — the gap *between* them is the lesson.

### G5. Do not auto-promote hypothesis to manuscript

A page going `hypothesis → validated` is allowed in the wiki. A page going
`validated → cited in MANUSCRIPT.md` requires a separate deliberation step.

### G6. Do not use Karpathy autoresearch loop

The companion [autoresearch](https://github.com/karpathy/autoresearch) repo
defines an autonomous overnight optimization loop with "NEVER STOP" doctrine.
We **do not** adopt it. Reasons:

1. **No single scalar objective.** JamuKG's central claim is "the 85.56% gap is
   structural, not parameter-tunable". An autonomous loop optimizing any
   gap-related metric would systematically violate the claim (Goodhart).
2. **Multi-axis methodology is the value.** Validation by convergence across
   plant-part + taxonomy + null-model is what makes findings trustworthy. A
   single-metric hill-climb destroys that.
3. **Operating principle conflict.** "Santai dalam waktu" vs "NEVER STOP" are
   irreconcilable. The user has explicitly chosen the former.

What we do borrow from autoresearch (in narrow scope, see G7):

- `program.md`-style brief per bounded sub-project
- `results.tsv` ledger discipline
- Explicit simplicity criterion ("if removing code keeps metric, keep
  removal")

### G7. Sub-project labs are bounded, not loops

A `wiki/labs/<topic>/` may exist with its own `program.md` + `results.tsv` for
a bounded technical sub-task. It is human-driven session-by-session, not
autonomous. The lab terminates with a synthesis page filed back to the wiki.

## 6. Why we deviate from Karpathy

| Karpathy default | JamuKG version | Reason |
|---|---|---|
| `index.md` content-oriented | Same | Adopted as-is |
| `log.md` chronological | Same | Adopted as-is |
| Schema = `CLAUDE.md` at root | `CLAUDE.md` at root **points to** `wiki/SCHEMA.md` | Schema is large; root file stays terse. Both are auto-loaded. |
| Wiki subsumes documents | Wiki **augments** existing canonical docs | We had MANUSCRIPT, MANIFESTO, etc. before adopting the wiki. Don't refactor pre-existing docs to fit the pattern. |
| Lint can be aggressive | Lint is advisory only; never auto-fix | Methodological discipline > tidiness |
| Single language | Bilingual ID/EN with explicit rule | User writes in Indonesian; sources are in English |
| No claim-provenance tags | Mandatory provenance tags on every quantitative claim | Anti-Goodhart, anti-vibe-knowledge |
| Optional "ingest one at a time" | Always one at a time | Slow tempo principle |
| Autoresearch loop available | Explicitly rejected (G6) | Conflicts with central paper claim and operating principle |
| Marp / dataview / fancy outputs | Plain markdown only for now | Add tools when needed, not preemptively |

## 7. Roadmap

What is bootstrapped (May 2026):
- Schema (this file), README, index, log
- Concept pages: validation_gap, forbidden_pairs, bridge_herb
- Entity pages: Zingiber officinale, Mazhab S0
- Source page: knapsack

What grows next (when the work demands):
- Remaining 4 bridge herbs (Curcuma zedoaria, Sauropus, Abrus, Woodfordia) —
  natural deliverable for the planned bridge investigation lab
- Remaining mazhab pages S1–S10
- Concept pages: consensus_louvain, ontology_split, jamu_grammar_roles
- Source pages: duke_ethnobotany, pubmed_evidence, farmakope_indonesia
- Synthesis: v07_to_v08_transition

What stays out:
- Per-formula pages (5,310 formulas — not page-worthy individually)
- Per-paper pages (literature_review_computational_jamu.md already serves)
- Auto-generated index of all 2,519 plants — that's data, not wiki
