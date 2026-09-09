# Installation and operation

**English** · [简体中文](usage.zh-CN.md)

This guide covers installing and operating OAuth for ZBoard. Provider setup is described in the configuration reference.

## Requirements

Choose a package matching the host application, host API version, operating system, and CPU architecture. A page contribution such as `admin` identifies where the UI appears; access to host operations is determined separately by capabilities and host policy.

Use a ZBoard build with import preview and per-plugin trust. It verifies signatures and records a confirmed signing key without editing the host configuration. For local builds, see the [development guide](development.md). Older hosts still require `plugins.trusted_publishers` configuration and a restart.

## Install a package

1. Open plugin management and choose offline import.
2. Select the signed `.zbplugin` file and open the preview. Check its name, publisher, capabilities and compatibility.
3. For an unfamiliar publisher, confirm the source and signing-key fingerprint. Trust applies only to this plugin. Confirm the import; a new installation remains disabled.
4. Open the plugin configuration page, save the settings, and run its configuration check.
5. Enable the plugin and verify a complete login with a real provider account.

The original v0.0.1 release packages do not embed their public key. On an updated host, expand the import dialog's compatibility options and provide the publisher public key from the release metadata. No configuration-file change or restart is needed. New packages built with the updated host packager include the key automatically. These packages require a host that accepts the optional `signature.json.public_key` field.

Installation, configuration, enabling, and disabling are dynamic operations and do not require a host restart. A configuration check may only validate settings or provider metadata; use a real account to verify the full login flow for an authentication plugin.

### Online installation

A configured signed catalog lets administrators select packages from the host's marketplace page. `plugins.catalog_url` must point to the catalog document. A catalog signed by a host-trusted market may authenticate a publisher public key for the selected plugin, so installing users do not copy individual publisher keys. The host still verifies the package signature, digest and identity. The source registry is not itself a signed installation catalog. Public distribution status is listed in the [project README](../README.md).

## Upgrade and restore

Back up the host database, plugin directory, and encryption keys together before an upgrade. Importing a new version of the same plugin invokes the host's upgrade process. The publisher and signing key must match the existing installation, including after uninstall. Key rotation requires a separate reviewed host workflow; it is not accepted silently.

ZBoard prepares the candidate configuration, private data, and runtime before committing the change. A successful upgrade preserves the enabled or disabled state; a failed preparation keeps the previous version and committed data. Packages without a tested-host declaration for the current version require the plugin to be disabled before upgrade.

To restore a retained version, disable the plugin and select the version in its detail page. The host checks configuration and data compatibility. Restoring an older binary does not perform a downward data migration.

## Disable, uninstall, and remove data

| Operation | Result in ZBoard |
| --- | --- |
| Disable | Stops the runtime and revokes plugin UI/call sessions; keeps installation and data. |
| Uninstall | Stops the plugin and removes its program and pages; keeps configuration, private data, and operation history. |
| Clear retained data | Available after uninstall; clears plugin configuration and private data through the host. |

Core records such as accounts, identity bindings, orders, and credentials remain owned by ZBoard. Removing a plugin does not delete these records or undo completed business transactions.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Marketplace is empty | Whether a catalog is configured, reachable, correctly signed, and unexpired. |
| Import is rejected | Publisher trust, package digest, host/API compatibility, and target platform. |
| Plugin fails to start | Plugin operation history, host logs, configuration, and platform execution policy. |
| Settings cannot be saved | Refresh after a revision conflict and reapply the intended changes. |

For OAuth-specific issues, see the [configuration reference](configuration.md). Include plugin and host versions and sanitized logs when [reporting a bug](../CONTRIBUTING.md).
