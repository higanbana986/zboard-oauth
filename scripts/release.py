#!/usr/bin/env python3
"""Validate release identity and generate marketplace submission metadata."""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = 'https://github.com/higanbana986/zboard-oauth'
PLATFORMS = ('linux-amd64', 'linux-arm64', 'darwin-amd64', 'darwin-arm64', 'windows-amd64')
NUMBER = r'(?:0|[1-9][0-9]*)'
VERSION = re.compile(rf'{NUMBER}\.{NUMBER}\.{NUMBER}(?:-(?:dev|rc)\.{NUMBER}(?:\.{NUMBER})*)?')


def check_version(root=ROOT, tag=None):
    manifest = json.loads((root / 'manifest.json').read_text())
    version = manifest['version']
    if not VERSION.fullmatch(version):
        raise ValueError('manifest.version must be an unprefixed stable, rc, or dev semantic version')
    runtime = re.search(r'^const Version = "([^"]+)"$', (root / 'internal/control/server.go').read_text(), re.M)
    if not runtime or runtime[1] != version:
        raise ValueError('manifest and runtime versions differ')
    if tag is not None and tag != f'v{version}':
        raise ValueError('release tag must be v' + version)
    return manifest


def public_key(value):
    key = base64.b64decode(value.strip(), validate=True)
    if len(key) != 32:
        raise ValueError('PLUGIN_PUBLIC_KEY must encode 32 bytes')
    return key


def publisher(environ=os.environ):
    identity = environ.get('PLUGIN_PUBLISHER_ID', '')
    key = environ.get('PLUGIN_PUBLIC_KEY', '').strip()
    if not re.fullmatch(r'[a-z0-9][a-z0-9._-]{0,79}', identity) or identity == 'oauth-local-dev':
        raise ValueError('set a non-development PLUGIN_PUBLISHER_ID')
    public_key(key)
    return {'id': identity, 'public_key': key}


def write_key(out, environ=os.environ):
    pub = publisher(environ)
    secret = environ.get('PLUGIN_SIGNING_KEY', '').strip()
    private = base64.b64decode(secret, validate=True)
    if len(private) != 64 or private[32:] != public_key(pub['public_key']):
        raise ValueError('PLUGIN_SIGNING_KEY must encode 64 bytes and match PLUGIN_PUBLIC_KEY')
    with os.fdopen(os.open(out, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), 'w') as stream:
        stream.write(secret + '\n')


def metadata(root, tag, commit, pub):
    manifest = check_version(root, tag)
    if not re.fullmatch(r'[a-f0-9]{40}', commit):
        raise ValueError('source commit must be a full Git SHA')
    artifacts = []
    for platform in PLATFORMS:
        path = root / 'dist' / f'zboard.oauth-{tag}-{platform}.zbplugin'
        data = path.read_bytes()
        if not 0 < len(data) <= 32 * 1024 * 1024:
            raise ValueError('package exceeds host size limit')
        with zipfile.ZipFile(path) as package:
            packed = json.loads(package.read('manifest.json'))
            signature = json.loads(package.read('signature.json'))
            for field in ('id', 'version', 'requires', 'capabilities', 'surfaces'):
                if packed[field] != manifest[field]:
                    raise ValueError('package metadata differs from source: ' + field)
            if signature['key_id'] != pub['id'] or signature['algorithm'] != 'ed25519':
                raise ValueError('package publisher differs from release publisher')
            executable = f'runtimes/{platform}/oauth' + ('.exe' if platform.startswith('windows-') else '')
            if packed['components']['server']['executables'] != {platform: executable}:
                raise ValueError('package platform differs from release target')
            for name, digest in packed['files'].items():
                if hashlib.sha256(package.read(name)).hexdigest() != digest:
                    raise ValueError('package file digest mismatch')
        artifacts.append({'platform': platform, 'url': f'{REPOSITORY}/releases/download/{tag}/{path.name}',
                          'sha256': hashlib.sha256(data).hexdigest(), 'size': len(data)})
    release = {'version': tag, 'source_commit': commit, 'requires': manifest['requires'],
               'surfaces': manifest['surfaces'], 'capabilities': manifest['capabilities'], 'artifacts': artifacts}
    return {'id': manifest['id'], 'name': 'OAuth for ZBoard',
            'description': 'Sign in to ZBoard with GitHub, Google or a custom OAuth2 / OpenID Connect provider.',
            'repository': REPOSITORY, 'license': 'MPL-2.0', 'maintainers': ['higanbana986'], 'publisher': pub,
            'source': {'version': tag, 'commit': commit, 'manifest': 'manifest.json'}, 'releases': [release]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    check = commands.add_parser('check')
    check.add_argument('--tag')
    key = commands.add_parser('key')
    key.add_argument('--out', type=Path, required=True)
    meta = commands.add_parser('metadata')
    meta.add_argument('--tag', required=True)
    meta.add_argument('--commit', required=True)
    args = parser.parse_args()
    try:
        if args.command == 'check':
            check_version(tag=args.tag)
        elif args.command == 'key':
            write_key(args.out)
        else:
            entry = metadata(ROOT, args.tag, args.commit, publisher())
            dist = ROOT / 'dist'
            (dist / 'marketplace-entry.json').write_text(json.dumps(entry, indent=2) + '\n')
            (dist / 'SHA256SUMS').write_text(''.join(f"{a['sha256']}  {a['url'].rsplit('/', 1)[1]}\n" for a in entry['releases'][0]['artifacts']))
            (dist / 'release-notes.md').write_text(f'''OAuth for ZBoard {args.tag}\n\nSign in with GitHub, Google or a custom OAuth2 / OpenID Connect provider. ZBoard owns account creation, registration policy and sessions.\n\nDownload the signed `.zbplugin` for your host platform. Verify its SHA-256 against `SHA256SUMS` and obtain the publisher public key through a trusted channel before offline import.\n\nSource: `{args.commit}`. See the repository configuration and installation guides. `marketplace-entry.json` is a submission record, not a host catalog or a trust grant. Cross-compilation does not establish target-platform or live-provider acceptance.\n''')
    except (ValueError, KeyError, OSError, zipfile.BadZipFile) as error:
        parser.exit(1, f'release: {error}\n')


if __name__ == '__main__':
    main()
