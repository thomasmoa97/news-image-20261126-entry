#!/usr/bin/env python3
"""Ship the 26 November 2026 front page.

The image is committed in this repository as entry.png. This program only
copies it to the output directory after proving the copy is byte-identical:
it hashes the source, copies it, then hashes the result and compares the two
digests against the digest recorded below. Standard library only.
"""

import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "f04e532487c6687d6d850dd18b814c362e9c4225b5ced0b0e4ed693fdd868f96"
IMAGE_NAME = "entry.png"


def digest_of(path):
    with open(path, "rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def copy_checked(source, target):
    if digest_of(source) != EXPECTED_SHA256:
        sys.exit("entry.png does not match the recorded digest; refusing to ship")
    source_size = os.path.getsize(source)
    shutil.copyfile(source, target)
    if os.path.getsize(target) != source_size:
        sys.exit("copied file size does not match the source")
    if digest_of(target) != EXPECTED_SHA256:
        sys.exit("copied file failed its digest check")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        sys.exit("MAKEFUN_OUTPUT_DIR is not set")
    os.makedirs(out_dir, exist_ok=True)
    copy_checked(os.path.join(here, IMAGE_NAME),
                 os.path.join(out_dir, IMAGE_NAME))


if __name__ == "__main__":
    main()
