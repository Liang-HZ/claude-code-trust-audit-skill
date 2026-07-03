---
name: claude-code-trust-audit
description: Use when a user wants Claude Code account-risk, ban-risk, or account-trust diagnostics from local network/browser signals and Claude Code local configuration traces, especially for Chinese users worried about non-official relays, mirrors, subscriptions, model IDs, or .claude settings/session history.
---

# Claude Code Trust Audit

## Overview

Run the public `network-fingerprint-audit` collector, read its JSON `agent_brief`, then inspect Claude Code local configuration only with user consent. Treat non-official Claude Code traces as high risk for this target audience.

## Workflow

1. Run `scripts/run_network_audit.py`.
   - Default command: `python3 scripts/run_network_audit.py`
   - Add `--default-browser-tracking-probe` only when the user accepts opening the default browser.
   - Add `--skip-network` only when the user explicitly wants no external lookups.
2. Open the JSON path printed at `audit.json_path`.
3. Read `agent_brief` first. Use raw fields only to verify evidence.
4. Read `references/claude-code-local-risk.md`.
5. Ask or confirm permission before reading `.claude` files or session transcripts.
6. Inspect Claude Code settings/session traces listed in `agent_brief.manual_agent_checks`.
7. Produce a concise report: verdict, high-risk sources, evidence paths/files, cleanup advice, and unverified checks.

## Interpretation Rules

- Do not present this as bypass guidance. Frame it as account-trust and environment consistency diagnostics.
- For this skill, unknown non-official Claude Code base URLs, relays, mirrors, subscriptions, helper credentials, or model IDs are high risk.
- Do not auto-delete `.claude` files. Recommend backup first, then user-controlled cleanup.
- Call out `unverified_or_failed_checks` before making strong claims.
- If evidence is absent because a probe was skipped, say so plainly.

## Output Shape

Use this order:

1. Overall risk level.
2. Top risk factors from `agent_brief.top_factors`.
3. Claude Code local high-risk traces, if any.
4. Low-risk conditions that are satisfied.
5. Recommended cleanup or retest steps.
6. Evidence paths and files reviewed.

Keep secrets redacted. Show config keys and file paths, not token values.
