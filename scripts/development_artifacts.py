#!/usr/bin/env python3
"""Prepare explicitly development-only artifacts for successful main builds."""
import hashlib
from pathlib import Path
import subprocess

from release import PLATFORMS, ROOT, check_version


def main():
    tag = 'v' + check_version()['version']
    dist = ROOT / 'dist'
    packages = [dist / f'zboard.oauth-{tag}-{platform}.zbplugin' for platform in PLATFORMS]
    checksums = [f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n' for path in packages]
    (dist / 'SHA256SUMS').write_text(''.join(checksums))
    (dist / 'oauth-local-dev.pub').write_text((ROOT / '.local/publisher.key.pub').read_text())
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    (dist / 'README.md').write_text(f"""# OAuth for ZBoard development packages

Version: {tag}. Source commit: `{commit}`.

These packages use a disposable CI key with publisher ID `oauth-local-dev`.
They are intended for isolated host testing, not production or marketplace installation.
The public key is in `oauth-local-dev.pub`; the private key is never uploaded.
Each CI run generates a different key. Compare package hashes with `SHA256SUMS`.

Select the package for your host OS and architecture. Configure the development
publisher only on a test ZBoard instance before offline import. Cross-compilation
and package verification do not establish target-platform or live-provider acceptance.
Artifacts expire after 14 days. Production packages are published separately in Releases.

## 简体中文

这些安装包使用临时 CI 开发密钥，发布者 ID 为 `oauth-local-dev`，仅用于隔离测试。
公钥位于 `oauth-local-dev.pub`，私钥不上传；每次 CI 运行的公钥不同。
请选择对应平台的包，对照 `SHA256SUMS` 核验摘要后，仅在测试宿主配置公钥并离线导入。
交叉编译与验签不代表实际平台运行或真实提供方登录验收。产物保留 14 天，正式包由 Releases 单独发布。
""")


if __name__ == '__main__':
    main()
