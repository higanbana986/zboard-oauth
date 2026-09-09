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
python3 scripts/package.py --zboard /path/to/zboard --dev-key --platform linux-amd64
```

Checks cover formatting, race tests, vet, the gRPC process boundary, browser behavior, release metadata and version consistency. Packages contain only the manifest, signature, UI and selected runtime. Generated files stay in `.build/`, `.local/` and `dist/`.

The SDK is pinned in `go.mod`; default checks use `GOWORK=off`. A local SDK workspace may be used for joint development, but run checks again against the locked dependency before submitting.

Build targets are Linux amd64/arm64, macOS amd64/arm64 and Windows amd64. Cross-compilation does not certify target execution. See [Publishing](publishing.md) for signing and release automation.
