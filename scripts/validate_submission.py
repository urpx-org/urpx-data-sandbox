#!/usr/bin/env python3
# SPDX-FileCopyrightText: The URPX Authors
# SPDX-License-Identifier: Apache-2.0

"""Gate 1: validate each submission against the URPX version it declares.

A submission declares the version it targets via ``urpx:targetURPXVersion``.
This script resolves that version's ontology and SHACL shapes from the
matching tagged release of urpx-org/urpx, then runs pyshacl against the
submission. A submission is validated against the version it declares, never
against whatever is current, so a submission does not silently rot at the
next release.
"""

from __future__ import annotations

import json
import pathlib
import sys
import tempfile

import requests
from pyshacl import validate

from urpx_version import release_version

RELEASE_REPO = "urpx-org/urpx"
GITHUB_API = f"https://api.github.com/repos/{RELEASE_REPO}/releases/tags"


def find_submission_files(root: pathlib.Path) -> list[pathlib.Path]:
    return sorted(
        path
        for path in root.rglob("*.jsonld")
        if "_template" not in path.parts
    )


def declared_version(path: pathlib.Path) -> str | None:
    data = json.loads(path.read_text())
    nodes = data if isinstance(data, list) else data.get("@graph", [data])
    for node in nodes:
        if not isinstance(node, dict):
            continue
        value = node.get("targetURPXVersion") or node.get("urpx:targetURPXVersion")
        if value is not None:
            return value["@value"] if isinstance(value, dict) else value
    return None


def fetch_release_shapes(
    version: str, cache_dir: pathlib.Path
) -> tuple[pathlib.Path, pathlib.Path]:
    tag = f"v{version}"
    dest = cache_dir / tag
    ontology_path = dest / f"urpx-ontology-{tag}.ttl"
    shacl_path = dest / f"urpx-shacl-{tag}.ttl"
    if ontology_path.exists() and shacl_path.exists():
        return ontology_path, shacl_path

    dest.mkdir(parents=True, exist_ok=True)
    response = requests.get(f"{GITHUB_API}/{tag}", timeout=30)
    response.raise_for_status()
    assets = {
        asset["name"]: asset["browser_download_url"]
        for asset in response.json()["assets"]
    }

    for name, out_path in (
        (f"urpx-ontology-{tag}.ttl", ontology_path),
        (f"urpx-shacl-{tag}.ttl", shacl_path),
    ):
        if name not in assets:
            raise RuntimeError(f"release {tag} of {RELEASE_REPO} does not carry {name}")
        asset_response = requests.get(assets[name], timeout=30)
        asset_response.raise_for_status()
        out_path.write_bytes(asset_response.content)

    return ontology_path, shacl_path


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_submission.py <submissions-dir>", file=sys.stderr)
        return 2

    root = pathlib.Path(argv[1])
    cache_dir = pathlib.Path(tempfile.gettempdir()) / "urpx-release-shapes"
    failures: list[str] = []

    submissions = find_submission_files(root)
    if not submissions:
        print("No submission files found; nothing to validate.")
        return 0

    for submission in submissions:
        declared = declared_version(submission)
        if not declared:
            failures.append(f"{submission}: does not declare targetURPXVersion")
            continue
        try:
            version = release_version(declared)
        except ValueError as error:
            failures.append(f"{submission}: {error}")
            continue

        try:
            ontology_path, shacl_path = fetch_release_shapes(version, cache_dir)
        except Exception as error:  # report and continue to the next submission
            failures.append(
                f"{submission}: could not fetch shapes for v{version}: {error}"
            )
            continue

        conforms, _, report_text = validate(
            str(submission),
            shacl_graph=str(shacl_path),
            ont_graph=str(ontology_path),
            data_graph_format="json-ld",
            shacl_graph_format="turtle",
            ont_graph_format="turtle",
            inference="rdfs",
        )

        if conforms:
            print(f"{submission}: conforms to v{version}")
        else:
            failures.append(f"{submission}: does not conform to v{version}\n{report_text}")

    if failures:
        print("Gate 1 failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Gate 1 passed for {len(submissions)} submission file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
