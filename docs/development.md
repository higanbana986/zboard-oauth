# Development

**English** · [简体中文](development.zh-CN.md)

Clone `https://github.com/higanbana986/zboard-oauth.git` and work from the repository root. Pull requests target `main`.

| Tool | Requirement |
| --- | --- |
| Go | 1.26.8, as pinned by go.mod |
| Node.js | 22 in CI; 18 or newer locally |
| Python | 3 |
| ZBoard packager | A checkout implementing the plugin SDK and `backend/tools/pluginpackager` |

```sh
sh scripts/check.sh
python3 scripts/package.py --zboard /path/to/zboard --platform linux-amd64
```

Checks cover formatting, race tests, vet, the gRPC process boundary, browser behavior, release metadata and version consistency. Packages contain only the manifest, signature, UI and selected runtime. Generated files stay in `.build/`, `.local/` and `dist/`.

The SDK is pinned in `go.mod`; default checks use `GOWORK=off`. A local SDK workspace may be used for joint development, but run checks again against the locked dependency before submitting.

Build targets are Linux amd64/arm64, macOS amd64/arm64 and Windows amd64. Cross-compilation does not certify target execution. See [Publishing](publishing.md) for signing and release automation.

Successful pushes to `main` upload `oauth-development-<commit>` under the Checks run's Artifacts section. The archive contains five platform packages, SHA-256 checksums, a temporary development public key and test instructions. Artifacts expire after 14 days; only the public key is uploaded. These packages are for isolated test hosts and cannot be submitted as production releases. Pull requests and release preflight checks build only the Linux amd64 development package and do not publish artifacts.

Without `--key`, packaging creates and reuses `.local/publisher.key` automatically. Keep this key to preserve the identity of subsequent local builds. With an updated ZBoard packager, the public key is included in the signed package metadata; the host shows a first-install trust confirmation scoped to this plugin. Older packages can supply the `.pub` file through the import dialog compatibility option. Explicit production `--key` and `--key-id` remain supported. Published releases are immutable; these development changes do not replace v0.0.1 assets.
