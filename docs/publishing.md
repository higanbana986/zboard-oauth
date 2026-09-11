# Publishing

**English** · [简体中文](publishing.zh-CN.md)

Each SemVer tag releases this plugin only. Development versions use `vX.Y.Z-dev.N`, release candidates use `vX.Y.Z-rc.N`, and stable versions use `vX.Y.Z`. The manifest and runtime must report the same version without the leading `v`. The current development release is `v0.0.2-dev.202609111158`.

## Configure Actions

Create an environment named `release` and restrict it to reviewed release tags. Configure:

| Setting | Type | Value |
| --- | --- | --- |
| `PLUGIN_SIGNING_KEY` | Environment secret | Base64 Ed25519 private key (64 bytes before encoding) |
| `PLUGIN_PUBLISHER_ID` | Environment variable | Stable publisher identifier; defaults to `higanbana986` |
| `PLUGIN_PUBLIC_KEY` | Environment variable | Matching base64 Ed25519 public key (32 bytes) |

Generate keys with ZBoard's `pluginpackager -keygen` in a secure location. Keep the private key outside Git and distribute the public key through a trusted channel. CI development keys must never be reused for a public release.

The release workflow verifies the tag against main history, runs checks without release secrets, builds five target packages, validates their metadata, creates checksums and `marketplace-entry.json`, then publishes a GitHub Release. Development and release-candidate tags are marked as GitHub prereleases. Existing releases are not overwritten. Failed draft releases remain drafts for inspection; remove an incomplete draft before retrying. A tag alone cannot publish if signing settings are missing.

## Trigger a release

After configuring the signing environment, choose a reviewed commit on `main` whose manifest and runtime versions agree. The current release is `v0.0.2-dev.202609111158`.

- Create `release/v0.0.2-dev.202609111158` from that commit to start a release without a pre-existing tag. After successful checks and signing, the workflow creates the tag and prerelease at the verified source commit.
- Alternatively, push the matching tag, or use Actions → Release → Run workflow from the reviewed main commit or release tag and enter the exact SemVer tag.

The workflow checks out the selected ref, verifies it belongs to main history, and rejects a mismatched existing tag or an existing Release. All release jobs are serialized and use the `release` environment. If that environment restricts deployment refs, explicitly allow the release branches or use an already allowed tag; the workflow does not bypass environment rules.

Checks artifacts are temporary development packages, separate from signed production Release assets. Keep production publisher keys stable across versions so hosts can verify upgrades.

## Submit to the market

Download `marketplace-entry.json` from the release and use the [market submission template](https://github.com/zerodenet/plugins/issues/new?template=submit-plugin.yml). Submit its plugin entry to `catalogs/zboard.json` in a focused PR. The marketplace reviews identity and key ownership, verifies package signatures and records tested host/platform evidence. No cross-repository write token is required by this plugin workflow.

GitHub Release URLs redirect. Existing ZBoard versions that reject redirects must use offline import or a compatible direct-download mirror; a marketplace listing alone does not change that host restriction.

Record real provider login and target-platform execution separately from CI. macOS signing/notarization is not supplied by these workflows.
