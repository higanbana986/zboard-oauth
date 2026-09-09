# Contributing

**English** · [简体中文](CONTRIBUTING.zh-CN.md)

Report reproducible OAuth defects with the plugin version, ZBoard build, provider type and sanitized logs. Report credential or authentication vulnerabilities using [Security](SECURITY.md).

Create a focused branch from `main`. Changes to provider behavior should cover successful authorization, rejected identity claims, timeouts and host policy boundaries. Run `sh scripts/check.sh` before opening a pull request. Update both language versions of affected guides.

Package and runtime versions must agree. Source builds and protocol fixtures do not demonstrate production-provider login or operating-system signing. Describe which checks were performed.

Plugins are submitted to the [ZeroDeNet marketplace](https://github.com/zerodenet/plugins) through its submission template after an independent signed release. OAuth source and releases stay in this repository.
