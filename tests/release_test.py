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
        release.check_version(tag='v0.0.1')
        for tag in ('0.0.1', 'vv0.0.1', 'v0.0.2', 'v0.0.1;echo unsafe'):
            with self.assertRaises(ValueError):
                release.check_version(tag=tag)
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root / 'internal/control').mkdir(parents=True)
            (root / 'manifest.json').write_text('{"version":"0.0.1"}')
            (root / 'internal/control/server.go').write_text('const Version = "0.0.2"')
            with self.assertRaises(ValueError):
                release.check_version(root)

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

    def test_metadata_requires_every_platform_and_matching_package(self):
        manifest = release.check_version()
        pub = {'id': 'test-publisher', 'public_key': base64.b64encode(b'p' * 32).decode()}
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root / 'internal/control').mkdir(parents=True)
            (root / 'dist').mkdir()
            (root / 'manifest.json').write_text(json.dumps(manifest))
            (root / 'internal/control/server.go').write_text('const Version = "0.0.1"')
            with self.assertRaises(FileNotFoundError):
                release.metadata(root, 'v0.0.1', 'a' * 40, pub)
            for platform in release.PLATFORMS:
                packed = dict(manifest)
                executable = f'runtimes/{platform}/oauth' + ('.exe' if platform.startswith('windows-') else '')
                packed['components'] = {'server': {'executables': {platform: executable}}}
                with zipfile.ZipFile(root / 'dist' / f'zboard.oauth-v0.0.1-{platform}.zbplugin', 'w') as z:
                    z.writestr('manifest.json', json.dumps(packed))
                    z.writestr('signature.json', json.dumps({'algorithm': 'ed25519', 'key_id': pub['id']}))
            entry = release.metadata(root, 'v0.0.1', 'a' * 40, pub)
            self.assertEqual(len(entry['releases'][0]['artifacts']), 5)
            self.assertTrue(all('/v0.0.1/' in a['url'] for a in entry['releases'][0]['artifacts']))
            with self.assertRaises(ValueError):
                release.metadata(root, 'v0.0.1', 'a' * 40, {'id': 'wrong'})


if __name__ == '__main__':
    unittest.main()
