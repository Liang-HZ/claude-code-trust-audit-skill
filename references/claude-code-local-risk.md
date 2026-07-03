# Claude Code Local Risk Checks

Use this reference after the network audit JSON is available.

## High-Risk Traces

Treat any of these as high risk for Chinese-user Claude Code account-trust diagnostics:

- Unknown `ANTHROPIC_BASE_URL`, relay domain, transfer station, mirror, reseller, or shared-subscription endpoint.
- Non-Anthropic or non-official model IDs in Claude Code settings or session transcripts.
- `ANTHROPIC_MODEL` or `ANTHROPIC_DEFAULT_*_MODEL` values that do not look like official Claude model IDs or clearly authorized cloud-provider IDs.
- `apiKeyHelper`, `ANTHROPIC_AUTH_TOKEN`, or `ANTHROPIC_API_KEY` used with an unknown base URL.
- Session transcripts under `~/.claude/projects/` showing non-official endpoint/model usage.

Official organization/cloud-provider setups can exist, but for this skill's target audience, unknown or unverifiable traces stay high risk until the user proves they are authorized.

## Paths To Inspect With Consent

- `~/.claude/settings.json`
- Current project `.claude/settings.json`
- Current project `.claude/settings.local.json`
- Relevant `~/.claude/projects/<project>/` session files
- Shell environment inherited by the current terminal

Do not print secrets. Redact token-like values and full cookies. Report presence and source path.

## Cleanup Advice

Never delete automatically. Tell the user to back up first, then remove suspicious settings or session cache:

1. Back up `~/.claude` and any project `.claude` folder.
2. Remove suspicious `env` entries, model overrides, base URLs, helper scripts, and local settings.
3. Remove related session cache if transcripts contain non-official traces.
4. Re-login through official Claude Code or a clearly authorized organization/cloud-provider path.

## Low-Risk Profile

Frame this as lower observed risk, not a guarantee:

- Egress IP is outside mainland China and in a supported region.
- IP country, timezone, DNS geography, browser language, and browser timezone are consistent.
- No mainland China locale, resolver, language, profile, or region trace.
- No WebRTC private host leak or public WebRTC egress mismatch.
- No proxy/VPN/datacenter abuse flags from structured IP intelligence.
- No non-official Claude Code config/session traces.
