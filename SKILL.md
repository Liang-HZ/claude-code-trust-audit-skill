---
name: claude-code-trust-audit
description: Use when a user wants Claude Code account-risk, ban-risk, or account-trust diagnostics from local network/browser signals and Claude Code local configuration traces, especially for Chinese users worried about non-official relays, mirrors, subscriptions, model IDs, or .claude settings/session history.
---

# Claude Code Trust Audit

## Overview

This skill uses a **two-step** model:
1. **User runs** the `network-fingerprint-audit` collector in their own terminal (full system permissions required — the collector calls `ps`, `nslookup`, route table queries, etc. that are blocked inside the Agent sandbox).
2. **Agent interprets** the collector's JSON output, inspects Claude Code local configuration (after consent), and produces a readable audit report.

Treat non-official Claude Code traces as high risk for this target audience.

## Prerequisites

- The `network-fingerprint-audit` collector repo is downloaded automatically by `scripts/run_network_audit.py`. No manual setup needed.
- The collector needs full system permission to run (`ps`, `nslookup`, route tables, etc.) — **it cannot run inside the Agent sandbox**. The Agent will download the repo, then give the user a single command to copy-paste into their own Terminal.

## Platform Support

- macOS is the primary supported and tested path.
- Windows support is in development. The collector has Windows code paths, but this skill should describe Windows results as experimental until they are verified on the user's machine.
- Linux is not currently supported by the collector.

## Consent Gate

Before listing, reading, grepping, or summarizing any `~/.claude`, project `.claude`, session transcript, or Claude-related environment variable value, ask the user and wait for confirmation. A user request that explicitly says to inspect local Claude Code config, `.claude`, or session files counts as consent for that scope. A general request like "run an audit" does not.

Use this prompt when consent is missing:

`Do you want me to inspect local Claude Code settings and session metadata under ~/.claude and project .claude paths? I will redact secrets and will not delete anything.`

## Workflow

### Step 1 — 准备采集器，让用户去新终端执行

运行 `scripts/run_network_audit.py`。脚本会自动下载采集器仓库，然后打印一段**中文提示**，告诉用户：

1. **打开一个新的终端窗口**（不要在 Claude Code 当前窗口执行）
2. 粘贴脚本给出的那一行命令，按回车
3. 采集大约需要 1 分钟

脚本执行完毕后，问用户是否已经跑完了，让用户把输出的 JSON 路径告诉 Agent（或 Agent 自行搜索最近的 audit-*.json）。

可选参数（仅当用户同意后添加到命令中）：
- `--default-browser-tracking-probe` — 打开默认浏览器做 WebRTC 探测（需用户同意）
- `--skip-network` — 跳过所有外部网络查询，只收集本地数据

### Step 2 — 读取采集器输出

1. Read the JSON file at the path printed by the script.
2. Read `agent_brief` first. Use raw fields only to verify evidence.
3. Read `references/claude-code-local-risk.md`.

### Step 3 — Local configuration inspection (after Consent Gate)

4. Pass the Consent Gate before reading `.claude` files, session transcripts, or Claude-related environment variable values.
5. Inspect Claude Code settings/session traces listed in `agent_brief.manual_agent_checks` (and any standard paths like `~/.claude/settings.json`).

### Step 4 — Report

6. Produce a concise report following the Output Shape below.

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
