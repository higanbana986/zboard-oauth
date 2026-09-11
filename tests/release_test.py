import base64
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

SPEC = importlib.util.spec_from_file_location('release', Path(__file__).resolve().parents[1] / 'scripts/release.py')
release = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(release)


class ReleaseTest(unittest.TestCase):
    def test_tag_requires_v_and_matches_runtime(self):
        version = release.check_version()['version']
        release.check_version(tag='v' + version)
        for tag in (version, 'vv' + version, 'v0.0.1', 'v0.0.2-beta.1', 'v' + version + ';echo unsafe'):
            with self.assertRaises(ValueError):
                release.check_version(tag=tag)
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root / 'internal/control').mkdir(parents=True)
            (root / 'manifest.json').write_text('{"version":"0.0.2-dev.1"}')
            (root / 'internal/control/server.go').write_text('const Version = "0.0.1"')
            with self.assertRaises(ValueError):
                release.check_version(root)

    def test_supported_release_channels(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root / 'internal/control').mkdir(parents=True)
            for version in ('0.0.2-dev.202609111158', '0.0.2-rc.1', '0.0.2'):
                (root / 'manifest.json').write_text(json.dumps({'version': version}))
                (root / 'internal/control/server.go').write_text(f'const Version = "{version}"')
                self.assertEqual(release.check_version(root, 'v' + version)['version'], version)
            for version in ('0.0.2-beta.1', '0.0.2-dev', '0.0.2-dev.01', '0.0.2+build'):
                (root / 'manifest.json').write_text(json.dumps({'version': version}))
                (root / 'internal/control/server.go').write_text(f'const Version = "{version}"')
                with self.assertRaises(ValueError):
                    release.check_version(root, 'v' + version)

    def test_key_requires_matching_public_key_and_refuses_overwrite(self):
        env = {'PLUGIN_PUBLISHER_ID': 'test-publisher', 'PLUGIN_PUBLIC_KEY': base64.b64encode(b'p' * 32).decode(),
               'PLUGIN_SIGNING_KEY': base64.b64encode(b's' * 32 + b'p' * 32).decode()}
        with tempfile.TemporaryDirectory() as name:
            path = Path(name) / 'private.key'
            release.write_key(path, env)
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            with self.assertRaises(FileExistsError):
                release.write_key(path, env)
            env['PLUGIN_PUBLIC_KEY'] = base64.b64encode(b'x' * 32).decode()
            with self.assertRaises(ValueError):
                release.write_key(Path(name) / 'bad.key', env)
        with self.assertRaises(ValueError):
            release.publisher({'PLUGIN_PUBLISHER_ID': 'oauth-local-dev'})

    def test_copied_key_text_allows_surrounding_whitespace_only(self):
        public = base64.b64encode(b'p' * 32).decode()
        secret = base64.b64encode(b's' * 32 + b'p' * 32).decode()
        env = {'PLUGIN_PUBLISHER_ID': 'test-publisher',
               'PLUGIN_PUBLIC_KEY': ' ' + public + '\r\n',
               'PLUGIN_SIGNING_KEY': '\n' + secret + '\r\n'}
        with tempfile.TemporaryDirectory() as name:
            path = Path(name) / 'private.key'
            release.write_key(path, env)
            self.assertEqual(path.read_text(), secret + '\n')
            self.assertEqual(release.publisher(env)['public_key'], public)
            env['PLUGIN_SIGNING_KEY'] = secret + 'invalid'
            with self.assertRaises(ValueError):
                release.write_key(Path(name) / 'invalid.key', env)

    def test_metadata_requires_every_platform_and_matching_package(self):
        manifest = release.check_version()
        version = manifest['version']
        tag = 'v' + version
        pub = {'id': 'test-publisher', 'public_key': base64.b64encode(b'p' * 32).decode()}
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root / 'internal/control').mkdir(parents=True)
            (root / 'dist').mkdir()
            (root / 'manifest.json').write_text(json.dumps(manifest))
            (root / 'internal/control/server.go').write_text(f'const Version = "{version}"')
            with self.assertRaises(FileNotFoundError):
                release.metadata(root, tag, 'a' * 40, pub)
            for platform in release.PLATFORMS:
                packed = dict(manifest)
                executable = f'runtimes/{platform}/oauth' + ('.exe' if platform.startswith('windows-') else '')
                packed['components'] = {'server': {'executables': {platform: executable}}}
                with zipfile.ZipFile(root / 'dist' / f'zboard.oauth-{tag}-{platform}.zbplugin', 'w') as z:
                    z.writestr('manifest.json', json.dumps(packed))
                    z.writestr('signature.json', json.dumps({'algorithm': 'ed25519', 'key_id': pub['id']}))
            entry = release.metadata(root, tag, 'a' * 40, pub)
            self.assertEqual(len(entry['releases'][0]['artifacts']), 5)
            self.assertTrue(all(f'/{tag}/' in a['url'] for a in entry['releases'][0]['artifacts']))
            with self.assertRaises(ValueError):
                release.metadata(root, tag, 'a' * 40, {'id': 'wrong'})


if __name__ == '__main__':
    unittest.main()
