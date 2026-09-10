import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


wallet = load('node_identity', ROOT / 'docs/scripts/prepare_node_identity.py')
guard = load('mainnet_guard', ROOT / 'docs/scripts/check_mainnet_docs.py')
# RFC 8032 test vector: public test material, never a funded wallet.
SEED = bytes.fromhex('9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60')
PUBLIC = bytes.fromhex('d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a')


class WalletPreparationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='pipe-wallet-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.keypair = self.root / 'wallet.json'
        self.keypair.write_text(json.dumps(list(SEED + PUBLIC)))
        self.data_dir = self.root / 'node'

    def test_import_matches_known_ed25519_identity_and_node_format(self):
        result = wallet.prepare_identity(self.data_dir, self.keypair)
        self.assertEqual(result['lattice_hex'], PUBLIC.hex())
        self.assertEqual((self.data_dir / 'node.key').read_text(), SEED.hex())
        self.assertEqual(stat.S_IMODE((self.data_dir / 'node.key').stat().st_mode), 0o600)
        self.assertEqual(json.loads(self.keypair.read_text()), list(SEED + PUBLIC))
        self.assertEqual(wallet.base58(bytes(32)), '1' * 32)

    def test_rejects_mismatched_keypair_before_creating_output(self):
        self.keypair.write_text(json.dumps(list(SEED + bytes(32))))
        with self.assertRaises(ValueError):
            wallet.prepare_identity(self.data_dir, self.keypair)
        self.assertFalse(self.data_dir.exists())

    def test_rejects_malformed_json_byte_values(self):
        for values in ([0] * 32, [True] * 64, [256] * 64, {}, 'invalid'):
            self.keypair.write_text(json.dumps(values))
            with self.assertRaises(ValueError):
                wallet.prepare_identity(self.data_dir, self.keypair)
        self.assertFalse(self.data_dir.exists())

    def test_existing_identity_and_node_data_are_preserved(self):
        self.data_dir.mkdir()
        original = self.data_dir / 'control-plane.json'
        original.write_text('existing enrollment')
        with self.assertRaises(ValueError):
            wallet.prepare_identity(self.data_dir, self.keypair)
        self.assertEqual(original.read_text(), 'existing enrollment')
        self.assertFalse((self.data_dir / 'node.key').exists())

    def test_create_never_overwrites_wallet_or_symlink(self):
        before = self.keypair.read_bytes()
        with self.assertRaises(FileExistsError):
            wallet.prepare_identity(self.data_dir, self.keypair, create=True)
        self.assertEqual(self.keypair.read_bytes(), before)
        link = self.root / 'wallet-link.json'
        link.symlink_to(self.keypair)
        with self.assertRaises(FileExistsError):
            wallet.prepare_identity(self.data_dir, link, create=True)
        self.assertEqual(self.keypair.read_bytes(), before)

    def test_generate_and_transfer_preserve_the_same_wallet(self):
        generated = self.root / 'generated.json'
        identity = wallet.prepare_identity(self.data_dir, generated, create=True)
        self.assertEqual(stat.S_IMODE(generated.stat().st_mode), 0o600)
        new_dir = self.root / 'host'
        installed = wallet.prepare_identity(new_dir, self.data_dir / 'node.key', node_key=True)
        self.assertEqual(identity, installed)
        self.assertEqual((new_dir / 'node.key').read_bytes(), (self.data_dir / 'node.key').read_bytes())
        self.assertEqual(wallet.read_keypair(generated)[32:].hex(), identity['lattice_hex'])

    def test_cli_prints_public_identity_only(self):
        result = subprocess.run([sys.executable, str(ROOT / 'docs/scripts/prepare_node_identity.py'),
                                 '--keypair', str(self.keypair), '--data-dir', str(self.data_dir)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('lattice_hex=' + PUBLIC.hex(), result.stdout)
        self.assertNotIn(SEED.hex(), result.stdout + result.stderr)
        self.assertEqual(len(result.stdout.splitlines()), 2)


class DocumentationGuardTests(unittest.TestCase):
    def test_fixed_cooldown_claims_are_detected(self):
        for text in ('This is a 30-day cooldown.', 'It has a fixed 30-day lock.', 'It uses a fixed 30 day lock.'):
            self.assertIn('incorrect fixed withdrawal period', guard.check_text(text))
        self.assertNotIn('incorrect fixed withdrawal period', guard.check_text('This is not a fixed 30-day lock.'))

    def test_current_stake_passes_but_old_minima_fail(self):
        self.assertEqual(guard.check_text('Mainnet requires 10,000 PIPE. There are no individual node rewards.'), [])
        for amount in ('100', '1,000', '1000'):
            self.assertIn('incorrect PIPE minimum', guard.check_text(f'Requires {amount} PIPE.'))

    def test_old_networks_and_assumed_split_are_detected(self):
        self.assertIn('obsolete network instructions', guard.check_text('Run on DevNet2'))
        self.assertIn('obsolete network instructions', guard.check_text('Testnet setup'))
        self.assertIn('unconfirmed burn percentage', guard.check_text('Burn 93%'))

    def test_registry_consistency_rejects_spec_version_drift(self):
        with tempfile.TemporaryDirectory(prefix='pipe-policy-test-') as path:
            target = Path(path) / 'docs'
            target.mkdir()
            for name in ('Tokenomics.md', 'tokenomics-operations-spec.md', 'tokenomics-params.json'):
                shutil.copyfile(ROOT / 'docs' / name, target / name)
            spec = target / 'tokenomics-operations-spec.md'
            spec.write_text(spec.read_text().replace('Version 3.0.0', 'Version 3.0.1'))
            result = subprocess.run([sys.executable, str(ROOT / 'docs/scripts/check_tokenomics_params_sync.py')],
                                    cwd=path, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Version mismatch', result.stdout)

    def test_link_check_rejects_private_file_even_when_it_exists(self):
        with tempfile.TemporaryDirectory(prefix='pipe-links-test-') as path:
            root = Path(path)
            (root / 'docs').mkdir()
            (root / 'internal').mkdir()
            (root / 'internal/notes.md').write_text('# Internal')
            (root / 'README.md').write_text('[Notes](internal/notes.md)')
            result = subprocess.run([sys.executable, str(ROOT / 'docs/scripts/check_markdown_links.py')],
                                    cwd=path, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('leaves the published documentation tree', result.stdout)


if __name__ == '__main__':
    unittest.main()
