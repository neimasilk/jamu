# CLAUDE.md

This file is auto-loaded by Claude Code at session start.

## How this project is operated

JamuKG is operated as a **persistent LLM-maintained wiki**, adapted from
[Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
with kearifan lokal (see `wiki/SCHEMA.md` §"Why we deviate from Karpathy").

The user reads, curates sources, and asks questions. Claude maintains the wiki
— writes pages, updates cross-references, flags contradictions, runs lint.

## Read on every session start

1. **`wiki/SCHEMA.md`** — schema, conventions, page templates, claim-provenance
   tags, ingest/query/lint workflows, guardrails. This is the keystone. Apply it.
2. **`HANDOFF.md`** — current state of the research (most recent session).
3. **`wiki/log.md`** — last 5–10 entries (`grep "^## \[" wiki/log.md | tail -10`).
4. **`wiki/index.md`** — only if you need to find a specific page.

## Three guardrails that override anything else

These come from accumulated user feedback. They beat any wiki convention:

1. **Do not edit `MANUSCRIPT.md` without prior deliberation.** Discuss the change
   first, then edit.
2. **Do not introduce new analysis without a robustness test.** If the
   robustness test cannot be specified, the analysis is not ready.
3. **Do not stay narrow for 3+ sessions.** After two consecutive narrow
   sessions, propose a zoom-out audit before starting another.

These are also restated in `wiki/SCHEMA.md` §Guardrails.

## Operating principle (user)

> Santai dalam waktu, serius dalam metodologi — peneliti boleh salah, gagal,
> pivot, asalkan tidak bohong.

Slow is fine. Pivot is fine. Smoothing contradictions to make the story neater
is not fine.

## What is NOT adopted from Karpathy's stack

The companion [`autoresearch`](https://github.com/karpathy/autoresearch) loop
(autonomous overnight optimization with `NEVER STOP` doctrine) is **not**
adopted — see `wiki/SCHEMA.md` §"Why autoresearch loop is rejected". The wiki
pattern is adopted; the autoresearch loop is not.
