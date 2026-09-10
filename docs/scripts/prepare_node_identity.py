#!/usr/bin/env python3
"""Prepare a new node.key from a validated Solana keypair, without network access."""

import argparse
import json
import os
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


def public_bytes(seed: bytes) -> bytes:
    return Ed25519PrivateKey.from_private_bytes(seed).public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw
    )


def base58(data: bytes) -> str:
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    value = int.from_bytes(data, "big")
    encoded = ""
    while value:
        value, digit = divmod(value, 58)
        encoded = alphabet[digit] + encoded
    return "1" * (len(data) - len(data.lstrip(b"\0"))) + encoded


def read_keypair(path: Path) -> bytes:
    try:
        values = json.loads(path.read_text())
    except (OSError, ValueError) as error:
        raise ValueError("Cannot read the Solana JSON keypair") from error
    if not isinstance(values, list) or len(values) != 64 or any(
        type(value) is not int or not 0 <= value <= 255 for value in values
    ):
        raise ValueError("Expected a Solana keypair array containing 64 byte values")
    keypair = bytes(values)
    if public_bytes(keypair[:32]) != keypair[32:]:
        raise ValueError("The keypair public key does not match its signing seed")
    return keypair


def write_private_new(path: Path, content: str) -> None:
    # O_EXCL also refuses existing symlinks. Never overwrite wallet material.
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w") as handle:
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())
    if os.name == "posix":
        directory_fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)


def prepare_identity(data_dir: Path, keypair_path: Path, create: bool = False, node_key: bool = False) -> dict:
    if data_dir.is_symlink() or (data_dir.exists() and any(data_dir.iterdir())):
        raise ValueError("Use a new, empty directory; existing node data must be preserved")
    if create:
        seed = os.urandom(32)
        keypair = seed + public_bytes(seed)
        write_private_new(keypair_path, json.dumps(list(keypair)) + "\n")
    elif node_key:
        seed = bytes.fromhex(keypair_path.read_text().strip())
        if len(seed) != 32:
            raise ValueError("Expected a 32-byte hexadecimal node seed")
        keypair = seed + public_bytes(seed)
    else:
        keypair = read_keypair(keypair_path)
    data_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    # Node persistence expects the 32-byte seed encoded as 64 hexadecimal characters.
    write_private_new(data_dir / "node.key", keypair[:32].hex())
    return {"lattice_hex": keypair[32:].hex(), "solana_address": base58(keypair[32:])}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--keypair", type=Path, help="Existing Solana JSON keypair to import")
    source.add_argument("--create-keypair", type=Path, help="Create a new Solana JSON keypair at this unused path")
    source.add_argument("--node-key", type=Path, help="Install a previously prepared hexadecimal node.key")
    parser.add_argument("--data-dir", required=True, type=Path, help="New, empty node data directory")
    args = parser.parse_args()
    try:
        identity = prepare_identity(
            args.data_dir, args.create_keypair or args.keypair or args.node_key,
            args.create_keypair is not None, args.node_key is not None
        )
    except (OSError, ValueError):
        # Do not print input contents or secret material in error diagnostics.
        parser.exit(1, "Preparation failed. Check the keypair format, permissions, and unused output paths. Existing files were not overwritten.\n")
    for name, value in identity.items():
        print(f"{name}={value}")


if __name__ == "__main__":
    main()
