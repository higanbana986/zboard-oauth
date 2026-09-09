# Repository guidelines

**English** · [简体中文](AGENTS.zh-CN.md)

OAuth is an independent plugin. Keep service code in `cmd/` and `internal/`, browser assets in `ui/`, and tests outside packaged assets. The plugin ID is `zboard.oauth`; the Go module is `github.com/higanbana986/zboard-oauth`.

Read [Contributing](CONTRIBUTING.md), [Development](docs/development.md), and [Architecture](docs/governance.md) before changing behavior. ZBoard owns accounts, registration policy, credentials, permissions and plugin lifecycle. Do not bypass its dedicated APIs.

Run `sh scripts/check.sh`; packaging changes also require a signed development package. Update the manifest, runtime version and documented version together. Keep English and Simplified Chinese documentation aligned. Never commit private keys, credentials, generated packages or local workspaces.

Pull requests target `main`. Releases are independent `vX.Y.Z` tags from reviewed main history. Publisher signing runs only in the protected release environment. Market submission is metadata, never a copy of the plugin source. Preserve existing authors and history when moving files.
