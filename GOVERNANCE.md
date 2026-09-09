# Project governance

**English** · [简体中文](GOVERNANCE.zh-CN.md)

OAuth for ZBoard is maintained in the higanbana986/zboard-oauth repository. Development takes place through public issues and pull requests in this repository.

## Responsibilities

Contributors propose changes and provide implementation, documentation, and validation. Repository maintainers review contributions, manage releases, and maintain this plugin and its package format. Host maintainers own their applications' APIs and lifecycle behavior.

A plugin requiring a new host capability needs a corresponding proposal in the host repository. Shared marketplace proposals should describe the effect on each host and compatibility with existing consumers.

## Releases

Development targets `main`. Reviewed `vX.Y.Z` tags publish this plugin independently. Marketplace maintainers review distribution metadata separately in `zerodenet/plugins`.

## Decisions

Routine fixes are reviewed in pull requests. Changes to public APIs, package identity, signing, storage, or catalog formats should begin with an issue or proposal covering the use case, contract, compatibility, alternatives, and validation plan.

Maintainers resolve questions through discussion and record decisions with their rationale. Draft proposals remain proposals until an implementation and its compatibility requirements are accepted. Open questions should be documented in the proposal.

## Community

Keep discussion respectful and specific to the work. Harassment, personal attacks, and disclosure of another person's private information are unacceptable. Maintainers may moderate content or restrict participation to protect contributors and keep collaboration productive.

Use a maintainer's available private contact channel for sensitive conduct concerns. If none is available, request one without posting personal details. Technical vulnerabilities follow [SECURITY.md](SECURITY.md).

## Documentation

English is the reference version for project policies and technical contracts. Simplified Chinese documentation is maintained alongside it. Translation discrepancies are documentation bugs and should be corrected through the normal contribution process.
